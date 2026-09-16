"""
Same erasure rule as 2026-09-16_10_erasure.py, same seed, applied to a
different source on purpose: not to make a second poem, but to find out
if the rule is a method or a one-off that happened to suit "The Raven."

Raven: ~1080 words, narrative, refrain-heavy, long middle to be "free"
in. Ozymandias: 14 lines, ~110 words, a sonnet with no refrain and
almost no middle to speak of. If the rule only looks right on something
shaped like the Raven, that's worth knowing.

Source: Percy Bysshe Shelley, "Ozymandias" (1818), public domain,
transcribed at Representative Poetry Online (University of Toronto,
https://rpo.library.utoronto.ca/content/ozymandias-0), saved verbatim
at 2026-09-16_ozymandias_source.txt. This is a transcription by a
third party, not a scan of the original publication -- noted, not
hidden.

Rule, unchanged from v1: word position is distance from the poem's
midpoint. Near the midpoint, keep each word by a loose coin flip. Near
either end, switch to a fixed mechanical rule, keep only every 7th
word. Erased words blank to their own length. Same seed (7) as v1, so
any difference in outcome is the source, not the dice.
"""
import random

SEED = 7
random.seed(SEED)

with open("works/2026-09-16_ozymandias_source.txt", encoding="utf-8") as f:
    text = f.read()

words = text.split()
n = len(words)
center = n / 2
half = n / 2

kept = []
for i, w in enumerate(words):
    dist = abs(i - center)
    pull = min(dist / (half * 0.55), 1.0)
    if pull < 0.6:
        keep = random.random() < 0.55
    else:
        keep = (i % 7 == 0)
    if keep:
        kept.append(w)
    else:
        kept.append("_" * min(len(w), 6))

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
n_kept = sum(1 for w in kept if not set(w) <= {"_"})

md = f"""# Erasure, Applied to "Ozymandias" -- a Second Source

Second test of the erasure rule from `2026-09-16_10_erasure.py`, same
seed (7), on a source picked for being nearly everything the Raven
isn't: short (14 lines, {n} words against ~1080), no refrain, no long
middle. Source: Percy Bysshe Shelley, *Ozymandias* (1818), public
domain, transcribed at Representative Poetry Online, University of
Toronto (rpo.library.utoronto.ca/content/ozymandias-0). Verbatim copy
at `2026-09-16_ozymandias_source.txt`.

{n_kept} of {n} words survive.

---

{body}
"""

with open("works/2026-09-16_11_erasure_v2.md", "w", encoding="utf-8") as f:
    f.write(md)

print(f"{n} words, {n_kept} kept")
