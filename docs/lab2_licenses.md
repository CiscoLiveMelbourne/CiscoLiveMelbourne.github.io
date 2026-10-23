# Lab 2 - License usage

**Time: 25-32 min**

Keep the Service App access token from Lab 1. List the same licenses in Bruno first, then in VS Code.

## Section 1 - List licenses

**Bruno**

1. Open **2. Licenses → List licenses**.
2. Confirm the URL includes `orgId={{org_id}}`. `org_id` is the value that starts with `Y2lz`.
3. Select **Send**.

Each license includes `name`, `totalUnits`, and `consumedUnits`.

**VS Code**

In the terminal, from `Desktop\admin-api`, run:

```bat
scripts\.venv\Scripts\python.exe scripts\02_license_usage.py
```

The table shows name, used, total, free, and a status of `ok`, `NEAR LIMIT`, or `OVER-ALLOCATED`. The numbers match the Bruno response.

## Section 2 - Flag licenses near their limit

**VS Code**

Bruno shows the raw numbers. The script can also flag any license that is 80% used:

```bat
scripts\.venv\Scripts\python.exe scripts\02_license_usage.py --threshold 0.8
```

## Checkpoint

You are ready for Lab 3 when:

* [ ] Bruno **List licenses** returned the organization license list
* [ ] VS Code printed used, total, and free for the same licenses

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 | Replace the Bruno secret and `WEBEX_ACCESS_TOKEN` with a new Service App access token. |
| Empty `orgId` or a 400 on the query | Run **0. Setup → List organizations** in Bruno again so `org_id` is set. |
| `WEBEX_ACCESS_TOKEN is not set` | Save `.env` in `Desktop\admin-api` and run the command from that folder. |

Continue to [Lab 3](lab3_roles.md).
