# Troubleshooting Matrix

| Symptom | Likely cause | Fix |
|---|---|---|
| Web RDP tab closed or disconnected | Browser tab closed, or the network dropped | Return to dCloud Expo and select **Open** for your existing **wkst1** session. Do not select **Logout and End Session**. If you cannot reconnect, ask a proctor |
| Paste does not work in the RDP session | The browser clipboard is not shared with the lab desktop | Open Guacamole's clipboard panel (press `Ctrl+Alt+Shift`), paste the text there, close the panel, then paste in the lab desktop. If it still fails, ask a proctor |
| `401 Unauthorized` | Personal token expired, or `.env` / Bruno does not have the current Service App **access_token** | For Who am I and Create user, copy a new personal token. For bulk create and Python, generate tokens again and replace `WEBEX_ACCESS_TOKEN` and the Bruno secret. Save `.env` as UTF-8 and start the run again |
| Python still returns 401 after you edited `.env` | The file is UTF-16, the token is split across lines, or the debug session kept the old value | Save As **All Files**, encoding **UTF-8**. Keep the token on one line. Start the VS Code run again |
| `403 Forbidden` assigning the Hybrid Calendar license | Missing scope | Add `spark-admin:people_write` and `spark-admin:licenses_read` to the Service App and re-authorize |
| `409` creating a user | Email already exists | Change the name in `users.csv`, or run cleanup first |
| SCIM `400` attribute `Operations` | Bulk list used the wrong field name | Rename it to `operations` |
| SCIM `403` or `400` on bulk | `org_id` is missing or from another organization, or more than 100 operations | Check that `org_id` in the Bruno Lab environment is the **Organization ID** from Control Hub (**Management → Account → Info**). Split more than 100 operations into batches |
| `429 Too Many Requests` | Rate limit | The client auto-retries on `Retry-After`; slow down loops |
| `No Hybrid Calendar license found` | The organization has no Hybrid Calendar license | Compare with the Bruno license list. Record it and continue |
| `WEBEX_ACCESS_TOKEN is not set` | Missing `.env`, or the terminal is outside `admin-api` | Save `env-template.txt` as `.env` in `C:\Users\cholland\Desktop\admin-api` with the Service App access token |
| Bruno Update/Delete fails | No `person_id` | Run **Create user** first |
| `run_lab.sh` not found | Wrong directory | Run it from the repository root |

If a write step fails under `./run_lab.sh`, the script stops (`set -e`). Fix the error and re-run the remaining exercise commands individually.
