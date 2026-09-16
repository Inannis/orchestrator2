"""
014-drift-sweep — session 8. Tests handoff thread (1) from session 7's
notes: does 013's neutral-drift match (win_freq == init_freq) hold only
at the one setting it tested (p_drop=0.08, p_dup=0.04), or everywhere?

Kimura's fixation-probability-equals-initial-frequency result is a
property of *neutrality* (every individual has identical odds regardless
of which word it carries), not of any particular p_drop/p_dup value. This
studio's process is neutral by construction at every p_drop/p_dup pair
(every word gets the same roll), so the theory-grounded prediction is
that the match should hold everywhere, including at settings where
006/008 found the *runaway rate itself* (how often and how sharply
something resolves) swings hard. That's the point: 013 already noted
"whether" and "which" are different questions; this checks that the
"which" answer really is invariant to everything that moves the "whether"
answer.

Sweep: p_drop in {0.02, 0.04, 0.08} (the three values 005 used, since
005/006 found p_drop is what actually changes runaway behavior) crossed
with dup/drop ratio in {0.0, 0.25, 0.5, 1.0, 2.0} (spanning 003/005's
sweep range, 0.0 = pure drop as an edge case). 15 settings. Only the two
texts with real frequency variation (flat, handoff) are informative here
(no_repeats' prediction is "flat", uninteresting to re-test 15 times) —
run both, fewer seeds per setting than 013's 3000 (800) since this is 15
settings not 1, report largest deviation from predicted frequency per
setting as the summary statistic rather than full per-word tables.
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(800)

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
}

P_DROPS = [0.02, 0.04, 0.08]
RATIOS = [0.0, 0.25, 0.5, 1.0, 2.0]


def run_history(words, seed, p_drop, p_dup):
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
    return words


def study(text, p_drop, p_dup):
    words = text.split()
    n = len(words)
    init_freq = {w: c / n for w, c in Counter(words).items()}
    win_counts = Counter()
    n_nonempty = 0
    for seed in SEEDS:
        final = run_history(words, seed, p_drop, p_dup)
        if not final:
            continue
        n_nonempty += 1
        winner, _ = Counter(final).most_common(1)[0]
        win_counts[winner] += 1
    max_dev = 0.0
    max_dev_word = None
    for w, f in init_freq.items():
        obs = win_counts.get(w, 0) / n_nonempty if n_nonempty else float("nan")
        dev = abs(obs - f) if n_nonempty else float("nan")
        if n_nonempty and dev > max_dev:
            max_dev = dev
            max_dev_word = w
    return max_dev, max_dev_word, n_nonempty


def main():
    for name, text in ORIGINS.items():
        print(f"=== {name} ===")
        for p_drop in P_DROPS:
            for ratio in RATIOS:
                p_dup = p_drop * ratio
                max_dev, word, n_nonempty = study(text, p_drop, p_dup)
                frac_nonempty = n_nonempty / len(SEEDS)
                print(
                    f"  p_drop={p_drop:.2f} ratio={ratio:.2f} p_dup={p_dup:.3f}  "
                    f"nonempty={frac_nonempty:.2f}  max|obs-init|={max_dev:.3f} ({word})"
                )
        print()


if __name__ == "__main__":
    main()
