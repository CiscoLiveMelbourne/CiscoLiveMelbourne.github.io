# Conclusion

You used Webex Admin APIs to provision users, inspect licenses, apply roles, and check Hybrid Services — against an isolated dCloud organization.

## Before you leave

1. Run cleanup so the reservation does not keep lab users:

    <copy>python scripts/01_bulk_users.py cleanup</copy>

2. Remove the token from `.env` or let the reservation expire.
3. Take the [take-home bundle](reference/take-home.md) with you.

## What you can reuse

- [`scripts/webex_client.py`](https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io/blob/main/admin-api/scripts/webex_client.py) — Bearer client, pagination, 429 retry
- The Bruno collection for the same APIs without Python
- The Service App scope list from [Overview](overview.md)

!!! warning
    Revalidate scopes, endpoints, and Control Hub behavior against current Webex documentation before using any of this against a production organization.

See the [completion checklist](reference/checklist.md) and [links](reference/links.md).
