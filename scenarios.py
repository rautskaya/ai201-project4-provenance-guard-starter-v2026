"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

MY_WRITING = [
  "Saturday I finally cleaned the garage, it took like 4 hours because I kept finding old stuff and stopping to look at it. Found my kids drawings from kindergarten. Sunday we just stayed home and ordered pizza, nobody wanted to cook.",
  "My job is mostly emails and meetings honestly. The meetings could be emails. When I get actual time to work on something I like it, but that's maybe 2 hours a day if I'm lucky.",
  "My mom makes this potato pancake thing, we call them draniki. You grate potatoes and onion, add egg and flour, fry it in a lot of oil. Eat with sour cream. I tried to make it myself but mine always fall apart, I don't know what she does different.",
  "The parking at my building is a mess this week. They're repainting the lines so half the spots are closed and people just park anywhere. Someone blocked me in yesterday and I was 20 min late.",
  "Hi Sarah, sorry I didn't finish the report yet. I had a problem with the data from last month, some numbers don't match. Can I send it on Thursday instead? I'll let you know if it takes longer.",
  "We went to Chicago in March which was a mistake, so cold and windy I couldn't feel my face. But the food was amazing. We had deep dish pizza twice and I'm not even sorry. Next time summer for sure.",
  "I signed up because at work everyone talks about AI now and I felt like I don't understand anything. Some weeks are hard and I have to watch the videos two times. But I already used one thing at my job so I guess it's working.",
  "If you didn't watch The Bear yet you should. First episode is very stressful, I almost stopped. Then it gets better and you start to care about everyone in the kitchen. Season 2 is my favorite.",
  "Alarm at 6:30, I snooze it at least two times, every day. Coffee first, nobody talks to me before coffee. Then I make lunch for my son and drive him to school, and usually I eat my breakfast in the car at red lights.",
  "Don't buy that white couch. Also stop worrying so much what other people think, most of them are not even thinking about you. And save some money, even small, it adds up more than you think."
]


# ─── AI-generated writing (criteria 2 and 3) ─────────────────────────────────
# Written by an AI model (Claude) in a typical assistant style: smooth, even
# sentences, common words, tidy structure.

AI_WRITING = [
    "Time management is an essential skill for students. By setting clear goals and creating a daily schedule, students can balance their academic responsibilities with their personal lives. It is also important to take regular breaks, as this helps maintain focus and prevents burnout. With consistent practice, effective time management can lead to better grades and reduced stress.",
    "Climate change is one of the most pressing challenges facing the world today. Rising temperatures, melting ice caps, and extreme weather events are affecting communities around the globe. To address this issue, governments, businesses, and individuals must work together to reduce greenhouse gas emissions and invest in renewable energy sources.",
    "Reading offers many benefits for people of all ages. It improves vocabulary, strengthens critical thinking skills, and allows readers to explore new ideas and perspectives. In addition, reading can be a relaxing activity that reduces stress. By making reading a daily habit, individuals can continue learning and growing throughout their lives.",
    "Social media has transformed the way people communicate and share information. On one hand, it allows users to stay connected with friends and family across long distances. On the other hand, it can contribute to misinformation and negative effects on mental health. It is important for users to approach social media thoughtfully and responsibly.",
    "Regular exercise is important for maintaining good physical and mental health. It helps strengthen the heart, improve mood, and increase energy levels. Experts recommend at least 150 minutes of moderate activity each week. Simple activities such as walking, cycling, or swimming can make a significant difference in overall well-being.",
    "Artificial intelligence is changing many industries, including healthcare, finance, and education. AI systems can analyze large amounts of data quickly and help people make better decisions. However, it is important to consider ethical issues such as privacy, fairness, and transparency. Responsible development will ensure that AI benefits society as a whole.",
    "Learning a new language can open many doors. It allows people to communicate with others from different cultures and can improve career opportunities. Studies also suggest that learning a language can enhance memory and problem-solving skills. With patience and regular practice, anyone can make steady progress toward fluency.",
    "Teamwork is a key factor in the success of any organization. When team members communicate openly and respect each other's ideas, they can solve problems more effectively. Strong teams also share responsibilities and support one another during challenging times. Building a positive team culture leads to higher productivity and job satisfaction.",
    "A healthy diet plays a vital role in overall well-being. Eating a variety of fruits, vegetables, whole grains, and lean proteins provides the nutrients the body needs to function properly. It is also important to limit processed foods and sugary drinks. Making small, consistent changes can lead to long-term health benefits.",
    "Volunteering is a meaningful way to give back to the community. It allows individuals to help others while also developing new skills and building connections. Many volunteers report feeling a greater sense of purpose and happiness. Whether it is helping at a food bank or tutoring students, every contribution makes a difference.",
]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Target: at most 1 of 10 labelled high-confidence AI, in every trial.
        "texts": MY_WRITING,
    },
    {
        "name": "spread AI",
        "criterion": 2,
        # Target: the average of these is at least 0.20 above the average of
        # "spread human" (your own writing). Compare combined_score per trial.
        "texts": AI_WRITING,
    },
    {
        "name": "spread human",
        "criterion": 2,
        "texts": MY_WRITING,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Target: all three labels (human, unsure, ai) show up in each trial.
        # One clear AI text, one casual text with typos and uneven sentences,
        # and one in between: plain, but with a personal detail.
        "texts": [
            AI_WRITING[0],
            "ok so the bus was late AGAIN today, like 25 min, and i missed the first half of chem. "
            "honestly whatever. my friend sent me her notes but half of them are just doodles of the teacher lol. "
            "test is friday. im not ready. at all. going to the library after dinner i guess, unless it rains, which it will.",
            "I started learning to cook last year because I was tired of eating takeout. At first I mostly made pasta. "
            "Over time I tried new recipes, and some of them worked better than others. Cooking at home saves money, "
            "and it is a good way to relax after a long day.",
        ],
    },
    # Criterion 4 (appeal path) is NOT here. It needs a submission first and
    # then an appeal against the content_id that came back, and run_eval.py
    # only sends to /submit. Test it by hand: submit 5 texts, appeal each
    # content_id, then check /log for 5 "appeal" entries with status
    # "under_review".
    {
        "name": "bad input",
        "criterion": 5,
        # Target: all 5 rejected with a clear error (400), no 500s.
        # Sent exactly as written.
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "This text has no creator id attached to it at all."},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
