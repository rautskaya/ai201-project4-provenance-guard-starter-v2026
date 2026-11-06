# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

The user submits text and their creator ID through the POST /submit endpoint.

The system checks that the input is valid.

detector.py analyzes how predictable the text is and returns an AI score between 0 and 1.

stylometry.py analyzes sentence lengths, vocabulary, and punctuation and returns another AI score between 0 and 1.

scoring.py combines both scores into one final AI score.

The system uses thresholds to decide whether the text is likely AI-written, likely human-written, or uncertain.

The system saves the result in the audit log and returns a content ID, guess, confidence score, and label to the user. If the user disagrees, they can submit an appeal through POST /appeal.

API Endpoints

1. POST /submit

Accepts text from a user and analyzes whether it might be AI-generated.

Input:

text (string): The text submitted by the user.

creator_id (string): Identifies the writer.

Output:

content_id (string): Unique ID for the submission.

guess (string): AI or human.

confidence (float): Confidence score between 0 and 1.

label (string): Message shown to the reader.

2. POST /appeal

Allows a writer to challenge the AI detection result.

Input:

content_id (string): ID of the original submission.

reasoning (string): Why the writer disagrees with the result.

Output:

content_id (string): ID of the original submission.

status (string): Changes to under_review.

message (string): Confirms the appeal was recorded.

The appeal is also saved in the audit log.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**
It measures how predictable the text is using a language model. More predictable text gets a higher AI score.

**Why that might differ between human and AI writing:**
AI often uses common words and predictable sentences. Human writing may have more unusual word choices.

**What it can't see:**
It cannot tell who actually wrote the text. A human using simple English may get a high AI score. AI text with unusual words may get a low AI score.

### Signal two — the style signal

**What it measures:**
It measures sentence length variation, vocabulary variety, and punctuation. It looks at how the text is written, not what it means.

**Why that might differ between human and AI writing:**
AI writing may have more similar sentence lengths and repeated words. Human writing may have more variation.

**What it can't see:**
It cannot understand the meaning or identify the real author. Someone can change punctuation, sentence lengths, or words in AI-generated text to make it look more human.

### The combining rule

**The rule:**
A weighted average of both signals. Give them equal weight. If the signals disagree, the final score will fall between them. If the result is not clear, the system will return an uncertain label.

**The numbers:**
Model signal: 50%

Style signal: 50%

Combined score = (model score × 0.5) + (style score × 0.5)

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

I tested both signals on the same three texts: AI-generated, human-like, and borderline writing.

In one test, the model signal gave a score of 0.80, while the style signal gave 0.30. The model considered the text AI-like, but the style signal considered it more human-like.

My combining rule gives both signals equal weight:

Combined score = (0.80 × 0.5) + (0.30 × 0.5) = 0.55.

Since the combined score is in my uncertain range, the system would return an "unsure" label.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.45 | This text is likely written by a human. |
| unsure | Above 0.45 and below 0.65 | We cannot confidently determine whether this text was written by a human or AI. |
| high-confidence AI | 0.65–1.00 | This text shows strong signs of AI-generated writing, but the result is not certain. |

**Why I worded the "unsure" one this way:**
I want to make it clear that the system cannot always tell whether text was written by AI or a human. I don't want to wrongly accuse someone of using AI when they wrote the text themselves.

---

## Sample Run

**A submission**
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"The bus was late again. Seven minutes, maybe eight. I stood beside a yellow newspaper box watching a pigeon attack someone'\''s abandoned sandwich. Strange little creature. Across the street, a man in a purple coat was arguing with a parking meter. I couldn'\''t hear what he was saying, but he looked genuinely offended. Then the bus appeared, completely empty except for a woman carrying an enormous plastic cactus. Why a cactus? No idea. I got on, tapped my card, and sat near the back. The driver had a tiny rubber duck attached to the dashboard. It squeaked every time we hit a bump.","creator_id":"user789"}'
{
  "combined_score": 0.51345,
  "confidence": 0.51345,
  "content_id": "e0619d2d-c26e-4d05-bc50-7ea55bb3a486",
  "guess": "unsure",
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "model_score": 0.573,
  "style_score": 0.4539
}

**An appeal**

curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"e9572934-b755-4045-956e-87c476797f93","reasoning":"I wrote this text myself and disagree with the AI detection result."}'
{
  "content_id": "e9572934-b755-4045-956e-87c476797f93",
  "message": "Your appeal has been recorded.",
  "status": "under_review"
}

**What the log shows afterwards**

