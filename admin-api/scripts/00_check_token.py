"""Exercise 0 - verify your token and discover your organization.

Run this first. It confirms the token works, prints who you are, and lists the
organization(s) the token can administer. The scripts read the organization id
from the token, so there is nothing to copy into .env.

    python scripts/00_check_token.py
"""

import webex_client as wx


def main() -> None:
    print("== Who am I ==")
    identity = wx.me()
    print(f"  Name        : {identity.get('displayName')}")
    print(f"  Emails      : {', '.join(identity.get('emails', []))}")
    print(f"  Person ID   : {identity.get('id')}")
    print(f"  Org ID      : {identity.get('orgId')}")
    print(f"  Roles       : {len(identity.get('roles', []))} assigned")

    print("\n== Organizations this token can administer ==")
    orgs = wx.get_all("/organizations")
    for org in orgs:
        print(f"  {org.get('id')}")
        print(f"    displayName : {org.get('displayName')}")
        print(f"    created     : {org.get('created')}")


if __name__ == "__main__":
    main()
