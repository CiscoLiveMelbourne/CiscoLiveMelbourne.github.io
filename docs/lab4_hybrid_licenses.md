# Lab 4 - Hybrid licenses in both tools

**Time: 40-48 min**

Bruno returns every license. The script prints only Hybrid Calendar, Hybrid Call, and Hybrid Message.

## Section 1 - Bruno

1. Open **2. Licenses → List licenses**.
2. Select **Send**.
3. In the response, find licenses whose names include **Hybrid**.

The query is still `GET /v1/licenses?orgId={{org_id}}`.

## Section 2 - Script

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py
```

To include the people who hold each Hybrid license:

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py --show-users
```

An empty result means this organization has no Hybrid license turned on. That is a valid result for this lab. Record it and continue.

## Checkpoint

You are ready for Lab 5 when:

* [ ] You found the Hybrid rows in the Bruno license list, or you confirmed there are none
* [ ] The script printed those Hybrid licenses, or it told you there are none

## Troubleshooting

| Problem | Solution |
| --- | --- |
| The script prints nothing about Hybrid | Compare it with the Bruno list. If Bruno also has no Hybrid license, the organization does not have one. |
| 401 | Use the current Service App access token in Bruno and in `.env`. |

Continue to [Lab 5](lab5_hybrid_health.md).
