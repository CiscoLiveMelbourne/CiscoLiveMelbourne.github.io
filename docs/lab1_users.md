# Lab 1 - Service App, then bulk users

**Time: 12-25 min**

A personal token can create one user. Bulk create needs a Service App access token. You create the Service App once, then every section runs in **Bruno first** and **VS Code second**.

## Section 1 - Create the Service App

1. At [developer.webex.com](https://developer.webex.com){:target="_blank"}, go to **My Webex Apps → Create a Service App**.
2. Request these scopes:
    * `spark-admin:people_read`
    * `spark-admin:people_write`
    * `identity:people_rw`
    * `spark-admin:licenses_read`
    * `spark-admin:roles_read`
    * `spark-admin:organizations_read`
3. In Control Hub, authorize the app for this lab organization.
4. Back on the Service App page, open **Org Authorizations**, select this organization, and choose **Generate tokens**.
5. Copy **access_token**. The value contains `_P0A1_` and lasts about 14 days.

Leave the client secret and the refresh token on that page. They do not go in Bruno or in `.env`.

## Section 2 - Put the Service App token in both tools

**Bruno**

1. Replace the **Lab** secret `access_token` with the Service App access token.
2. Run **0. Setup → Who am I** again. **displayName** is now the Service App, not the lab administrator.
3. Run **0. Setup → List organizations**.
4. Confirm the environment now has `org_id`, the value that starts with `Y2lz`.

`org_id` is the only organization id you need. Bulk create converts it to the UUID form that SCIM uses before it sends.

**VS Code**

1. Open `Desktop\admin-api\env-template.txt` in Notepad.
2. Fill only the `WEBEX_ACCESS_TOKEN` line with the same Service App access token, on one line, with no quotes. The scripts read the organization id from the token.

    ```text
    WEBEX_ACCESS_TOKEN=

    WEBEX_API_BASE=https://webexapis.com/v1
    WEBEX_SCIM_BASE=https://webexapis.com/identity/scim
    ```

3. Choose **File → Save As**. Set **Save as type** to **All Files** and **Encoding** to **UTF-8**. Save the file as `.env` in `Desktop\admin-api`. Do not choose **Unicode**.
4. In VS Code, choose **File → Open Folder** and open `Desktop\admin-api` if it is not already open.
5. Select the interpreter `scripts\.venv\Scripts\python.exe`.
6. Open a terminal. It opens in `admin-api`. Run every command in this lab from that folder.

## Section 3 - Bulk create

**Bruno**

1. Open **1. Users → Bulk create users**.
2. Confirm the URL is `{{scim_base}}/{{orgid}}/v2/Bulk`. The request fills `orgid` from `org_id` when you send it.
3. Confirm the JSON list is named `operations`.
4. Select **Send**.

Each user in the response has a status starting with `201`.

**VS Code**

1. Open `data\users.csv`.
2. Change `@lab.invalid` to <copy><w class="TestDomain">your verified domain</w></copy> and save.
3. In the terminal, run:

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py create --csv data\users.csv --mode scim
```

Each created user prints a status starting with `201`. The script records the new ids in `data\created_users.json`, so cleanup deletes only these users.

## Section 4 - Update

**Bruno**

1. Open **1. Users → Update user**.
2. Select **Send**.

The request uses `person_id` saved by **Create user** in Lab 0 and sets the title `Cisco Live Attendee`.

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py update --title "Cisco Live Attendee"
```

This updates only the people listed in `data\created_users.json`. In Control Hub, open one of them and confirm the title.

## Checkpoint

You are ready for Lab 2 when:

* [ ] **Who am I** in Bruno shows the Service App
* [ ] Bruno has `org_id`
* [ ] `.env` is saved as UTF-8 with the Service App access token
* [ ] Bulk create returned `201` in Bruno and in VS Code
* [ ] Update set the title in both tools

You delete these users at the end of the lab, in the [Conclusion](conclusion.md). Keep them for now; Lab 3 assigns a role to one of them, and Lab 4 assigns them the Hybrid Calendar license.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 | Generate tokens again. Replace the Bruno secret and `WEBEX_ACCESS_TOKEN`. Save `.env` as UTF-8 and try again. |
| Who am I still shows the administrator | Bruno still has the personal token. Paste the Service App access token into the `access_token` secret. |
| `WEBEX_ACCESS_TOKEN is not set` | `.env` is missing, saved as `.env.txt`, or saved outside `admin-api`. Save it again with **Save as type: All Files**. |
| `could not read the organization id from the token` | `.env` has the wrong token. Paste the Service App access token into `WEBEX_ACCESS_TOKEN` and save `.env`. |
| SCIM 400 on `Operations` | Rename that field to `operations`. |
| SCIM rejects the organization id | Send **0. Setup → List organizations** again so `org_id` belongs to this organization, then send bulk create again. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 409 on create | That email already exists. Use a different address in the CSV or in the Bruno body. |

Continue to [Lab 2](lab2_licenses.md).
