# Lab 1 - Service App, then bulk users

**Time: 12-25 min**

A personal token can create one user. Bulk create needs a Service App access token. You create the Service App once, then every section runs in **Bruno first** and **VS Code second**.

## Section 1 - Create the Service App

You play two roles here: the developer who creates the app, and the full administrator who approves it. The lab administrator account is both.

### Step 1 - Register the app

1. Open [developer.webex.com](https://developer.webex.com){:target="_blank"} and confirm you are signed in as <copy><w class="WbxUser">your lab admin</w></copy>. Use the same browser session as Lab 0.
2. Select your avatar at the top right, then select **My Webex Apps**.
3. The lab administrator has no apps yet, so the **What would you like to configure?** page opens. Find the **Service App** card and select **Onboard Service App**.
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
6. Two tokens appear: **access_token** and **refresh_token**. Select the copy icon next to **access_token**, not refresh_token. The access token lasts about 14 days.

Leave the refresh token on that page. It does not go in Bruno or in `.env`. You can close the Notepad window with the client secret without saving it.

## Section 2 - Put the Service App token in Bruno and VS Code

### What you are doing in this section

In Lab 0, Bruno used your **personal access token**. That token acts as you, the lab administrator, and expires in about 12 hours. For the rest of this lab you use the **Service App access token** you generated in Step 4. It acts as the Service App, has only the six scopes you approved, and is the kind of token you would use for real automation.

You put the same Service App access token in two places, because the lab uses two tools:

| Tool | Where the token goes | What uses it |
| --- | --- | --- |
| Bruno | The `access_token` secret in the **Lab** environment | Every Bruno request in Labs 1 to 4 |
| VS Code | A file named `.env` in `Desktop\admin-api` | Every Python script in Labs 1 to 4 |

At the end of this section, you check that each tool now acts as the Service App. Keep the developer.webex.com tab with the access token open until you finish this section.

### Part A - Bruno

**Replace the token**

1. Switch to **Bruno**.
2. Open the environment list at the top right of the window and select **Configure**. The **Environments** tab opens, with **Lab** selected in the left list.
3. Select the **Secrets** tab.
4. In the `access_token` row, select the **Value** field and delete the personal access token from Lab 0.
5. Paste the Service App access token into **Value**, then select **Save**.

You do not change any other variable. `test_domain` and `org_id` stay as you set them in Lab 0.

**Check that Bruno now acts as the Service App**

1. In the Bruno left sidebar, expand **Webex Admin API Lab**, then expand **0. Setup**, and select **Who am I (/people/me)**.
2. Select the arrow (**Send**) at the right end of the URL bar.
3. In the response pane, check **displayName**. It is now **AdminAPI-Lab**, the Service App, instead of the lab administrator. This confirms Bruno is using the new token.
4. In the same **0. Setup** folder, select **List organizations** and select **Send**.
5. In the response pane, confirm the list shows your lab organization and its **displayName**. This confirms the Service App is authorized for your organization.

The `id` in this response is in a different format from the Organization ID you copied from Control Hub. That is expected. Do not copy it into Bruno. Keep `org_id` as you set it in Lab 0; it is the only organization ID you need.

### Part B - VS Code

The Python scripts do not use Bruno. They read the token from a file named `.env` in the `admin-api` folder. You create that file from a template, then open the folder in VS Code and run a script that checks the token.

**Create the `.env` file**

1. On the lab desktop, open **File Explorer** and go to **Desktop → admin-api**.
2. Right-click `env-template.txt` and select **Open with → Notepad**. The file looks like this:

    ```text
    WEBEX_ACCESS_TOKEN=

    WEBEX_API_BASE=https://webexapis.com/v1
    WEBEX_SCIM_BASE=https://webexapis.com/identity/scim
    ```

3. Select the end of the `WEBEX_ACCESS_TOKEN=` line and paste the Service App access token directly after the `=`. Keep it on one line, with no spaces and no quotes. Do not change the other lines.

    You add only the token. The scripts read the organization ID from the token, so `.env` has no organization ID line.

4. In Notepad, select **File → Save As**, and set these fields:
    * **Folder**: `Desktop\admin-api`, the same folder as the template
    * **File name**: `.env`
    * **Save as type**: **All Files (\*.\*)**. If you leave **Text Documents**, Notepad saves `.env.txt` and the scripts cannot find it.
    * **Encoding**: **UTF-8**. Do not choose **Unicode**.
5. Select **Save**, then close Notepad. `Desktop\admin-api` now has a file named `.env` next to `env-template.txt`.

!!! warning "Treat `.env` like a password"
    `.env` now contains a live access token. Do not open it during a screen share, attach it, or paste it into chat.

**Open the lab folder in VS Code**

1. Open **VS Code**.
2. If the **Explorer** panel on the left already shows **ADMIN-API** at the top, the folder is open. Go to the next step. Otherwise, select **File → Open Folder**, select `Desktop\admin-api`, and select **Select Folder**. If VS Code asks whether you trust the authors of the files, select **Yes, I trust the authors**.
3. In the **Explorer** panel, confirm you can see the `scripts` and `data` folders and the `.env` file.

**Open a terminal**

All the Python commands in this lab run in the VS Code terminal.

1. In the VS Code menu bar at the top, select **Terminal → New Terminal**. You can also press `` Ctrl+` ``, the backtick key to the left of `1`.
2. A terminal panel opens at the bottom of the VS Code window. The prompt shows the current folder and ends with `Desktop\admin-api>`.
3. If the prompt shows a different folder, type the command below and press `Enter`:

    ```bat
    cd $HOME\Desktop\admin-api
    ```

To run a command from this guide, select the copy icon on the code block, right-click in the terminal to paste, and press `Enter`. Run every command in this lab from this terminal, in the `admin-api` folder. Each command starts with `scripts\.venv\Scripts\python.exe`, the Python that is already installed for this lab, so you do not need to install or select anything.

**Check that the scripts now act as the Service App**

1. In the terminal, run:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\00_check_token.py
    ```

2. Under **Who am I**, check that **Name** is **AdminAPI-Lab**, the same result Bruno gave you. Under **Organizations this token can administer**, check that your lab organization's **displayName** is listed.

If you see `WEBEX_ACCESS_TOKEN is not set` or a 401 error, see the troubleshooting table at the end of this lab.

### What you have now

* Bruno and the Python scripts both use the Service App access token.
* Both tools showed **AdminAPI-Lab** as the identity, so they act as the Service App, not as you.
* The personal access token from Lab 0 is no longer used anywhere in this lab.

In the next section, you create users in bulk, first in Bruno and then with a script.

## Section 3 - Bulk create

### What you are doing in this section

In Lab 0 you created one user with one call. To create many users at once, you use **SCIM 2.0 Bulk**, `POST /identity/scim/{orgId}/v2/Bulk`. One request carries a list of `operations`, and each operation creates one user.

| Tool | Which users it creates | Where the list comes from |
| --- | --- | --- |
| Bruno | `labuser02` to `labuser06` | The request body in the collection |
| VS Code | The five people in `data\users.csv`, such as `barbara.liskov` | The CSV file |

### Part A - Bruno

**Send the request**

1. In the Bruno left sidebar, under **Webex Admin API Lab**, expand the **1. Users** folder and select **Bulk create users (SCIM 2.0)**.
2. Confirm the URL bar shows `{{scim_base}}/{{org_id}}/v2/Bulk`.
3. Select the **Body** tab and confirm the JSON list is named `operations`. It creates `labuser02` to `labuser06`. `labuser01` is the user you created in Lab 0, so it is not in this list.
4. Select the arrow (**Send**) at the right end of the URL bar.

**Read the response**

The response has one entry in its operations list for each user in the request. For each entry:

* `bulkId` matches the `bulkId` in the request, such as `user-002`, so you can tell which user it is.
* `status` is `201`, which means **Created**.
* `location` is the address of the new user. The last part of it is the new user's id.

If one user fails, the whole request stops at that user, because the body sets `failOnErrors` to `1`. A `409` status means that user already exists.

### Part B - VS Code

`data\users.csv` lists names only, such as `barbara.liskov`. The script finds your pod's domain from the users already in the organization, adds it to each name, and prints it as **Lab domain**. It matches <copy><w class="TestDomain">your verified domain</w></copy>. You do not edit the CSV.

**Run the bulk create**

1. In the VS Code terminal, check that the prompt ends with `Desktop\admin-api>`.
2. Copy the command below, right-click in the terminal to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py create --csv data\users.csv --mode scim
    ```

    * `create` runs the create step of the users script.
    * `--csv data\users.csv` is the list of users to create.
    * `--mode scim` sends all users in one SCIM bulk request, the same API as Bruno.

**Read the output**

```text
Lab domain: your-domain
Creating 5 users via scim...
  [201] barbara.liskov@your-domain -> <new user id>
  ...

Done. 5 users created. Tracked in created_users.json.
```

* **Lab domain** is the domain the script added to each name in the CSV.
* Each line in brackets is one user: the status, the email address, and the new user id. `201` means **Created**.
* The last line says how many users were created. The script records their ids in `data\created_users.json`. Section 4 updates exactly these users, and cleanup deletes exactly these users, so no other user in the organization is touched.

## Section 4 - Update user titles in Bruno and VS Code

### What you are doing in this section

You now have lab users in your organization. In this section you change an attribute on them, the job **title**, and set it to `Cisco Live Attendee`. Both tools use the People API call `PUT /v1/people/{id}`, which updates one person at a time.

Each tool updates a different set of users:

| Tool | Which users it updates | How it finds them |
| --- | --- | --- |
| Bruno | The one user you created in Lab 0, `labuser01` | The `person_id` variable that **Create user** saved in the Lab environment |
| VS Code | Every user the script created in Section 3 | The ids the script recorded in `data\created_users.json` |

`PUT` replaces the whole person record, not only the fields you send. That is why each request sends the user's email address and names together with the new title. If it sent only the title, the other fields would be cleared.

### Part A - Bruno

**Send the update**

1. Switch to **Bruno**.
2. In the left sidebar, expand **Webex Admin API Lab**, then expand **1. Users**, and select **Update user (People API)**. It opens in a new tab.
3. Look at the URL bar. It shows `PUT {{base_url}}/people/{{person_id}}`. Bruno fills `{{person_id}}` with the id of `labuser01`, which **Create user** saved in Lab 0.
4. Select the **Body** tab. The JSON contains the email address, display name, first name, last name, and `"title": "Cisco Live Attendee"`. You do not need to change anything.
5. Select the arrow (**Send**) at the right end of the URL bar.

**Check the result**

1. In the response pane on the right, check that the status is **200**.
2. In the response body, find `title`. It is now `Cisco Live Attendee`.

If the status is **404**, `person_id` is empty or belongs to a user that no longer exists. Run **Create user (People API)** from Lab 0 again, then send **Update user (People API)** again.

### Part B - VS Code

The script does the same update as Bruno, but for every user it created in Section 3. For each user, it first reads the current record, then sends the full record back with the new title, so no other field is lost.

**Open the terminal**

1. Switch to **VS Code**.
2. If the terminal panel from Section 2 is still open at the bottom of the window, select it. Otherwise, select **Terminal → New Terminal** in the menu bar, or press `` Ctrl+` ``.
3. Check that the prompt ends with `Desktop\admin-api>`. If it does not, run `cd $HOME\Desktop\admin-api`.

**Run the update**

1. Select the copy icon at the top right of the code block below to copy the command:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py update --title "Cisco Live Attendee"
    ```

2. Right-click in the terminal to paste the command, then press `Enter`.

    The command has three parts:

    * `scripts\.venv\Scripts\python.exe` is the Python installed for this lab.
    * `scripts\01_bulk_users.py update` runs the update step of the users script.
    * `--title "Cisco Live Attendee"` is the title to set. Keep the quotes, because the title contains spaces.

3. Wait for the prompt to come back. The output looks like this, with one `updated` line for each user from Section 3:

    ```text
    Updating 5 users (title -> 'Cisco Live Attendee')...
      updated barbara.liskov@your-domain
      ...
    Done.
    ```

    The number of users and their email addresses depend on `data\users.csv` and on your lab domain.

If you see `Nothing to update - run 'create' first.`, the script has no users recorded in `data\created_users.json`. Go back to Section 3, run the VS Code bulk create command, and then run this update again.

**Check the result in Control Hub**

1. Switch to the browser tab with Control Hub at [admin.webex.com](https://admin.webex.com){:target="_blank"}.
2. In the left menu, under **Management**, select **Users**.
3. Search for one of the email addresses from the script output, and select that user to open their details.
4. Check that the title is **Cisco Live Attendee**.
5. Search for `labuser01` as well, and check that the Bruno update also set its title.

### What you have now

* `labuser01` has the title `Cisco Live Attendee`, set by Bruno.
* Every user the script created in Section 3 has the same title, set by VS Code.
* You saw that `PUT /v1/people/{id}` needs the full person record, and that the script reads each record before it updates it.

Go through the checkpoint below before you start Lab 2.

## Checkpoint

You are ready for Lab 2 when:

* [ ] **Who am I** in Bruno shows the Service App
* [ ] **List organizations** shows your lab organization
* [ ] `.env` is saved as UTF-8 with the Service App access token, and `00_check_token.py` shows **AdminAPI-Lab**
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
| SCIM rejects the organization id | In Bruno, open the Lab environment (**Configure**) and check that `org_id` is the **Organization ID** from Control Hub (**Management → Account → Info**). Select **Save**, then send bulk create again. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 409 on create | That email already exists. Use a different address in the CSV or in the Bruno body. |

Continue to [Lab 2](lab2_licenses.md).
