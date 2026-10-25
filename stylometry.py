"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())

def sentence_length_spread(text: str) -> float:
    """
    Measures variation in sentence lengths.
    Higher = more variation.
    Lower = less variation.
    """
    lengths = [
        len(words(sentence))
        for sentence in sentences(text)
    ]

    lengths = [length for length in lengths if length > 0]

    if len(lengths) < 2:
        return 0.0

    return statistics.stdev(lengths) / statistics.mean(lengths)

def type_token_ratio(text: str) -> float:
    """
    Measures vocabulary variety.

    Returns:
        A float between 0 and 1.
        Higher = more varied vocabulary.
        Lower = more repeated words.
    """
    word_list = words(text)

    if not word_list:
        return 0.0

    # Count unique words
    unique_words = set(word_list)

    # Divide unique words by total words
    return len(unique_words) / len(word_list)

def punctuation_density(text: str) -> float:
    """
    Measures punctuation usage relative to text length.

    Returns:
        A float between 0 and 1.
        Higher = more punctuation.
        Lower = less punctuation.
    """
    # Handle empty text
    if not text:
        return 0.0

    # Count punctuation characters
    punctuation_count = sum(
        1 for char in text if char in ".,!?;:-—"
    )

    # Divide by total characters, excluding spaces
    text_length = len(text.replace(" ", ""))

    if text_length == 0:
        return 0.0

    return punctuation_count / text_length

# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    Combines three writing-style measurements into one AI score.

    Returns:
        A float between 0 and 1.
        Higher = more AI-like writing.
    """
    if not words(text):
        return 0.5

    # Measure the text
    spread = sentence_length_spread(text)
    vocabulary = type_token_ratio(text)
    punctuation = punctuation_density(text)

    # Convert each measurement to an AI-like score (0–1)
    spread_score = 1.0 - min(spread, 1.0)
    vocabulary_score = 1.0 - vocabulary

    # More punctuation is treated as less AI-like
    punctuation_score = 1.0 - min(punctuation / 0.15, 1.0)

    # Combine all three with equal weights
    combined = (
        spread_score +
        vocabulary_score +
        punctuation_score
    ) / 3.0

    return round(max(0.0, min(combined, 1.0)), 4)

if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
