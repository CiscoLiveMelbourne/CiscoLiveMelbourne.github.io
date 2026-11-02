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
* Check Hybrid licenses in both tools, and assign the Hybrid Calendar license from the script.

## Learning objectives

By the end of this lab you will be able to:

* Tell a personal access token apart from a Service App access token, and put each one in the right place.
* Create one user with the People API and many users with SCIM bulk.
* Read organization license usage and admin roles.
* Assign an admin role from a script.
* Check Hybrid Services licenses and assign the Hybrid Calendar license from a script.
* Remove only the users this lab created.

## Disclaimer

Although the lab design and configuration examples could be used as a reference, for design related questions for your production environments please contact your representative at Cisco, or a Cisco partner.

Use only the lab organization. Do not connect these tokens or scripts to your production Webex organization.

## Lab access

Your pod is a Cisco dCloud Windows desktop with a browser, **Bruno**, **VS Code**, and the prepared `Desktop\admin-api` folder. You do not need to install any software. Use **Google Chrome on your own computer** for both this lab guide and the dCloud Web RDP session.

!!! danger "Do not end your dCloud session during the lab"
    **Do not select "Logout and End Session" in dCloud Expo.**

    That tears down your assigned lab pod, including the prepared Windows desktop and its Webex organization, and bringing it back can take longer than this lab. If your Web RDP tab closes or disconnects, return to Expo and select **Open** for your existing **wkst1** session. If you cannot reconnect, ask a proctor for help; do not end or restart the session yourself.

1. In Chrome on your own computer, open the Cisco Live dCloud Expo lab.
2. Enter your email address and accept the lab terms. Expo assigns your session ID; keep it available in case you need a proctor's help.
3. Select **Open** to launch the browser-based RDP session for **wkst1**, using the Windows user **cholland**.
4. Your proctor gives you the Webex administrator email, password, and verified email domain for this pod. Use them only inside the lab desktop.
5. Keep this lab guide open in a **second Chrome tab on your own computer**. Copy commands and values from that tab and paste them into Bruno, VS Code, or Notepad in the RDP tab. You do not need to open the guide inside the lab desktop. Open Control Hub and developer.webex.com **inside** the lab desktop when the guide asks you to sign in.

If Expo access or sign-in fails, give your session ID to a proctor. Do not enter the administrator password anywhere except the Webex sign-in pages on the lab desktop and the form below, which stays in your browser.

If pasting into the RDP session does not work, use Guacamole's clipboard panel or ask a proctor. See the [Troubleshooting Matrix](reference/troubleshooting.md).

### Enter your lab values

Enter the administrator email, password, and verified email domain from your proctor below, and the organization ID you copy from Control Hub. The guide then fills these values into the steps for you. They stay in this browser only.

### Find your organization ID

1. On the lab desktop, open a browser and go to [admin.webex.com](https://admin.webex.com){:target="_blank"}.
2. Sign in with the Webex admin email and password from your proctor.
3. In the left menu, under **Management**, select **Account**.
4. On the **Info** tab, find **Organization ID** and select the copy icon next to it.
5. Paste the value into the **Organization ID** field below.

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
> Organization ID: <copy><w class="OrgId">Copied from Control Hub</w></copy>

</div>

!!! important
    The values you enter above are stored only in your own browser session. They are never sent anywhere.

!!! danger "Do not put your access token in this form"
    Tokens belong in a Bruno secret or in `.env`. Do not paste them into this guide, chat, or a screenshot.

## Getting started

### What you should know

You should be comfortable signing in to Control Hub and reading a JSON response. You do not need to write Python. Every section has a **Bruno** step and then a **VS Code** step. Always run Bruno first.

**Bruno** sends one REST call that you can read. **The script** sends the same kind of call for every row in a file, and it records the users it created so cleanup can delete only those users.

### Your first five minutes

1. On the lab desktop, open **Control Hub** and sign in as <copy><w class="WbxUser">your lab admin</w></copy>. Confirm you can see users.
2. Open **Bruno** and **VS Code**. Lab 0 walks you through Bruno, and Lab 1 through VS Code.
3. Continue to [Lab 0](lab0_token.md).

## Lab rules

1. **Keep the token in Bruno or `.env`.** Do not paste it into chat, a screenshot, or this guide.
2. **Stay in the lab organization.** Do not point these calls at production.
3. **Clean up at the end.** The script deletes only users it recorded. Confirm the result in Control Hub.

## Lab flow and timing

| Time | Module | What you do |
| ---: | --- | --- |
| 0-8 min | Orientation | Sign in, open Bruno and VS Code |
| 8-12 min | [Lab 0](lab0_token.md) | Who am I and Create user in Bruno |
| 12-25 min | [Lab 1](lab1_users.md) | Service App token, then bulk create and update in both tools |
| 25-32 min | [Lab 2](lab2_licenses.md) | List licenses in both tools |
| 32-40 min | [Lab 3](lab3_roles.md) | List roles in both tools; assign a role from the script |
| 40-55 min | [Lab 4](lab4_hybrid_licenses.md) | Hybrid licenses in both tools; assign Hybrid Calendar from the script |
| 55-60 min | [Wrap-up](conclusion.md) | Cleanup and take-home |

!!! note
    Lab 0 is Bruno only, with your personal access token. From Lab 1 on, every section is Bruno first, then VS Code, with the same Service App access token.
