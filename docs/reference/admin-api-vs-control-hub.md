# Admin API vs Control Hub

Control Hub is the interactive admin surface. The Webex Admin APIs are the same objects, callable from scripts and collections.

| Task | Control Hub | This lab |
|---|---|---|
| See who you are | Profile / org settings | `GET /people/me` |
| List the org | Organization details | `GET /organizations` |
| Create users | Users → Manage users | `POST /people` or SCIM Bulk |
| License consumption | Licensing | `GET /licenses` |
| Admin roles | Users → Roles | `GET /roles` + `PUT /people/{id}` |
| Hybrid Calendar license | Users → Licenses | `PATCH /licenses/users` |

!!! curious "When to use which"
    Use Control Hub to confirm what a human would see. Use the Admin APIs when the same action must be repeatable, bulk, or unattended (Service App).

The token in this lab is an **org admin** credential. Treat it like the Control Hub administrator password.
