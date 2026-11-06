# Capstone run log — before

`python capstone_trial.py --label before`, 2026-11-06 11:28, 3 trials, each a fresh start of `app.py` on port 5001.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request is logged | 23 of 23 | 23/23 | 23/23 | 23/23 | MET |
| C2. Bad requests get an error, not a crash | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| C3. The logged time is correct (within 20 ms of curl) | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| C4. Every submission under 1 s, even the first | 10 of 10 | 9/10 | 9/10 | 9/10 | MISSED |
| C5. The original results didn't change | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

## Trial 1 — the normal submissions

| # | curl ms | logged ms | diff | result | response guess = decision guess |
|---|---|---|---|---|---|
| writer-1 | 4199.5 | 4198.1 | 1.4 | unsure | True |
| writer-2 | 29.9 | 28.8 | 1.1 | human | True |
| writer-3 | 33.3 | 32.0 | 1.3 | unsure | True |
| writer-4 | 28.5 | 27.6 | 0.9 | unsure | True |
| writer-5 | 29.6 | 28.6 | 1.0 | ai | True |
| writer-6 | 20.3 | 19.4 | 0.9 | human | True |
| writer-7 | 25.4 | 24.6 | 0.8 | ai | True |
| writer-8 | 25.1 | 24.1 | 0.9 | human | True |
| writer-9 | 25.3 | 24.3 | 1.0 | ai | True |
| writer-10 | 26.0 | 25.1 | 0.9 | human | True |

## Trial 1 — the bad requests

| request | expected | got | logged error |
|---|---|---|---|
| empty text | 400 | 400 | Text is required |
| only spaces | 400 | 400 | Text is required |
| over 10,000 chars | 400 | 400 | Text must be 10,000 characters or fewer |
| no creator_id | 400 | 400 | Creator ID is required |
| not JSON | 400 | 400 | Expected a JSON object |
| appeal unknown id | 404 | 404 | Submission not found |
| appeal no reasoning | 400 | 400 | Reasoning is required |
| flooder #6 | 429 | 429 | rate_limited |

## Trial 1 — raw request log lines

```
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 4198.1, "input_chars": 92, "input_preview": "I walked to the market this morning and bought apples, then sat by the river rea", "creator_id": "writer-1", "content_id": "ad76b368-5c41-48a6-a32f-fdc7014ea516", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 28.8, "input_chars": 86, "input_preview": "Honestly the bus was late again so I missed the first ten minutes of class. Not ", "creator_id": "writer-2", "content_id": "e164d2f0-1638-4a58-af65-c2c5032bbe17", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 32.0, "input_chars": 136, "input_preview": "In conclusion, artificial intelligence offers numerous benefits across various i", "creator_id": "writer-3", "content_id": "29d45d28-dc66-4099-b328-b450d8ec8299", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 27.6, "input_chars": 81, "input_preview": "My grandma makes the best dumplings. She never measures anything, she just knows", "creator_id": "writer-4", "content_id": "afb02246-ee43-4163-b5c1-abb34456b523", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 28.6, "input_chars": 109, "input_preview": "Climate change represents one of the most significant challenges facing humanity", "creator_id": "writer-5", "content_id": "ff35c303-2866-413a-8a9a-777f64cbe292", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.4, "input_chars": 70, "input_preview": "lol my cat knocked my coffee onto my keyboard and now the e key sticks", "creator_id": "writer-6", "content_id": "6b968189-c884-4dbf-9b9d-c0f5d4077d4b", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 24.6, "input_chars": 113, "input_preview": "Effective time management is essential for achieving personal and professional g", "creator_id": "writer-7", "content_id": "0dd7f68e-1436-4d70-863f-9bff1f8cc1db", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 24.1, "input_chars": 84, "input_preview": "We drove six hours to see the lake and it rained the entire weekend. Still worth", "creator_id": "writer-8", "content_id": "af0a2c52-e649-4b6d-9d83-34adca73cf0c", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 24.3, "input_chars": 105, "input_preview": "The French Revolution was a period of radical political and societal change in F", "creator_id": "writer-9", "content_id": "90dd5791-a8b1-4d4f-a8da-5e839a5d551b", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 25.1, "input_chars": 97, "input_preview": "I tried to fix the sink myself and now there is water in the hallway. Calling a ", "creator_id": "writer-10", "content_id": "8685f59a-b512-4954-b0d3-0e5b566f8362", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.2, "input_chars": 0, "input_preview": "", "creator_id": "bad-1", "content_id": null, "result": null, "error": "Text is required"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.1, "input_chars": 5, "input_preview": "     ", "creator_id": "bad-2", "content_id": null, "result": null, "error": "Text is required"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.2, "input_chars": 10001, "input_preview": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "creator_id": "bad-3", "content_id": null, "result": null, "error": "Text must be 10,000 characters or fewer"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.1, "input_chars": 16, "input_preview": "Some words here.", "creator_id": null, "content_id": null, "result": null, "error": "Creator ID is required"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.2, "input_chars": 0, "input_preview": null, "creator_id": null, "content_id": null, "result": null, "error": "Expected a JSON object"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/appeal", "method": "POST", "http_status": 404, "duration_ms": 0.8, "input_chars": 4, "input_preview": "mine", "creator_id": null, "content_id": null, "result": null, "error": "Submission not found"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/appeal", "method": "POST", "http_status": 400, "duration_ms": 0.1, "input_chars": 0, "input_preview": null, "creator_id": null, "content_id": null, "result": null, "error": "Reasoning is required"}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.5, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "2f1e9bdd-50be-4a7d-83ae-ecdbbf29da75", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 22.1, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "3936d910-aa04-41f0-a9a3-ecfff87d32f6", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 18.6, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "eea4073e-ecec-4ff7-b3f3-48308e3b3f08", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 18.4, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "d1fe73cf-13ee-4edb-9fc1-d7c111fb32d9", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 18.3, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "d87d8ddf-0bf6-43c3-8f42-37554912c18d", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:28:23+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 429, "duration_ms": 0.3, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": null, "result": null, "error": "rate_limited"}
```
