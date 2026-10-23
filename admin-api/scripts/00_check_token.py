"""Exercise 0 - verify your token and discover your organization.

Run this first. It confirms the token works, prints who you are, and lists the
organization(s) the token can administer. Copy the printed SCIM orgid into
.env as WEBEX_ORG_ID for the bulk-user exercise.

    python scripts/00_check_token.py
"""

import webex_client as wx


def main() -> None:
    print("== Who am I ==")
    identity = wx.me()
    print(f"  Name        : {identity.get('displayName')}")
    print(f"  Emails      : {', '.join(identity.get('emails', []))}")
    print(f"  Person ID   : {identity.get('id')}")
    encoded_org_id = identity.get("orgId") or ""
    print(f"  Org ID      : {encoded_org_id}")
    print(f"  SCIM orgid  : {wx.scim_org_id(encoded_org_id)}")
    print(f"  Roles       : {len(identity.get('roles', []))} assigned")

    print("\n== Organizations this token can administer ==")
    orgs = wx.get_all("/organizations")
    for org in orgs:
        print(f"  {org.get('id')}")
        print(f"    displayName : {org.get('displayName')}")
        print(f"    created     : {org.get('created')}")

    print("\nTip: put SCIM orgid above into .env as WEBEX_ORG_ID.")
    print("That UUID is the value after ORGANIZATION/ in the base64 Org ID.")


if __name__ == "__main__":
    main()
