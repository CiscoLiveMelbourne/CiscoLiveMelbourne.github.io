# Lab 2 - License usage

**Time: 25-32 min**

Keep the Service App access token from Lab 1. List the same licenses in Bruno first, then in VS Code.

## Section 1 - List licenses

### What you are doing in this section

Every Webex organization has a set of licenses, such as Meetings, Messaging, Calling, and Hybrid Services. Each license has a fixed number of units, and each user who holds the license uses one unit. In this section you read that usage with one API call, `GET /v1/licenses`, in both tools:

| Tool | What it shows |
| --- | --- |
| Bruno | The raw JSON response, exactly as the API returns it |
| VS Code | The same data as a table, with free units and a status for each license |

### Part A - Bruno

**Send the request**

1. Switch to **Bruno**.
2. In the left sidebar, expand **Webex Admin API Lab**, then expand **2. Licenses**, and select **List licenses (usage)**.
3. Confirm the URL bar includes `orgId={{org_id}}`. `org_id` is the organization ID you set in the Lab environment in Lab 0.
4. Select the arrow (**Send**) at the right end of the URL bar.

**Read the response**

The status is **200**. The response body has an `items` list with one entry for each license in the organization. Each entry includes:

| Field | What it tells you |
| --- | --- |
| `id` | The license id. Scripts use it to assign the license to a user. |
| `name` | The license name, for example `Webex Meetings Suite` |
| `totalUnits` | How many units the organization owns |
| `consumedUnits` | How many units are assigned to users |

Bruno does not calculate anything. To know how many units are free, you subtract `consumedUnits` from `totalUnits` yourself. The script does that for you in Part B.

### Part B - VS Code

**Open the terminal**

1. Switch to **VS Code**.
2. If the terminal panel from Lab 1 is still open at the bottom of the window, select it. Otherwise, select **Terminal → New Terminal** in the menu bar, or press `` Ctrl+` ``.
3. Check that the prompt ends with `Desktop\admin-api>`. If it does not, run `cd $HOME\Desktop\admin-api`.

**Run the license report**

1. Select the copy icon at the top right of the code block below to copy the command:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\02_license_usage.py
    ```

2. Right-click in the terminal to paste the command, then press `Enter`.

**Read the output**

The script prints a table with one row per license, sorted by name, and then a summary:

| Column | What it tells you |
| --- | --- |
| **License** | The license name, the same as `name` in Bruno |
| **Used** | Units assigned to users, the same as `consumedUnits` in Bruno |
| **Total** | Units the organization owns, the same as `totalUnits` in Bruno |
| **Free** | Units still available, calculated as Total minus Used |
| **Status** | `ok`, `NEAR LIMIT (n%)` when the license is at least 90% used, or `OVER-ALLOCATED` when more units are used than owned |

Under **Validation summary**, the script lists every license that needs attention. On a typical lab pod it reports **4 license(s) need attention**: the licenses that are 100% used, such as **Basic Messaging** with `19/19`. Your exact licenses and numbers depend on your pod.

Compare a few rows with the Bruno response. The Used and Total numbers match, because both tools read the same API.

## Section 2 - Flag licenses near their limit

### What you are doing in this section

The script decides what **NEAR LIMIT** means with a threshold. By default, it flags a license when it is at least **90%** used. You can change the threshold with the `--threshold` option, without changing the script. The value is a fraction, so `0.15` means 15%.

In this section you run the same report with `--threshold 0.15`. The lab pods have low license usage, so a low threshold is needed to make the effect visible. In a production organization you would use a value such as `0.8` or `0.9` to get a warning before a license runs out.

This is VS Code only. Bruno shows the raw numbers and does not apply a threshold.

### Run the report with a lower threshold

1. In the VS Code terminal, copy and paste the command below, then press `Enter`:

    ```bat
    scripts\.venv\Scripts\python.exe scripts\02_license_usage.py --threshold 0.15
    ```

### Read the output

Compare this output with the one from Section 1.

* **Used**, **Total**, and **Free** are exactly the same. The data in the organization did not change.
* The **Status** column changes for licenses that are between 15% and 90% used. For example, licenses with `8` used out of `50` (16%), such as **Advanced Messaging**, **Advanced Space Meetings**, **Real-Time Translations**, and **Webex Meetings Suite**, change from `ok` to `NEAR LIMIT (16%)`.
* Licenses that are 100% used are flagged in both runs. Licenses with `0` used stay `ok`.
* The **Validation summary** grows, for example from **4** to **8** licenses that need attention.

Only the rule changed, not the data. This is the difference between the two tools: Bruno shows you what the API returns, and the script applies a policy that you choose on top of it.

If the Status column does not change, your pod has no licenses between 15% and 90% used. That is a valid result. Record it and continue.

## Checkpoint

You are ready for Lab 3 when:

* [ ] Bruno **List licenses (usage)** returned the organization license list
* [ ] VS Code printed used, total, and free for the same licenses
* [ ] The `--threshold 0.15` run flagged more licenses than the default run, or you confirmed your pod has no licenses between 15% and 90% used

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 | Replace the Bruno secret and `WEBEX_ACCESS_TOKEN` with a new Service App access token. |
| Empty `orgId` or a 400 on the query | `org_id` is not set. In Bruno, enter the **Organization ID** from Control Hub in the Lab environment as in Lab 0, select **Save**, and send again. |
| `WEBEX_ACCESS_TOKEN is not set` | Save `.env` in `Desktop\admin-api` and run the command from that folder. |
| `No licenses returned` | The Service App is missing the `spark-admin:licenses_read` scope. Add the scope, authorize the app again in Control Hub, and generate a new access token. |
| `--threshold` run looks the same as the default run | No license is between 15% and 90% used on your pod. This is expected. |

Continue to [Lab 3](lab3_roles.md).
