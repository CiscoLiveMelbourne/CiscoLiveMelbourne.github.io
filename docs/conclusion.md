# Conclusion

You used Webex Admin APIs to provision users, inspect licenses, apply roles, and check Hybrid Services — against an isolated dCloud organization.

## Before you leave

Clean up so the reservation does not keep lab users. Bruno first, then VS Code.

**Bruno**

1. In the Bruno left sidebar, under **Webex Admin API Lab**, expand the **1. Users** folder and select **Delete user (lifecycle)**.
2. Select the arrow (**Send**) at the right end of the URL bar. This deletes the one user you created in Lab 0, `labuser01`, stored in `person_id`.

The call is `DELETE /v1/people/{{person_id}}`. The status is **204 No Content** and the response body is empty. That means the user was deleted; a delete has nothing to return. If you send it again, the status is **404**, because the user no longer exists.

**VS Code**

1. In the VS Code terminal, check that the prompt ends with `Desktop\admin-api>`.
2. Copy the command below, right-click in the terminal to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py cleanup
    ```

The output looks like this:

```text
Deleting 5 lab users...
  deleted barbara.liskov@your-domain
  ...
Done.
```

The script deletes only the users recorded in `data\created_users.json`, the users it created in Lab 1, and then removes them from that file. If you run it again, it prints `Nothing to clean up.` Confirm in Control Hub, under **Management → Users**, that they are gone.

Then remove the token from `.env`, or let the reservation expire, and take the [take-home bundle](reference/take-home.md) with you.

## What you can reuse

- [`scripts/webex_client.py`](https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io/blob/main/admin-api/scripts/webex_client.py) — Bearer client, pagination, 429 retry
- The Bruno collection for the same APIs without Python
- The Service App scope list from [Overview](overview.md)

!!! warning
    Revalidate scopes, endpoints, and Control Hub behavior against current Webex documentation before using any of this against a production organization.

See the [completion checklist](reference/checklist.md) and [links](reference/links.md).
