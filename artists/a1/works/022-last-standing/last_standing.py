"""
022-last-standing — session 9, fifth piece, same day. Direct response to
021's own top-priority item: does 013's fixation-probability-equals-
initial-frequency match survive once 021's finding (this process is a
subcritical branching process, total population dies with probability 1
given enough time) is taken seriously, or does the whole question stop
being well-posed?

013 measured: whenever the population was nonempty at generation 60,
which word was most common, and compared that word's win frequency to
its starting frequency. Found a close match, borrowed Kimura's neutral-
drift theory (fixation probability = initial frequency) as the reason
why. But Kimura's theorem describes a *constant-size* process (Wright-
Fisher), where the population never goes extinct, only one type does or
doesn't take over the others. This process is not constant-size — 021
found it's subcritical, so "population survives to generation 60 with
one word dominant" was never heading toward permanent fixation, it was a
snapshot mid-collapse.

The guess (written before running anything): there is a well-posed
question that survives 021's correction, using a different event than
"who's ahead at a fixed generation." Since every individual's dynamics
are independent and identical regardless of word identity, and the whole
population eventually goes extinct with probability 1, there is a
well-defined event — "which word type is the last to have zero
survivors" (the last-standing type, i.e. whichever word's lineage outlives
every other word's lineage) — that doesn't depend on an arbitrary
generation cutoff at all. By the same exchangeability argument Kimura's
theorem rests on (each individual is interchangeable with any other,
differing only in which word it happens to be), the guess is that
P(word W is last-standing) = W's starting frequency, exactly as 013 found
for "winner at generation 60" — except this version is a real, well-posed
endpoint instead of a snapshot, and should hold arbitrarily well (given
enough seeds) rather than needing a "long enough window" caveat, since
extinction happens with probability 1 in finite (though unbounded) time.

Method: run each text at 1x scale (small population, fast extinction),
p_drop=0.08/p_dup=0.04 (this studio's most-used point), up to MAX_GEN
generations or until the whole population is extinct, whichever comes
first. Record the last word type to have any survivors (the word present
at the last nonempty generation) -- if multiple words are tied at the
very last nonempty generation, that run is excluded (ambiguous "last
standing", small-population tie). Compare each word's last-standing win
frequency to its starting frequency, same table format 013 used.
"""
import random
from collections import Counter

MAX_GEN = 1500
P_DROP = 0.08
P_DUP = 0.04
SEEDS = range(3000)

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}


def run_to_extinction(words, seed):
    rng = random.Random(seed)
    words = list(words)
    last_nonempty = list(words)
    for gen in range(MAX_GEN):
        out = []
        for w in words:
            r = rng.random()
            if r < P_DROP:
                continue
            out.append(w)
            if P_DROP <= r < P_DROP + P_DUP:
                out.append(w)
        words = out
        if not words:
            return last_nonempty, True  # extinct, last nonempty state
        last_nonempty = words
    return last_nonempty, False  # hit MAX_GEN still alive


def main():
    for name, text in ORIGINS.items():
        base = text.split()
        start_counts = Counter(base)
        total = len(base)
        start_freq = {w: c / total for w, c in start_counts.items()}

        wins = Counter()
        n_extinct = 0
        n_timeout = 0
        n_tied = 0
        for seed in SEEDS:
            last_state, extinct = run_to_extinction(base, seed)
            if extinct:
                n_extinct += 1
            else:
                n_timeout += 1
                continue  # didn't reach a well-defined last-standing event
            c = Counter(last_state)
            top = c.most_common()
            if len(top) > 1 and top[0][1] == top[1][1]:
                n_tied += 1
                continue
            winner = top[0][0]
            wins[winner] += 1

        n_decided = sum(wins.values())
        print(f"=== {name} (start counts: {dict(start_counts)}) ===")
        print(f"  extinct={n_extinct}/{len(SEEDS)}  timeout(>{MAX_GEN} gens, still alive)={n_timeout}  tied_last_gen={n_tied}  decided={n_decided}")
        print(f"  {'word':>12} {'start_freq':>11} {'win_freq':>9}")
        for w in sorted(start_freq, key=lambda w: -start_freq[w]):
            wf = wins.get(w, 0) / n_decided if n_decided else float("nan")
            print(f"  {w:>12} {start_freq[w]:>11.4f} {wf:>9.4f}")
        print()


if __name__ == "__main__":
    main()
