# Lab 1 - Service App, then bulk users in both tools

**Time: 12-25 min**

A personal token can create one user. Bulk create needs a Service App access token. You will put that token in Bruno and in `.env`, then run bulk create, update, and cleanup in both tools.

## Section 1 - Create the Service App

1. At [developer.webex.com](https://developer.webex.com){:target="_blank"}, go to **My Webex Apps → Create a Service App**.
2. Request these scopes:
    * `spark-admin:people_read`
    * `spark-admin:people_write`
    * `identity:people_rw`
    * `spark-admin:licenses_read`
    * `spark-admin:roles_read`
    * `spark-admin:organizations_read`
    * `spark-admin:hybrid_clusters_read`
    * `spark-admin:hybrid_connectors_read`
3. In Control Hub, authorize the app for this lab organization.
4. Back on the Service App page, open **Org Authorizations**, select this organization, and choose **Generate tokens**.
5. Copy **access_token**. The value contains `_P0A1_` and lasts about 14 days.

Leave the client secret and the refresh token on that page. They do not go in Bruno or in `.env`.

## Section 2 - Put the same token in Bruno and in `.env`

**Bruno**

1. Replace the **Lab** secret `access_token` with the Service App access token.
2. Run **0. Setup → Who am I** again. **displayName** is now the Service App, not the lab administrator.
3. Run **0. Setup → List organizations**.
4. Confirm the environment now has `org_id` (the value that starts with `Y2lz`) and `orgid` (a UUID).

`orgid` is the part after `ORGANIZATION/` when `org_id` is decoded. Licenses use `org_id`. SCIM bulk uses `orgid`.

**`.env`**

1. Open `Desktop\admin-api\env-template.txt` in Notepad.
2. Fill only these four lines. `WEBEX_ACCESS_TOKEN` is the Service App access token, on one line, with no quotes. `WEBEX_ORG_ID` is the same UUID as Bruno `orgid`.

```text
WEBEX_ACCESS_TOKEN=
WEBEX_ORG_ID=

WEBEX_API_BASE=https://webexapis.com/v1
WEBEX_SCIM_BASE=https://webexapis.com/identity/scim
```

3. Choose **File → Save As**. Set **Save as type** to **All Files** and **Encoding** to **UTF-8**. Save the file as `.env` in `Desktop\admin-api`. Do not choose **Unicode**.

**VS Code**

1. Open the `Desktop\admin-api` folder if it is not already open.
2. Select the interpreter `scripts\.venv\Scripts\python.exe`.
3. Open the terminal in that folder and run:

```bat
scripts\.venv\Scripts\python.exe scripts\00_check_token.py
```

**Name** is the Service App. If `WEBEX_ORG_ID` is empty, copy the printed **SCIM orgid** into `.env` and save the file again.

## Section 3 - Bulk create

**Bruno**

1. Open **1. Users → Bulk create users**.
2. Confirm the URL is `{{scim_base}}/{{orgid}}/v2/Bulk`.
3. Confirm the JSON list is named `operations`.
4. Select **Send**.

Each user in the response has a status starting with `201`. Bruno does not read `data\users.csv`.

**Script**

1. Open `Desktop\admin-api\data\users.csv`.
2. Change `@lab.invalid` to <copy><w class="TestDomain">your verified domain</w></copy>.
3. In the VS Code terminal, from the `admin-api` folder, run:

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py create --csv data\users.csv --mode scim
```

The script writes the new ids to `data\created_users.json`. Bruno does not write that file.

## Section 4 - Update

**Bruno.** Open **1. Users → Update user** and select **Send**. The request uses `person_id` saved by **Create user** and sets the title `Cisco Live Attendee`.

**Script.** This updates only the people listed in `data\created_users.json`.

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py update --title "Cisco Live Attendee"
```

## Section 5 - Cleanup

Run this at the end of the lab, after Lab 3, if you still need the users for role assignment.

**Bruno.** Open **1. Users → Delete user** and select **Send**. This deletes the one user stored in `person_id`.

**Script.** This deletes only the users the script created.

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py cleanup
```

## Checkpoint

You are ready for Lab 2 when:

* [ ] **Who am I** shows the Service App
* [ ] Bruno has `org_id` and `orgid`
* [ ] `.env` is UTF-8 and contains the Service App access token and the UUID
* [ ] Bulk create returned `201` in Bruno and in the script
* [ ] You know cleanup runs at the end, and the script deletes only tracked users

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 | Generate tokens again. Replace the Bruno secret and `WEBEX_ACCESS_TOKEN`. Save `.env` as UTF-8 and send the request again. |
| Who am I still shows the administrator | That tool still has the personal token. Paste the Service App access token. |
| SCIM 400 on `Operations` | Rename that field to `operations`. |
| SCIM rejects the organization id | Use `orgid` and `WEBEX_ORG_ID`. Both are the UUID, not the `Y2lz` value. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 409 on create | That email already exists. Use a different address in the CSV or in the Bruno body. |

Continue to [Lab 2](lab2_licenses.md).
