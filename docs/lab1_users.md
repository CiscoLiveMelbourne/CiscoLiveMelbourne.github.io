# Lab 1 - Service App, then bulk users

**Time: 12-25 min**

A personal token can create one user. Bulk create needs a Service App access token. You create the Service App once, then every section runs in **Bruno first** and **VS Code second**.

## Section 1 - Create the Service App

You play two roles here: the developer who creates the app, and the full administrator who approves it. The lab administrator account is both.

### Step 1 - Register the app

1. Open [developer.webex.com](https://developer.webex.com){:target="_blank"} and confirm you are signed in as <copy><w class="WbxUser">your lab admin</w></copy>. Use the same browser session as Lab 0.
2. Select your avatar at the top right, then select **My Webex Apps**.
3. Select **Create a New App**, then select **Create a Service App**.
4. Fill in the form:
    * **App name**: `AdminAPI-Lab`. You search for this name in Control Hub in Step 3.
    * **Icon**: select any of the default icons
    * **Description**: `Cisco Live lab: bulk users, licenses, and roles`
    * **Contact email**: <copy><w class="WbxUser">your lab admin</w></copy>
5. Under **Scopes**, tick these six boxes and nothing else:
    * `spark-admin:people_read`
    * `spark-admin:people_write`
    * `identity:people_rw`
    * `spark-admin:licenses_read`
    * `spark-admin:roles_read`
    * `spark-admin:organizations_read`
6. Scroll to the bottom and select **Add Service App**.

### Step 2 - Save the client secret

The next page shows the **Client ID** and the **Client Secret**.

1. Copy the **Client Secret** and paste it into a new Notepad window. Do not save that Notepad file.

!!! warning "The client secret is shown once"
    You need it in Step 4 to generate tokens. If you lose it, select **Regenerate** next to **Client Secret** on the app page and copy the new value. The client secret never goes in Bruno or in `.env`.

### Step 3 - Authorize the app in Control Hub

1. On the same app page, select **Request Admin Authorization**. This makes the app visible in your organization's Control Hub.
2. In a new browser tab, open [admin.webex.com](https://admin.webex.com){:target="_blank"} and sign in as <copy><w class="WbxUser">your lab admin</w></copy>.
3. In the left menu, under **Management**, select **Apps**.
4. Select the **Service Apps** tab.
5. Scroll to **Other service apps**. New apps that are waiting for approval are listed there, not under the apps already authorized.
6. Find **AdminAPI-Lab** and select it. Type the name in the search box if the list is long.
7. In the panel that opens, check that the scopes match the six you ticked.
8. Select **Authorize**, then select **Save**. The app now shows as authorized.

### Step 4 - Generate the access token

1. Go back to the developer.webex.com tab and refresh the app page.
2. Scroll down to **Org Authorizations**.
3. In the organization list, select your lab organization. It is the only organization listed.
4. Paste the client secret from Notepad into the **Client Secret** field.
5. Select **Generate tokens**.
6. Copy **access_token**. The value contains `_P0A1_` and lasts about 14 days.

Leave the refresh token on that page. It does not go in Bruno or in `.env`. You can close the Notepad window with the client secret without saving it.

## Section 2 - Put the Service App token in both tools

**Bruno**

1. Replace the **Lab** secret `access_token` with the Service App access token. Use the row with **Secret** ticked, the same one you used in Lab 0.
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

`data\users.csv` lists names only, such as `barbara.liskov`. The script finds your pod's domain from the users already in the organization, adds it to each name, and prints it as **Lab domain**. It matches <copy><w class="TestDomain">your verified domain</w></copy>. You do not edit the CSV.

In the terminal, run:

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
| Service App is not listed in Control Hub | On the app page at developer.webex.com, select **Request Admin Authorization**. Then refresh **Management → Apps → Service Apps** and look under **Other service apps** for your app name. |
| **Org Authorizations** has no organization | The app is not authorized yet. Finish Step 3, then refresh the app page. |
| **Generate tokens** rejects the client secret | The secret was not copied in full. Select **Regenerate** next to **Client Secret**, copy the new value, and try again. |
| 401 | Generate tokens again. Replace the Bruno secret and `WEBEX_ACCESS_TOKEN`. Save `.env` as UTF-8 and try again. |
| Who am I still shows the administrator | Bruno still has the personal token. Paste the Service App access token into the `access_token` secret. |
| `WEBEX_ACCESS_TOKEN is not set` | `.env` is missing, saved as `.env.txt`, or saved outside `admin-api`. Save it again with **Save as type: All Files**. |
| `could not read the organization id from the token` | `.env` has the wrong token. Paste the Service App access token into `WEBEX_ACCESS_TOKEN` and save `.env`. |
| SCIM 400 on `Operations` | Rename that field to `operations`. |
| SCIM rejects the organization id | Send **0. Setup → List organizations** again so `org_id` belongs to this organization, then send bulk create again. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 409 on create | That email already exists. Use a different address in the CSV or in the Bruno body. |

Continue to [Lab 2](lab2_licenses.md).
