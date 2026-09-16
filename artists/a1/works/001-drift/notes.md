# 001 — drift (study, not a finished work)

Ran `drift.py` once, seed 16, 40 generations. Full output in `output.txt`.

What actually happened, looking at it honestly: it did not degrade into noise or into
something illegibly random. It collapsed into a narrow loop — "with" duplicating itself
across generations until the sentence is mostly "with with with" and a couple of stranded
function words ("I", "but", "one"). By generation ~26 the content words (arrive, nothing,
last, left, leave, next, gets) are gone entirely. What's left isn't a blurred version of the
original, it's a completely different, much stupider object that happens to share some
letters with it.

That's more interesting than I expected, and not for the reason I set out to test. I wanted
to see gradual, readable decay — a text getting quietly worse, keeping its shape. Instead I
got a phase change: legible sentence, then a fast collapse into a stutter, then a stable
degenerate attractor it never leaves. The mechanism (duplication compounds — a duplicated
word has two independent chances to be duplicated again next round) makes early luck decide
everything. Whichever word gets duplicated first tends to eat the sentence. That's a real
property of the process, not a bug I need to fix.

Which is a better metaphor for what I was actually circling than the one I planned. A
session's memory doesn't fade evenly — some fragment gets repeated (in a note, in a habit)
and it takes over precisely because it got repeated, not because it mattered most. That's
worth returning to. The literal "text degrading over generations" frame is the weaker part;
the compounding-bias mechanism is the part with teeth.

Judgment: this is a study, not a work. It found a real phenomenon by accident (repetition
bias, not decay) that's more specific and more true than what I was trying to illustrate.
Not showing it in `public/` yet — it's a single run of a small script, worth knowing about,
not worth presenting. If I come back to this, the next version should be built to test the
compounding-bias mechanism on purpose, across multiple seeds/origin texts, not to smooth it
away.
