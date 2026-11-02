# Lab 0 - Who am I and create one user

**Time: 8-12 min**

This lab is Bruno only. Use your personal access token to see who you are, then create one user. VS Code starts in Lab 1, after you create the Service App.

## Section 1 - Open Bruno

The collection is already on the lab desktop.

1. On the lab desktop, open **Bruno**.
2. Look at the left sidebar of Bruno. If **Webex Admin API Lab** is already listed, the collection is already open. Select it and go to step 3. If it is not listed, select **Open Collection** and choose the folder `Desktop\admin-api\bruno\Webex Admin API Lab`.
3. In Bruno, open the environment list at the top right of the window. On the **Collection** tab, select **Lab**.
4. Open the same environment list again and select **Configure**. The **Environments** tab opens, with **Lab** selected in the left list. You set every lab variable here, on the **Variables** tab.
5. In the `test_domain` row, set **Value** to <copy><w class="TestDomain">your verified domain</w></copy>. Do not type `@`.
6. In the `org_id` row, set **Value** to <copy><w class="OrgId">your organization ID</w></copy>. Select the copy icon to copy the value you entered on the [Overview](overview.md) page. Every request that needs the organization uses this one variable.
7. Select **Save**.

## Section 2 - Add your personal access token

1. On the lab desktop, open a browser and go to [developer.webex.com](https://developer.webex.com){:target="_blank"}. Sign in as <copy><w class="WbxUser">your lab admin</w></copy>.
2. Select your avatar at the top right of the page. The menu shows your **Bearer** token, which is your personal access token. Select the copy icon next to it. The token lasts about 12 hours.
3. Go back to Bruno. In the **Environments** tab, with **Lab** selected, select the **Secrets** tab.
4. In the `access_token` row, paste the token into **Value**, then select **Save**.

## Section 3 - Who am I

1. In the Bruno left sidebar, expand **Webex Admin API Lab**, then expand the **0. Setup** folder.
2. Select the request **Who am I (/people/me)**. It opens in a new tab.
3. Select the arrow (**Send**) at the right end of the URL bar, or press `Ctrl+Enter`.

The call is `GET /v1/people/me`. It returns the person who owns the access token, so it is the quickest way to check which identity a token acts as.

In the response pane on the right, the status is **200** and the body describes you:

| Field | What it tells you |
| --- | --- |
| `displayName` | Your name. It is the lab administrator, because you used your personal access token. |
| `emails` | Your sign-in address, <copy><w class="WbxUser">your lab admin</w></copy> |
| `id` | Your person id in Webex |
| `orgId` | The organization you belong to. It is in a different format from the Organization ID in Control Hub, which is expected. |
| `roles` | The administrator roles you hold, as role ids |
| `licenses` | The licenses assigned to you, as license ids |

If you see **401** instead, the token is missing or expired. See the troubleshooting table at the end of this lab.

## Section 4 - Create one user

1. In the Bruno left sidebar, under **Webex Admin API Lab**, expand the **1. Users** folder.
2. Select the request **Create user (People API)**.
3. Select the **Body** tab and confirm the email address ends with `@{{test_domain}}`.
4. Select the arrow (**Send**) at the right end of the URL bar, or press `Ctrl+Enter`.

The call is `POST /v1/people`. It creates one user, `labuser01`, with the name **Ada Lovelace**.

In the response pane, the status is **200** and the body is the new user record:

* `id` is the new user's person id. Bruno saves it in the Lab environment as `person_id`, so you do not have to copy it. You use it again when you update this user in Lab 1 and delete it in the Conclusion.
* `emails`, `displayName`, `firstName`, and `lastName` are the values from the request body.
* `orgId` shows the user was created in your lab organization.
* `created` is the date and time the user was created.

To check the result, open Control Hub at [admin.webex.com](https://admin.webex.com){:target="_blank"} in the browser. In the left menu, under **Management**, select **Users**, and confirm the new person is listed.

## Checkpoint

You are ready for Lab 1 when:

* [ ] **Lab** is the selected Bruno environment
* [ ] `test_domain` and `org_id` are set in the Lab environment
* [ ] `access_token` is the personal access token, stored as a secret
* [ ] **Who am I** shows the lab administrator
* [ ] **Create user** succeeded and the person is visible in Control Hub

## Troubleshooting

| Problem | Solution |
| --- | --- |
| 401 on Who am I | Copy the personal access token again and replace the `access_token` secret. Send the request again. |
| 401 right after you pasted a fresh token | The environment was not saved. Paste the token into `access_token` again, save the environment, and send again. |
| displayName is not the lab administrator | Sign out of developer.webex.com and sign in as <copy><w class="WbxUser">your lab admin</w></copy>. |
| Create user returns 409 | That email already exists. Change the address in the request body and send again. |

Continue to [Lab 1](lab1_users.md).
