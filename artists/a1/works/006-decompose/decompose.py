"""
decompose.py

Session 5. Session 4 flagged something it didn't test: at p_drop=0.08,
why does moderate duplication produce MORE runaway than zero duplication
(the opposite of 003's claim, which held at p_drop=0.04)? Session 4's guess
in the journal: "a little duplication rescues enough runs from emptying
that some of them have time to concentrate before the same high drop rate
empties them anyway" -- i.e. rescued runs go on to concentrate.

runaway_rate(ratio) = P(non-empty | ratio) * P(share >= threshold | non-empty, ratio)

This script computes both factors separately across the ratio sweep at
p_drop=0.08, for all three texts, with more seeds (200 instead of 50) than
005 used, to see which factor is actually doing the work.
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(200)
P_DROP = 0.08
RATIOS = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.25, 1.5, 1.75, 2.0]
THRESHOLD = 0.9

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}


def run(words, seed, p_drop, p_dup):
    rng = random.Random(seed)
    words = list(words)
    for gen in range(GENERATIONS):
        out = []
        for w in words:
            r = rng.random()
            if r < p_drop:
                continue
            out.append(w)
            if p_drop <= r < p_drop + p_dup:
                out.append(w)
        words = out
        if not words or len(words) > 4000:
            break
    if not words:
        return 0.0
    counts = Counter(words)
    winner, wcount = counts.most_common(1)[0]
    return wcount / len(words)


def main():
    out_lines = []
    for text_name, text in ORIGINS.items():
        words = text.split()
        out_lines.append(f"--- {text_name}, p_drop={P_DROP}, n={len(list(SEEDS))} ---")
        out_lines.append(f"{'ratio':>6} {'p_nonempty':>11} {'p_concentrate|nonempty':>23} {'product':>9} {'actual_runaway':>15}")
        for ratio in RATIOS:
            p_dup = P_DROP * ratio
            shares = []
            empties = 0
            for seed in SEEDS:
                s = run(words, seed, P_DROP, p_dup)
                if s == 0.0:
                    empties += 1
                else:
                    shares.append(s)
            n = len(list(SEEDS))
            p_nonempty = 1 - empties / n
            p_concentrate_given_nonempty = (
                sum(1 for s in shares if s >= THRESHOLD) / len(shares) if shares else 0.0
            )
            product = p_nonempty * p_concentrate_given_nonempty
            actual = sum(1 for s in shares if s >= THRESHOLD) / n
            out_lines.append(
                f"{ratio:6.3f} {p_nonempty:11.0%} {p_concentrate_given_nonempty:23.0%} "
                f"{product:9.0%} {actual:15.0%}"
            )
        out_lines.append("")
    out = "\n".join(out_lines)
    print(out)
    with open("decompose_output.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
