# Conclusion

You used Webex Admin APIs to provision users, inspect licenses, apply roles, and check Hybrid Services — against an isolated dCloud organization.

## Before you leave

Clean up so the reservation does not keep lab users. Bruno first, then VS Code.

**Bruno**

1. Open **1. Users → Delete user**.
2. Select **Send**. This deletes the one user you created in Lab 0, stored in `person_id`.

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py cleanup
```

This deletes only the users the script created in Lab 1. Confirm in Control Hub that they are gone.

Then remove the token from `.env`, or let the reservation expire, and take the [take-home bundle](reference/take-home.md) with you.

## What you can reuse

- [`scripts/webex_client.py`](https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io/blob/main/admin-api/scripts/webex_client.py) — Bearer client, pagination, 429 retry
- The Bruno collection for the same APIs without Python
- The Service App scope list from [Overview](overview.md)

!!! warning
    Revalidate scopes, endpoints, and Control Hub behavior against current Webex documentation before using any of this against a production organization.

See the [completion checklist](reference/checklist.md) and [links](reference/links.md).
