"""
ratio.py

Session 3. Direct continuation of 002's named-but-untested next question:
is there a critical p_dup:p_drop ratio that separates "extinction" (drop
wins, text erased) from "runaway" (one word takes over, text survives)?

002 only tested two points: (0.04, 0.0) = drop-only = mostly extinct, and
(0.04, 0.03) = both = mostly runaway. That's not a sweep, it's two dots.
This holds p_drop fixed at 0.04 (same as 001/002, so results stay
comparable) and sweeps p_dup from 0 up past 0.04, looking at where the
extinction rate crosses over into runaway.

Definitions, kept identical to isolate.py so numbers are comparable:
  - "emptied" = text reaches zero words before GENERATIONS runs out.
  - "runaway" = text survives AND max single-word share >= 0.9 at the end.
  - anything else = "mixed" (survives, no single word dominates).
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(50)  # more seeds than 002 since we need a cleaner crossover point
P_DROP = 0.04
RATIOS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]  # p_dup / p_drop

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
        return "empty", 0.0
    counts = Counter(words)
    winner, wcount = counts.most_common(1)[0]
    share = wcount / len(words)
    return ("runaway" if share >= 0.9 else "mixed"), share


def summarize(text, p_drop, ratio):
    p_dup = p_drop * ratio
    words = text.split()
    outcomes = Counter()
    shares = []
    for seed in SEEDS:
        outcome, share = run(words, seed, p_drop, p_dup)
        outcomes[outcome] += 1
        shares.append(share)
    n = len(SEEDS)
    avg = sum(shares) / n
    return (
        f"  ratio={ratio:4.2f} p_dup={p_dup:.4f}  "
        f"empty={outcomes['empty']:2d}/{n}  mixed={outcomes['mixed']:2d}/{n}  "
        f"runaway={outcomes['runaway']:2d}/{n}  avg_share={avg:.0%}"
    )


def main():
    lines = []
    for text_name, text in ORIGINS.items():
        lines.append(f"=== {text_name} === (p_drop fixed at {P_DROP})")
        for ratio in RATIOS:
            lines.append(summarize(text, P_DROP, ratio))
        lines.append("")
    out = "\n".join(lines)
    print(out)
    with open("ratio_output.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
