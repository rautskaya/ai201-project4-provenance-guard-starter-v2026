# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 07:57
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `af39dcec-e96f-40aa-aba2-ef64396880dd` | human | 0.389 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ddf831e8-8bbc-447d-888b-6fb2d38ea5c8` | unsure | 0.488 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d093e7cc-d68d-4004-8e49-1b021f7b2e4c` | unsure | 0.593 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `f5544312-fa53-4f03-bf14-dcbbcbb27e4f` | unsure | 0.608 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `9ee20fc2-d5ac-46ed-bf5f-5053453f0295` | human | 0.379 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2b96fafe-0b3d-4cdf-966e-fbe82cc875a2` | unsure | 0.478 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `57caf340-20bb-49b9-ab03-626397759ad6` | unsure | 0.625 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `da4dc26b-1c82-4a78-8ee1-d0e85bbb81d3` | human | 0.369 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `17be5759-6ab0-45ea-b032-da9c3948895c` | unsure | 0.609 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `8ca9602c-a1cc-4241-b82e-c25b8488182a` | ai | 0.863 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f6f81856-2993-4063-8bd3-d676a3105d21` | unsure | 0.588 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `e960a460-b6a4-4a36-82bd-6c841439546d` | ai | 0.689 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `ffae6989-75be-4b62-9a48-015440122918` | ai | 0.704 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `cc95658b-a892-4490-8667-f2f8bc327955` | ai | 0.694 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d44c2ebe-085e-4bdd-b036-d693d805f6de` | ai | 0.726 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `fca4cf00-f197-4951-849c-7c5e168519cb` | ai | 0.705 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `59ffad08-6a31-4878-9b0a-3168c0ea7873` | ai | 0.707 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `766c1816-44f5-419d-a89b-c77e215a0b59` | human | 0.307 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `bc580fc6-197d-4178-95bc-256d91050b76` | human | 0.445 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `d4235b02-9ee0-442d-9fbc-8e9e027ed78e` | human | 0.303 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f66076b6-396b-4675-a101-79980133b126` | unsure | 0.571 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4503d158-0497-499f-8168-4f9cde83e925` | unsure | 0.516 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `8b6327fe-5bb7-4e1b-989e-eecca189fe88` | unsure | 0.527 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9c18104f-f3b1-4c3c-96b4-7e3d8ae64b5a` | unsure | 0.562 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `022a8894-f5db-45a0-b41d-38edb8619481` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `23d5f701-13ea-4d54-9e76-bc816e1c4047` | human | 0.256 |  |
| MF05 | malformed | text is a very long single word | 200 | `0fc505e3-9020-4c52-a2d7-f6ce9d927fa8` | ai | 0.832 |  |
| MF06 | malformed | text is emoji only | 200 | `f2207e1d-9765-497e-8309-fe9eca2dfce7` | ai | 0.748 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c9650e9f-0fe4-4873-a36e-d44714792430` | ai | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b06db594-c430-4ee7-aff8-1fe70759abf4` | human | 0.324 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c49e6e80-f3dc-4e0f-a9f4-fc162c9f831d` | human | 0.324 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2ccf801d-4cab-4f5f-b1da-1ff2245b95ca` | human | 0.324 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `67f60940-831d-4261-be09-9ba037158968` | human | 0.324 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9cad8190-e131-46ba-8c4c-11dd686e0079` | human | 0.324 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "af39dcec-e96f-40aa-aba2-ef64396880dd",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.38855,
  "model_score": 0.1635,
  "style_score": 0.6136,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ddf831e8-8bbc-447d-888b-6fb2d38ea5c8",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.48760000000000003,
  "model_score": 0.5943,
  "style_score": 0.3809,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d093e7cc-d68d-4004-8e49-1b021f7b2e4c",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.59275,
  "model_score": 0.6662,
  "style_score": 0.5193,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "f5544312-fa53-4f03-bf14-dcbbcbb27e4f",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.60815,
  "model_score": 0.6114,
  "style_score": 0.6049,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "9ee20fc2-d5ac-46ed-bf5f-5053453f0295",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.37905,
  "model_score": 0.3212,
  "style_score": 0.4369,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2b96fafe-0b3d-4cdf-966e-fbe82cc875a2",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4785,
  "model_score": 0.5727,
  "style_score": 0.3843,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "57caf340-20bb-49b9-ab03-626397759ad6",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6250500000000001,
  "model_score": 0.5862,
  "style_score": 0.6639,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "da4dc26b-1c82-4a78-8ee1-d0e85bbb81d3",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3691,
  "model_score": 0.2452,
  "style_score": 0.493,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "17be5759-6ab0-45ea-b032-da9c3948895c",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6091,
  "model_score": 0.7042,
  "style_score": 0.514,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "8ca9602c-a1cc-4241-b82e-c25b8488182a",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8634,
  "model_score": 0.9792,
  "style_score": 0.7476,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f6f81856-2993-4063-8bd3-d676a3105d21",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5880000000000001,
  "model_score": 0.6175,
  "style_score": 0.5585,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "e960a460-b6a4-4a36-82bd-6c841439546d",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.68875,
  "model_score": 0.7387,
  "style_score": 0.6388,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "ffae6989-75be-4b62-9a48-015440122918",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7041999999999999,
  "model_score": 0.8051,
  "style_score": 0.6033,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "cc95658b-a892-4490-8667-f2f8bc327955",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6939500000000001,
  "model_score": 0.8329,
  "style_score": 0.555,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "d44c2ebe-085e-4bdd-b036-d693d805f6de",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7256,
  "model_score": 0.8005,
  "style_score": 0.6507,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "fca4cf00-f197-4951-849c-7c5e168519cb",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.70495,
  "model_score": 0.8814,
  "style_score": 0.5285,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "59ffad08-6a31-4878-9b0a-3168c0ea7873",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7066,
  "model_score": 0.8816,
  "style_score": 0.5316,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "766c1816-44f5-419d-a89b-c77e215a0b59",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.30735,
  "model_score": 0.3223,
  "style_score": 0.2924,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "bc580fc6-197d-4178-95bc-256d91050b76",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.44510000000000005,
  "model_score": 0.4625,
  "style_score": 0.4277,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "d4235b02-9ee0-442d-9fbc-8e9e027ed78e",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3028,
  "model_score": 0.2044,
  "style_score": 0.4012,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "f66076b6-396b-4675-a101-79980133b126",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5713,
  "model_score": 0.5943,
  "style_score": 0.5483,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "4503d158-0497-499f-8168-4f9cde83e925",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5157499999999999,
  "model_score": 0.4998,
  "style_score": 0.5317,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "8b6327fe-5bb7-4e1b-989e-eecca189fe88",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5266,
  "model_score": 0.6401,
  "style_score": 0.4131,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "9c18104f-f3b1-4c3c-96b4-7e3d8ae64b5a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.56155,
  "model_score": 0.5583,
  "style_score": 0.5648,
  "label": "We cannot confidently determine whether this text was written by a human or AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "022a8894-f5db-45a0-b41d-38edb8619481",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.33335,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "23d5f701-13ea-4d54-9e76-bc816e1c4047",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "0fc505e3-9020-4c52-a2d7-f6ce9d927fa8",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.83215,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "f2207e1d-9765-497e-8309-fe9eca2dfce7",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7484500000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c9650e9f-0fe4-4873-a36e-d44714792430",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text shows signs of AI-generated writing, but this result is not proof.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "b06db594-c430-4ee7-aff8-1fe70759abf4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.32404999999999995,
  "model_score": 0.0287,
  "style_score": 0.6194,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c49e6e80-f3dc-4e0f-a9f4-fc162c9f831d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.32404999999999995,
  "model_score": 0.0287,
  "style_score": 0.6194,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "2ccf801d-4cab-4f5f-b1da-1ff2245b95ca",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.32404999999999995,
  "model_score": 0.0287,
  "style_score": 0.6194,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "67f60940-831d-4261-be09-9ba037158968",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.32404999999999995,
  "model_score": 0.0287,
  "style_score": 0.6194,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "9cad8190-e131-46ba-8c4c-11dd686e0079",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.32404999999999995,
  "model_score": 0.0287,
  "style_score": 0.6194,
  "label": "This text is likely written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
