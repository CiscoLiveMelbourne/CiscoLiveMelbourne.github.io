# Lab 3 - List roles in both tools, then assign one

**Time: 32-40 min**

List the administrator roles in Bruno and in the script. Assigning a role is the script only. Bruno has no assign request.

## Section 1 - List roles in Bruno

1. Open **3. Roles → List roles**.
2. Select **Send**.

The call is `GET /v1/roles`. Note the name you will assign. This lab uses **Read-only Administrator**.

## Section 2 - List roles in the script

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py list
```

The printed names match the Bruno response.

## Section 3 - Assign a role

Use a person you created in this lab. Replace the domain with <copy><w class="TestDomain">your verified domain</w></copy>.

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py assign --email labuser01@YOUR-DOMAIN --role "Read-only Administrator"
```

The script reads the person's current roles, adds this role, and sends `PUT /v1/people/{id}`.

In Control Hub, open that user and confirm the role is listed.

## Checkpoint

You are ready for Lab 4 when:

* [ ] Bruno and the script both listed roles
* [ ] The script assigned **Read-only Administrator** to one lab user, or you can explain the `PUT` it sends
* [ ] You did not assign the role from Bruno, because that request is not in the collection

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Assign says the user was not found | The email domain must be <copy><w class="TestDomain">your verified domain</w></copy>, and that user must already exist. |
| 403 on assign | The Service App needs `spark-admin:people_write` and `spark-admin:roles_read`. Add the scope, authorize the app again, and generate a new access token. |

Continue to [Lab 4](lab4_hybrid_licenses.md).
