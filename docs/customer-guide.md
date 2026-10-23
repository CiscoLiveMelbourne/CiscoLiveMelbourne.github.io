# Customer guide

This is the lab. Keep Bruno and VS Code open together. Your folder is `C:\Users\cholland\Desktop\admin-api`. You do not install Python.

**Who am I** and **Create user** run in Bruno first, with your personal access token. Every later call runs in Bruno and in the Python script, with the same Service App access token.

## 1. Sign in and open both tools

Sign in to [Control Hub](https://admin.webex.com){:target="_blank"} with the lab administrator from the [Overview](overview.md) form.

**Bruno**

1. Open Bruno and select **Open Collection**. Choose `C:\Users\cholland\Desktop\admin-api\bruno\Webex Admin API Lab`.
2. Select the **Lab** environment.
3. Set `test_domain` to the verified domain from the Overview form. Do not include `@`.

**VS Code**

1. Choose **File → Open Folder** and open `C:\Users\cholland\Desktop\admin-api`.
2. Select the Python interpreter `scripts\.venv\Scripts\python.exe`.
3. Open a terminal in that window. The working directory must stay `admin-api`.

## 2. Who am I and Create user in Bruno

Open [developer.webex.com](https://developer.webex.com){:target="_blank"} as the lab administrator. On any API page, copy your **personal access token**. It lasts about 12 hours.

1. Put that token in the Bruno secret `access_token`. Leave it out of the Headers tab.
2. Run **0. Setup → Who am I**. **displayName** is the lab administrator.
3. Run **1. Users → Create user**. Control Hub shows the new user.

Stop there in Bruno. Bulk create and the later calls use a Service App token in both tools.

## 3. Put the Service App token in both tools

1. At [developer.webex.com](https://developer.webex.com){:target="_blank"}, go to **My Webex Apps → Create a Service App**.
2. Request these scopes:
    - `spark-admin:people_read`, `spark-admin:people_write`
    - `identity:people_rw`
    - `spark-admin:licenses_read`
    - `spark-admin:roles_read`
    - `spark-admin:organizations_read`
    - `spark-admin:hybrid_clusters_read`
    - `spark-admin:hybrid_connectors_read`
3. In Control Hub, authorize the app for this dCloud organization.
4. On the Service App page, open **Org Authorizations**, select this org, and choose **Generate tokens**.
5. Copy **access_token**. That value contains `_P0A1_` and lasts about 14 days. Leave the client secret and the refresh token where they are.

**Bruno.** Replace the `access_token` secret with this Service App access token. Run **0. Setup → List organizations**. That saves the base64 organization id as `org_id` and the UUID as `orgid`.

**`.env`.** Open `C:\Users\cholland\Desktop\admin-api\env-template.txt`. The file contains only these four lines:

```text
WEBEX_ACCESS_TOKEN=
WEBEX_ORG_ID=

WEBEX_API_BASE=https://webexapis.com/v1
WEBEX_SCIM_BASE=https://webexapis.com/identity/scim
```

| Line | What you paste |
|---|---|
| `WEBEX_ACCESS_TOKEN` | The same Service App **access_token**. One line, no quotes. |
| `WEBEX_ORG_ID` | The SCIM UUID, the same value as Bruno `orgid`. It is the part after `ORGANIZATION/`. |

Leave the two URL lines as they are. No spaces around `=`. Do not paste a JSON body, the client secret, the refresh token, or the personal access token into this file.

In Notepad, choose **File → Save As**. Set **Save as type** to **All Files** and **Encoding** to **UTF-8**. Name the file `.env` and save it in `C:\Users\cholland\Desktop\admin-api`. Do not choose **Unicode**.

**Check both tools.** Bruno **Who am I** now shows the Service App. In the VS Code terminal:

```bat
scripts\.venv\Scripts\python.exe scripts\00_check_token.py
```

**Name** is the Service App. If `WEBEX_ORG_ID` is empty, copy the printed **SCIM orgid** into that line and save `.env` again.

## 4. The same calls, both ways

Run the Bruno request, then the script command under it. Licenses and hybrid calls in Bruno use `org_id` (base64). SCIM bulk uses `orgid` (UUID).

### Bulk create {#bulk-create}

Edit `data\users.csv` so each email uses the verified domain before you run the script.

| Bruno | Script |
|---|---|
| **1. Users → Bulk create users**. URL `{{scim_base}}/{{orgid}}/v2/Bulk`. The JSON field is `operations`. | The command below. The script reads the CSV and writes new ids to `data\created_users.json`. Bruno does not write that file. |

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py create --csv data\users.csv --mode scim
```

Each created user prints a status starting with `201`.

### Update {#update}

| Bruno | Script |
|---|---|
| **1. Users → Update user**. Uses `person_id` saved by **Create user**, and sets the title `Cisco Live Attendee`. | Updates every user the script recorded in `data\created_users.json`. |

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py update --title "Cisco Live Attendee"
```

### Cleanup {#cleanup}

Run this at the end of the lab if you still need the users for role assignment.

| Bruno | Script |
|---|---|
| **1. Users → Delete user**. Deletes the one user in `person_id`. | Deletes only the users this script created. |

```bat
scripts\.venv\Scripts\python.exe scripts\01_bulk_users.py cleanup
```

### Licenses {#licenses}

| Bruno | Script |
|---|---|
| **2. Licenses → List licenses**. `GET /licenses?orgId={{org_id}}`. | Prints used, total, free, and flags a license near the limit. |

```bat
scripts\.venv\Scripts\python.exe scripts\02_license_usage.py
```

### Roles {#roles}

| Bruno | Script |
|---|---|
| **3. Roles → List roles**. | Prints the same role names and ids. |

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py list
```

Assigning a role is the script only. Bruno has no assign request. Use an email on your verified domain:

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py assign --email labuser01@YOUR-DCLOUD-DOMAIN --role "Read-only Administrator"
```

### Hybrid licenses {#hybrid-licenses}

| Bruno | Script |
|---|---|
| **2. Licenses → List licenses** includes Hybrid licenses in the full list. | Prints only Hybrid Calendar, Call, and Message licenses. |

```bat
scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py
```

Add `--show-users` to list who holds each Hybrid license. An empty result means this organization has no Hybrid license enabled.

### Hybrid clusters and connectors {#hybrid-health}

| Bruno | Script |
|---|---|
| **4 & 5. Hybrid Services → List hybrid clusters**, then **List hybrid connectors**. | Prints both lists and flags a connector that is not `running`. |

```bat
scripts\.venv\Scripts\python.exe scripts\05_hybrid_health.py
```

An empty list is normal on this lab when no Expressway connector is registered.

## If a call fails

| What you see | What to do |
|---|---|
| 401 | Generate a new Service App **access_token**. Replace the Bruno secret and `WEBEX_ACCESS_TOKEN`. Save `.env` as UTF-8 and start the run again. |
| Who am I still shows the lab administrator | That tool still has the personal token. Put the Service App access token in the Bruno secret and in `.env`. |
| CSV file not found | The VS Code terminal is not in `C:\Users\cholland\Desktop\admin-api`. |
| SCIM 400 on `Operations` | Rename that JSON field to `operations`. |
| SCIM bulk rejects the org id | Bruno `orgid` and `WEBEX_ORG_ID` must be the UUID, not the `Y2lz` value. |
