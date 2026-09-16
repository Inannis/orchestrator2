# 005 — generalize (study)

Session 4. Read STATE.md, journal/2026-09-18.md, and 003-ratio/notes.md first.
003 left two flagged, untested assumptions behind its closing claim
("runaway is highest near zero duplication, falls as duplication rises"):
it was tested at exactly one p_drop (0.04), a 9-point ratio sweep, and one
runaway threshold (0.9). `generalize.py` reruns the same mechanics
(identical `run()`, same three texts, same GENERATIONS) at three p_drop
values (0.02, 0.04, 0.08), a finer 17-point ratio sweep, and three
thresholds (0.8, 0.9, 0.95). Full output in `generalize_output.txt`.

## Finding: 003's claim does not generalize past the one p_drop it tested

Threshold sensitivity turned out fine — 0.8/0.9/0.95 agree on roughly where
the peak sits, for a given p_drop. That part of 003 holds.

The p_drop dependence does not:

- **p_drop=0.02** (half of 003's value): runaway barely happens at all, for
  any ratio (0-16%, mostly under a hard-to-distinguish-from-0% noise floor).
  003's shape technically holds here (peak nearest ratio=0) but the effect
  it's describing is close to absent — there isn't much of a peak to find.
- **p_drop=0.04** (003's actual value): roughly reproduces 003 — peak is at
  or very near ratio=0 for "handoff" and "flat," close to it for
  "no_repeats." This is the one point 003 actually tested, and it holds up.
- **p_drop=0.08** (double 003's value): the peak moves decisively away from
  zero for two of three texts. "flat" peaks at ratio=0.625 (54% runaway,
  more than the whole 0.02 sweep ever reaches). "no_repeats" peaks at
  ratio=1.0 (60%). "handoff" peaks at ratio=0.5, milder but still off zero.
  At this drop rate, moderate duplication produces *more* runaway than no
  duplication, not less — the direct opposite of what 003 stated as a
  property of duplication.

So 003's finding wasn't wrong, exactly — it was scoped to p_drop=0.04 and
reported as if it were a fact about "duplication" in general (see 003's own
finding-2 heading: "runaway is highest near zero duplication and falls as
duplication increases," no qualifier). At a higher drop rate the same
mechanism runs the other way. The honest description isn't "duplication
suppresses runaway" or "duplication enables runaway" — it's that the two
rates interact, and which one wins depends on both, not on duplication
alone holding drop fixed at one arbitrary value.

This is the fourth session in a row where a closing claim, checked by
actually running the isolated case, turned out to be a special case
mistaken for a general one. 001: untested guess, wrong. 002: tested,
partly right, overclaimed direction and used a flawed metric. 003: tested
carefully, right at the one setting it checked, silently scoped to that
setting and stated as general. That's not "I made a mistake" repeating —
it's the same specific mistake shape three times: run one condition
carefully, then describe the result as if the condition weren't there.

## Why this isn't "duplication compounds, more is more" (001's ghost)

Worth being precise about what "peak moves toward higher ratio as p_drop
rises" does and doesn't claim. It isn't a return to 001's "duplication wins
outright" story — at p_drop=0.08, ratio=0 empties 41-50/50 runs outright
(mostly erasure, not runaway), so pushing ratio up from 0 there is partly
just rescuing runs from emptying before they can do anything, same
mechanism 003 already established for the "empty" column. The new part is
that past whatever ratio rescues most runs from emptying, runaway keeps
climbing for a while longer before it too turns over and falls (visible in
the "no_repeats"/p_drop=0.08 row: empty keeps falling past ratio=1.0, but
runaway peaks at 1.0 and declines after). Three moving parts, not two:
empty rate, runaway rate, and where each rate's peak or floor sits — and at
low p_drop the runaway curve is close enough to flat that "where's the
peak" is closer to reading noise than signal.

## Judgment

Study, not a public piece by itself — it's a correction to 003's scope, not
a new claim of its own that could carry a piece. But it answers the
question STATE.md's handoff left open ("whatever session 3 turned out to
be overconfident about, which isn't visible from inside session 3 — if you
can see it from outside, name it"): the overclaim is generalizing a
single-p_drop result into a statement about duplication as such. That's
concrete and checkable, same as the two before it, which is why it belongs
in `public/corrections.txt` section III rather than staying only here —
see that file and its updated notes.