curl "http://127.0.0.1:5000/log?limit=2"
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.51345,
      "content_id": "e0619d2d-c26e-4d05-bc50-7ea55bb3a486",
      "creator_id": "user789",
      "guess": "unsure",
      "label": "We cannot confidently determine whether this text was written by a human or AI.",
      "model_score": 0.573,
      "status": "decided",
      "style_score": 0.4539,
      "timestamp": "2026-10-25T18:12:09+00:00"
    },
    {
      "content_id": "e9572934-b755-4045-956e-87c476797f93",
      "creator_id": "user123",
      "event": "appeal",
      "reasoning": "I wrote this text myself and disagree with the AI detection result.",
      "status": "under_review",
      "timestamp": "2026-10-25T18:12:41+00:00"
    }
  ]
}

## How I Used AI

Moment 1 — Understanding the scoring system

What I asked for: Explain how the two signals work, why they might disagree, and how to combine their scores.

What came back: The differences between the signals and how weighted averages and thresholds work.

What I changed: I decided to give both signals equal weight (50/50) and chose my own thresholds for human (0.45) and AI (0.65).

Moment 2 — Implementing the API endpoints

What I asked for: Help me implement the /submit and /appeal endpoints.

What came back: Processing submissions, saving results, and recording appeals.

What I changed: Tested the endpoints using curl, and adjusted the scoring thresholds based on my test results.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**

