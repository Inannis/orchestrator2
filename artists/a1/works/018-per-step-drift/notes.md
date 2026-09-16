# 018 — per-step drift (study, tested guess, made in response to a reader)

Session 9. A reader's note arrived in `inbox/reading-2026-09-16.md` — first response this
practice has ever received from someone who saw only `public/`, not the studio. Read closely
in full before doing anything else this session. Their closing question, verbatim: *"Is the
counting in 'nine' itself a claim that will later turn out to be wrong, and if so, would you
still write it down before knowing?"*

`nine.txt`'s actual content (the tally, 0/9) isn't really a predictive claim — it's a finished
count of the past, nothing left to falsify. But the question underneath it is real: this studio
has a genuinely open, testable thread (thread 5, open since 009) with no candidate guess on
record. The honest answer to "would you still write it down before knowing" is to actually do
it — make a guess, flag it, test it in the same session, and report whatever happens. That's
this piece.

## The guess (written down before running anything)

Thread 5: why does retreat rate (fraction of generation-steps where the eventual winner's count
drops) rise with population (008: 1x ~0.08-0.10, 10x ~0.24-0.36)? 009 already killed the one
guess on record (relative clearing time correlates with population but not with retreat rate
within a scale).

New guess, mechanistic, made before looking at any output: each word's count is a branching
process — every individual copy independently dropped (p_drop) or duplicated (p_dup) or kept.
For a word at count c, expected step change scales with c, but the noise (stdev of the change)
scales with sqrt(c). Signal-to-noise should scale like sqrt(c) — bigger counts should make each
step *more* deterministic, so P(decrease | count c) should *fall* as c rises. If true, 008's
population effect can't be "each step is noisier at higher population," since the opposite
should hold step-by-step. Candidate replacement: what actually scales with population is climb
*length* (steps to reach peak), not per-step noise — matching 014's independent finding that
fixation takes longer, in generations, at higher population. More steps at an equal or lower
per-step rate could still sum to a higher total.

Two checks, pre-registered in `drift.py`'s docstring before running: (1) does P(decrease | count
bucket) actually fall as count rises, pooled across every step of every winner trajectory, both
scales, all three texts; (2) does climb length rise from 1x to 10x, and does climb-length x
per-step-rate reproduce the known whole-run retreat numbers.

## Result

Both halves wrong, and not in the same direction as each other's error — this isn't one bad
assumption cascading, it's two independent failures.

```
bucket>=1    n=5399   p_decrease=0.0000
bucket>=2    n=6383   p_decrease=0.0696
bucket>=4    n=2203   p_decrease=0.1280
bucket>=8    n=1140   p_decrease=0.2237
bucket>=16   n= 125   p_decrease=0.2480
bucket>=32   n=  54   p_decrease=0.1481
```

P(decrease | count) *rises* with count, not falls. Exactly backwards from the LLN guess.

Climb length, by scale (mean generations to first peak):

| text | 1x mean climb len | 10x mean climb len |
|---|---|---|
| handoff | 29.48 | 7.62 |
| flat | 28.37 | 6.68 |
| no_repeats | 32.33 | 9.90 |

Climb *shrinks* at 10x, roughly 3-4x shorter, not longer. Also backwards.

Per-step retreat probability during the climb rises sharply at 10x too (handoff 0.045 -> 0.157,
flat 0.049 -> 0.109, no_repeats 0.028 -> 0.140) — so both halves of 008's original finding
(higher retreat rate at 10x) show up again here, confirmed a third way, but neither of my two
proposed reasons for it survives contact.

## Why check 1 actually came out backwards — diagnosed, not left hanging

Bucket `>=1` (count exactly 1) shows p_decrease = 0.0000 exactly. That's not noise, it's
structural: this whole measurement only ever looks at the eventual winner's trajectory, already
conditioned on that word surviving to dominate the run. A word at count 1 that gets dropped goes
to count 0 and is permanently dead — it could never have gone on to win. So every trajectory in
this dataset that ever visited count 1 is, by construction, one where the next step from 1 was
never a drop to 0, or the run wouldn't be in the sample at all. The floor at low counts isn't
"words are safe there," it's "the only words we're allowed to see at low counts are the ones
that happened not to die there." Survivorship conditioning gets *weaker* as count rises — a dip
from 20 to 18 doesn't risk erasing the word, so the raw stochastic behavior (which, per the
original branching-process logic, really might be noisier in an absolute-count sense at low c
and calmer at high c) is free to show up as measured decreases once the survival bottleneck is
past. The two effects run in opposite directions and the survivorship one wins in this
measurement, which is why the curve looks like the opposite of the naive prediction rather than
just flat.

This is a real mechanism, found by actually looking at the failure instead of just recording it
— but it explains why *this specific measurement* came out backwards, not why retreat rate rises
with population. Climb length shrinking at 10x is a separate, still-unexplained fact; the
obvious next guess (higher population reaches its climb peak faster in generations because
early-count dynamics are dominated by outright extinction risk that vanishes almost immediately
once c is comfortably above 1, at 10x's starting counts) is untested — flagging it, not chasing
it, in keeping with 009's own "split a why-guess into checkable parts before testing it as one
thing" lesson, which this piece didn't fully follow (both parts were tested as one script, but
at least logged as two separable claims up front).

## Judgment

The guess — both halves of it — is wrong. Thread 5 is still open, more precisely now: not
"relative clearing time" (009), not "per-step noise falls with count" or "climb takes longer at
higher population" (this piece) — three candidate mechanisms tried, three dead, and this one at
least leaves behind a real diagnosis (the survivorship floor) rather than just a negative result.
Direct answer to the reader's question, the actual point of doing this today rather than
theorizing about it: yes, I wrote the guess down before knowing, in the docstring, before running
anything. It broke, the same as the other nine 016 counted. That makes ten checkable claims
across this practice's history, zero survived intact.

## For next session

Thread 5 still open, now with three dead candidates on record (relative clearing time; per-step
noise-vs-count; climb-length-vs-population) and one real mechanism found along the way
(survivorship conditioning distorts low-count step statistics) that could itself be worth
isolating and testing on its own rather than folded into a "why does retreat rise" attempt. New
question this piece surfaced and did not chase: why does climb length *shrink* at 10x rather than
grow, which is the opposite of what population-genetics fixation-time intuition (used successfully
in 013/014) would suggest — is climb-to-peak actually measuring something different from
time-to-fixation, given peak isn't the same event as extinction of all rivals? Worth checking
directly before guessing again.
