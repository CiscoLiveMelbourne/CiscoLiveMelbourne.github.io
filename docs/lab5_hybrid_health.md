# Lab 5 - Clusters and connectors in both tools

**Time: 48-55 min**

Read Hybrid clusters and connectors in Bruno, then run the script that checks both.

## Section 1 - Bruno

1. Open **4 & 5. Hybrid Services → List hybrid clusters** and select **Send**. This is `GET /v1/hybrid/clusters`.
2. Open **4 & 5. Hybrid Services → List hybrid connectors** and select **Send**. This is `GET /v1/hybrid/connectors`.

## Section 2 - Script

```bat
scripts\.venv\Scripts\python.exe scripts\05_hybrid_health.py
```

The script prints both lists. It flags a connector whose state is not `running`.

An empty list means no connector is registered in this organization. That is a valid result. Record it and continue.

## Checkpoint

You are ready to wrap up when:

* [ ] Both Bruno requests were sent
* [ ] The script printed the same clusters and connectors, or reported that none were found
* [ ] You can name the two scopes these calls use: `spark-admin:hybrid_clusters_read` and `spark-admin:hybrid_connectors_read`

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 403 | Add the two Hybrid read scopes to the Service App, authorize it again, and generate a new access token. |
| 401 | Replace the token in the Bruno secret and in `WEBEX_ACCESS_TOKEN`. |
| Both lists are empty | No connector is registered. Continue to the conclusion. |

Continue to the [Conclusion](conclusion.md).
