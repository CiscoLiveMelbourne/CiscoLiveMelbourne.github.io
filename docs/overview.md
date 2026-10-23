# Overview

**Format:** hands-on lab · **Level:** intermediate · **Duration:** ~45–60 min

**Audience:** administrators and automation engineers comfortable with REST APIs

## What you will build

You will call the Webex Admin APIs for your lab organization from two tools at the same time: Bruno, and a Python script in VS Code. The folder `Desktop\admin-api` is already on the lab desktop. You do not install Python.

1 - See who the token is, and create one user

* Sign in to Control Hub and to developer.webex.com as the lab administrator.
* In Bruno, run **Who am I** and **Create user** with your personal access token.

2 - Create many users, then manage what you created

* Authorize a Service App and use its access token in Bruno and in `.env`.
* Create users from a CSV with SCIM bulk, in Bruno and in the script.
* Update their title, then delete only the users this lab created.

3 - Read licenses, roles, and Hybrid Services

* List license usage in Bruno and in the script.
* List roles in both tools, and assign one role from the script.
* Check Hybrid licenses, clusters, and connectors in both tools.

## Learning objectives

By the end of this lab you will be able to:

* Tell a personal access token apart from a Service App access token, and put each one in the right place.
* Create one user with the People API and many users with SCIM bulk.
* Read organization license usage and admin roles.
* Assign an admin role from a script.
* Check Hybrid Services licenses, clusters, and connectors.
* Remove only the users this lab created.

## Disclaimer

Although the lab design and configuration examples could be used as a reference, for design related questions for your production environments please contact your representative at Cisco, or a Cisco partner.

Use only the lab organization. Do not connect these tokens or scripts to your production Webex organization.

## Lab access

The lab desktop already has Bruno, VS Code, and the `admin-api` folder. Your proctor gives you the administrator email, password, and verified email domain. Enter them below. They stay in this browser only.

<div class="grid" markdown>

<form id="info">
<label for="info">Enter the values provided by your proctor</label><br>

  <label for="WbxUser">Webex admin email:</label>
  <input type="text" id="WbxUser" name="WbxUser"><br>

  <label for="WbxPW">Webex admin password:</label>
  <input type="text" id="WbxPW" name="WbxPW"><br>

  <label for="TestDomain">Verified email domain:</label>
  <input type="text" id="TestDomain" name="TestDomain"><br>

  <label for="OrgId">Organization ID:</label>
  <input type="text" id="OrgId" name="OrgId"><br>
  <br>
  <button onclick="setValues()">Update Lab Guide</button>
</form>

> Webex admin email: <copy><w class="WbxUser">Provided by proctor</w></copy>
>
> Webex admin password: <copy><w class="WbxPW">Provided by proctor</w></copy>
>
> Verified email domain: <copy><w class="TestDomain">Provided by proctor</w></copy>
>
> Organization ID: <copy><w class="OrgId">Fill after List organizations</w></copy>

</div>

!!! important
    The values you enter above are stored only in your own browser session. They are never sent anywhere.

!!! danger "Do not put your access token in this form"
    Tokens belong in a Bruno secret or in `.env`. Do not paste them into this guide, chat, or a screenshot.

## Getting started

### What you should know

You should be comfortable signing in to Control Hub and reading a JSON response. You do not need to write Python. Each lab shows the Bruno request and, from Lab 1 on, the matching script command.

**Bruno** sends one REST call that you can read. **The script** sends the same kind of call for every row in a file, and it records the users it created so cleanup can delete only those users.

### Your first five minutes

1. On the lab desktop, open **Control Hub** and sign in as <copy><w class="WbxUser">your lab admin</w></copy>. Confirm you can see users.
2. Open **Bruno**. Choose **Open Collection** and select `Desktop\admin-api\bruno\Webex Admin API Lab`. Select the **Lab** environment.
3. Open **VS Code**. Choose **File → Open Folder** and open `Desktop\admin-api`. Select the interpreter `scripts\.venv\Scripts\python.exe`.
4. Continue to [Lab 0](lab0_token.md). Lab 0 is Bruno only.

## Lab rules

1. **Keep the token in Bruno or `.env`.** Do not paste it into chat, a screenshot, or this guide.
2. **Stay in the lab organization.** Do not point these calls at production.
3. **Clean up at the end.** The script deletes only users it recorded. Confirm the result in Control Hub.

## Lab flow and timing

| Time | Module | What you do |
| ---: | --- | --- |
| 0-8 min | Orientation | Sign in, open Bruno and VS Code |
| 8-12 min | [Lab 0](lab0_token.md) | Who am I and Create user in Bruno |
| 12-25 min | [Lab 1](lab1_users.md) | Service App token, then bulk create, update, and cleanup in both tools |
| 25-32 min | [Lab 2](lab2_licenses.md) | List licenses in both tools |
| 32-40 min | [Lab 3](lab3_roles.md) | List roles in both tools; assign a role from the script |
| 40-48 min | [Lab 4](lab4_hybrid_licenses.md) | Hybrid licenses in both tools |
| 48-55 min | [Lab 5](lab5_hybrid_health.md) | Clusters and connectors in both tools |
| 55-60 min | [Wrap-up](conclusion.md) | Cleanup and take-home |

!!! note
    Do Lab 0 in Bruno before you create the Service App. From Lab 1 on, run the Bruno request and then the script command in the same section.
