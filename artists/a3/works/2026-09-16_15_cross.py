"""
Crossing the studio's two methods on purpose, per the open question
from earlier today: pull-from-origin (radial -- free near a "home",
mechanical/rigid far from it, used for the walk, the field, and both
erasures) and copy-decay (chain -- damage accumulates generation over
generation with no home at all, used for 12/13/14 today).

Here: home is still word position (distance from the poem's midpoint),
but instead of a single-pass keep/erase decision, every word is
copied, generation after generation, through the same per-character
noise as 2026-09-16_12 -- except the per-character error rate itself
is now controlled by the word's pull. Near home: low error rate, a
word can survive many generations almost untouched. Near the edges:
high error rate, a word is chewed up fast. So position (radial) sets
*how fast* the chain (linear) destroys a given word -- the two
mechanisms are no longer independent registers, one is now a
parameter of the other.

Source: same Raven opening stanza already in this studio. 20
generations. One seed, no rewriting after the fact -- including if the
"home should survive best" prediction turns out wrong on this run.
"""
import random

SEED = 11
random.seed(SEED)

SRC = ("Once upon a midnight dreary, while I pondered, weak and weary, "
       "Over many a quaint and curious volume of forgotten lore— "
       "While I nodded, nearly napping, suddenly there came a tapping, "
       "As of some one gently rapping, rapping at my chamber door. "
       "’Tis some visiter,” I muttered, “tapping at my chamber door— "
       "Only this and nothing more.”")

words = SRC.split()
n = len(words)
center = n / 2
half = n / 2

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def pull(i):
    dist = abs(i - center)
    return min(dist / (half * 0.7), 1.0)  # 0 at home, 1 at the edges

def error_rate(word_pull):
    # near home: very low error. near edge: high error. same "free vs
    # mechanical" shape as the erasure rule, but feeding a continuous
    # rate instead of a binary keep/erase.
    return 0.003 + word_pull * 0.09

def copy_word(word, rate):
    out = []
    for ch in word:
        r = random.random()
        if r < rate * 0.4:
            continue
        elif r < rate:
            out.append(random.choice(ALPHABET) if ch.isalpha() else ch)
        elif r < rate * 1.3:
            out.append(ch); out.append(ch)
        else:
            out.append(ch)
    return "".join(out)

cur_words = list(words)
N_GEN = 20
generations = [" ".join(cur_words)]
for g in range(N_GEN):
    nxt = []
    for i, w in enumerate(cur_words):
        nxt.append(copy_word(w, error_rate(pull(i))))
    cur_words = nxt
    generations.append(" ".join(cur_words))

lines_out = []
for i, g in enumerate(generations):
    lines_out.append(f"--- generation {i} ---")
    lines_out.append(g)
    lines_out.append("")

with open("works/2026-09-16_15_cross.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines_out))

# quick check of the actual claim: is the middle third of words, by
# character count, more intact after N_GEN than the outer thirds?
def survival(word_orig, word_now):
    return 1.0 if word_orig.strip(".,—“”’").lower() == word_now.strip(".,—“”’").lower() else 0.0

third = n // 3
scores = [survival(words[i], cur_words[i]) for i in range(n)]
home_band = scores[third:2*third]
edge_band = scores[:third] + scores[2*third:]
print("home-band survival:", sum(home_band)/len(home_band))
print("edge-band survival:", sum(edge_band)/len(edge_band))
