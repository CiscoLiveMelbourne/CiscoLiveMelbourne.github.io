# Completion Checklist

Use this checklist to confirm you have completed the core lab exercises.

## Core path

- [ ] I reserved a dCloud Webex lab and waited until it was Active
- [ ] I signed in to Control Hub with the reservation administrator
- [ ] I ran Bruno Who am I and Create user with my personal access token
- [ ] I created a Service App and put **access_token** in the Bruno secret and in `.env`
- [ ] `.env` is UTF-8 and has the Service App access token
- [ ] I ran bulk create, update, licenses, roles, and Hybrid licenses in Bruno and in the script
- [ ] The script printed **Lab domain** matching my verified domain
- [ ] Lab 2 printed license used / total / free
- [ ] Lab 3 listed roles
- [ ] Lab 3 assigned a role to a lab user (optional if short on time)
- [ ] Lab 4 listed Hybrid licenses or explained why none exist
- [ ] Lab 4 assigned the Hybrid Calendar license to the CSV users
- [ ] I ran `python scripts/01_bulk_users.py cleanup`

## Both tools

- [ ] Bruno and VS Code were open on `Desktop\admin-api`
- [ ] List organizations saved `org_id`
- [ ] Role assign and Hybrid Calendar license assign ran from the script

## Optional

- [ ] I ran `./run_lab.sh` as a guided demo
- [ ] I compared People API vs SCIM Bulk
- [ ] I confirmed a created user in Control Hub
