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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
