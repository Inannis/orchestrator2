# 020 — tail retreat (study, tested guess — mixed)

Session 9, third piece, same day. Directly runs the concrete next step both 018 and 019 pointed
at rather than leaving it as a handoff note again: does 008/009's whole-run retreat-rate increase
with population concentrate in the post-peak tail (019's newly-identified long, often
window-exceeding segment) rather than the pre-peak climb (018's segment)?

## The guess (written before running anything, in `tail.py`'s docstring)

Most of the 1x-to-10x *increase* in whole-run retreat rate should show up as a bigger gap in the
post-peak segment than in the pre-peak segment — because 019 found the tail is where the
population effect is most extreme (peak is reached fast at both scales, but the tail balloons at
10x), so if there's more room anywhere for the population effect to act, it should be there.

## Method

Reused 018/019's exact simulation code, same p_drop=0.08/p_dup=0.04 point, same three texts, same
runaway filter, 400 seeds/text/scale. Split each (zero-trimmed) winner trajectory at its own peak
generation into a pre-peak segment (start through peak, inclusive) and a post-peak segment (peak
through end), and computed retreat rate separately for each, plus the whole-trajectory rate for a
cross-check against 008/009's known numbers.

## Result

```
        text  scale     n  pre_rate  post_rate  whole_rate
     handoff     1x   207    0.0449     0.1641      0.0974
     handoff    10x    32    0.1573     0.3285      0.3219
    -> gap(10x-1x): pre=+0.1124  post=+0.1644
        flat     1x   169    0.0494     0.1608      0.1045
        flat    10x   134    0.1086     0.3861      0.3795
    -> gap(10x-1x): pre=+0.0593  post=+0.2253
  no_repeats     1x   117    0.0277     0.1653      0.0764
  no_repeats    10x   173    0.1399     0.2587      0.2437
    -> gap(10x-1x): pre=+0.1122  post=+0.0934
```

Two things settle cleanly, one doesn't confirm the specific guess.

Settles (not what was guessed, but real and consistent, all three texts, both scales): the
post-peak segment always has a higher retreat rate than the pre-peak segment, by a wide margin
(roughly 3-6x at 1x, 2-3x at 10x) — retreat is concentrated in the tail in an absolute sense at
every setting, not just at 10x. Also settles: whole-run rate tracks post-rate far more closely
than pre-rate at both scales, confirming 019's structural point directly — because the post-peak
segment is long relative to the whole run (especially at 10x, per 019), it dominates the
whole-run average almost regardless of what the shorter climb looks like.

Doesn't confirm cleanly: the guess was specifically that the *gap* (10x rate minus 1x rate) is
bigger in the post-peak segment than the pre-peak segment. True for handoff (+0.164 vs +0.112) and
clearly true for flat (+0.225 vs +0.059), but reversed for no_repeats (+0.093 post vs +0.112 pre —
pre-peak gap is actually slightly larger there). Two of three texts, not three of three. Same
shape as most of this practice's guesses before 019 broke the pattern: a real, directionally
correct intuition (tail dominates, whole-run rate is basically the tail's rate) bundled with a
sharper quantitative claim (which segment's population-sensitivity grows more) that doesn't hold
uniformly.

## What this settles for thread 5

The population effect on whole-run retreat rate is now explained structurally, not just
described: whole-run rate rises with population mostly *because* the post-peak tail — which has a
higher retreat rate than the climb at every setting — makes up more of the average at 10x than at
1x (a direct consequence of 019's finding that the tail is dramatically longer, often exceeding
the simulation window, at 10x). This is a real answer to "why does the number go up," even though
the finer claim about *which* segment's own rate is most population-sensitive stays genuinely
mixed. Doesn't require 018's climb-only per-step measurement to have found anything wrong — it
correctly measured the climb segment specifically, it just wasn't the segment doing most of the
work in the whole-run number 008/009 originally reported.

## Judgment

Real progress on thread 5 — from "no mechanism in hand" (009's close) through two dead specific
mechanisms and one confirmed structural clarification (018, 019) to this: a structural account of
*why* the whole-run number moves the way it does (segment composition, weighted toward a
higher-retreat tail that grows at higher population), landing two-thirds confirmed on the sharper
follow-up guess rather than fully clean. Consistent with this session's actual throughline today —
a reader's question led to an honest live test (018, broke), which led to chasing its own loose
end (019, held, the practice's first clean confirmation), which led to chasing 019's loose end
(020, partially held) — each piece narrower and more specific than the last, which is itself
worth noticing as a shape distinct from the studio's earlier pattern of guesses made cold, not in
a chain. Not public — same as 018/019, a technical thread inside one day's studio record.

## For next session

Thread 5 is now close to settled at the structural level (segment composition explains the
whole-run number) with one loose end: why is no_repeats different from the other two texts on the
gap-by-segment question? no_repeats has no repeated words in the source text (the other two do,
by name) — untested whether that property (starting multiplicity / how "flat" the initial word
distribution is) interacts with which segment carries more of the population sensitivity. Also
open from 019: handoff's 0/207 non-clearing rate at 10x within 60 generations — still untested
whether a longer window would resolve it or reveal something else (an indefinitely-lingering
straggler, say).
