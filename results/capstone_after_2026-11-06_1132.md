# Capstone run log — after

`python capstone_trial.py --label after`, 2026-11-06 11:32, 3 trials, each a fresh start of `app.py` on port 5001.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request is logged | 23 of 23 | 23/23 | 23/23 | 23/23 | MET |
| C2. Bad requests get an error, not a crash | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| C3. The logged time is correct (within 20 ms of curl) | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| C4. Every submission under 1 s, even the first | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| C5. The original results didn't change | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

## Trial 1 — the normal submissions

| # | curl ms | logged ms | diff | result | response guess = decision guess |
|---|---|---|---|---|---|
| writer-1 | 62.6 | 61.2 | 1.4 | unsure | True |
| writer-2 | 49.8 | 47.3 | 2.5 | human | True |
| writer-3 | 40.4 | 38.8 | 1.6 | unsure | True |
| writer-4 | 44.7 | 42.7 | 2.0 | unsure | True |
| writer-5 | 50.0 | 47.9 | 2.1 | ai | True |
| writer-6 | 32.1 | 30.7 | 1.4 | human | True |
| writer-7 | 51.5 | 50.3 | 1.2 | ai | True |
| writer-8 | 68.7 | 67.4 | 1.3 | human | True |
| writer-9 | 38.6 | 37.5 | 1.1 | ai | True |
| writer-10 | 48.6 | 47.3 | 1.3 | human | True |

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
{"timestamp": "2026-11-06T19:32:25+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 61.2, "input_chars": 92, "input_preview": "I walked to the market this morning and bought apples, then sat by the river rea", "creator_id": "writer-1", "content_id": "04e9607b-ff9c-4da0-b1f9-be29676babe0", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:32:25+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 47.3, "input_chars": 86, "input_preview": "Honestly the bus was late again so I missed the first ten minutes of class. Not ", "creator_id": "writer-2", "content_id": "aeaaf51a-926e-4157-8f20-429479310b7b", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:25+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 38.8, "input_chars": 136, "input_preview": "In conclusion, artificial intelligence offers numerous benefits across various i", "creator_id": "writer-3", "content_id": "24a3c167-306a-4771-8715-95cef011aefd", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:32:25+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 42.7, "input_chars": 81, "input_preview": "My grandma makes the best dumplings. She never measures anything, she just knows", "creator_id": "writer-4", "content_id": "dcbd0362-f04d-40ba-aadb-44596ffc2768", "result": "unsure", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 47.9, "input_chars": 109, "input_preview": "Climate change represents one of the most significant challenges facing humanity", "creator_id": "writer-5", "content_id": "1e8103f6-c9d6-4f72-8c9c-d0ec93a3a532", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 30.7, "input_chars": 70, "input_preview": "lol my cat knocked my coffee onto my keyboard and now the e key sticks", "creator_id": "writer-6", "content_id": "7548a900-4adb-443d-a2fa-e87056e76065", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 50.3, "input_chars": 113, "input_preview": "Effective time management is essential for achieving personal and professional g", "creator_id": "writer-7", "content_id": "180198c4-3c54-43bc-b439-90da173f424e", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 67.4, "input_chars": 84, "input_preview": "We drove six hours to see the lake and it rained the entire weekend. Still worth", "creator_id": "writer-8", "content_id": "bac67d04-7784-4c4c-a74f-3171b0e1b1de", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 37.5, "input_chars": 105, "input_preview": "The French Revolution was a period of radical political and societal change in F", "creator_id": "writer-9", "content_id": "194666f3-2c3b-43eb-9570-71de2031fb5d", "result": "ai", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 47.3, "input_chars": 97, "input_preview": "I tried to fix the sink myself and now there is water in the hallway. Calling a ", "creator_id": "writer-10", "content_id": "53d95e72-ec26-454e-8e24-13e0fa5f68dd", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.3, "input_chars": 0, "input_preview": "", "creator_id": "bad-1", "content_id": null, "result": null, "error": "Text is required"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.3, "input_chars": 5, "input_preview": "     ", "creator_id": "bad-2", "content_id": null, "result": null, "error": "Text is required"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.2, "input_chars": 10001, "input_preview": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "creator_id": "bad-3", "content_id": null, "result": null, "error": "Text must be 10,000 characters or fewer"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.2, "input_chars": 16, "input_preview": "Some words here.", "creator_id": null, "content_id": null, "result": null, "error": "Creator ID is required"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 400, "duration_ms": 0.1, "input_chars": 0, "input_preview": null, "creator_id": null, "content_id": null, "result": null, "error": "Expected a JSON object"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/appeal", "method": "POST", "http_status": 404, "duration_ms": 1.6, "input_chars": 4, "input_preview": "mine", "creator_id": null, "content_id": null, "result": null, "error": "Submission not found"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/appeal", "method": "POST", "http_status": 400, "duration_ms": 0.1, "input_chars": 0, "input_preview": null, "creator_id": null, "content_id": null, "result": null, "error": "Reasoning is required"}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.0, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "1b9ba82b-fa89-46ea-8be3-0255527bb770", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.2, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "7da5fb9b-ac7b-4a19-bcd5-8f9c19cb02e8", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 18.9, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "8bb8710d-fe98-476d-b98f-a647f9b1c539", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.1, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "ec75f0e9-60e9-4caf-a910-247cbde83d0b", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 200, "duration_ms": 19.7, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": "a6302abf-73e8-4d52-9084-36301b293cb1", "result": "human", "error": null}
{"timestamp": "2026-11-06T19:32:26+00:00", "event": "request", "endpoint": "/submit", "method": "POST", "http_status": 429, "duration_ms": 0.4, "input_chars": 58, "input_preview": "Testing the rate limit with the same short sentence again.", "creator_id": "flooder", "content_id": null, "result": null, "error": "rate_limited"}
```
