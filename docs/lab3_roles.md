# Lab 3 - Roles

**Time: 32-40 min**

List the administrator roles in Bruno first, then in VS Code. Assigning a role runs in VS Code only, because the Bruno collection has no assign request.

## Section 1 - List roles

**Bruno**

1. Open **3. Roles → List roles**.
2. Select **Send**.

The call is `GET /v1/roles`. Find **Read-only Administrator**. You assign it in Section 2.

**VS Code**

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py list
```

The printed names and ids match the Bruno response.

## Section 2 - Assign a role

**VS Code**

Use a person you created in Lab 1. Give just the name; the script adds your lab domain.

```bat
scripts\.venv\Scripts\python.exe scripts\03_roles.py assign --email labuser01 --role "Read-only Administrator"
```

The script reads the person's current roles, adds this role, and sends `PUT /v1/people/{id}`.

In Control Hub, open that user and confirm the role is listed.

## Checkpoint

You are ready for Lab 4 when:

* [ ] Bruno and VS Code both listed the roles
* [ ] VS Code assigned **Read-only Administrator** to one lab user, and Control Hub shows it

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Assign says the user was not found | That user must already exist. If you typed a full email, its domain must be <copy><w class="TestDomain">your verified domain</w></copy>. |
| 403 on assign | The Service App needs `spark-admin:people_write` and `spark-admin:roles_read`. Add the scope, authorize the app again, and generate a new access token. |

Continue to [Lab 4](lab4_hybrid_licenses.md).
