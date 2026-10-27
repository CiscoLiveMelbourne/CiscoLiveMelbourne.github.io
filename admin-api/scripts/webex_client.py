"""Shared Webex Admin API client used by all lab exercises.

Centralizes authentication, base URLs, pagination, and rate-limit handling so
each exercise script stays focused on the API being demonstrated.

The admin token is read from the WEBEX_ACCESS_TOKEN environment variable and is
never written to disk or logged. Treat it like a password.
"""

import base64
import csv
import os
import sys
import time
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("WEBEX_API_BASE", "https://webexapis.com/v1").rstrip("/")
SCIM_BASE = os.getenv("WEBEX_SCIM_BASE", "https://webexapis.com/identity/scim").rstrip("/")

# Requests to Webex are rate limited; on HTTP 429 we honor Retry-After.
_MAX_RETRIES = 5


def _token() -> str:
    token = os.getenv("WEBEX_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit(
            "ERROR: WEBEX_ACCESS_TOKEN is not set. Copy .env.example to .env "
            "and paste your dCloud organization admin/service-app token."
        )
    return token


def _headers(extra: dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {_token()}",
        "Content-Type": "application/json",
    }
    if extra:
        headers.update(extra)
    return headers


def _request(method: str, url: str, **kwargs) -> requests.Response:
    """Perform a request with basic 429/backoff handling."""
    for attempt in range(_MAX_RETRIES):
        response = requests.request(method, url, timeout=30, **kwargs)
        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 2 ** attempt))
            print(f"  rate limited, retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)
            continue
        return response
    return response


def get(path: str, params: dict | None = None) -> dict:
    """GET a Webex v1 resource. `path` is relative, e.g. '/licenses'."""
    url = f"{API_BASE}{path}"
    response = _request("GET", url, headers=_headers(), params=params)
    response.raise_for_status()
    return response.json()


def get_all(path: str, params: dict | None = None) -> list:
    """GET every page of a collection endpoint, following RFC-5988 Link headers.

    Returns the concatenated `items` arrays. Webex signals the next page via a
    Link header with rel="next". Some endpoints (e.g. /hybrid/clusters) return
    a bare JSON array instead of {"items": [...]}; both shapes are accepted.
    """
    url = f"{API_BASE}{path}"
    items: list = []
    while url:
        response = _request("GET", url, headers=_headers(), params=params)
        response.raise_for_status()
        body = response.json()
        items.extend(body if isinstance(body, list) else body.get("items", []))
        # After the first call, params are already baked into the "next" URL.
        params = None
        url = response.links.get("next", {}).get("url")
    return items


def post(path: str, payload: dict) -> dict:
    url = f"{API_BASE}{path}"
    response = _request("POST", url, headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json() if response.text else {}


def put(path: str, payload: dict) -> dict:
    url = f"{API_BASE}{path}"
    response = _request("PUT", url, headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json() if response.text else {}


def patch(path: str, payload: dict) -> dict:
    url = f"{API_BASE}{path}"
    response = _request("PATCH", url, headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json() if response.text else {}


def delete(path: str) -> None:
    url = f"{API_BASE}{path}"
    response = _request("DELETE", url, headers=_headers())
    response.raise_for_status()


def scim_org_id(org_id: str) -> str:
    """Return the UUID the SCIM path requires.

    Who am I and List Organizations return a base64 organization id. Decoded,
    that value is ``ciscospark://us/ORGANIZATION/<uuid>``. SCIM bulk uses the
    UUID. A value that is already a UUID is returned unchanged.
    """
    org_id = (org_id or "").strip()
    if not org_id.startswith("Y2"):
        return org_id
    padding = "=" * ((4 - len(org_id) % 4) % 4)
    try:
        text = base64.b64decode(org_id + padding).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return org_id
    marker = "ORGANIZATION/"
    if marker not in text:
        return org_id
    return text.split(marker, 1)[1]


def scim_post(org_id: str, resource: str, payload: dict) -> dict:
    """POST to the SCIM 2.0 base, e.g. resource='/v2/Bulk' or '/v2/Users'."""
    url = f"{SCIM_BASE}/{scim_org_id(org_id)}{resource}"
    response = _request("POST", url, headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json() if response.text else {}


def me() -> dict:
    """Return the identity behind the current token (sanity check)."""
    return get("/people/me")


def org_id() -> str:
    """Return the base64 organization id of the token's own organization."""
    return me().get("orgId") or ""


_lab_domain: str | None = None


def lab_domain() -> str:
    """Return the most common email domain among the organization's users.

    Every dCloud pod has its own verified domain, and the users that come with
    the session are on it, so the lab never has to hardcode a domain.
    """
    global _lab_domain
    if _lab_domain is None:
        counts = Counter()
        for person in get("/people", params={"max": 100}).get("items", []):
            for email in person.get("emails") or []:
                if "@" in email:
                    counts[email.rsplit("@", 1)[1].lower()] += 1
        if not counts:
            sys.exit("ERROR: could not detect the lab domain; the organization has no users")
        _lab_domain = counts.most_common(1)[0][0]
        print(f"Lab domain: {_lab_domain}")
    return _lab_domain


def full_email(value: str) -> str:
    """Add the lab domain to a bare name such as 'barbara.liskov'."""
    value = (value or "").strip()
    if not value or "@" in value:
        return value
    return f"{value}@{lab_domain()}"


def read_users_csv(csv_path) -> list:
    """Read a users CSV and complete every 'email' value with the lab domain."""
    with open(csv_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["email"] = full_email(row.get("email") or "")
    return [row for row in rows if row["email"]]
