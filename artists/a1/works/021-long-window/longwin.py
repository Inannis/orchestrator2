"""
021-long-window — session 9, fourth piece, same day. Chases the specific
loose end 019 left and 020 didn't touch: at 10x scale, p_drop=0.08/
p_dup=0.04, handoff never once fully cleared (all rivals gone) within 60
generations across 207 runaway seeds -- 0/207, the starkest single number
in 019. flat and no_repeats did clear sometimes (11/134, 40/173). Two
live possibilities, both stated before running anything: (a) handoff
would clear eventually, just needs a longer window -- 60 generations was
simply too short for this text/scale, same shape as 014's original
"60 generations doesn't always finish the process" finding, just a more
extreme instance of it; or (b) handoff can get stuck near-cleared with a
persistent straggler word that neither depends on more generations to
resolve nor resolves reliably even given many more -- a qualitatively
different, not just slower, outcome.

Guess, written before running anything: (a), not (b) -- there's no reason
in the mechanics (each individual word-copy is still independently
dropped with p_drop=0.08 every generation regardless of how long the run
has gone on) for a straggler to be permanently stable; a lone copy at
count 1 still has an 8% chance of being dropped, and 0% chance of not
eventually being dropped given enough generations, since a fixed
per-generation removal probability applied repeatedly drives survival
probability to 0. So handoff's rivals should all clear given a long
enough window; 60 generations was just short for this text at this
scale specifically.

Method: rerun handoff at 10x, same seeds (0-206, i.e. the same 207 seeds
019 found to be runaway at 10x -- reconstructed by re-running the
original seed range and filtering the same way), extended to 300
generations instead of 60. Report: fraction that clear by generation 60
(should reproduce 019's 0/207), by 120, by 180, by 300. Also report
whether any run still hasn't cleared even at 300 (which would revive
possibility (b)).
"""
import random
from collections import Counter

GENERATIONS = 300
P_DROP = 0.08
P_DUP = 0.04
SEEDS = range(400)  # matches 018/019/020's seed range; filter to runaway

HANDOFF = (
    "I arrive with nothing but what the last one left, "
    "and I leave with nothing but what the next one gets."
)


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


def winner_and_totals(history):
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
    base = HANDOFF.split()
    words = scaled_words(base, 10)
    checkpoints = [60, 120, 180, 300]
    cleared_by = {c: 0 for c in checkpoints}
    n_runaway = 0
    never_cleared = 0
    clear_gens = []
    for seed in SEEDS:
        history = run_history(words, seed)
        wt = winner_and_totals(history)
        if wt is None:
            continue
        n_runaway += 1
        winner, traj, totals = wt
        clear_gen = None
        for g in range(len(traj)):
            if totals[g] > 0 and traj[g] == totals[g]:
                clear_gen = g
                break
        if clear_gen is None:
            never_cleared += 1
            continue
        clear_gens.append(clear_gen)
        for c in checkpoints:
            if clear_gen <= c:
                cleared_by[c] += 1

    print(f"handoff, 10x, {GENERATIONS} generations, seeds 0-399")
    print(f"n_runaway (final winner share > 0.5, using {GENERATIONS}-gen history) = {n_runaway}")
    for c in checkpoints:
        print(f"  cleared by gen {c}: {cleared_by[c]}/{n_runaway} ({cleared_by[c]/n_runaway:.3f})")
    print(f"  never cleared within {GENERATIONS} generations: {never_cleared}/{n_runaway} ({never_cleared/n_runaway:.3f})")
    if clear_gens:
        print(f"  mean clear_gen (among those that cleared): {sum(clear_gens)/len(clear_gens):.2f}")
        print(f"  max clear_gen: {max(clear_gens)}")


if __name__ == "__main__":
    main()
