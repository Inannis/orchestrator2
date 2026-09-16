"""
009-clearing — session 7. Tests the one live guess 008 left open: *why*
does higher population mean more retreat texture (008: 1x retreat rate
0.08-0.10, 10x: 0.24-0.36, opposite of the small-N-noise prediction)?

008's untested guess: at higher population, a near-extinct rival word
takes longer (in generations) to actually hit exactly zero, because
there's more of it to whittle down. So the "field" stays contested for
longer relative to the run, giving the eventual winner more chances at a
temporary reversal before rivals are fully cleared.

This makes a specific, checkable claim: relative time-to-clear-rivals
(generation rivals hit zero, divided by how long the run takes to
stabilize) should be larger at 10x than at 1x, and — within a scale — runs
with a later relative clearing time should have more retreat.

Method: same mechanic and same three texts as 007/008 (independent
per-word drop/dup, p_drop=0.08, p_dup=0.04). For each of 200 seeds per
text per scale, keep only "runaway" runs (008's definition: final
non-empty, winner share > 0.5). For each:
  - stabilize_gen: first generation after which the state never changes
    again (population size and composition frozen) or GENERATIONS if it
    never stabilizes.
  - clear_gen: first generation at which every non-winner word is gone
    (0 if the winner already had the field alone at gen 0).
  - relative_clear = clear_gen / stabilize_gen (0 if stabilize_gen is 0,
    i.e. degenerate single-word text).
  - retreat_rate: whole_run_retreats from 008, unchanged.

Then: (a) compare mean relative_clear at 1x vs 10x — the guess predicts
10x should be higher; (b) within each scale, correlate relative_clear
with retreat_rate across runs — the guess predicts a positive
relationship (later clearing -> more retreat chances -> higher rate).
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


def stabilize_gen(history):
    """First generation g such that history[g] == history[g+1] == ... to
    the end (composition, as a multiset, frozen). Returns len(history)-1
    if it never stabilizes before the run ends."""
    last = len(history) - 1
    frozen = Counter(history[last])
    g = last
    while g > 0 and Counter(history[g - 1]) == frozen:
        g -= 1
    return g


def clear_gen(history, winner):
    """First generation at which every word except `winner` is gone."""
    for g, gen in enumerate(history):
        c = Counter(gen)
        rivals = sum(v for w, v in c.items() if w != winner)
        if rivals == 0:
            return g
    return len(history) - 1


def scaled_words(words, factor):
    out = []
    for w in words:
        out.extend([w] * factor)
    return out


def study(factor):
    per_text = {}
    for name, text in ORIGINS.items():
        base_words = text.split()
        words = scaled_words(base_words, factor)
        rows = []
        for seed in SEEDS:
            history = run_history(words, seed, P_DROP, P_DUP)
            wt = winner_trajectory(history)
            if wt is None:
                continue
            winner, traj = wt
            wr = whole_run_retreats(traj)
            if wr is None:
                continue
            retreats, steps = wr
            if steps == 0:
                continue
            rate = retreats / steps
            sg = stabilize_gen(history)
            cg = clear_gen(history, winner)
            rel_clear = cg / sg if sg > 0 else 0.0
            rows.append((rel_clear, rate, sg, cg))
        per_text[name] = rows
    return per_text


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return cov / (vx * vy) ** 0.5


def main():
    for factor in (1, 10):
        print(f"=== population scale {factor}x ===")
        per_text = study(factor)
        for name, rows in per_text.items():
            n = len(rows)
            mean_rel_clear = sum(r[0] for r in rows) / n
            mean_rate = sum(r[1] for r in rows) / n
            corr = pearson([r[0] for r in rows], [r[1] for r in rows])
            print(
                f"{name:12s} n={n:3d} mean_rel_clear={mean_rel_clear:.3f} "
                f"mean_retreat_rate={mean_rate:.3f} corr(rel_clear,retreat)={corr}"
            )
        print()


if __name__ == "__main__":
    main()
