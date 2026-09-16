"""
isolate.py

Follow-up to attractor.py, same session. attractor.py showed duplication
alone does not produce a single-word collapse. This checks the other half:
does DROP alone produce one, or does collapse really require both forces
at once (thinning + multiplying) interacting?

Three conditions, same texts/seeds as attractor.py:
  - drop only  (P_DROP=0.04, nothing else)
  - duplicate only (P_DUPLICATE=0.03, nothing else) -- rerun here for a
    direct side-by-side, same numbers as attractor.py's run
  - both together (P_DROP=0.04, P_DUPLICATE=0.03) -- the original drift.py
    condition minus swap, to isolate drop+duplicate from swap's effect

Reports max single-word share reached in each condition, across seeds,
per text. A real collapse should show that share approaching 100% for
"both", and staying low for the single-force conditions.
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(30)

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
        return 1.0, 0  # fully collapsed to nothing counts as total collapse
    counts = Counter(words)
    winner, wcount = counts.most_common(1)[0]
    return wcount / len(words), len(words)


def summarize(name, text, p_drop, p_dup):
    words = text.split()
    shares = []
    empties = 0
    for seed in SEEDS:
        share, length = run(words, seed, p_drop, p_dup)
        if length == 0:
            empties += 1
        shares.append(share)
    avg = sum(shares) / len(shares)
    mx = max(shares)
    return f"  {name:12s} p_drop={p_drop} p_dup={p_dup}  avg_max_share={avg:.0%}  peak={mx:.0%}  emptied={empties}/{len(SEEDS)}"


def main():
    lines = []
    for text_name, text in ORIGINS.items():
        lines.append(f"=== {text_name} ===")
        lines.append(summarize("drop-only", text, 0.04, 0.0))
        lines.append(summarize("dup-only", text, 0.0, 0.03))
        lines.append(summarize("both", text, 0.04, 0.03))
        lines.append("")
    out = "\n".join(lines)
    print(out)
    with open("isolate_output.txt", "w", encoding="utf-8") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
