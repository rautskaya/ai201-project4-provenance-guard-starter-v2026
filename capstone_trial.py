#!/usr/bin/env python3
"""
Capstone trials — runs the trial defined in criteria.md and scores C1–C5.

One trial = start the service fresh, send the fixed 23 requests, stop it.

    python capstone_trial.py --label before            # 3 trials
    python capstone_trial.py --label after --trials 3

Writes a markdown run log to results/capstone_<label>_<timestamp>.md.
Uses curl for every request, so C3 compares the log against curl's own clock.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import config

PORT = int(os.getenv("CAPSTONE_PORT", "5001"))  # 5000 is AirPlay on macOS
BASE = f"http://127.0.0.1:{PORT}"

NORMAL_TEXTS = [
    "I walked to the market this morning and bought apples, then sat by the river reading a book.",
    "Honestly the bus was late again so I missed the first ten minutes of class. Not great.",
    "In conclusion, artificial intelligence offers numerous benefits across various industries, including healthcare, finance, and education.",
    "My grandma makes the best dumplings. She never measures anything, she just knows.",
    "Climate change represents one of the most significant challenges facing humanity in the twenty-first century.",
    "lol my cat knocked my coffee onto my keyboard and now the e key sticks",
    "Effective time management is essential for achieving personal and professional goals in today's fast-paced world.",
    "We drove six hours to see the lake and it rained the entire weekend. Still worth it.",
    "The French Revolution was a period of radical political and societal change in France that began in 1789.",
    "I tried to fix the sink myself and now there is water in the hallway. Calling a plumber tomorrow.",
]

# (name, endpoint, body, expected status) — body None means "not JSON"
BAD_REQUESTS = [
    ("empty text", "submit", {"text": "", "creator_id": "bad-1"}, 400),
    ("only spaces", "submit", {"text": "     ", "creator_id": "bad-2"}, 400),
    ("over 10,000 chars", "submit", {"text": "a" * 10001, "creator_id": "bad-3"}, 400),
    ("no creator_id", "submit", {"text": "Some words here."}, 400),
    ("not JSON", "submit", None, 400),
    ("appeal unknown id", "appeal", {"content_id": "does-not-exist", "reasoning": "mine"}, 404),
    ("appeal no reasoning", "appeal", {"content_id": "does-not-exist"}, 400),
]

FLOOD_TEXT = "Testing the rate limit with the same short sentence again."
NINE_FIELDS = ["timestamp", "content_id", "creator_id", "guess", "model_score",
               "style_score", "combined_score", "label", "status"]


def curl(endpoint: str, body) -> tuple[int, dict, float]:
    """POST with curl. Returns status, parsed JSON body, curl's total time in ms."""
    data = "hello" if body is None else json.dumps(body)
    cmd = ["curl", "-s", "-X", "POST", f"{BASE}/{endpoint}", "--data-binary", "@-",
           "-w", "\n%{http_code} %{time_total}"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json"]
    out = subprocess.run(cmd, input=data, capture_output=True, text=True).stdout
    payload, _, tail = out.rpartition("\n")
    code, seconds = tail.split()
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        parsed = {}
    return int(code), parsed, float(seconds) * 1000


def start_service() -> subprocess.Popen:
    env = {**os.environ, "PORT": str(PORT)}
    proc = subprocess.Popen([sys.executable, "app.py"], env=env, start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{BASE}/health"],
                           capture_output=True, text=True)
        if r.stdout == "200":
            return proc
        time.sleep(0.5)
    stop_service(proc)
    raise RuntimeError(f"service did not start on port {PORT}")


def stop_service(proc: subprocess.Popen) -> None:
    os.killpg(proc.pid, signal.SIGTERM)  # debug mode runs a reloader child too
    proc.wait(timeout=10)


def log_lines() -> list[dict]:
    if not config.AUDIT_LOG.exists():
        return []
    return [json.loads(l) for l in config.AUDIT_LOG.read_text().splitlines() if l.strip()]


def run_trial() -> dict:
    before = len(log_lines())
    proc = start_service()
    sent = []  # (kind, name, status, body, client_ms, expected)
    try:
        for i, text in enumerate(NORMAL_TEXTS, 1):
            status, body, ms = curl("submit", {"text": text, "creator_id": f"writer-{i}"})
            sent.append(("normal", f"writer-{i}", status, body, ms, 200))
        for name, endpoint, req, expected in BAD_REQUESTS:
            status, body, ms = curl(endpoint, req)
            sent.append(("bad", name, status, body, ms, expected))
        for i in range(1, 7):
            status, body, ms = curl("submit", {"text": FLOOD_TEXT, "creator_id": "flooder"})
            kind = "bad" if i == 6 else "flood"
            sent.append((kind, f"flooder #{i}", status, body, ms, 429 if i == 6 else 200))
    finally:
        stop_service(proc)

    new = log_lines()[before:]
    requests = [e for e in new if e.get("event") == "request"]
    decisions = {e["content_id"]: e for e in new if e.get("status") == "decided"}

    # C1 — one request line per request, same status, same order
    c1 = sum(1 for s, e in zip(sent, requests) if e["http_status"] == s[2])
    if len(requests) != len(sent):
        c1 = min(c1, len(sent) - abs(len(requests) - len(sent)))

    # C2 — the 8 failures: expected 4xx, never 500, logged with an error
    c2 = 0
    for s, e in zip(sent, requests):
        if s[0] == "bad" and s[2] == s[5] and s[2] != 500 and e.get("error"):
            c2 += 1

    normals = [(s, e) for s, e in zip(sent, requests) if s[0] == "normal"]
    # C3 — logged duration within 20 ms of curl's time
    c3 = sum(1 for s, e in normals if abs(e["duration_ms"] - s[4]) <= 20)
    # C4 — every normal submission under 1,000 ms
    c4 = sum(1 for s, e in normals if e["duration_ms"] < 1000)
    # C5 — response matches decision line, which still has all nine fields
    c5 = 0
    for s, e in normals:
        body = s[3]
        d = decisions.get(body.get("content_id"))
        if (d and all(k in d for k in NINE_FIELDS)
                and all(d[k] is not None for k in ("model_score", "style_score", "combined_score"))
                and d["guess"] == body.get("guess") and d["label"] == body.get("label")
                and d["combined_score"] == body.get("combined_score")):
            c5 += 1

    return {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5,
            "sent": sent, "requests": requests, "decisions": decisions,
            "normals": normals}


TARGETS = [
    ("C1. Every request is logged", "c1", 23),
    ("C2. Bad requests get an error, not a crash", "c2", 8),
    ("C3. The logged time is correct (within 20 ms of curl)", "c3", 10),
    ("C4. Every submission under 1 s, even the first", "c4", 10),
    ("C5. The original results didn't change", "c5", 10),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="before")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    trials = []
    for t in range(1, args.trials + 1):
        print(f"Trial {t}…", flush=True)
        trials.append(run_trial())

    header = "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, len(trials) + 1)) + " | Verdict |"
    rows = [header, "|" + "---|" * (len(trials) + 3)]
    for name, key, target in TARGETS:
        scores = [t[key] for t in trials]
        verdict = "MET" if all(s >= target for s in scores) else "MISSED"
        rows.append(f"| {name} | {target} of {target} | "
                    + " | ".join(f"{s}/{target}" for s in scores) + f" | {verdict} |")
    table = "\n".join(rows)
    print("\n" + table)

    first = trials[0]
    out = [f"# Capstone run log — {args.label}", "",
           f"`python capstone_trial.py --label {args.label}`, {datetime.now():%Y-%m-%d %H:%M}, "
           f"{len(trials)} trials, each a fresh start of `app.py` on port {PORT}.", "", table, "",
           "## Trial 1 — the normal submissions", "",
           "| # | curl ms | logged ms | diff | result | response guess = decision guess |",
           "|---|---|---|---|---|---|"]
    for s, e in first["normals"]:
        d = first["decisions"].get(s[3].get("content_id"), {})
        out.append(f"| {s[1]} | {s[4]:.1f} | {e['duration_ms']} | {abs(e['duration_ms'] - s[4]):.1f} "
                   f"| {e.get('result')} | {d.get('guess') == s[3].get('guess')} |")
    out += ["", "## Trial 1 — the bad requests", "",
            "| request | expected | got | logged error |", "|---|---|---|---|"]
    for s, e in zip(first["sent"], first["requests"]):
        if s[0] == "bad":
            out.append(f"| {s[1]} | {s[5]} | {s[2]} | {e.get('error')} |")
    out += ["", "## Trial 1 — raw request log lines", "", "```"]
    out += [json.dumps(e) for e in first["requests"]]
    out += ["```", ""]

    path = Path("results") / f"capstone_{args.label}_{datetime.now():%Y-%m-%d_%H%M}.md"
    path.write_text("\n".join(out))
    print(f"\nWritten to {path}")


if __name__ == "__main__":
    main()
