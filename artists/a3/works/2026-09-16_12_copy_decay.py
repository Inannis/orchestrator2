"""
A second method, on purpose. Everything in the studio so far shares one
mechanism: distance from an origin point, free near it, mechanical far
from it. That's a spatial/field logic. This is not that.

Generational copy error: a chain, not a field. Generation 0 is a
verbatim found text (the opening stanza of Poe's "The Raven," already
sourced in this studio at works/2026-09-16_raven_source.txt). Each
later generation is produced only from the immediately preceding one,
by a fixed per-character chance of substitution, deletion, or
duplication -- like a photocopy of a photocopy, or a message passed
person to person. There is no "home" to return to and no pull that
grows with distance; there is only step count, and the process cannot
look back past the previous generation. Errors compound and never
self-correct. This is monotonic, not radial.

30 generations, one seed, one pass -- same no-rewrite discipline as the
erasures.
"""
import random

SEED = 3
random.seed(SEED)

SRC_LINES = [
    "Once upon a midnight dreary, while I pondered, weak and weary,",
    "Over many a quaint and curious volume of forgotten lore—",
    "While I nodded, nearly napping, suddenly there came a tapping,",
    "As of some one gently rapping, rapping at my chamber door.",
    "’Tis some visiter,” I muttered, “tapping at my chamber door—",
    "                                   Only this and nothing more.”",
]
gen0 = "\n".join(SRC_LINES)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
P_SUB = 0.012
P_DEL = 0.006
P_DUP = 0.006

def copy_once(text):
    out = []
    for ch in text:
        r = random.random()
        if r < P_DEL:
            continue  # dropped in copying
        elif r < P_DEL + P_SUB:
            out.append(random.choice(ALPHABET) if ch.isalpha() else ch)
        elif r < P_DEL + P_SUB + P_DUP:
            out.append(ch)
            out.append(ch)  # copyist's hand slipped, repeated a stroke
        else:
            out.append(ch)
    return "".join(out)

N_GEN = 30
generations = [gen0]
for i in range(N_GEN):
    generations.append(copy_once(generations[-1]))

def readable_frac(text, ref_words):
    words = text.split()
    ref = set(ref_words)
    hits = sum(1 for w in words if w.strip(".,—“”’") .lower() in ref)
    return hits / max(len(ref_words), 1)

ref_words = [w.strip(".,—“”’").lower() for w in gen0.split()]

lines_out = []
for i, g in enumerate(generations):
    frac = readable_frac(g, ref_words)
    lines_out.append(f"--- generation {i} (~{frac*100:.0f}% of original words still present, exact match) ---")
    lines_out.append(g)
    lines_out.append("")

report = "\n".join(lines_out)
with open("works/2026-09-16_12_copy_decay.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("done,", N_GEN, "generations")
print("gen 0 len", len(gen0), "gen", N_GEN, "len", len(generations[-1]))
