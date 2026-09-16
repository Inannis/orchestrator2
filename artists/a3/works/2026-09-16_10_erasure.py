"""
A fourth register, and the first work built from something I didn't
make: found text instead of a generated point. Source is Poe's "The
Raven," fetched verbatim from Project Gutenberg (plain-text ebook #1065,
public domain) and saved unmodified alongside this script as
2026-09-16_raven_source.txt, so the source is checkable, not just
trusted.

The erasure rule is the walk rule, translated a second time (first was
the walking score) -- this time onto a sequence of words instead of a
sequence of headings:

  - Treat the poem's word sequence as the walk: position in the poem is
    distance from "home" (the poem's midpoint).
  - Near home (close to the midpoint), keep/erase each word by a loose
    coin flip -- freedom, like the wander term.
  - Far from home (near either end), stop flipping coins and fall into
    a fixed, mechanical rule -- keep only every 7th word -- the way the
    walk's heading stops wandering and starts committing to an arc.

One seed, one pass, no rewriting after the fact -- if the output reads
badly in places, it stays, the same way a bad stretch of a walk stays
in the render.
"""
import random, re

SEED = 7
random.seed(SEED)

with open("works/2026-09-16_raven_source.txt", encoding="utf-8") as f:
    text = f.read()

words = text.split()
n = len(words)
center = n / 2
half = n / 2

kept = []
for i, w in enumerate(words):
    dist = abs(i - center)
    pull = min(dist / (half * 0.55), 1.0)  # same shape as the walk's pull
    if pull < 0.6:
        keep = random.random() < 0.55
    else:
        keep = (i % 7 == 0)
    if keep:
        kept.append(w)
    else:
        kept.append("_" * min(len(w), 6))

# rewrap at roughly the source's line width so it stays a poem, not a
# paragraph
out_lines = []
line = []
line_len = 0
for w in kept:
    line.append(w)
    line_len += len(w) + 1
    if line_len > 60:
        out_lines.append(" ".join(line))
        line = []
        line_len = 0
if line:
    out_lines.append(" ".join(line))

body = "\n".join(out_lines)

md = f"""# Erasure, Applied to "The Raven"

Source: Edgar Allan Poe, *The Raven* (1845), Project Gutenberg eBook
#1065, public domain. Verbatim source saved at
`2026-09-16_raven_source.txt`. Rule and seed ({SEED}) in
`2026-09-16_10_erasure.py`.

Near the poem's midpoint, each word is kept by a loose coin flip. Near
either end, the coin flip is replaced by a fixed rule -- keep only
every 7th word -- the same shape as the walk rule this whole studio
started from: free near home, mechanical far from it. Erased words are
blanked to their own length, not removed, so the poem's shape stays
visible even where its words don't.

---

{body}
"""

with open("works/2026-09-16_10_erasure.md", "w", encoding="utf-8") as f:
    f.write(md)

print(f"{n} words, {sum(1 for w in kept if not set(w) <= {'_'})} kept")
