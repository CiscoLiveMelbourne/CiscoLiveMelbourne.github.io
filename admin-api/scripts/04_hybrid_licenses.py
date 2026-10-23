"""Exercise 4 - manage Hybrid Services licenses and their assigned users.

Hybrid Services (Hybrid Calendar, Hybrid Call, Hybrid Message) appear as
licenses in the org. This script isolates the hybrid licenses, shows their
consumption, and lists which users are assigned each hybrid license so you can
validate coverage.

    python scripts/04_hybrid_licenses.py
    python scripts/04_hybrid_licenses.py --show-users   # also list assigned users

Notes:
  * "assignedTo" style enumeration below iterates org members and inspects each
    person's `licenses` array, which is portable across dCloud lab
    organizations. For large orgs prefer server-side filtering.
"""

import argparse

import webex_client as wx

HYBRID_KEYWORDS = ("hybrid", "calendar", "call service", "message")


def is_hybrid(license_name: str) -> bool:
    name = (license_name or "").lower()
    return any(keyword in name for keyword in HYBRID_KEYWORDS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Webex Hybrid Services license report")
    parser.add_argument("--show-users", action="store_true", help="list users per hybrid license")
    args = parser.parse_args()

    licenses = wx.get_all("/licenses")
    hybrid = [lic for lic in licenses if is_hybrid(lic.get("name", ""))]

    if not hybrid:
        print("No Hybrid Services licenses found in this org.")
        print("(Enable a Hybrid Service in Control Hub to see them here.)")
        print("\nLicenses in this org:")
        for lic in sorted(licenses, key=lambda l: l.get("name", "")):
            print(f"  {lic.get('name')}  ({lic.get('consumedUnits', '-')} / {lic.get('totalUnits', '-')})")
        return

    print("== Hybrid Services licenses ==")
    for lic in hybrid:
        total = lic.get("totalUnits", "-")
        consumed = lic.get("consumedUnits", "-")
        print(f"  {lic.get('name')}")
        print(f"    id       : {lic.get('id')}")
        print(f"    consumed : {consumed} / {total}")

    if not args.show_users:
        print("\nRe-run with --show-users to list assigned users.")
        return

    hybrid_ids = {lic["id"]: lic["name"] for lic in hybrid}
    print("\n== Assigned users per hybrid license ==")

    assignments: dict[str, list] = {name: [] for name in hybrid_ids.values()}
    people = wx.get_all("/people", params={"max": 1000})
    for person in people:
        for license_id in person.get("licenses", []):
            if license_id in hybrid_ids:
                email = (person.get("emails") or [""])[0]
                assignments[hybrid_ids[license_id]].append((person.get("displayName") or "", email))

    for name, users in assignments.items():
        print(f"  {name}: {len(users)} user(s)")
        for display_name, email in sorted(users, key=lambda u: u[1]):
            print(f"    - {display_name:30} {email}")
    print(f"\n{len(people)} users scanned.")


if __name__ == "__main__":
    main()
