# Known Caveats

- dCloud reservations expire and may be reset. Do not store work that must persist.
- A personal access token lasts about 12 hours. Prefer a Service App for the automation story.
- Exercises 4 and 5 need Hybrid Services (and an Expressway/connector for cluster/connector data). Not every dCloud Webex lab includes that infrastructure.
- Bruno does not include role assignment or the hybrid-license assigned-user report. Use the Python scripts for those.
- `run_lab.sh` uses `python` (not `python3`), does not activate `.venv`, and leaves cleanup to you.
- Sample emails in `data/users.csv` use `@lab.invalid` and must be remapped to a verified domain.
- SCIM Bulk requires `failOnErrors: 1` and the body field `operations`. The path takes `orgid`, the UUID inside the base64 `WEBEX_ORG_ID`. Licenses and hybrid calls keep the base64 `org_id`.
- Product behavior, scopes, and endpoint names must be revalidated against current Webex documentation before any non-lab use.
