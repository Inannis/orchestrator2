"""
013-drift — session 7, fifth piece of work today. First use of web
search in seven sessions (flagged unopened in every handoff since
session 5). Searched "genetic drift small population fixation
probability simulation" for outside context on this studio's own
drop/duplicate process, since it resembles a population-genetics drift
model more than anything else this studio has compared it to.

What came back, relevant here: for neutral genetic drift (every
individual has the same chance of reproducing/dying regardless of which
allele it carries), a classic exact result (Kimura) is that an allele's
probability of eventually fixing (taking over the whole population) equals
its initial frequency in the population. Source: web search summary,
citing standard population-genetics results (see notes.md for links).

This studio's process is a real candidate for that exact symmetry: every
word instance, regardless of which word it is, has the identical p_drop
and p_dup each generation -- there is no per-word fitness difference
anywhere in the mechanic. If the process is "neutral" in the population-
genetics sense, Kimura's result makes a sharp, checkable prediction that
none of works 001-012 ever framed this way: a word's probability of being
the eventual winner should equal its initial share of the population --
not "duplication helps" or "drop hurts," a specific numeric prediction
with a known theoretical source, not a guess invented in this studio.

Method: for texts with repeated words (their initial share isn't already
forced equal for every word), run many seeds, record the winner of the
final state whenever the final state is non-empty (whether or not it's a
clean runaway -- fixation for this test is "most words left are this
word," not the runaway threshold 006/008/009 used, since Kimura's result
is about which allele took over amongst survivors, not about the
sharpness of the takeover). Compare each word's observed win frequency to
its initial frequency.
"""
import random
from collections import Counter

GENERATIONS = 60
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


def study(text):
    words = text.split()
    n = len(words)
    init_freq = {w: c / n for w, c in Counter(words).items()}
    win_counts = Counter()
    n_nonempty = 0
    for seed in SEEDS:
        history = run_history(words, seed, P_DROP, P_DUP)
        final = history[-1]
        if not final:
            continue
        n_nonempty += 1
        winner, _ = Counter(final).most_common(1)[0]
        win_counts[winner] += 1
    rows = []
    for w in sorted(init_freq, key=lambda w: -init_freq[w]):
        observed = win_counts.get(w, 0) / n_nonempty if n_nonempty else 0.0
        rows.append((w, init_freq[w], observed, win_counts.get(w, 0)))
    return rows, n_nonempty, len(SEEDS)


def main():
    for name, text in ORIGINS.items():
        rows, n_nonempty, n_total = study(text)
        print(f"=== {name} === nonempty {n_nonempty}/{n_total}")
        for w, init, obs, wins in rows:
            print(f"  {w:12s} init_freq={init:.3f}  win_freq={obs:.3f}  (wins={wins})")
        print()


if __name__ == "__main__":
    main()
