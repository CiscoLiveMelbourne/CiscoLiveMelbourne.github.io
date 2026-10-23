# Troubleshooting Matrix

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` | Personal token expired, or `.env` / Bruno does not have the current Service App **access_token** | For Who am I and Create user, copy a new personal token. For bulk create and Python, generate tokens again and replace `WEBEX_ACCESS_TOKEN` and the Bruno secret. Save `.env` as UTF-8 and start the run again |
| Python still returns 401 after you edited `.env` | The file is UTF-16, the token is split across lines, or the debug session kept the old value | Save As **All Files**, encoding **UTF-8**. Keep the token on one line. Start the VS Code run again |
| `403 Forbidden` on hybrid calls | Missing scope | Add `spark-admin:hybrid_*_read` to the Service App and re-authorize |
| `409` creating a user | Email already exists | Change the email/domain in `users.csv` |
| SCIM `400` attribute `Operations` | Bulk list used the wrong field name | Rename it to `operations` |
| SCIM `403` or `400` on bulk | Base64 `org_id` was placed in the SCIM path | Use `orgid`, the UUID decoded from that base64 value. More than 100 operations must be split |
| `429 Too Many Requests` | Rate limit | The client auto-retries on `Retry-After`; slow down loops |
| Hybrid lists empty | Selected dCloud lab has no registered connector | Use a dCloud lab that includes Hybrid Services infrastructure |
| `WEBEX_ACCESS_TOKEN is not set` | Missing `.env`, or the terminal is outside `admin-api` | Save `env-template.txt` as `.env` in `C:\Users\cholland\Desktop\admin-api` with the Service App access token and the SCIM UUID |
| Bruno Update/Delete fails | No `person_id` | Run **Create user** first |
| `run_lab.sh` not found | Wrong directory | Run it from the repository root |

If a write step fails under `./run_lab.sh`, the script stops (`set -e`). Fix the error and re-run the remaining exercise commands individually.
