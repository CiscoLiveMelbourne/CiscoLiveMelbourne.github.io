# Lab 4 - Hybrid Services licenses

**Time: 40-48 min**

Bruno returns every license. The script prints only Hybrid Calendar, Hybrid Call, and Hybrid Message. Check Bruno first, then VS Code.

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

## Section 2 - See who holds each Hybrid license

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py --show-users
```

An empty result means this organization has no Hybrid license turned on. That is a valid result for this lab. Record it and continue.

## Checkpoint

You are ready for Lab 5 when:

* [ ] You found the Hybrid rows in the Bruno license list, or confirmed there are none
* [ ] VS Code printed the same Hybrid licenses, or reported there are none

## Troubleshooting

| Problem | Solution |
| --- | --- |
| VS Code prints nothing about Hybrid | Compare it with the Bruno list. If Bruno also has no Hybrid license, the organization does not have one. |
| 401 | Use the current Service App access token in Bruno and in `.env`. |

Continue to [Lab 5](lab5_hybrid_health.md).
