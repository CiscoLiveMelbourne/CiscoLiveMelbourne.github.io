"""Exercise 1 - bulk user creation, update, and lifecycle actions.

Demonstrates two complementary approaches:

  * People API (/v1/people)       - simple, one call per user, great for demos
                                     and small batches.
  * SCIM 2.0 Bulk API (/Bulk)     - up to 100 operations in a single request,
                                     the right tool for real bulk provisioning.

Usage:
    # Create users from a CSV using the People API (default)
    python scripts/01_bulk_users.py create --csv data/users.csv

    # Create users using the SCIM 2.0 bulk endpoint (needs WEBEX_ORG_ID)
    python scripts/01_bulk_users.py create --csv data/users.csv --mode scim

    # Update the display name / title of users created above
    python scripts/01_bulk_users.py update --title "Cisco Live Attendee"

    # Lifecycle: deactivate then delete the lab users we created
    python scripts/01_bulk_users.py cleanup

Created user ids are tracked in data/created_users.json so cleanup only ever
touches users this lab created - never pre-existing org members.
"""

import argparse
import csv
import json
import os
import sys
import uuid
from pathlib import Path

import webex_client as wx

TRACK_FILE = Path(__file__).resolve().parent.parent / "data" / "created_users.json"


def _load_tracked() -> list:
    if TRACK_FILE.exists():
        return json.loads(TRACK_FILE.read_text())
    return []


def _save_tracked(users: list) -> None:
    TRACK_FILE.write_text(json.dumps(users, indent=2))


def _read_csv(csv_path: str) -> list:
    with open(csv_path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def create_people_api(rows: list) -> list:
    """Create users one-by-one with the People API."""
    created = []
    for row in rows:
        payload = {
            "emails": [row["email"]],
            "displayName": row.get("displayName") or row["email"],
            "firstName": row.get("firstName", ""),
            "lastName": row.get("lastName", ""),
        }
        person = wx.post("/people", payload)
        created.append({"id": person["id"], "email": row["email"]})
        print(f"  created {row['email']} -> {person['id']}")
    return created


def create_scim_bulk(rows: list, org_id: str) -> list:
    """Create up to 100 users in a single SCIM 2.0 bulk request."""
    if not org_id:
        sys.exit("ERROR: --mode scim requires WEBEX_ORG_ID in your .env")

    operations = []
    bulk_index = {}
    for row in rows:
        bulk_id = str(uuid.uuid4())
        bulk_index[f"bulkId:{bulk_id}"] = row["email"]
        operations.append(
            {
                "method": "POST",
                "path": "/Users",
                "bulkId": bulk_id,
                "data": {
                    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
                    "userName": row["email"],
                    "displayName": row.get("displayName") or row["email"],
                    "name": {
                        "givenName": row.get("firstName", ""),
                        "familyName": row.get("lastName", ""),
                    },
                    "emails": [{"value": row["email"], "type": "work", "primary": True}],
                    "active": True,
                },
            }
        )

    body = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:BulkRequest"],
        "failOnErrors": 1,
        "operations": operations,
    }
    result = wx.scim_post(org_id, "/v2/Bulk", body)

    created = []
    for op in result.get("operations", result.get("Operations", [])):
        location = op.get("location", "")
        person_id = location.rstrip("/").split("/")[-1] if location else None
        email = bulk_index.get(op.get("bulkId", ""), "unknown")
        status = op.get("status", "?")
        print(f"  [{status}] {email} -> {person_id}")
        if person_id and str(status).startswith("2"):
            created.append({"id": person_id, "email": email, "scim": True})
    return created


def cmd_create(args) -> None:
    rows = _read_csv(args.csv)
    print(f"Creating {len(rows)} users via {args.mode}...")
    if args.mode == "scim":
        created = create_scim_bulk(rows, os.getenv("WEBEX_ORG_ID", "").strip())
    else:
        created = create_people_api(rows)

    tracked = _load_tracked() + created
    _save_tracked(tracked)
    print(f"\nDone. {len(created)} users created. Tracked in {TRACK_FILE.name}.")


