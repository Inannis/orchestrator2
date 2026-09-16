"""
012-scar-check — session 7, fourth piece of work today (study, not
image). Answers the question 011's own notes proposed: does the visible
trunk-scarring in `public/rooting.png` (thin gaps in an otherwise solid
winner-color trunk) actually track 008/009's measured retreat rate, or is
"it looks scarred" a different thing from "it measures as high-retreat"?

Method: take the exact three seeds `runaway_settling.py` found and used
(handoff=1, flat=2, no_repeats=6) and compute 008's `whole_run_retreats`
rate for each one specifically. Then, separately, run the same 200-seed
runaway-only sample 008/009 already used at 1x population (same
p_drop=0.08/p_dup=0.04 point) and find each single seed's percentile
within that distribution -- answers "is this seed typical, or did the
rule that picked it (first runaway seed found) happen to also pick an
unusually smooth or scarred run, which would undermine reading the image
as representative of anything beyond itself."
"""
import random
from collections import Counter

GENERATIONS = 60
P_DROP = 0.08
P_DUP = 0.04
SEEDS = range(200)

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}

ROOTING_SEEDS = {"handoff": 1, "flat": 2, "no_repeats": 6}


def run_history(words, seed, p_drop, p_dup):
    rng = random.Random(seed)
    words = list(words)
    history = [list(words)]
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
        history.append(list(words))
        if not words or len(words) > 4000:
            break
    return history


def winner_trajectory(history):
    final = history[-1]
    if not final:
        return None
    counts_final = Counter(final)
    winner, wcount = counts_final.most_common(1)[0]
    if wcount / len(final) <= 0.5:
        return None
    traj = [Counter(gen).get(winner, 0) for gen in history]
    return winner, traj


def whole_run_retreats(traj):
    end = len(traj)
    while end > 1 and traj[end - 1] == 0:
        end -= 1
    seg = traj[:end]
    if len(seg) < 4:
        return None
    retreats = sum(1 for i in range(1, len(seg)) if seg[i] < seg[i - 1])
    return retreats, len(seg) - 1


def rate_for_seed(words, seed):
    history = run_history(words, seed, P_DROP, P_DUP)
    wt = winner_trajectory(history)
    if wt is None:
        return None
    _, traj = wt
    wr = whole_run_retreats(traj)
    if wr is None:
        return None
    retreats, steps = wr
    return retreats / steps if steps else None


def distribution(words):
    rates = []
    for seed in SEEDS:
        r = rate_for_seed(words, seed)
        if r is not None:
            rates.append(r)
    return sorted(rates)


def percentile(sorted_rates, value):
    n = len(sorted_rates)
    below = sum(1 for r in sorted_rates if r < value)
    return below / n


def main():
    for name, text in ORIGINS.items():
        words = text.split()
        rooting_seed = ROOTING_SEEDS[name]
        rooting_rate = rate_for_seed(words, rooting_seed)
        dist = distribution(words)
        mean_rate = sum(dist) / len(dist)
        pct = percentile(dist, rooting_rate) if rooting_rate is not None else None
        print(
            f"{name:12s} rooting seed={rooting_seed} retreat_rate={rooting_rate:.3f} "
            f"| distribution: n={len(dist)} mean={mean_rate:.3f} "
            f"| rooting seed sits at percentile {pct:.2f}"
        )


if __name__ == "__main__":
    main()
