# Lab 4 - Hybrid Services licenses

**Time: 40-48 min**

Bruno returns every license. The script prints only Hybrid Calendar, Hybrid Call, and Hybrid Message. Check Bruno first, then VS Code. Then assign the Hybrid Calendar license to the users in `data\users.csv` and see who holds it.

No Hybrid Services setup is needed. The Hybrid Calendar license is part of the organization's subscription, so you can assign it even when no Expressway connector is running.

## Section 1 - Find the Hybrid licenses

**Bruno**

1. Open **2. Licenses → List licenses**.
2. Select **Send**.
3. In the response, find licenses whose names include **Hybrid**.

The query is the same `GET /v1/licenses?orgId={{org_id}}` you ran in Lab 2.

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py
```

## Section 2 - Assign the Hybrid Calendar license

Assigning the license is VS Code only. Bruno has no assign request. The script reads the same `data\users.csv` you used for bulk create in Lab 1.

**VS Code**

Run it once with `--dry-run` to see what would change, then without it to assign:

```bat
scripts\.venv\Scripts\python.exe scripts\06_assign_hybrid_calendar.py --dry-run
scripts\.venv\Scripts\python.exe scripts\06_assign_hybrid_calendar.py
```

The script skips anyone who already holds the license, so running it again is safe. For each user it calls `PATCH /v1/licenses/users` with the user's email, the organization id, and the license id with `"operation": "add"`.

## Section 3 - See who holds each Hybrid license

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py --show-users
```

The Hybrid Calendar license now lists the users from `data\users.csv`.

An empty result means this organization has no Hybrid license turned on. That is a valid result for this lab. Record it and continue.

## Checkpoint

You are ready for Lab 5 when:

* [ ] You found the Hybrid rows in the Bruno license list, or confirmed there are none
* [ ] VS Code printed the same Hybrid licenses, or reported there are none
* [ ] VS Code assigned the Hybrid Calendar license to the CSV users
* [ ] `--show-users` lists the CSV users under the Hybrid Calendar license

## Troubleshooting

| Problem | Solution |
| --- | --- |
| VS Code prints nothing about Hybrid | Compare it with the Bruno list. If Bruno also has no Hybrid license, the organization does not have one. |
| `No Hybrid Calendar license found in this org` | The organization has no Hybrid Calendar license. Record it and continue. |
| `not found` for CSV users | Those users do not exist. Run the Lab 1 bulk create first, and check that the CSV emails use your lab domain. Cleanup runs only in the [Conclusion](conclusion.md). |
| 403 on assign | The Service App needs `spark-admin:people_write` and `spark-admin:licenses_read`. Add the scope, authorize the app again, and generate a new access token. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 401 | Use the current Service App access token in Bruno and in `.env`. |

Continue to [Lab 5](lab5_hybrid_health.md).
