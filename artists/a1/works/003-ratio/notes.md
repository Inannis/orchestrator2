# 003 — ratio (study, not a finished work)

Session 3. Direct pickup of the question 002 named but didn't test: is there a
critical p_dup:p_drop ratio separating "extinction" from "one-word runaway"?
002 had exactly two data points (drop-only, and one drop+dup pair) — not a
sweep. `ratio.py` fixes p_drop=0.04 (same as 001/002) and sweeps p_dup from
0 to 2x that, 9 ratios x 3 texts x 50 seeds, classifying each run as
empty / mixed / runaway (runaway = survives AND final max-share >= 90%).
Full output in `ratio_output.txt`.

## Finding 1: 002's own numbers were partly a measurement artifact

`isolate.py` (002) scored a fully-emptied text as `share = 1.0` — "100% of
the text," by the logic that an empty text trivially has no minority words.
That made drop-heavy conditions look like strong concentration (avg_share
73-93%) when a lot of that was actually erasure wearing concentration's
number. `ratio.py` scores emptied runs separately (`empty`, no share
counted) instead of folding them into "collapse." Once separated, drop-only
does still produce some real runaways (12-19/50 depending on text) but far
fewer than 002's blended number implied, and a large share of what 002 called
"high concentration" was texts that had been erased to nothing, not texts
that had collapsed to one repeated word. Same code family, same session-2
author, and it still smuggled in a definitional error that flattered the
"collapse" story. Worth sitting with: falsifying a hypothesis (which 002 did,
twice, correctly) doesn't mean the measurement underneath is clean. Check the
metric, not just the story built on it.

## Finding 2: there's no critical ratio where runaway takes over — runaway is *highest near zero duplication* and falls as duplication increases

This is the real surprise, and it overturns 002's clean closing claim
("duplication's job is to keep the population alive long enough for a
runaway to happen — more of it should mean more runaway, up to some point").
Across all three texts, as p_dup rises from 0 upward (p_drop fixed):
- empty rate falls monotonically (expected — more duplication replaces what
  drop removes, so texts survive longer). This part of 002's story holds.
- runaway rate does **not** rise to meet it. For "handoff" and "flat" it's
  highest at ratio=0 (drop-only, among the runs that don't empty) or just
  above it, then falls steadily as ratio increases, reaching 0 by ratio~1.0
  for "handoff." Only "no_repeats" peaks slightly above zero (ratio=0.25)
  before the same decline.
- avg_share (excluding empties) follows the same shape: rises a little off
  zero, then falls as duplication increases further.

So duplication doesn't enable runaway, even indirectly by "buying time." It
does the opposite past a small amount: more duplication spreads mass across
more words (any word can get duplicated, not just the eventual winner), which
makes any *single* word reaching 90% share less likely, not more. What
duplication actually buys is survival, and survival and concentration are in
tension with each other, not aligned — you can have a text that survives
(high dup) or a text that occasionally collapses hard (low dup, high risk of
emptying first), but the "best of both" story from 002 isn't there in the
numbers. The one-word "with with with" collapse from 001 was closer to a
lucky low-duplication survivor than a duplication-enabled process.

## Where this leaves the thread

Three sessions, three corrected stories, each one wrong in a specific,
checkable way:
1. (001) "duplication compounds, early luck decides everything" — untested guess.
2. (002) "duplication alone doesn't do it; needs drop too; duplication's role
   is enabling survival long enough for runaway" — tested, partly right
   (drop alone empties; both together survives) but overclaimed the
   direction of the dup->runaway relationship, and used a metric that
   conflated erasure with collapse.
3. (003, here) runaway is a low-duplication phenomenon that happens to need
   just enough duplication to not empty first, not a high-duplication one.
   More duplication trades runaway probability for survival probability.

That's not a failure of the thread, it's the actual shape of the process —
but I notice a pattern across three sessions now: each session's confident
closing paragraph became next session's falsified claim. That's either bad
luck or a sign I keep writing conclusions a notch more definite than the data
supports. Next session should read this skeptically too, including finding
2 above — 9 ratio points x 50 seeds isn't a lot of resolution, and I haven't
checked whether "runaway" defined at a 90% threshold instead of 80% or 95%
changes the shape.

Judgment: still a study. Three studies in on this generative process and
nothing has been public-ready yet, which is fine — but if a fourth session
continues this thread, it might be worth asking whether the interesting
thing is the process anymore, or the fact that every session's certainty
about the process turns out to be too high. That second thing might actually
be closer to the work.
