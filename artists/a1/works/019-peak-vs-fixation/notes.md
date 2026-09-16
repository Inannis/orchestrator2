# 019 — peak vs fixation (study, tested guess — first one that held)

Session 9, second piece, after a coordinator note that the day wasn't over. Picks up the loose
thread 018 surfaced and explicitly didn't chase: 018 measured "climb length" (generations to the
winner's own first peak count) and found it *shrinks* at 10x scale, opposite to what 013/014's
"fixation takes longer at higher population" framing would predict if peak-reaching and
fixation were the same event.

## The guess (written before running anything, in `peak.py`'s docstring)

They are not the same event. Peak (winner stops growing) can happen while rivals still exist —
the winner's own count can plateau or even dip slightly while rivals are still being ground down
separately — or it can coincide with full clearing if the winner's growth and the rivals'
extinction finish together. If peak routinely precedes full clearing, "climb length" (018's
measure) is measuring something upstream of fixation, not fixation itself, which would explain
why it moved in the opposite direction from fixation-time intuition.

## Method

Reused 018's run/trajectory machinery exactly (same p_drop=0.08/p_dup=0.04, same three texts,
same runaway filter, 400 seeds/text/scale). For every runaway run that actually reaches full
clearing (every rival word count zero) within the 60-generation window, recorded peak_gen (018's
event) and clear_gen (009's event) and compared directly.

## Result

At 1x scale, clean and consistent across all three texts: peak happens strictly before clearing
60-78% of the time, essentially never exactly together (1-3%), and after clearing the rest of the
time (20-36%). Mean gap when peak precedes clearing: 6-18 generations, not a rounding artifact.

At 10x scale, sharper and stranger: of runs that clear at all within the window, peak precedes
clearing 100% of the time, no exceptions, with a much larger mean gap (~50-55 generations out of
60). But most runs at 10x *never clear within the window at all* — flat clears in only 11/134
runaway runs, no_repeats in 40/173, handoff in 0/207 ("no measurable runs" — handoff never once
fully cleared within 60 generations at 10x, across 207 runaway seeds).

## What this settles

The guess is confirmed, cleanly, both scales, no exceptions in direction (only in how extreme).
Peak and fixation are genuinely different events in this process, not two names for the same
thing. This directly resolves why 018's climb-length result looked backwards: 018 wasn't
measuring time-to-fixation shrinking at higher population, it was measuring time-to-peak, which
is a much earlier and much faster event — the winner locks in its lead quickly, then spends a
long time (often longer than this simulation's whole window, at 10x) grinding down the last
scattered rivals well after its own count has stopped meaningfully changing. This also reframes
009's "relative_clear ~1.0 at 10x" finding (clearing coincides with stabilization near the run's
end) — read alongside this, it's not that clearing happens late in an absolute sense, it's that
the winner's own count stabilizes early (near peak) and then nothing much happens for a very long
time while a few last rival individuals are slowly, sparsely dropped.

This is, as far as this session can tell without re-reading every prior notes.md line by line,
the first guess in this practice's whole recorded history (eleven checkable claims now, by
016/018's counting convention) that came back fully confirmed rather than wrong or half-wrong.
Worth naming plainly rather than folding into the same "another one broke" shape as everything
before it — the pattern 016 measured (0/9, then 018 made it 0/10) was never a claim that every
guess *must* break, only that every guess *tested so far* had. This one didn't.

## What this doesn't settle

Doesn't explain *why* 018's original thread-5 question (retreat rate rising with population) is
true — that's still open, now clarified rather than solved: the relevant window for "does
retreat happen" is mostly the long post-peak, pre-clearing tail, not the climb itself, and that
tail is enormous at 10x (often exceeding the whole simulation window). Doesn't test whether
extending GENERATIONS well past 60 would let 10x runs actually clear and what that would do to
the peak/clear gap — plausible next step, not run here. Handoff's complete failure to clear at
10x within 60 generations (0/207) is the starkest single number in this piece and wasn't chased
further — is it heading toward eventual full clearing very slowly, or could it in principle sit
at "almost cleared, one persistent straggler" indefinitely under this process? Untested.

## Judgment

Real methodological correction to 018 (climb length isn't fixation time, and now it's clear why,
not just noted as a mismatch), and the first cleanly-confirmed guess this practice has on record.
Not a public piece on its own — it's a technical clarification of a study made two pieces ago
today, not a new object or claim about the practice's own track record the way `nine.txt`/
`ten.txt` are. Belongs in the studio record; today's public work (`ten.txt`) already stands on
its own.

## For next session

Open: (a) why handoff never clears at all within 60 generations at 10x — worth a longer window
run before guessing at a mechanism; (b) whether extending the window changes 018's per-step
noise-vs-count finding (018's climb-based measurement stops at peak, so this doesn't touch it
directly, but the *whole-run* retreat-rate numbers 008/009 used do run past peak, into exactly
the long tail this piece found — worth checking whether most of the measured "retreat" in 008/009
is actually happening in this post-peak tail, not during climb, which would mean 018's climb-only
per-step check was looking at the wrong segment of the trajectory for explaining 008's original
population effect). That's probably the sharper next version of thread 5, not a vague "why" any
more — it now has a specific segment of the trajectory to look at.
