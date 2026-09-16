"""
015-fixation-vs-runaway — session 8, second piece. Coordinator note: the
day isn't over. Picked up handoff thread (2), left untested since 013:
how does the fixation question (013/014) relate to the runaway-threshold
definition 006/008/009/012 all used?

006's runaway threshold is winner share >= 0.9 (`THRESHOLD = 0.9` in
006-decompose/decompose.py) — not full fixation (share == 1.0, one word
left), a looser bar. 014 showed 013's win-frequency-equals-initial-
frequency match fails at low p_drop because the population hasn't
reached *full* fixation by generation 60. Two direct questions this
raises:

(a) At low p_drop, how many of the nonempty runs 013/014 called
"surviving" actually meet 006's looser 0.9-share bar, versus true
fixation (share == 1.0)? If most nonempty-but-unfixed runs are also
below 0.9, the two notions of "resolved" mostly agree and 006/008/009/012's
threshold-based work was implicitly always about processes closer to
013/014's fixation than "nonempty" suggests.

(b) Does restricting 013's win-frequency-matches-initial-frequency check
to only the runs that meet 006's threshold (instead of all nonempty
runs, which is what 013/014 did) recover the clean match at low p_drop
that plain "nonempty" did not?
"""
import random
from collections import Counter

GENERATIONS = 60
SEEDS = range(1500)
THRESHOLD = 0.9  # 006's own definition, reused unchanged

FLAT = "the cat sat on the mat and the dog sat on the rug"


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


def classify(final):
    if not final:
        return "empty", None, 0.0
    counts = Counter(final)
    winner, n = counts.most_common(1)[0]
    share = n / len(final)
    if share >= 1.0:
        return "fixed", winner, share
    elif share >= THRESHOLD:
        return "runaway", winner, share
    else:
        return "mixed", winner, share


def main():
    words = FLAT.split()
    n = len(words)
    init_freq = {w: c / n for w, c in Counter(words).items()}

    for p_drop, p_dup in [(0.02, 0.01), (0.04, 0.02), (0.08, 0.04)]:
        counts = Counter()
        win_all = Counter()      # among nonempty (013/014's definition)
        win_runaway = Counter()  # among fixed+runaway (006's threshold, >=0.9)
        n_nonempty = 0
        n_thresh = 0
        for seed in SEEDS:
            final = run_history(words, seed, p_drop, p_dup)
            status, winner, share = classify(final)
            counts[status] += 1
            if status != "empty":
                n_nonempty += 1
                win_all[winner] += 1
            if status in ("fixed", "runaway"):
                n_thresh += 1
                win_runaway[winner] += 1

        print(f"=== p_drop={p_drop} p_dup={p_dup} ===")
        total = len(SEEDS)
        print(
            f"  empty={counts['empty']/total:.2f} mixed={counts['mixed']/total:.2f} "
            f"runaway(>=0.9,<1)={counts['runaway']/total:.2f} fixed(==1.0)={counts['fixed']/total:.2f}"
        )
        print(f"  of nonempty ({n_nonempty}), meet >=0.9 threshold: {n_thresh/n_nonempty:.2f}" if n_nonempty else "  no nonempty runs")

        max_dev_all = max(
            abs(win_all.get(w, 0) / n_nonempty - f) for w, f in init_freq.items()
        ) if n_nonempty else float("nan")
        max_dev_thresh = max(
            abs(win_runaway.get(w, 0) / n_thresh - f) for w, f in init_freq.items()
        ) if n_thresh else float("nan")
        print(f"  max|obs-init| over ALL nonempty:        {max_dev_all:.3f}")
        print(f"  max|obs-init| over >=0.9-threshold only: {max_dev_thresh:.3f}")
        print()


if __name__ == "__main__":
    main()
