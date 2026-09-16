"""
020-tail-retreat — session 9, third piece, same day. Directly checks the
concrete next step both 018 and 019 pointed at: 008/009's "whole_run_
retreat_rate" (fraction of generation-steps where the eventual winner's
count drops, measured across the *entire* trajectory) rises sharply with
population (1x ~0.08-0.10, 10x ~0.24-0.36). 018 measured retreat only
during the climb-to-peak segment and found the per-step rate there also
rises with population, but 019 showed peak and full clearing are
different events, with a long tail after peak (often exceeding this
simulation's 60-generation window at 10x) that neither 018's climb
measure nor a simple peak-based split has actually isolated and compared
against the pre-peak segment on its own.

Guess, written before running anything: most of the *increase* in
whole-run retreat rate from 1x to 10x is concentrated in the post-peak
tail, not the pre-peak climb — because the tail is where 019 found the
population effect is most extreme (peak reached fast either way, but the
tail balloons at 10x), so if there's more opportunity for retreat
anywhere, it should be there. Specifically: splitting whole-run retreat
into a pre-peak-segment rate and a post-peak-segment rate, the *gap*
between 1x and 10x should be larger in the post-peak segment than in the
pre-peak segment.

Method: reuse 018/019's exact run/trajectory code, same p_drop/p_dup
point, same three texts, same runaway filter, 400 seeds/text/scale. For
every runaway run, split the (zero-trimmed) trajectory at its own peak
generation into pre-peak (inclusive of peak) and post-peak (peak to end)
segments, and compute retreat rate (fraction of steps where count drops)
separately for each segment, at both scales.
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


def winner_traj(history):
    final = history[-1]
    if not final:
        return None
    counts_final = Counter(final)
    winner, wcount = counts_final.most_common(1)[0]
    if wcount / len(final) <= 0.5:
        return None
    return [Counter(gen).get(winner, 0) for gen in history]


def scaled_words(words, factor):
    out = []
    for w in words:
        out.extend([w] * factor)
    return out


def retreat_rate(seg):
    if len(seg) < 2:
        return None
    r = sum(1 for i in range(1, len(seg)) if seg[i] < seg[i - 1])
    return r / (len(seg) - 1)


def main():
    results = {}
    for factor in (1, 10):
        results[factor] = {}
        for name, text in ORIGINS.items():
            base = text.split()
            words = scaled_words(base, factor)
            pre_rates, post_rates, whole_rates = [], [], []
            n = 0
            for seed in SEEDS:
                history = run_history(words, seed)
                traj = winner_traj(history)
                if traj is None:
                    continue
                # trim trailing zeros (shouldn't occur given filter, but safe)
                end = len(traj)
                while end > 1 and traj[end - 1] == 0:
                    end -= 1
                seg = traj[:end]
                if len(seg) < 4:
                    continue
                n += 1
                peak = max(seg)
                peak_gen = seg.index(peak)
                pre = seg[: peak_gen + 1]
                post = seg[peak_gen:]
                pr = retreat_rate(pre)
                po = retreat_rate(post)
                wr = retreat_rate(seg)
                if pr is not None:
                    pre_rates.append(pr)
                if po is not None:
                    post_rates.append(po)
                if wr is not None:
                    whole_rates.append(wr)
            results[factor][name] = {
                "n": n,
                "pre": sum(pre_rates) / len(pre_rates) if pre_rates else float("nan"),
                "post": sum(post_rates) / len(post_rates) if post_rates else float("nan"),
                "whole": sum(whole_rates) / len(whole_rates) if whole_rates else float("nan"),
                "n_pre": len(pre_rates),
                "n_post": len(post_rates),
            }

    print(f"{'text':>12} {'scale':>6} {'n':>5} {'pre_rate':>9} {'post_rate':>10} {'whole_rate':>11}")
    for name in ORIGINS:
        for factor in (1, 10):
            r = results[factor][name]
            print(
                f"{name:>12} {factor:>5}x {r['n']:>5} {r['pre']:>9.4f} {r['post']:>10.4f} {r['whole']:>11.4f}"
            )
        gap_pre = results[10][name]["pre"] - results[1][name]["pre"]
        gap_post = results[10][name]["post"] - results[1][name]["post"]
        print(f"    -> gap(10x-1x): pre={gap_pre:+.4f}  post={gap_post:+.4f}")


if __name__ == "__main__":
    main()
