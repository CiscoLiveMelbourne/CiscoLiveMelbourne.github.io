# Lab 2 - Read license usage in both tools

**Time: 25-32 min**

Keep the Service App access token from Lab 1. List the same licenses in Bruno and in the script.

## Section 1 - Bruno

1. Open **2. Licenses → List licenses**.
2. Confirm the URL includes `orgId={{org_id}}`. `org_id` is the value that starts with `Y2lz`.
3. Select **Send**.

Each license includes `name`, `totalUnits`, and `consumedUnits`.

## Section 2 - Script

In the VS Code terminal, from `Desktop\admin-api`, run:

```bat
scripts\.venv\Scripts\python.exe scripts\02_license_usage.py
```

The table shows name, used, total, free, and a status of `ok`, `NEAR LIMIT`, or `OVER-ALLOCATED`.

To flag a license when 80% of its units are used:

```bat
scripts\.venv\Scripts\python.exe scripts\02_license_usage.py --threshold 0.8
```

## Checkpoint

You are ready for Lab 3 when:

* [ ] Bruno **List licenses** returned the organization license list
* [ ] The script printed used, total, and free for those licenses

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 | Replace the Bruno secret and `WEBEX_ACCESS_TOKEN` with a new Service App access token. |
| Empty `orgId` or a 400 on the query | Run **List organizations** in Lab 1 again so `org_id` is set. |
| The script says the token is not set | Save `.env` in `Desktop\admin-api` and run the command from that folder. |

Continue to [Lab 3](lab3_roles.md).
