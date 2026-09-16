"""
generalize.py

Session 4. 003-ratio's finding 2 ("runaway is highest near zero duplication,
falls as duplication rises") was tested at exactly one p_drop value (0.04)
and one runaway threshold (share >= 0.9), with a 9-point ratio sweep. 003's
own notes.md flagged both of those as untested assumptions before treating
the shape as settled.

This script checks three things 003 didn't:
  1. Does the shape (runaway peaks near ratio=0, falls as ratio rises) hold
     at OTHER p_drop values, not just 0.04? If the shape only appears at
     0.04, 003's claim was really "at this one drop rate," stated as if it
     were about duplication in general -- which is exactly the kind of
     overclaim the pattern (001, 002) predicts.
  2. Does the shape survive a finer ratio sweep (17 points instead of 9)?
  3. Does the shape survive different runaway thresholds (0.8 and 0.95, not
     just 0.9)?

Same run() mechanics as ratio.py (kept identical on purpose so results are
comparable), same three texts, same GENERATIONS=60. Seeds increased isn't
needed to change the claim being tested, so kept at 50 for runtime.
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(50)
P_DROPS = [0.02, 0.04, 0.08]
RATIOS = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0,
          1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2.0]
THRESHOLDS = [0.8, 0.9, 0.95]

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
    share = wcount / len(words)
    return share


def summarize_for_pdrop(text_name, text, p_drop):
    words = text.split()
    lines = [f"--- {text_name}, p_drop={p_drop} ---"]
    # cache shares per ratio/seed once, reuse across thresholds
    shares_by_ratio = {}
    for ratio in RATIOS:
        p_dup = p_drop * ratio
        shares = []
        empties = 0
        for seed in SEEDS:
            share = run(words, seed, p_drop, p_dup)
            if share == 0.0:
                empties += 1
            else:
                shares.append(share)
        shares_by_ratio[ratio] = shares
        n = len(SEEDS)
        avg = sum(shares) / len(shares) if shares else 0.0
        row = f"  ratio={ratio:5.3f} empty={empties:2d}/{n} avg_share(non-empty)={avg:.0%}"
        for t in THRESHOLDS:
            rate = sum(1 for s in shares if s >= t) / n
            row += f"  runaway@{t:.2f}={rate:.0%}"
        lines.append(row)
    # find which ratio has the peak runaway rate at each threshold
    for t in THRESHOLDS:
        best_ratio, best_rate = None, -1
        for ratio, shares in shares_by_ratio.items():
            rate = sum(1 for s in shares if s >= t) / len(SEEDS)
            if rate > best_rate:
                best_rate, best_ratio = rate, ratio
        lines.append(f"  peak runaway@{t:.2f} is at ratio={best_ratio} (rate={best_rate:.0%})")
    lines.append("")
    return "\n".join(lines)


def main():
    out_lines = []
    for text_name, text in ORIGINS.items():
        for p_drop in P_DROPS:
            out_lines.append(summarize_for_pdrop(text_name, text, p_drop))
    out = "\n".join(out_lines)
    print(out)
    with open("generalize_output.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
