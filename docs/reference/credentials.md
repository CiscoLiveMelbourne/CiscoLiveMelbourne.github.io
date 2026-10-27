# Lab Credentials

Use the reservation administrator for Control Hub and token generation. Put the **access token** only in `.env` or Bruno — not on this page.

## Your account

<div class="grid" markdown>

<form id="info">
<label for="info">Enter the values provided by your proctor</label><br>

  <label for="WbxUser">Webex admin email:</label>
  <input type="text" id="WbxUser" name="WbxUser"><br>

  <label for="WbxPW">Webex admin password:</label>
  <input type="text" id="WbxPW" name="WbxPW"><br>

  <label for="TestDomain">dCloud verified domain:</label>
  <input type="text" id="TestDomain" name="TestDomain"><br>

  <label for="OrgId">Organization ID:</label>
  <input type="text" id="OrgId" name="OrgId"><br>

  <label for="Pod">Pod ID:</label>
  <input type="text" id="Pod" name="Pod"><br>
  <br>
  <button onclick="setValues()">Update Lab Guide</button>
</form>

> Webex admin email: <copy><w class="WbxUser">Provided by proctor</w></copy>
>
> Webex admin password: <copy><w class="WbxPW">Provided by proctor</w></copy>
>
> dCloud verified domain: <copy><w class="TestDomain">Provided by proctor</w></copy>
>
> Organization ID: <copy><w class="OrgId">Fill after Lab 1</w></copy>
>
> Pod ID: <copy><w class="Pod">Provided by proctor</w></copy>

</div>

!!! important "Lab use only"
    These credentials are valid only for the duration of this lab session. The reservation and organization may be reset after the event.

!!! note
    Values you enter above are stored only in your own browser session. They are never sent anywhere.

## Where you will use these credentials

| Step | Where | What you do |
| --- | --- | --- |
| Overview | [dcloud.cisco.com](https://dcloud.cisco.com/){:target="_blank"} | Confirm reservation Active |
| Overview | [admin.webex.com](https://admin.webex.com/){:target="_blank"} | Sign in and confirm the org |
| Lab 0 | [developer.webex.com](https://developer.webex.com/){:target="_blank"} | Copy the personal access token |
| Lab 1 | Service App **Org Authorizations** | Copy **access_token** after you authorize the app |
| Bruno, Lab 0 | Lab environment secret `access_token` | Personal access token for Who am I and Create user |
| Bruno, Lab 1 onward | Same secret, replaced | Service App access token, `test_domain`, `org_id` |
| VS Code | Local `.env` | `WEBEX_ACCESS_TOKEN` is the Service App access token. The scripts read the organization id from it |

## Tokens you will generate

| Token | Created in | Where it goes | Lifetime |
| --- | --- | --- | --- |
| Personal access token | developer.webex.com, any API page | Bruno secret `access_token` for Who am I and Create user | ~12 hours |
| Service App access token | Org Authorizations → Generate tokens | Bruno secret `access_token` for bulk create, and `.env` as `WEBEX_ACCESS_TOKEN` | ~14 days |

!!! danger "Protect every token"
    Do not paste tokens into this guide, source files, screenshots, Git repositories, or Webex messages.
