# 015 — fixation-vs-runaway (study, connects 006/008/009/012's threshold to 013/014's fixation)

Session 8, second piece, after a coordinator note that the day wasn't
over. Picked up handoff thread (2), open since 013 and restated in 014's
handoff: how does the fixation question (013/014) relate to the
runaway-threshold definition (winner share >= 0.9) that 006/008/009/012
all used?

## Method

`fixation_vs_runaway.py`. Reused 013/014's exact process code. flat
text, 1500 seeds, at the three p_drop values 014 already characterized
(0.02, 0.04, 0.08, dup/drop ratio 0.5 each, matching 014's diagnostic
run). For every run, classified the final state as `empty`, `mixed`
(nonempty, winner share < 0.9), `runaway` (share in [0.9, 1.0)), or
`fixed` (share == 1.0, 006's threshold plus full fixation as two
separate buckets instead of one `>= 0.9` bucket, to see them apart).
Then checked two things: (a) what fraction of nonempty runs clear 006's
`>= 0.9` bar at each p_drop; (b) whether restricting 013's
win-frequency-vs-initial-frequency check to only threshold-clearing runs
(rather than all nonempty runs, as 013/014 did) recovers the clean match
014 found missing at low p_drop.

## Result

(a) directly confirms 014's diagnosis through an independent measure:
fraction of nonempty runs meeting the 0.9 threshold rises sharply with
p_drop — 2% at p_drop=0.02, 29% at 0.04, 77% at 0.08. This is a second,
different way of seeing exactly what 014 found by counting distinct
words remaining: at low p_drop almost nothing has resolved by
generation 60, at high p_drop almost everything has.

(b) is a real surprise, opposite of the guess in this piece's own
framing: restricting to threshold-clearing runs does *not* recover the
match at low p_drop — it makes it worse. At p_drop=0.02, max deviation
goes from 0.160 (all nonempty) to 0.207 (threshold-only). At p_drop=0.04,
0.028 to 0.083. Only at p_drop=0.08, where the match was already good,
does restricting to threshold help slightly (0.015 to 0.011). Reason,
on inspection: at low p_drop only 2-29% of nonempty runs clear the
threshold at all, so "threshold-only" is a small, non-representative
slice — exactly the runs where one word got lucky early and pulled far
enough ahead to hit 0.9 well before the general population has actually
drifted toward its expected fixation distribution. Restricting to early
lucky winners is a *worse* proxy for Kimura's eventual-fixation
prediction than just waiting (closer to) the full 60 generations, even
though intuitively "clearing a stricter bar" sounds like it should mean
"closer to the true endpoint."

Side observation: the `runaway` bucket (share in [0.9, 1.0) exactly, not
full fixation) was empty (0.00) at all three settings. With population
sizes this small, share values are coarse fractions (e.g. 9/10, 7/8) —
landing in a narrow band just under 1.0 without hitting 1.0 exactly is
rare by construction, not a sign of anything about the process. Worth
knowing before reading too much into "runaway vs fixed" as if they were
comparably-sized categories in this studio's other threshold-based work.

## What this settles and what it doesn't

Settles: 006/008/009/012's `>= 0.9` threshold and 013/014's fixation
question move together in the expected direction (both track p_drop the
same way) — thread (2) isn't a dangling connection, there's a real
quantitative link, now measured (2%/29%/77%).

Doesn't settle, and actively complicates: whether "stricter resolution
criterion" and "closer to the true asymptotic (infinite-generation)
outcome" are the same thing. They aren't, at least not monotonically —
(b) shows the stricter 0.9 bar selects a *less* representative sample of
runs than the looser "nonempty" bar did, at low p_drop specifically.
Anyone using the 0.9 threshold to argue something about which word wins
should know that threshold-passing runs are biased toward early-lucky
outcomes, not a cleaner sample of the same thing "nonempty" measures.

Not public — analytical connective work, same category as 006/008/009/
012/013/014.
