"""
019-peak-vs-fixation — session 9, second piece. Tests the question 018
surfaced but didn't chase: 018 measured "climb length" as generations to
the winner's own first peak count, and found it *shrinks* at 10x scale
(29 -> 8 gens roughly). 013/014 used a different notion, "time to
fixation" (population genetics: when the drifting allele takes over
completely), and found fixation takes *longer*, in generations, at lower
p_drop — the studio has never directly checked whether "reach your own
peak count" and "clear out every rival" are even close to the same event
in this process, or whether they're two different things that happened to
both move with p_drop/population in 013/014's work without anyone
checking they're the same event.

Guess, written before running anything: they are NOT the same event, and
that's *why* 018's climb-length result looked backwards relative to
fixation-time intuition. Specifically: "first peak" can happen while
rivals still exist (the winner keeps growing after because rivals are
still shrinking, so total dips below peak temporarily even while the
winner is still going to fully take over) OR peak can happen at the exact
moment of clearing (no more losses to offset). If peak routinely happens
*before* clearing, "climb length" is measuring something upstream of
fixation, not fixation itself, and the two are only loosely related.

Method: reuse 018's run/winner_trajectory machinery. For every runaway
run (both scales, all three texts, same p_drop=0.08/p_dup=0.04 point as
006-018), find: peak_gen (018's climb-length event), clear_gen (first
generation all non-winner words are gone — 009's definition). Compare
directly: what fraction of runs have peak_gen < clear_gen (peak reached
strictly before rivals cleared)? What's the mean gap (clear_gen -
peak_gen)? Does this relationship change between 1x and 10x scale (the
guess predicts scale shouldn't matter much to *whether* peak precedes
clearing, since it's about the shape of individual trajectories, not
population size directly)?
"""
import random
from collections import Counter

GENERATIONS = 60
P_DROP = 0.08
P_DUP = 0.04
SEEDS = range(400)

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}


def run_history(words, seed):
    rng = random.Random(seed)
    words = list(words)
    history = [list(words)]
    for gen in range(GENERATIONS):
        out = []
        for w in words:
            r = rng.random()
            if r < P_DROP:
                continue
            out.append(w)
            if P_DROP <= r < P_DROP + P_DUP:
                out.append(w)
        words = out
        history.append(list(words))
        if not words or len(words) > 40000:
            break
    return history


def winner_and_traj(history):
    final = history[-1]
    if not final:
        return None
    counts_final = Counter(final)
    winner, wcount = counts_final.most_common(1)[0]
    if wcount / len(final) <= 0.5:
        return None
    traj = [Counter(gen).get(winner, 0) for gen in history]
    totals = [len(gen) for gen in history]
    return winner, traj, totals


def scaled_words(words, factor):
    out = []
    for w in words:
        out.extend([w] * factor)
    return out


def main():
    for factor in (1, 10):
        print(f"=== scale {factor}x ===")
        for name, text in ORIGINS.items():
            base = text.split()
            words = scaled_words(base, factor)
            n_runaway = 0
            n_peak_before_clear = 0
            n_peak_at_clear = 0
            n_peak_after_clear = 0
            gaps = []
            for seed in SEEDS:
                history = run_history(words, seed)
                wt = winner_and_traj(history)
                if wt is None:
                    continue
                winner, traj, totals = wt
                n_runaway += 1
                peak = max(traj)
                peak_gen = traj.index(peak)
                # clear_gen: first generation where winner count == total
                # count (every rival gone)
                clear_gen = None
                for g in range(len(traj)):
                    if traj[g] == totals[g] and totals[g] > 0:
                        clear_gen = g
                        break
                if clear_gen is None:
                    continue  # never fully cleared within window
                gap = clear_gen - peak_gen
                gaps.append(gap)
                if peak_gen < clear_gen:
                    n_peak_before_clear += 1
                elif peak_gen == clear_gen:
                    n_peak_at_clear += 1
                else:
                    n_peak_after_clear += 1
            n_measured = len(gaps)
            if n_measured == 0:
                print(f"  {name}: no measurable runs")
                continue
            mean_gap = sum(gaps) / n_measured
            print(
                f"  {name}: n_runaway={n_runaway} n_cleared_in_window={n_measured}  "
                f"peak_before_clear={n_peak_before_clear/n_measured:.3f}  "
                f"peak_at_clear={n_peak_at_clear/n_measured:.3f}  "
                f"peak_after_clear={n_peak_after_clear/n_measured:.3f}  "
                f"mean_gap(clear-peak)={mean_gap:.2f}"
            )


if __name__ == "__main__":
    main()
