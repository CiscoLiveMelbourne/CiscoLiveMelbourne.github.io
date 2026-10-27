"""Exercise 3 - retrieve available roles and apply consistent admin access.

Lists all administrative roles available in the org (the role ids you use when
assigning admin access to people), and optionally assigns a role to a user so
you can demonstrate consistent, repeatable access control.

    python scripts/03_roles.py list
    python scripts/03_roles.py users
    python scripts/03_roles.py users --role "Full Administrator"
    python scripts/03_roles.py assign --email barbara.liskov --role "Read-only Administrator"
"""

import argparse
import sys

import webex_client as wx


def cmd_list(_args) -> None:
    roles = wx.get_all("/roles")
    print(f"{'Role name':40} Role ID")
    print("-" * 80)
    for role in sorted(roles, key=lambda r: r.get("name", "")):
        print(f"{(role.get('name') or '')[:39]:40} {role.get('id')}")
    print(f"\n{len(roles)} roles available.")


def cmd_users(args) -> None:
    role_names = {r["id"]: r.get("name") or r["id"] for r in wx.get_all("/roles")}
    people = wx.get_all("/people", params={"max": 1000})

    by_role: dict[str, list[str]] = {}
    for person in people:
        email = (person.get("emails") or [""])[0]
        role_ids = person.get("roles") or []
        if not role_ids:
            by_role.setdefault("No admin role", []).append(email)
        for role_id in role_ids:
            by_role.setdefault(role_names.get(role_id, role_id), []).append(email)

    for role_name in sorted(by_role):
        if args.role and role_name.lower() != args.role.lower():
            continue
        emails = sorted(by_role[role_name])
        print(f"\n{role_name} ({len(emails)})")
        print("-" * 80)
        for email in emails:
            print(f"  {email}")
    print(f"\n{len(people)} users scanned.")


def _find_role_id(role_name: str) -> str:
    roles = wx.get_all("/roles")
    for role in roles:
        if (role.get("name") or "").lower() == role_name.lower():
            return role["id"]
    sys.exit(f"Role '{role_name}' not found. Run 'list' to see valid names.")


def _find_person(email: str) -> dict:
    people = wx.get_all("/people", params={"email": email})
    if not people:
        sys.exit(f"No user found with email {email}.")
    return people[0]


def cmd_assign(args) -> None:
    args.email = wx.full_email(args.email)
    role_id = _find_role_id(args.role)
    person = _find_person(args.email)

    existing = set(person.get("roles", []))
    existing.add(role_id)

    # PUT replaces the person object, so preserve required fields.
    payload = {
        "emails": person.get("emails", [args.email]),
        "displayName": person.get("displayName", args.email),
        "firstName": person.get("firstName", ""),
        "lastName": person.get("lastName", ""),
        "roles": sorted(existing),
    }
    wx.put(f"/people/{person['id']}", payload)
    print(f"Assigned role '{args.role}' to {args.email}.")
    print(f"  {args.email} now has {len(existing)} role(s).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Webex roles demo")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list available roles")
    p_list.set_defaults(func=cmd_list)

    p_users = sub.add_parser("users", help="list users grouped by admin role")
    p_users.add_argument("--role", help="only show this role, e.g. 'Full Administrator'")
    p_users.set_defaults(func=cmd_users)

    p_assign = sub.add_parser("assign", help="assign a role to a user")
    p_assign.add_argument("--email", required=True,
                          help="full email, or just the name; the lab domain is added")
    p_assign.add_argument("--role", required=True, help="role name, e.g. 'Read-only Administrator'")
    p_assign.set_defaults(func=cmd_assign)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
