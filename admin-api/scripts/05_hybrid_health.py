"""Exercise 5 - monitor Hybrid Clusters and Hybrid Connectors.

Retrieves the org's Hybrid Clusters and the Hybrid Connectors running on their
on-prem hosts, then surfaces any connector that is not "running" or that has
unresolved alarms - exactly the signal an admin wants for "reliable
configuration" monitoring.

    python scripts/05_hybrid_health.py

Required token scopes:
    spark-admin:hybrid_clusters_read
    spark-admin:hybrid_connectors_read
"""

import webex_client as wx


def main() -> None:
    clusters = wx.get_all("/hybrid/clusters")
    connectors = wx.get_all("/hybrid/connectors")

    if not clusters and not connectors:
        print("No hybrid clusters or connectors found in this org.")
        print("(Register an Expressway/connector host in Control Hub to populate this.)")
        return

    cluster_names = {c.get("id"): c.get("name", "unknown") for c in clusters}

    print(f"== Hybrid Clusters ({len(clusters)}) ==")
    for cluster in clusters:
        print(f"  {cluster.get('name')}  [{cluster.get('id')}]")
        print(f"    resourceGroupId: {cluster.get('resourceGroupId')}")

    print(f"\n== Hybrid Connectors ({len(connectors)}) ==")
    unhealthy = []
    for connector in connectors:
        name = connector.get("hostname") or connector.get("name") or connector.get("id")
        conn_type = connector.get("type", "?")
        status = connector.get("status", "unknown")
        cluster = cluster_names.get(connector.get("hybridClusterId"), "-")
        alarms = connector.get("alarms", []) or []

        flag = "" if status == "running" and not alarms else "  <-- CHECK"
        if flag:
            unhealthy.append((name, status, len(alarms)))
        print(f"  {name} ({conn_type}) cluster={cluster} status={status} alarms={len(alarms)}{flag}")

        for alarm in alarms:
            print(f"      ALARM [{alarm.get('severity', '?')}] {alarm.get('title', '')}")

    print("\n== Monitoring summary ==")
    if unhealthy:
        print(f"  {len(unhealthy)} connector(s) need attention:")
        for name, status, alarm_count in unhealthy:
            print(f"    - {name}: status={status}, alarms={alarm_count}")
    else:
        print("  All connectors running with no unresolved alarms.")


if __name__ == "__main__":
    main()
