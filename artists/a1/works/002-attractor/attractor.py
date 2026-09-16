"""
attractor.py

Session 2. Direct test of the thing 001-drift found by accident: duplication
compounds because a duplicated word gets two independent chances to be
duplicated again next round, so early luck (not meaning, not position,
not word length) decides which word eats the sentence.

This version strips the mechanism down to ONLY duplication -- no drop, no
swap -- so nothing else can explain the outcome. If a text still collapses
to a single repeated word under pure duplication, and if the winner is
consistently the word that happened to duplicate first, that confirms the
mechanism directly instead of inferring it after the fact from 001.

For each (origin text, seed) pair:
  - run GENERATIONS passes of: each word independently has probability
    P_DUPLICATE of being duplicated in place.
  - record the first word (by original position) to ever get duplicated.
  - record the word that has the largest share of the final generation.
  - report whether they match.

Deterministic given a seed. Run across many seeds per text to see the
match rate, not just one anecdote.
"""
import random
from collections import Counter

P_DUPLICATE = 0.03
GENERATIONS = 60
SEEDS = range(30)

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": (
        "the cat sat on the mat and the dog sat on the rug"
    ),
    "no_repeats": (
        "glass water window ladder river copper distance evening"
    ),
}


def run(words, seed):
    rng = random.Random(seed)
    words = list(words)
    first_duplicated = None
    for gen in range(GENERATIONS):
        out = []
        for i, w in enumerate(words):
            out.append(w)
            if rng.random() < P_DUPLICATE:
                out.append(w)
                if first_duplicated is None:
                    first_duplicated = (i, w)
        words = out
        if len(words) > 4000:  # runaway growth, stop early
            break
    counts = Counter(words)
    if not counts:
        return first_duplicated, None, 0, len(words)
    winner, wcount = counts.most_common(1)[0]
    return first_duplicated, winner, wcount, len(words)


def main():
    lines = []
    for name, text in ORIGINS.items():
        words = text.split()
        lines.append(f"=== {name} === ({len(words)} words: {' '.join(words)})")
        matches = 0
        total = 0
        for seed in SEEDS:
            fd, winner, wcount, total_len = run(words, seed)
            total += 1
            if fd is None:
                lines.append(f"  seed {seed:2d}: no word ever duplicated (nothing to collapse into)")
                continue
            fd_idx, fd_word = fd
            share = wcount / total_len if total_len else 0
            match = (fd_word == winner)
            if match:
                matches += 1
            lines.append(
                f"  seed {seed:2d}: first-duplicated='{fd_word}' (pos {fd_idx})  "
                f"final-winner='{winner}' ({wcount}/{total_len}={share:.0%})  "
                f"{'MATCH' if match else 'no match'}"
            )
        lines.append(f"  -> first-duplicated predicts final winner in {matches}/{total} runs\n")

    text = "\n".join(lines)
    print(text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
