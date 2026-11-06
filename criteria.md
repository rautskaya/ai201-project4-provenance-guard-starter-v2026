# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives
Out of 10 human-written texts, no more than 1 should be labeled as high-confidence AI. 

**Why this target:**
I want to avoid incorrectly accusing real writers of using AI. A false accusation can be more harmful than failing to detect AI-generated text.


---

## 2. Score spread

The average AI score for 10 AI-generated texts should be at least 0.20 higher than the average score for 10 human-written texts.


**Why this target:**
We need to show a clear difference between human and AI writing. If the scores are too similar, the system cannot distinguish them well.


---

## 3. Label coverage

The system should be able to return all three labels: high-confidence human, unsure, and high-confidence AI. 


**Why this target:**
The system should handle both clear and uncertain cases instead of forcing every submission to be labeled AI or human.


---

## 4. Appeal path

All 5 valid appeals should change the submission status to under_review and create a record in the audit log.

**Why this target:**
Writers should have a way to challenge incorrect results. Every appeal should be recorded so it can be reviewed later.

---

## 5. Bad input
The system should reject all 5 invalid submissions. Each should return a clear error without crashing the service.


**Why this target:**
The system should handle invalid requests safely and provide useful error messages instead of crashing.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria (unit 9)

Written before running any capstone tests.

**One trial** = start the service fresh with `python app.py`, then send the
same 23 requests:

- 10 normal submissions (10 different short texts, 10 different creators)
- 7 bad requests (empty text, only spaces, text over 10,000 characters,
  no creator_id, not JSON, appeal for an id that doesn't exist, appeal with
  no reasoning)
- 6 quick submissions from one creator (the limit is 5 a minute, so the 6th
  should be blocked)

I run 3 trials. A target has to hold in all 3.

---

## C1. Every request is logged

Each of the 23 requests writes one `"event": "request"` line to the log, with
the same status code the client got back.

**Target:** 23 of 23

**Why:** The extension's job is to record everything. If even one request is
missing, a failure could go unnoticed, and my cost number (taken from the log)
would be wrong.

---

## C2. Bad requests get an error, not a crash

All 8 bad requests (the 7 bad ones plus the 6th quick one) return 400, 404 or
429 (never 500), and their log line says what went wrong in `error`.

**Target:** 8 of 8

**Why:** Before this unit, a 400 left no trace in the log. Without the reason,
I can't tell what went wrong. These errors happen the same way every time, so
there's no excuse for missing one.

---

## C3. The logged time is correct

For the 10 normal submissions, `duration_ms` in the log is within 20 ms of the
time curl measured.

**Target:** 10 of 10

**Why:** My cost number comes from `duration_ms`, so it has to be right.
20 ms leaves room for curl's own overhead, but it's less than one normal
request (about 28 ms), so a broken timer would be caught.

---

## C4. Every submission takes under 1 second, even the first one

For the 10 normal submissions, `duration_ms` is under 1,000 ms. This includes
the first request after starting the service.

**Target:** 10 of 10

**Why:** Normal requests take about 30 ms, so 1 second is generous. The first
user after a restart shouldn't wait much longer than everyone else.

---

## C5. The original results didn't change

For the 10 normal submissions, the response and the decision line in the log
show the same `guess`, `label` and `combined_score`, and the decision line
still has all nine fields from unit 8.

**Target:** 10 of 10

**Why:** My change added new log lines. It must not break the old decision
lines, because appeals rely on them.
