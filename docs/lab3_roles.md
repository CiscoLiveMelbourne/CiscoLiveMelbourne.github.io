# Lab 3 - Roles

**Time: 32-40 min**

List the administrator roles in Bruno first, then in VS Code. Assigning a role runs in VS Code only, because the Bruno collection has no assign request.

## Section 1 - List roles

### What you are doing in this section

Administrator roles, such as **Full Administrator** and **Read-only Administrator**, control what a person can do in Control Hub. Each role has a name and an id. To assign a role with the API, you need its id, so you first list the roles with `GET /v1/roles`.

### Part A - Bruno

1. In the Bruno left sidebar, under **Webex Admin API Lab**, expand the **3. Roles** folder and select **List available roles**.
2. Select the arrow (**Send**) at the right end of the URL bar.

**Read the response**

The status is **200**. The `items` list has one entry per role:

* `name` is the role name you see in Control Hub, for example **Read-only Administrator**.
* `id` is the role id. This is the value the People API stores in a person's `roles` list.

Find **Read-only Administrator**. You assign it in Section 2.

### Part B - VS Code

1. In the VS Code terminal, check that the prompt ends with `Desktop\admin-api>`.
2. Copy the command below, right-click in the terminal to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\03_roles.py list
    ```

**Read the output**

The script prints a table sorted by name, with **Role name** on the left and **Role ID** on the right. The last line, `<n> roles available.`, says how many roles the organization has. The names and ids match the Bruno response.

## Section 2 - Assign a role

### What you are doing in this section

You give the **Read-only Administrator** role to `labuser01`, the user you created in Lab 0. The script does three things:

1. It finds the id of the role by its name.
2. It reads the user's current record, including the roles the user already has.
3. It adds the new role and sends the full record back with `PUT /v1/people/{id}`, so the user keeps any roles they already had.

This is VS Code only.

### Run the assignment

1. In the VS Code terminal, copy the command below, right-click to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\03_roles.py assign --email labuser01 --role "Read-only Administrator"
    ```

    * `--email labuser01` is the user. You give only the name, and the script adds your lab domain.
    * `--role "Read-only Administrator"` is the role name, exactly as the list shows it. Keep the quotes, because the name contains spaces.

### Read the output

```text
Lab domain: your-domain
Assigned role 'Read-only Administrator' to labuser01@your-domain.
  labuser01@your-domain now has 1 role(s).
```

* The first line is the domain the script added to `labuser01`.
* The second line confirms the role was assigned.
* The third line is the total number of roles the user now holds. It is `1` because `labuser01` had no roles before.

### Check the result in Control Hub

1. In Control Hub at [admin.webex.com](https://admin.webex.com){:target="_blank"}, under **Management**, select **Users**.
2. Search for `labuser01` and select the user to open their details.
3. Check that **Read-only Administrator** is listed as the user's administrator role.

## Checkpoint

You are ready for Lab 4 when:

* [ ] Bruno and VS Code both listed the roles
* [ ] VS Code assigned **Read-only Administrator** to `labuser01`, and Control Hub shows it

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `No user found with email` | That user must already exist. Run **Create user (People API)** from Lab 0 first. If you typed a full email, its domain must be <copy><w class="TestDomain">your verified domain</w></copy>. |
| `Role '...' not found` | The role name is mistyped. Run the `list` command and copy the name exactly. |
| 403 on assign | The Service App needs `spark-admin:people_write` and `spark-admin:roles_read`. Add the scope, authorize the app again, and generate a new access token. |

Continue to [Lab 4](lab4_hybrid_licenses.md).