def cmd_update(args) -> None:
    """PUT a title/displayName suffix onto every lab-created user (People API)."""
    tracked = _load_tracked()
    if not tracked:
        sys.exit("Nothing to update - run 'create' first.")
    print(f"Updating {len(tracked)} users (title -> '{args.title}')...")
    for user in tracked:
        # PUT replaces the person, so fetch current state first.
        current = wx.get(f"/people/{user['id']}")
        payload = {
            "emails": current.get("emails", [user["email"]]),
            "displayName": current.get("displayName", user["email"]),
            "firstName": current.get("firstName", ""),
            "lastName": current.get("lastName", ""),
            "title": args.title,
        }
        wx.put(f"/people/{user['id']}", payload)
        print(f"  updated {user['email']}")
    print("Done.")


def cleanup_from_csv(csv_path: str) -> None:
    """Delete users whose emails appear in the CSV, after an explicit confirmation.

    Use this when the users exist but were not created by this script (for example
    by the Bruno bulk request), so they are not in created_users.json.
    """
    matches = []
    for row in _read_csv(csv_path):
        email = row["email"].strip()
        found = wx.get("/people", params={"email": email}).get("items", [])
        if found:
            matches.append({"id": found[0]["id"], "email": email,
                            "displayName": found[0].get("displayName", "")})
        else:
            print(f"  not found: {email}")

    if not matches:
        print("None of the CSV emails exist in the org. Nothing to delete.")
        return

    print(f"\nThese {len(matches)} users will be permanently deleted:")
    for user in matches:
        print(f"  {user['email']}  ({user['displayName']})")
    if input("\nType DELETE to confirm: ").strip() != "DELETE":
        print("Cancelled. Nothing was deleted.")
        return

    deleted_ids = set()
    for user in matches:
        try:
            wx.delete(f"/people/{user['id']}")
            deleted_ids.add(user["id"])
            print(f"  deleted {user['email']}")
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"  FAILED {user['email']}: {exc}")
    _save_tracked([u for u in _load_tracked() if u["id"] not in deleted_ids])
    print("Done.")


def cmd_cleanup(args) -> None:
    """Lifecycle teardown: delete every user this lab created."""
    if args.csv:
        cleanup_from_csv(args.csv)
        return
    tracked = _load_tracked()
    if not tracked:
        print("Nothing to clean up.")
        return
    print(f"Deleting {len(tracked)} lab users...")
    remaining = []
    for user in tracked:
        try:
            wx.delete(f"/people/{user['id']}")
            print(f"  deleted {user['email']}")
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"  FAILED {user['email']}: {exc}")
            remaining.append(user)
    _save_tracked(remaining)
    print("Done." if not remaining else f"{len(remaining)} users could not be deleted.")


EXAMPLES = """\
examples (run from the repo root):
  python scripts/01_bulk_users.py create --csv data/users.csv
  python scripts/01_bulk_users.py create --csv data/users.csv --mode scim
  python scripts/01_bulk_users.py update --title "Cisco Live Attendee"
  python scripts/01_bulk_users.py cleanup
  python scripts/01_bulk_users.py cleanup --csv data/users.csv

running from inside scripts/? use --csv ../data/users.csv instead.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Webex bulk user lifecycle demo",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="create users from a CSV")
    p_create.add_argument("--csv", default="data/users.csv")
    p_create.add_argument("--mode", choices=["people", "scim"], default="people")
    p_create.set_defaults(func=cmd_create)

    p_update = sub.add_parser("update", help="update lab-created users")
    p_update.add_argument("--title", default="Cisco Live Attendee")
    p_update.set_defaults(func=cmd_update)

    p_cleanup = sub.add_parser("cleanup", help="delete lab-created users")
    p_cleanup.add_argument(
        "--csv",
        help="instead of created_users.json, delete the users whose emails are in "
        "this CSV (asks you to type DELETE first)",
    )
    p_cleanup.set_defaults(func=cmd_cleanup)

    return parser


def main() -> None:
    parser = build_parser()
    if len(sys.argv) == 1:
        print("No command given - pick one of: create, update, cleanup.\n")
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
