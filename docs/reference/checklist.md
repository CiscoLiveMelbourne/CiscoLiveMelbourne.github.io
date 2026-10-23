# Completion Checklist

Use this checklist to confirm you have completed the core lab exercises.

## Core path

- [ ] I reserved a dCloud Webex lab and waited until it was Active
- [ ] I signed in to Control Hub with the reservation administrator
- [ ] I ran Bruno Who am I and Create user with my personal access token
- [ ] I created a Service App and put **access_token** in the Bruno secret and in `.env`
- [ ] `.env` is UTF-8, and `WEBEX_ORG_ID` is the SCIM UUID
- [ ] I ran bulk create, update, licenses, roles, and hybrid checks in Bruno and in the script
- [ ] I remapped `data/users.csv` to the verified dCloud domain before the script bulk create
- [ ] Lab 2 printed license used / total / free
- [ ] Lab 3 listed roles
- [ ] Lab 3 assigned a role to a lab user (optional if short on time)
- [ ] Lab 4 listed Hybrid licenses or explained why none exist
- [ ] Lab 5 listed clusters/connectors or reported none found
- [ ] I ran `python scripts/01_bulk_users.py cleanup`

## Both tools

- [ ] Bruno and VS Code were open on `Desktop\admin-api`
- [ ] List organizations saved base64 `org_id` and UUID `orgid`
- [ ] Role assign ran from the script

## Optional

- [ ] I ran `./run_lab.sh` as a guided demo
- [ ] I compared People API vs SCIM Bulk
- [ ] I confirmed a created user in Control Hub
