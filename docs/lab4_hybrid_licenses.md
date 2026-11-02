# Lab 4 - Hybrid Services licenses

**Time: 40-55 min**

Bruno returns every license. The script prints only the Hybrid Services licenses. Check Bruno first, then VS Code. Then assign the Hybrid Calendar license to the users in `data\users.csv` and see who holds it.

No Hybrid Services setup is needed. The Hybrid Calendar license is part of the organization's subscription, so you can assign it even when no Expressway connector is running.

## Section 1 - Find the Hybrid licenses

### What you are doing in this section

Hybrid Services connect Webex to systems you run yourself, such as Microsoft Exchange or Google calendars. Each Hybrid Service is a license in the organization, so you find them with the same `GET /v1/licenses` call you ran in Lab 2. Bruno returns every license, and you look for the Hybrid ones yourself. The script filters the list for you.

### Part A - Bruno

1. In the Bruno left sidebar, under **Webex Admin API Lab**, expand the **2. Licenses** folder and select **List licenses (usage)**.
2. Select the arrow (**Send**) at the right end of the URL bar.
3. In the response pane on the right, find the licenses whose `name` starts with **Hybrid**.

**Read the response**

On a typical lab pod you find three Hybrid licenses: **Hybrid - Exchange Calendar**, **Hybrid - Google Calendar**, and **Hybrid - Message**. For each one, `consumedUnits` is `0`, because no user holds it yet, and `totalUnits` is the number the organization owns, for example `19`. Note the numbers so you can compare them after Section 2.

### Part B - VS Code

1. In the VS Code terminal, check that the prompt ends with `Desktop\admin-api>`.
2. Copy the command below, right-click in the terminal to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py
    ```

**Read the output**

Under **== Hybrid Services licenses ==**, the script prints each Hybrid license with:

* `id`, the license id that the assign script uses in Section 2
* `consumed`, shown as used / total, for example `0 / 19`

The last line, `Re-run with --show-users to list assigned users.`, points to Section 3. The licenses and numbers match the Hybrid rows in Bruno.

If the script prints `No Hybrid Services licenses found in this org.`, your organization has no Hybrid license. It then lists all licenses instead. That is a valid result for this lab. Record it and continue.

## Section 2 - Assign the Hybrid Calendar license

### What you are doing in this section

You assign the Hybrid Calendar license to the five users in `data\users.csv`, the same users you created in Lab 1. For each user, the script calls `PATCH /v1/licenses/users` with the user's email, the organization id, the license id, and `"operation": "add"`. `PATCH` adds the license without removing any license the user already has.

This is VS Code only. Bruno has no assign request.

You run the script twice:

| Run | What it does |
| --- | --- |
| With `--dry-run` | Shows what would change. Nothing is assigned. |
| Without `--dry-run` | Assigns the license. |

A dry run is a safe habit before any change to many users at once.

### Run a dry run

1. In the VS Code terminal, copy the command below, right-click to paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\05_assign_hybrid_calendar.py --dry-run
    ```

2. Read the output:

    ```text
    Lab domain: your-domain
    Several calendar licenses found; using the first:
      Hybrid - Exchange Calendar  [<license id>]
      Hybrid - Google Calendar  [<license id>]
    License: Hybrid - Exchange Calendar (0 / 19 used)
    Users in users.csv: 5  [dry run]

      would assign   barbara.liskov@your-domain
      ...

    Would assign: 5  Already had it: 0  Not found: 0  Failed: 0
    ```

    * **Several calendar licenses found** appears because the pod has both an Exchange and a Google calendar license. The script uses the first one in the list. Your pod may pick either.
    * **License** is the license the script will assign, with its current usage.
    * Each `would assign` line is a user who does not have the license yet.
    * The last line is the summary. Nothing has changed yet.

### Assign the license

1. Copy the command below, paste it in the terminal, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\05_assign_hybrid_calendar.py
    ```

2. Read the output. It is the same as the dry run, except:

    * Each user line says `assigned` instead of `would assign`.
    * The summary starts with `Assigned: 5`.

If you run the command again, each user shows `already has it` and the summary shows `Already had it: 5`. The script skips users who already hold the license, so running it again is safe.

## Section 3 - See who holds each Hybrid license

### What you are doing in this section

You check the result of Section 2. The script lists every user in the organization and groups them by the Hybrid licenses they hold.

1. In the VS Code terminal, copy the command below, paste it, and press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\04_hybrid_licenses.py --show-users
    ```

### Read the output

The first part is the same Hybrid license list as Section 1. The calendar license you assigned now shows `consumed : 5 / 19` instead of `0 / 19`. If it still shows `0`, wait a minute and run the command again; the usage count can take a short time to update.

Under **== Assigned users per hybrid license ==**, each Hybrid license shows how many users hold it, followed by their names and email addresses:

```text
  Hybrid - Exchange Calendar: 5 user(s)
    - Barbara Liskov                 barbara.liskov@your-domain
    ...
  Hybrid - Google Calendar: 0 user(s)
  Hybrid - Message: 0 user(s)

<n> users scanned.
```

* The license you assigned lists the five users from `data\users.csv`.
* The other Hybrid licenses show `0 user(s)`.
* `users scanned` is how many users in the organization the script checked.

You can also send **List licenses (usage)** in Bruno again. `consumedUnits` for that calendar license is now `5`.

## Checkpoint

You are ready for the conclusion when:

* [ ] You found the Hybrid rows in the Bruno license list, or confirmed there are none
* [ ] VS Code printed the same Hybrid licenses, or reported there are none
* [ ] The dry run showed `would assign` for the CSV users
* [ ] VS Code assigned the Hybrid Calendar license to the CSV users
* [ ] `--show-users` lists the CSV users under the Hybrid Calendar license

## Troubleshooting

| Problem | Solution |
| --- | --- |
| VS Code prints nothing about Hybrid | Compare it with the Bruno list. If Bruno also has no Hybrid license, the organization does not have one. |
| `No Hybrid Calendar license found in this org` | The organization has no Hybrid Calendar license. Record it and continue. |
| `not found` for CSV users | Those users do not exist. Run the Lab 1 bulk create first, and check that the **Lab domain** the script prints is your verified domain. Cleanup runs only in the [Conclusion](conclusion.md). |
| `FAILED` with 403 on assign | The Service App needs `spark-admin:people_write` and `spark-admin:licenses_read`. Add the scope, authorize the app again, and generate a new access token. |
| CSV file not found | The VS Code terminal is not in `Desktop\admin-api`. |
| 401 | Use the current Service App access token in Bruno and in `.env`. |

Continue to the [Conclusion](conclusion.md).
