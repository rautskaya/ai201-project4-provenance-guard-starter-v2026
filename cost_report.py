#!/usr/bin/env python3
"""
Cost report — capstone.

Reads the "request" entries from the audit log and summarizes how long
requests took. There's no API bill for this service (the model runs locally),
so the cost of one run is seconds of compute.

    python cost_report.py                       # every request ever logged
    python cost_report.py --since 2026-11-06T19:00:00
"""

import argparse
import statistics

import audit


def percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    index = round(pct / 100 * (len(ordered) - 1))
    return ordered[index]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="only entries at or after this ISO timestamp (UTC)")
    args = parser.parse_args()

    requests = [e for e in audit.read_entries() if e.get("event") == "request"]
    if args.since:
        requests = [e for e in requests if e["timestamp"] >= args.since]
    if not requests:
        print("No request entries in the log yet.")
        return

    print(f"{len(requests)} requests\n")
    print(f"{'endpoint':<9} {'status':>6} {'count':>5} {'avg ms':>9} {'p50 ms':>9} {'p95 ms':>9} {'max ms':>9}")

    groups: dict[tuple[str, int], list[float]] = {}
    for e in requests:
        groups.setdefault((e["endpoint"], e["http_status"]), []).append(e["duration_ms"])

    for (endpoint, status), times in sorted(groups.items()):
        print(
            f"{endpoint:<9} {status:>6} {len(times):>5} {statistics.mean(times):>9.1f} "
            f"{percentile(times, 50):>9.1f} {percentile(times, 95):>9.1f} {max(times):>9.1f}"
        )

    scored = groups.get(("/submit", 200), [])
    if scored:
        avg_s = statistics.mean(scored) / 1000
        print(f"\nCost of one scored /submit: {avg_s:.3f} s of compute (average of {len(scored)})")
        print(f"100 submissions a day: 100 x {avg_s:.3f} s = {100 * avg_s:.1f} s of compute")


if __name__ == "__main__":
    main()
