# Take-Home Bundle

Clone the lab repository. Everything you used on the lab desktop is in its `admin-api/` folder. Do not take a dCloud organization or a live token with you.

<copy>git clone https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io.git</copy>

## What to keep

- `scripts/` — one exercise per file plus `webex_client.py`
- `bruno/Webex Admin API Lab/` — REST collection
- `postman/Webex_Admin_API_Lab.postman_collection.json`
- `data/users.csv` — names only; the scripts add your org's domain
- `.env.example` — template only

## What not to keep

- `.env` or any file that contains a token
- `data/created_users.json` from a live run
- dCloud administrator passwords
- Production org IDs

## After the event

1. Point the scripts at a **non-production** organization you own.
2. Create a new Service App and authorize it on that org.
3. Revalidate scopes and endpoints against current [developer.webex.com](https://developer.webex.com){:target="_blank"} docs.
4. Run `01_bulk_users.py cleanup` after experiments.

Repository: [https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io](https://github.com/CiscoLiveMelbourne/CiscoLiveMelbourne.github.io){:target="_blank"}
