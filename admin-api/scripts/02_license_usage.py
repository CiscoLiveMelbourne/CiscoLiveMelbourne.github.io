"""Exercise 2 - view and validate organization-wide license usage.

Lists every license in the org with total vs. consumed units, flags licenses
that are over-allocated or nearly exhausted, and prints a compact summary you
can read out during the demo.

    python scripts/02_license_usage.py
    python scripts/02_license_usage.py --threshold 0.8   # warn at 80% used
"""

import argparse

import webex_client as wx


def main() -> None:
    parser = argparse.ArgumentParser(description="Webex org license usage report")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.9,
        help="fraction of consumed units at which to warn (default 0.9)",
    )
    args = parser.parse_args()

    licenses = wx.get_all("/licenses")
    if not licenses:
        print("No licenses returned. Check the token's admin scope.")
        return

    print(f"{'License':45} {'Used':>8} {'Total':>8} {'Free':>8}  Status")
    print("-" * 84)

    warnings = []
    for lic in sorted(licenses, key=lambda x: x.get("name", "")):
        name = (lic.get("name") or "")[:44]
        total = lic.get("totalUnits")
        consumed = lic.get("consumedUnits")

        if total is None or consumed is None:
            print(f"{name:45} {'-':>8} {'-':>8} {'-':>8}  (no unit data)")
            continue

        free = total - consumed
        ratio = consumed / total if total else 0
        if consumed > total:
            status = "OVER-ALLOCATED"
            warnings.append(f"{name}: {consumed}/{total} (over-allocated)")
        elif ratio >= args.threshold:
            status = f"NEAR LIMIT ({ratio:.0%})"
            warnings.append(f"{name}: {consumed}/{total} ({ratio:.0%} used)")
        else:
            status = "ok"
        print(f"{name:45} {consumed:>8} {total:>8} {free:>8}  {status}")

    print("\n== Validation summary ==")
    if warnings:
        print(f"  {len(warnings)} license(s) need attention:")
        for warning in warnings:
            print(f"    - {warning}")
    else:
        print("  All licenses within healthy limits.")


if __name__ == "__main__":
    main()
