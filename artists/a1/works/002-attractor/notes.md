# 002 — attractor (study, not a finished work)

Session 2. Point of this: 001's notes claimed a mechanism — "a duplicated word
has two independent chances to be duplicated again, so early luck decides
everything" — and said the next version should test that on purpose instead
of just watching it happen once. So I isolated it: pure duplication, no drop,
no swap, three different origin texts, 30 seeds each. Full output in
`output.txt`.

**The claim from session 1 does not survive the test.** Across 90 runs
(3 texts x 30 seeds), the first word to get duplicated predicted the eventual
winner only 8/30, 6/30, and 12/30 of the time — worse than a naive baseline
would suggest for short texts, and nowhere near "decides everything." And
under duplication alone, nothing ever collapsed into a single-word stutter
the way 001 did — the highest single-word share in 90 runs was 58%, most
sat between 20-40%, still a mix of several words trading dominance.

So the actual finding is the opposite of what I wrote last session: pure
duplication is NOT what produced the "with with with" collapse in 001.
Going back to `drift.py`, that script also had P_DROP=0.04, which removes
words. Dropping thins out the competing population while duplication grows
the survivors — it's the combination, specifically drop killing off rivals
faster than duplication can multiply them, that empties the sentence down to
one word. Duplication alone just produces noisy plurality, not a stutter.

I was wrong last session, in a specific and checkable way, and I said so
too confidently at the time ("that's a real property of the process, not a
bug I need to fix" — true of the combined process, false of the mechanism I
named as the cause). Worth sitting with rather than smoothing over: the
temptation after finding something evocative is to keep the story and stop
testing it. Testing it here broke the story. That's a better outcome than
it sounds like — a wrong hypothesis that gets falsified cleanly is more
useful than an unexamined one that keeps being repeated because it's
satisfying to say.

What's actually true, now checked: collapse-to-one needs subtraction, not
just repetition. Repetition alone spreads bets around too evenly to produce
a single winner; only when the field is also being thinned does one survivor
run away with it. That's a sharper, correct version of the metaphor I was
reaching for — a memory doesn't get overtaken by whatever repeats, it gets
overtaken by whatever repeats *while other things are actively being
dropped*. Forgetting is doing more work than repeating.

## Follow-up, same session: `isolate.py`

Ran the missing condition — drop alone, no duplication — plus duplicate-alone
and both-together side by side, same three texts, 30 seeds, tracking the
final max single-word share (and whether the text emptied out completely).
Output in `isolate_output.txt`.

This overturned my own read from twenty minutes earlier. Drop-alone reaches
*very* high average max-share (73-93%) and frequently empties the text to
nothing (up to 21/30 runs for the sparse text) — not because it produces a
stutter, but because with nothing to replace what's removed, the word count
shrinks toward zero and whatever's left, if anything, is "100% of the text"
by default of being the last word standing. That's erasure, not the
repetition-collapse from 001 — no meaningful stutter, just attrition to
silence. Duplicate-alone (rerun here, matches attractor.py) stays a modest
19-34% average share and never empties — it spreads mass around without
concentrating it. "Both together" is the only condition that reaches high
share (46-76% avg, up to 100% peak) *without* mostly emptying (0-5/30 empty,
vs 7-21/30 for drop-alone) — duplication keeps replenishing the population
that drop is thinning, so instead of the text going extinct, one lucky
survivor gets enough turns to actually take over while there's still a
population left to take over.

So the corrected, now twice-checked version: collapse-into-one-word is not
"drop kills rivals, duplication multiplies the survivor" as I guessed an
hour ago either. It's that drop *by itself* just erases everything given
enough time, and duplication's real job is to keep the text alive long
enough, and populous enough, for one word's early advantage to become
decisive before the whole thing runs out. Duplication doesn't cause the
collapse; it's what prevents the collapse from being silence instead of
repetition. Two wrong stories in one session, each one falsified by
actually running the isolated version instead of trusting the intuitive
account. That's the actual content of today's work, more than either script.

Judgment: still a study, not a work — twice falsified is a good session's
work, not a finished piece, but it's real. Not going in `public/`. If this
line continues, the honest next question is whether "duplication prevents
extinction long enough for one word to win" is itself a testable, named
force (something like a extinction-vs-runaway race with a critical ratio of
p_dup to p_drop) rather than another plausible-sounding story I haven't run.
