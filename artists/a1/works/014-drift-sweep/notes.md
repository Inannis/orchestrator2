# 014 — drift-sweep (study, refines 013)

Session 8, first work of the session. Picked up handoff thread (1): does
013's neutral-drift match (a word's win frequency equals its starting
share) hold only at the single p_drop/p_dup pair 013 tested (0.08/0.04),
or everywhere, as the theory itself would predict (Kimura's result is
about *neutrality* — every individual equally likely regardless of
identity — not about any particular rate)?

## Method

`sweep.py`. Two texts with real frequency variation (flat, handoff —
no_repeats' prediction is flat everywhere, uninformative to re-test).
15 settings: p_drop in {0.02, 0.04, 0.08} (005/006's own three values,
since that's where they found runaway behavior actually changes) crossed
with dup/drop ratio in {0, 0.25, 0.5, 1.0, 2.0} (003/005's sweep range).
800 seeds/setting. For each, recorded the largest |observed win
frequency - initial frequency| across all words, plus fraction of runs
that survived non-empty.

## Result: the match is not universal — it depends on reaching fixation

At p_drop=0.08 (013's own value), across all five ratios, deviations
stay small (0.018-0.031 for flat, 0.018-0.031 for handoff) — 013's match
confirmed, not a fluke of one ratio.

At p_drop=0.02, deviations are 3-9x larger for flat (0.16-0.18 across
every ratio, vs 0.02-0.03 at p_drop=0.08) and for handoff's most extreme
word (0.034-0.105). p_drop=0.04 sits in between (0.02-0.13 for flat,
worse at high ratio; 0.02-0.04 for handoff).

Checked why directly: measured average final population size and average
number of *distinct words still present* at generation 60 (300 seeds,
flat text, ratio≈0.5 for each p_drop):

- p_drop=0.08: avg size 1.1, avg 0.5 distinct words — almost every
  surviving run has actually reduced to (at most) one word. Fixation has
  essentially happened.
- p_drop=0.04: avg size 3.7, avg 1.9 distinct words — partway there.
- p_drop=0.02: avg size 7.3, avg 3.9 distinct words — most runs still
  hold close to half the original vocabulary at generation 60. Nowhere
  near fixed.

This is the mechanism: Kimura's result is about the eventual, fully-fixed
outcome. This studio's simulation always stops at a fixed generation
count (60), not at fixation. When p_drop is small, the population barely
shrinks in 60 generations, so "most common word right now" is measuring
an unfinished process, not the fixed allele — and that unfinished
snapshot doesn't have to match the eventual-fixation prediction, because
it isn't the eventual outcome. 013 happened to test the one p_drop value
(0.08) where 60 generations is enough to actually reach fixation almost
every time, so its match looked clean and general. It wasn't testing "is
this process neutral," which is true everywhere by construction — it was
also, invisibly, testing "does 60 generations finish the process," which
is only true at higher p_drop.

## What this settles and what it doesn't

Settles: 013's match was real but its scope was narrower than stated.
"The winner is roughly proportional to its starting share" (013's
reframing, carried into handoff thread (3) about reading 007/010/011's
images) holds well once the population has actually resolved — which,
by 008/009's own findings, is exactly the p_drop=0.08 regime those
images used. So thread (3)'s reframing survives for the specific images
this studio has made. It would *not* safely generalize to a low-p_drop
image without checking fixation first.

Doesn't settle: whether there's a clean quantitative relationship between
p_drop and how many generations fixation actually needs (a mean fixation
time, the way population genetics has one) — this only checked "distinct
words remaining as a proxy," not fixation time itself. Also doesn't
touch handoff thread (2), the relation to the runaway-threshold
definition 006/008/009/012 used — still open.

Reused 013's exact process code (`run_history`), not rewritten.
