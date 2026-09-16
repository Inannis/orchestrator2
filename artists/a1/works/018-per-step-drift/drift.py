"""
018-per-step-drift — session 9. Names and tests an actual candidate for
thread (5), left open since 009: *why* does retreat rate (fraction of
generation-steps where the eventual winner's count drops) rise with
population (008: 1x 0.08-0.10, 10x 0.24-0.36)? 009 killed the only guess
on record (relative clearing time) as a mechanism. No replacement guess
has existed until now.

The guess, made before running anything below:

Each word's count evolves independently, individual by individual: each
copy is dropped with p_drop, duplicated with p_dup, else kept. This is a
branching process. For a word at count c, the expected next-step change
scales with c (drift ~ c), but the standard deviation of the change scales
with sqrt(c) (binomial-like noise). So the *signal-to-noise ratio* of the
step, drift/noise, scales like sqrt(c) — bigger counts should make each
individual step *more* deterministic, not less. That predicts, per step,
P(decrease | current count c) should *fall* as c grows.

If that's right, then 008's finding (more retreat at 10x) can't be
explained by "each step is noisier at higher population" — the opposite
should be true, step by step. The candidate replacement mechanism: what
scales with population isn't per-step noise, it's the *number of steps*
the climb takes before the winner locks in (population genetics: fixation
time grows with population size, already established for a different
purpose in 014). More steps, even at a lower or equal per-step retreat
probability, can still add up to a higher total retreat rate over the
climb.

Two checks, in order:
(1) Does P(decrease | count c) actually fall as c rises, pooling every
    single-generation step from every trajectory, both scales, all texts?
    (Tests the LLN half of the guess directly, the part 008/009 never
    measured at all.)
(2) Does climb length (generations to first peak) rise from 1x to 10x,
    and does multiplying (mean per-step retreat probability along the
    climb) x (climb length) reproduce something close to the actual
    measured retreat rate at each scale? (Tests whether "more steps"
    alone is sufight to explain 008's finding without any change in
    per-step noise character.)
"""
import random
from collections import Counter, defaultdict

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


def winner_trajectory(history):
    final = history[-1]
    if not final:
        return None
    counts_final = Counter(final)
    winner, wcount = counts_final.most_common(1)[0]
    if wcount / len(final) <= 0.5:
        return None
    traj = [Counter(gen).get(winner, 0) for gen in history]
    return traj


def scaled_words(words, factor):
    out = []
    for w in words:
        out.extend([w] * factor)
    return out


def climb(traj):
    """trajectory truncated to first generation it reaches its own
    eventual peak. Returns list of counts, len >= 1."""
    peak = max(traj)
    first_peak_gen = traj.index(peak)
    return traj[: first_peak_gen + 1]


def main():
    # --- Check 1: P(decrease | count c), pooled across everything -----
    # bucket by count on a log-ish scale so both 1x (small counts) and
    # 10x (large counts) contribute readable bins
    bucket_total = defaultdict(int)
    bucket_decrease = defaultdict(int)

    def bucket_of(c):
        if c <= 0:
            return None
        # log2 buckets: 1, 2, 4, 8, 16, 32, 64, 128, 256+
        b = 0
        while (1 << (b + 1)) <= c:
            b += 1
        return 1 << b  # bucket label = power-of-two floor

    climb_lengths = {1: defaultdict(list), 10: defaultdict(list)}
    climb_mean_retreat = {1: defaultdict(list), 10: defaultdict(list)}
    whole_retreat_rate = {1: defaultdict(list), 10: defaultdict(list)}

    for factor in (1, 10):
        for name, text in ORIGINS.items():
            base = text.split()
            words = scaled_words(base, factor)
            for seed in SEEDS:
                history = run_history(words, seed)
                traj = winner_trajectory(history)
                if traj is None:
                    continue
                cl = climb(traj)
                # per-step bucketed decrease stats, over the whole
                # trajectory (not just climb) -- more data, and the
                # guess is about the general step relationship, not
                # climb-only
                n_dec_climb = 0
                for i in range(1, len(cl)):
                    prev = cl[i - 1]
                    b = bucket_of(prev)
                    if b is None:
                        continue
                    bucket_total[b] += 1
                    if cl[i] < prev:
                        bucket_decrease[b] += 1
                        n_dec_climb += 1
                if len(cl) > 1:
                    climb_lengths[factor][name].append(len(cl) - 1)
                    climb_mean_retreat[factor][name].append(
                        n_dec_climb / (len(cl) - 1)
                    )
                # whole-run retreat rate (008/009 definition) for
                # cross-check against known numbers
                end = len(traj)
                while end > 1 and traj[end - 1] == 0:
                    end -= 1
                seg = traj[:end]
                if len(seg) >= 4:
                    r = sum(
                        1 for i in range(1, len(seg)) if seg[i] < seg[i - 1]
                    )
                    whole_retreat_rate[factor][name].append(r / (len(seg) - 1))

    print("=== Check 1: P(decrease | count bucket), pooled ===")
    print(f"{'bucket>=':>10} {'n_steps':>10} {'p_decrease':>12}")
    for b in sorted(bucket_total):
        n = bucket_total[b]
        if n < 30:
            continue
        p = bucket_decrease[b] / n
        print(f"{b:>10} {n:>10} {p:>12.4f}")

    print()
    print("=== Check 2: climb length and retreat rate by scale ===")
    for name in ORIGINS:
        print(f"-- {name} --")
        for factor in (1, 10):
            lens = climb_lengths[factor][name]
            rr_climb = climb_mean_retreat[factor][name]
            rr_whole = whole_retreat_rate[factor][name]
            if not lens:
                print(f"  {factor}x: no runaway runs")
                continue
            mean_len = sum(lens) / len(lens)
            mean_rr_climb = sum(rr_climb) / len(rr_climb)
            mean_rr_whole = sum(rr_whole) / len(rr_whole) if rr_whole else float("nan")
            print(
                f"  {factor}x: n={len(lens):4d}  mean_climb_len={mean_len:6.2f}  "
                f"mean_per_step_p_decrease(climb)={mean_rr_climb:.4f}  "
                f"whole_run_retreat_rate={mean_rr_whole:.4f}"
            )


if __name__ == "__main__":
    main()
