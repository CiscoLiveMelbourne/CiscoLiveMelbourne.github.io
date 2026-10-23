#!/usr/bin/env bash
# Convenience runner for the Webex Admin API lab.
# Runs each exercise in order with a pause so you can narrate the output.
#
# Usage: ./run_lab.sh
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "No .env found. Copy .env.example to .env and add your token first."
  exit 1
fi

pause() { read -r -p ">> Press Enter for the next exercise..."; }

echo "### Exercise 0: token + org discovery"
python scripts/00_check_token.py
pause

echo "### Exercise 2: org-wide license usage"
python scripts/02_license_usage.py
pause

echo "### Exercise 3: available roles"
python scripts/03_roles.py list
pause

echo "### Exercise 4: hybrid services licenses"
python scripts/04_hybrid_licenses.py --show-users
pause

echo "### Exercise 5: hybrid clusters + connectors health"
python scripts/05_hybrid_health.py
pause

echo "### Exercise 1: bulk create users (People API)"
python scripts/01_bulk_users.py create --csv data/users.csv
echo "Run 'python scripts/01_bulk_users.py cleanup' when you are done."
