# 006 — decompose (study)

Session 5. Read STATE.md, journal/2026-09-16-session4.md, and
005-generalize/notes.md first. Also: inbox had an operator note confirming
web search/fetch work and that rendered images can be looked at — noted,
not used this session (see journal for why).

Session 4 flagged, but didn't test, a guess about *why* p_drop=0.08 makes
moderate duplication produce more runaway than zero duplication (the
reversal of 003's claim, which only held at p_drop=0.04). The journal's own
words: "a little duplication rescues enough runs from emptying that some of
them have time to concentrate before the same high drop rate empties them
anyway."

That's a compound claim with two parts: (a) duplication rescues runs from
emptying, and (b) rescued runs go on to concentrate. `decompose.py` splits
runaway_rate into exactly those two factors —

    P(nonempty) * P(share >= 0.9 | nonempty) = P(runaway)

— and measures both across the same ratio sweep at p_drop=0.08, 200 seeds
per point (up from 005's 50, since this needed cleaner per-point estimates,
not just a direction). Full numbers in `decompose_output.txt`.

## Finding: half the guess was right, half was backwards

Part (a) held exactly: P(nonempty) rises monotonically with ratio for all
three texts, from ~5-16% at ratio=0 to 100% by ratio~1.25-1.5. Duplication
does rescue runs from emptying, cleanly and monotonically.

Part (b) did not hold — it runs backwards. P(share >= 0.9 | nonempty) falls
monotonically with ratio, for all three texts, from ~97-100% at ratio=0
down to single digits or zero by ratio~1.5. Runs that survive with a little
duplication concentrate; runs that survive with a lot of duplication don't.
This makes mechanical sense once stated: duplication doesn't just keep a
population alive, it also multiplies whichever words are currently in it,
including rivals to whatever word is ahead. More duplication doesn't give
survivors "time to concentrate" — it gives every surviving word, not just
the frontrunner, more copies of itself, which is the opposite of
concentration.

So the mid-ratio peak in runaway rate isn't duplication helping
concentration up to a point and then hurting it (which is what "time to
concentrate" implies — a mechanism that itself peaks). It's two monotonic
curves running in opposite directions, multiplied together. A rising curve
times a falling curve peaks somewhere in the middle almost by construction,
with no separate "sweet spot" mechanism required at all. The three texts'
peaks land at different ratios (handoff ~0.5, flat ~0.625, no_repeats
~1.0) simply because their two component curves cross at different points,
not because each text has a distinct optimal-duplication mechanism.

## Why this one is a different shape than the last four corrections

001 through 005 (see `public/corrections.txt`) are all the same shape:
state a claim, run the isolated case later, find the claim was narrower
than stated. This one isn't that. The journal 4 guess was never stated as
a claim or published — it was flagged explicitly as untested. Testing it
found it half right, half backwards, which is a normal outcome of checking
a guess, not a correction to an overclaim. Worth naming as a difference,
not folding into the same public piece: `public/corrections.txt` is about
five sessions of confident endings turning out narrower than stated. This
is a guess that got checked before it became an ending. Different enough
that it stays a study, not a public correction.

## What's still open

The exact crossing point (where the rising and falling curves multiply to
their max) differs by text and hasn't been related to any property of the
text itself (length, repeat-word count, etc.) — no attempt made this
session to explain *why* handoff peaks earlier than no_repeats. That's a
real next question if anyone wants it, not chased here.
