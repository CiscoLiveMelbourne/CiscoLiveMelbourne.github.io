# Known Caveats

- dCloud reservations expire and may be reset. Do not store work that must persist.
- A personal access token lasts about 12 hours. Prefer a Service App for the automation story.
- Exercise 4 needs a Hybrid Calendar license in the organization. Assigning it needs no Hybrid Services setup or Expressway connector.
- Bruno does not include role assignment, Hybrid Calendar license assignment, or the hybrid-license assigned-user report. Use the Python scripts for those.
- `run_lab.sh` uses `python` (not `python3`), does not activate `.venv`, and leaves cleanup to you.
- `data/users.csv` lists names only. The scripts add the pod's domain, taken from the most common email domain among the organization's users. A full email in the CSV is used as it is.
- SCIM Bulk requires `failOnErrors: 1` and the body field `operations`. The path takes the UUID inside the base64 `org_id`; Bruno and the scripts convert it for you. Every other call uses `org_id` as it is.
- Product behavior, scopes, and endpoint names must be revalidated against current Webex documentation before any non-lab use.
