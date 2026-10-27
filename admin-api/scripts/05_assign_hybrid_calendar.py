"""Exercise 4 - assign the Hybrid Calendar license to the users in a CSV.

The license is part of the org's subscription, so no Hybrid Services setup or
running connector is needed to assign it. Users who already hold the license
are skipped, so re-running is safe.

    python scripts/05_assign_hybrid_calendar.py --dry-run
    python scripts/05_assign_hybrid_calendar.py
    python scripts/05_assign_hybrid_calendar.py --csv data/users.csv

Required token scopes:
    spark-admin:licenses_read
    spark-admin:people_read
    spark-admin:people_write
"""

import argparse
import csv
import sys
from pathlib import Path

import requests

import webex_client as wx

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "data" / "users.csv"


def find_calendar_license() -> dict:
    licenses = wx.get_all("/licenses")
    matches = [lic for lic in licenses if "calendar" in (lic.get("name") or "").lower()]
    if not matches:
        sys.exit("No Hybrid Calendar license found in this org.")
    if len(matches) > 1:
        print("Several calendar licenses found; using the first:")
        for lic in matches:
            print(f"  {lic.get('name')}  [{lic.get('id')}]")
    return matches[0]


def read_emails(csv_path: Path) -> list[str]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        emails = [(row.get("email") or "").strip() for row in csv.DictReader(handle)]
    return [email for email in emails if email]


def find_person(email: str) -> dict | None:
    people = wx.get("/people", params={"email": email}).get("items", [])
    return people[0] if people else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Assign the Hybrid Calendar license to CSV users")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="CSV with an 'email' column")
    parser.add_argument("--dry-run", action="store_true", help="show changes without assigning")
    args = parser.parse_args()

    if not args.csv.is_file():
        sys.exit(f"CSV not found: {args.csv}")
    emails = read_emails(args.csv)
    if not emails:
        sys.exit(f"No emails found in {args.csv} (expected an 'email' column).")

    license_ = find_calendar_license()
    license_id = license_["id"]
    org_id = wx.org_id()
    print(f"License: {license_.get('name')} "
          f"({license_.get('consumedUnits', '-')} / {license_.get('totalUnits', '-')} used)")
    print(f"Users in {args.csv.name}: {len(emails)}{'  [dry run]' if args.dry_run else ''}\n")

    assigned, already, missing, failed = [], [], [], []
    for email in emails:
        person = find_person(email)
        if person is None:
            missing.append(email)
            print(f"  not found      {email}")
            continue
        if license_id in (person.get("licenses") or []):
            already.append(email)
            print(f"  already has it {email}")
            continue
        if args.dry_run:
            assigned.append(email)
            print(f"  would assign   {email}")
            continue
        try:
            wx.patch("/licenses/users", {
                "email": email,
                "orgId": org_id,
                "licenses": [{"id": license_id, "operation": "add"}],
            })
        except requests.HTTPError as err:
            failed.append(email)
            print(f"  FAILED         {email}: {err.response.status_code} {err.response.text[:200]}")
            continue
        assigned.append(email)
        print(f"  assigned       {email}")

    verb = "Would assign" if args.dry_run else "Assigned"
    print(f"\n{verb}: {len(assigned)}  Already had it: {len(already)}  "
          f"Not found: {len(missing)}  Failed: {len(failed)}")
    if missing:
        print("Users not found must exist in the org first "
              "(python scripts/01_bulk_users.py create --csv data/users.csv).")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
