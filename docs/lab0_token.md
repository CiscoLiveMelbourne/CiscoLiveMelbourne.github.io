# Lab 0 - Who am I and create one user

**Time: 8-12 min**

This lab is Bruno only. Use your personal access token to see who you are, then create one user. VS Code starts in Lab 1, after you create the Service App.

## Section 1 - Open Bruno

The collection is already on the lab desktop.

1. Open **Bruno**.
2. Select **Open Collection** and choose `Desktop\admin-api\bruno\Webex Admin API Lab`.
3. In the environment list at the top right, select **Lab**.
4. Set `test_domain` to <copy><w class="TestDomain">your verified domain</w></copy>. Do not type `@`.

## Section 2 - Add your personal access token

1. On the lab desktop, open [developer.webex.com](https://developer.webex.com){:target="_blank"} and sign in as <copy><w class="WbxUser">your lab admin</w></copy>.
2. Open any API page and copy the **personal access token**. It lasts about 12 hours.
3. In the **Lab** environment, open **Secrets** and paste the token into `access_token`.
4. Leave **Headers** as `Accept: application/json`. Do not put the token in a header yourself. The collection already sends it as `Authorization: Bearer`.

## Section 3 - Who am I

1. Open **0. Setup → Who am I**.
2. Select **Send**.

**displayName** is the lab administrator. The call is `GET /v1/people/me`.

## Section 4 - Create one user

1. Open **1. Users → Create user**.
2. Confirm the email uses `{{test_domain}}`.
3. Select **Send**.

The response status is **200**. Bruno saves `person_id` from the response. You will use that value when you update or delete this user in Lab 1.

4. In Control Hub, open **Users** and confirm the new person is listed.

## Checkpoint

You are ready for Lab 1 when:

* [ ] **Lab** is the selected Bruno environment
* [ ] `access_token` is the personal access token, stored as a secret
* [ ] **Who am I** shows the lab administrator
* [ ] **Create user** succeeded and the person is visible in Control Hub

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 on Who am I | Copy the personal access token again and replace the `access_token` secret. Send the request again. |
| displayName is not the lab administrator | Sign out of developer.webex.com and sign in as <copy><w class="WbxUser">your lab admin</w></copy>. |
| Create user returns 409 | That email already exists. Change the address in the request body and send again. |

Continue to [Lab 1](lab1_users.md).