- **A real writer** might paste a draft, fix a paragraph, and check again. That is maybe 3 or 4 checks in a few minutes, and a few dozen on a busy day. 5 per minute and 50 per day never get in their way.
- **A script** trying to find my thresholds needs about 1,000 test submissions. At 5 per minute that takes over 3 hours. At 50 per day it takes about 20 days. That makes the attack slow and easy to spot in the log.
- I did not go lower (like 2 per minute), because a real writer fixing small mistakes could hit the limit. I did not go higher (like the starter's 10 per minute and 200 per day), because a script could finish in about 5 days instead of 20.

**What a caller counts as:** per `creator_id`. If a request has no `creator_id`, the limit uses the caller's IP address instead.

- **Weakness:** a script can make up a new `creator_id` for every request, and each new ID gets a fresh limit. So my limit only stops a script that keeps using the same ID.
- Limiting by IP address only would have the opposite problem: people who share one network, like a family or a school, would share one limit.
- Every blocked request is still saved in the audit log with `"reason": "rate_limited"`, so a flood of blocked requests is easy to find later.

**The run of status codes when I pushed past it:**

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited.
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "62097c21-9ac3-481a-aafc-85915c19a3ea", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6388, "combined_score": 0.68875, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "1861bc1f-85c4-4b82-81f8-c59dc30d753c", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6033, "combined_score": 0.7041999999999999, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "14c15a58-c9f1-4222-b754-b9c5b71438b4", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.555, "combined_score": 0.6939500000000001, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "e04e18bc-48c3-4981-91be-46a21ae4f48b", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6507, "combined_score": 0.7256, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:52+00:00", "content_id": "94a27ad2-81f2-4494-afcf-5d861ad11828", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.6136, "combined_score": 0.38855, "label": "This text is likely written by a human.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:52+00:00", "content_id": "98409580-e2e1-4c29-a58a-267405e95293", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.4369, "combined_score": 0.37905, "label": "This text is likely written by a human.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "2d681001-523d-438f-b28c-e44fd0ba1442", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.514, "combined_score": 0.6091, "label": "We cannot confidently determine whether this text was written by a human or AI.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "1c43ebcc-3ce0-4887-9e44-c335489d5b38", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.6667, "combined_score": 0.33335, "label": "This text is likely written by a human.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:54+00:00", "content_id": "4c16b865-1c9e-4707-9c40-4e4edd8e41cb", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.5, "combined_score": 0.7484500000000001, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
{"timestamp": "2026-11-04T23:22:54+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}


```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:
{"timestamp": "2026-11-04T23:22:53+00:00", "content_id": "1861bc1f-85c4-4b82-81f8-c59dc30d753c", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6033, "combined_score": 0.7041999999999999, "label": "This text shows signs of AI-generated writing, but this result is not proof.", "status": "decided"}
The worst outcome was FP03: genuine human writing by a non-native English speaker was labeled AI with a combined score of 0.7042. This could unfairly damage the writer’s credibility because of how they write. The warning that the result is not proof does not undo the false accusation.

---

## Run Log and Verdicts

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | 	≤1 of 10 labeled AI | 0/10 | 0/10 | 0/10 | MET |
| 2. Score spread | 	Difference ≥0.20 | 0.2291 | 0.2291 | 0.2291 | MET |
| 3. Label coverage | All 3 labels reachable | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal path | 5/5 under_review and logged | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | All 5 rejected with clear errors | 4/5 rejected | 4/5 rejected | 4/5 rejected | MISSED |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Source report: `results/run_2026-11-04_1621_before.md`
Produced by: `run_eval.py::main`
Requests handled by: `app.py::submit`
Scores combined by: `scoring.py::combine_signals`

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.36465000000000003,
    "model_score": 0.2986,
    "style_score": 0.4307,
    "label": "This text is likely written by a human.",
    "sent": "Saturday I finally cleaned the garage, it took like 4 hours because I "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4535,
    "model_score": 0.5336,
    "style_score": 0.3734,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "My job is mostly emails and meetings honestly. The meetings could be e"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3881,
    "model_score": 0.3482,
    "style_score": 0.428,
    "label": "This text is likely written by a human.",
    "sent": "My mom makes this potato pancake thing, we call them draniki. You grat"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.46575,
    "model_score": 0.3533,
    "style_score": 0.5782,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "The parking at my building is a mess this week. They're repainting the"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6335500000000001,
    "model_score": 0.7599,
    "style_score": 0.5072,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Hi Sarah, sorry I didn't finish the report yet. I had a problem with t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.46365,
    "model_score": 0.5271,
    "style_score": 0.4002,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "We went to Chicago in March which was a mistake, so cold and windy I c"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5688500000000001,
    "model_score": 0.527,
    "style_score": 0.6107,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "I signed up because at work everyone talks about AI now and I felt lik"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.49745,
    "model_score": 0.5001,
    "style_score": 0.4948,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "If you didn't watch The Bear yet you should. First episode is very str"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.47805000000000003,
    "model_score": 0.5148,
    "style_score": 0.4413,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Alarm at 6:30, I snooze it at least two times, every day. Coffee first"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.50395,
    "model_score": 0.5816,
    "style_score": 0.4263,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Don't buy that white couch. Also stop worrying so much what other peop"
  }
]
```

### Appeal output — Trial 1

Appeals handled by: `app.py::appeal`
Audit-log output returned by: `app.py::get_log`
{
  "count": 5,
  "entries": [
    {
      "content_id": "1861bc1f-85c4-4b82-81f8-c59dc30d753c",
      "creator_id": "attacker_FP03",
      "event": "appeal",
      "reasoning": "I wrote this text myself and disagree with the AI label.",
      "status": "under_review",
      "timestamp": "2026-11-05T00:25:44+00:00"
    },
    {
      "content_id": "62097c21-9ac3-481a-aafc-85915c19a3ea",
      "creator_id": "attacker_FP02",
      "event": "appeal",
      "reasoning": "I wrote this formal text myself and disagree with the AI label.",
      "status": "under_review",
      "timestamp": "2026-11-05T00:27:10+00:00"
    },
    {
      "content_id": "14c15a58-c9f1-4222-b754-b9c5b71438b4",
      "creator_id": "attacker_FP04",
      "event": "appeal",
      "reasoning": "I wrote this essay myself and disagree with the AI label.",
      "status": "under_review",
      "timestamp": "2026-11-05T00:27:15+00:00"
    },
    {
      "content_id": "e04e18bc-48c3-4981-91be-46a21ae4f48b",
      "creator_id": "attacker_FP05",
      "event": "appeal",
      "reasoning": "I wrote this documentation myself and disagree with the AI label.",
      "status": "under_review",
      "timestamp": "2026-11-05T00:27:20+00:00"
    },
    {
      "content_id": "e5499a68-395f-4dff-8915-69e6c9b51866",
      "creator_id": "attacker_FP06",
      "event": "appeal",
      "reasoning": "I wrote this text using a template and disagree with the AI label.",
      "status": "under_review",
      "timestamp": "2026-11-05T00:27:25+00:00"
    }
  ]
}

**Diagnoses**

Missed criterion 5 — Bad input

Stage: route (app.py::submit). The route checks that text is a nonempty string, but does not check its maximum length. The oversized input therefore reached the detector and returned 200 with an AI label, instead of being rejected. This happened in all three trials: only 4 of 5 invalid requests were rejected.

Broken attacks
Attacks	Stage	What went wrong
EV01, EV05, EV08	Signal one and combining rule	The model gave these AI samples low scores. Averaging with the style scores still produced human labels. For example, EV01’s text with typos received a model score of 0.164 and a final score of 0.389, labeled human.
EV02, EV06	Signal two and combining rule	Lower style scores pulled the final scores into the unsure range. For example, EV02 received 0.594 from the model and 0.381 from style, producing 0.488 overall.
EV03, EV09	Combining rule	Lower style scores reduced higher model scores, resulting in unsure. For example, EV09’s model score was 0.704, but combining it with style produced 0.609.
MF03–MF06	Route validation	Nonempty strings were accepted without checking whether they contained enough meaningful writing to classify. Control characters, punctuation, a long single word, and emoji all received authorship labels. For example, emoji-only MF06 was labeled AI with a score of 0.748.
---

## The Improvement

**What I changed:**
Added a 10,000-character limit in app.py::submit. Longer text now returns a clear 400 error before scoring. This prevents oversized submissions from being processed, but also rejects legitimate writing above the limit.

**Which diagnosis pointed at it:**
Criterion 5 showed missing length validation: oversized text was accepted and labeled AI instead of rejected. Attack MF08 showed the same issue with 60,000 characters. After the change, both oversized tests returned 400; the evaluation test did so in all three trials.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | 	≤1 of 10 labeled AI | 0/10 | 0/10 | 0/10 | MET |
| 2. Score spread | 	Difference ≥0.20 | 0.2291 | 0.2291 | 0.2291 | MET |
| 3. Label coverage | All 3 labels reachable | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal path | 5/5 under_review and logged | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | All 5 rejected with clear errors | All five blocked: four 400s and one 429 per trial. Missing-creator validation confirmed separately after reset. | All five blocked | All five blocked | MET |

Source report: `results/run_2026-11-05_0758_after.md`
Produced by: `run_eval.py::main`
Requests handled by: `app.py::submit`
Scores combined by: `scoring.py::combine_signals`
**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.36465000000000003,
    "model_score": 0.2986,
    "style_score": 0.4307,
    "label": "This text is likely written by a human.",
    "sent": "Saturday I finally cleaned the garage, it took like 4 hours because I "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4535,
    "model_score": 0.5336,
    "style_score": 0.3734,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "My job is mostly emails and meetings honestly. The meetings could be e"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3881,
    "model_score": 0.3482,
    "style_score": 0.428,
    "label": "This text is likely written by a human.",
    "sent": "My mom makes this potato pancake thing, we call them draniki. You grat"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.46575,
    "model_score": 0.3533,
    "style_score": 0.5782,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "The parking at my building is a mess this week. They're repainting the"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6335500000000001,
    "model_score": 0.7599,
    "style_score": 0.5072,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Hi Sarah, sorry I didn't finish the report yet. I had a problem with t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.46365,
    "model_score": 0.5271,
    "style_score": 0.4002,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "We went to Chicago in March which was a mistake, so cold and windy I c"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5688500000000001,
    "model_score": 0.527,
    "style_score": 0.6107,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "I signed up because at work everyone talks about AI now and I felt lik"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.49745,
    "model_score": 0.5001,
    "style_score": 0.4948,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "If you didn't watch The Bear yet you should. First episode is very str"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.47805000000000003,
    "model_score": 0.5148,
    "style_score": 0.4413,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Alarm at 6:30, I snooze it at least two times, every day. Coffee first"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.50395,
    "model_score": 0.5816,
    "style_score": 0.4263,
    "label": "We cannot confidently determine whether this text was written by a human or AI.",
    "sent": "Don't buy that white couch. Also stop worrying so much what other peop"
  }
]
```
Appeal path: Not retested after the change because only text-length validation in /submit was modified. The appeal code was unchanged. Earlier appeal results are reported as before evidence, not as new after results.

**Did it help, and how do I know:**

Yes. Before the change, oversized text was accepted and labeled AI. After adding the 10,000-character limit, the oversized evaluation input returned 400 in all three trials. The 60,000-character attack, MF08, also returned 400.

---

## What's Still Broken

AI text still escapes detection, some human writing is labeled AI, and meaningless input still receives labels. Next steps would be improving scoring, adjusting thresholds, and checking for meaningful text.

These were left unchanged to measure the length-limit fix on its own.

**The trade I'd make if this ran for real:**

The system should avoid wrongly accusing real writers, even if it misses some AI text. The site and its readers would see more AI content, but honest writers would face fewer false accusations.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

<!-- ═══════════════════════ UNIT 9 — THE CAPSTONE ═══════════════════════ -->

## What This Extends

This extends **Provenance Guard** (project 4), the Flask service that labels
submitted text as likely AI-written or human-written and lets writers appeal.

What's new: the audit log now records **how each request went**, not just what
was decided. Every request, including the ones that fail, writes a log line
with how long it took, how long the input was, which endpoint it hit, and the
HTTP status it returned. That makes the service's speed and failures visible
after the fact, and gives a measured cost per request.

## The Shape

**Shape A — Deploy and instrument.** The extension is the operational layer:
a documented one-command run path, timing and status fields on every audit log
record, failure records for every rejected request, and a measured
cost-per-request number taken from the log.

**Out of scope:**

- **Hosting.** The detector model is about 550 MB, more than the 512 MB free
  hosting tier allows, so the service runs locally (Path B).
- **The detector and scoring.** I'm not changing `detector.py`,
  `stylometry.py`, or `scoring.py`. The labels should come out the same as in
  unit 8.
- **New endpoints or features.** No new routes and no interface. Only
  `/submit`, `/appeal` and `/log` as they already exist.

## Running It

## Instrumentation

## What It Costs

## Run Log and Verdicts (Capstone)

## The Improvement (Capstone)

## What's Still Broken (Capstone)

## How I Used AI (Capstone)

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
