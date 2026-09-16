"""
008-texture — session 6. Tests the live thread from 007-see: the "noisy
top, jagged resolution, retreats and recoveries" texture seen in three
cherry-picked trajectory images — is it a real dynamic, or an artifact of
small population size (007 ran on 8-12 word texts, so counts are tiny and
any single drop/dup event swings the picture a lot)?

Method: same generation mechanic as 007's trajectory.py (independent
per-word drop/dup each generation). Run it at two population scales on the
same three texts: 1x (original word count, matches 007) and 10x (each
word replicated 10 times at the start, so ~10x the population, same
word *ratios*). For each run that survives non-empty and concentrates
(winner's final share > 0.5 — matches 006's "runaway" definition), take
the winner's count trajectory and measure how often it drops from one
generation to the next *before* it first reaches its own eventual peak
value — that's the "climb" phase, where a monotonic climb would have zero
drops. If the small-population-noise hypothesis is right, retreat
frequency during the climb should fall substantially from 1x to 10x. If
it's a real dynamic (e.g. genuine local reversals independent of scale),
it should stay roughly similar.

200 seeds per text per scale, same p_drop=0.08, p_dup=0.04 region 006 and
007 both used.
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
        if not words or len(words) > 20000:
            break
    return history


def winner_trajectory(history, orig_words):
    """Return (winner_word, [count per gen]) or None if not runaway
    (empty at end, or final winner share <= 0.5)."""
    final = history[-1]
    if not final:
        return None
    counts_final = Counter(final)
    winner, wcount = counts_final.most_common(1)[0]
    if wcount / len(final) <= 0.5:
        return None
    traj = [Counter(gen).get(winner, 0) for gen in history]
    return winner, traj


def climb_retreats(traj):
    """Fraction of steps, up to and including the first generation the
    trajectory reaches its own eventual max, where count dropped from the
    previous generation. Returns (n_retreats, n_climb_steps) or None if
    climb is too short to be meaningful (<3 steps)."""
    peak = max(traj)
    first_peak_gen = traj.index(peak)
    if first_peak_gen < 3:
        return None
    climb = traj[: first_peak_gen + 1]
    retreats = sum(1 for i in range(1, len(climb)) if climb[i] < climb[i - 1])
    return retreats, len(climb) - 1


def whole_run_retreats(traj):
    """Fraction of steps across the *entire* trajectory (not just the
    climb to first peak) where count dropped from the previous
    generation, restricted to generations before the winner's count hits
    zero (if it ever does -- it needn't, since we already required final
    share > 0.5). Avoids climb_retreats' bias: at larger populations the
    winner can reach its eventual peak in 1-2 generations, which starved
    climb_retreats of measurable runs (n_climb_steps < 3) rather than
    showing anything about texture."""
    # trim trailing generations once the word is extinct (shouldn't
    # happen given the runaway filter, but be safe)
    end = len(traj)
    while end > 1 and traj[end - 1] == 0:
        end -= 1
    seg = traj[:end]
    if len(seg) < 4:
        return None
    retreats = sum(1 for i in range(1, len(seg)) if seg[i] < seg[i - 1])
    return retreats, len(seg) - 1


def scaled_words(words, factor):
    out = []
    for w in words:
        out.extend([w] * factor)
    return out


def study(factor):
    results = {}
    for name, text in ORIGINS.items():
        base_words = text.split()
        words = scaled_words(base_words, factor)
        rates = []
        whole_rates = []
        n_runaway = 0
        n_total = 0
        for seed in SEEDS:
            n_total += 1
            history = run_history(words, seed, P_DROP, P_DUP)
            wt = winner_trajectory(history, base_words)
            if wt is None:
                continue
            n_runaway += 1
            _, traj = wt
            cr = climb_retreats(traj)
            wr = whole_run_retreats(traj)
            if cr is not None:
                retreats, steps = cr
                if steps > 0:
                    rates.append(retreats / steps)
            if wr is not None:
                retreats, steps = wr
                if steps > 0:
                    whole_rates.append(retreats / steps)
        results[name] = {
            "n_total": n_total,
            "n_runaway": n_runaway,
            "n_measured_climb": len(rates),
            "mean_retreat_rate_climb": sum(rates) / len(rates) if rates else None,
            "n_measured_whole": len(whole_rates),
            "mean_retreat_rate_whole": sum(whole_rates) / len(whole_rates) if whole_rates else None,
        }
    return results


def main():
    for factor in (1, 10):
        print(f"=== population scale {factor}x (start size ~{factor * 8}-{factor * 12} words) ===")
        results = study(factor)
        for name, r in results.items():
            print(
                f"{name:12s} runaway {r['n_runaway']:3d}/{r['n_total']} "
                f"climb: measured {r['n_measured_climb']:3d} rate={r['mean_retreat_rate_climb']} | "
                f"whole: measured {r['n_measured_whole']:3d} rate={r['mean_retreat_rate_whole']}"
            )
        print()


if __name__ == "__main__":
    main()
