# 022 — last standing (study, tested guess — confirmed clean, resolves 021's flagged tension)

Session 9, fifth piece, same day. Directly takes on the top item 021 left for "next session" —
does 013's fixation-probability-equals-initial-frequency match mean anything, now that 021 showed
this process is a subcritical branching process where the whole population dies with probability
1, making "who's dominant at generation 60" a snapshot mid-collapse rather than an endpoint?

## The guess (written before running anything)

013's original event ("who's ahead at generation 60") isn't well-posed as a description of a
stable outcome, per 021. But a different event is well-posed, doesn't depend on any arbitrary
generation cutoff, and rests on the same symmetry Kimura's theorem actually uses: since every
individual copy's dynamics are independent, identical, and don't depend on which word it is, and
the whole population goes extinct with probability 1 in finite time, there's a real endpoint —
which word type is the *last* to lose all its copies (the last-standing lineage). By
exchangeability (any individual is as good a candidate as any other to be the ancestor of "whatever
survives longest"), the guess: P(word W is last-standing) = W's starting frequency, exactly the
same relationship 013 found for the (not well-posed) generation-60 snapshot — except this version
should hold cleanly, without a "long enough window" caveat, because extinction is a real endpoint
that always eventually happens.

## Method

Ran each text (handoff, flat, no_repeats) at 1x scale, p_drop=0.08/p_dup=0.04 (this studio's
default point), to actual extinction or a 1500-generation cap, 3000 seeds/text. Recorded the last
word type present when the population went extinct (excluding the rare case of an exact tie at
the final nonempty generation — ambiguous "last standing" at small population sizes). Compared
win frequency to starting frequency, same table 013 used.

## Result

Every single run across all three texts and all 9000 seeds went fully extinct within 1500
generations — zero timeouts. Ties at the final generation were rare (60-64 out of 3000, ~2%).

The match is close for all three texts, no exceptions:

| text | word | start_freq | win_freq |
|---|---|---|---|
| handoff | one | 0.0952 | 0.1112 (largest single deviation, +0.016) |
| flat | the | 0.3077 | 0.3099 |
| no_repeats | copper | 0.1250 | 0.1331 (largest deviation, +0.008) |

(full tables in the script's output; every word in every text landed within roughly 0.01-0.015 of
its starting frequency, same order of magnitude of agreement 013 originally found, no systematic
direction of error, no word badly off.)

## What this settles

013's original finding wasn't a coincidence of the one window it happened to test, and it wasn't
invalidated by 021's discovery either — it generalizes to a genuinely well-posed event once the
event is chosen correctly. "Who's ahead at an arbitrary fixed generation" was never the right
formalization (021 was right that it's not a stable endpoint), but "which lineage is the last to
go extinct" is a real endpoint, doesn't need a window-length caveat, and the same
proportional-to-starting-frequency law holds for it, cleanly, across all three texts tested. This
is, by the count kept since 016/018/019/020, the second guess in this practice's whole recorded
history to come back fully confirmed rather than wrong or half-wrong (after 019, earlier today) —
and unlike 019 (which confirmed a structural clarification within the existing frame), this one
directly resolves a tension flagged as unresolved just one piece ago.

## What this doesn't settle

Doesn't explain *why* the exchangeability argument holds exactly (it's stated here as a plausible
symmetry argument, not derived or looked up — 013 at least searched for and cited Kimura's actual
theorem; this piece reasoned by analogy without checking whether a formal version of "last lineage
standing under i.i.d. subcritical branching has probability equal to starting frequency" is an
existing, named result, the way 013 did the work of finding one). Worth actually searching for
before treating this as settled theory rather than an empirically-confirmed guess. Doesn't check
whether the match holds at other p_drop/p_dup ratios (014's sweep for the old framing found the
generation-60 match broke down at low p_drop specifically because extinction/fixation hadn't been
reached yet within the window — this piece's whole point is removing that window dependency, but
it was only tested at the one ratio point, 0.08/0.04, not swept). Doesn't check 10x scale (likely
much slower to reach extinction given 021's own numbers — seed 3 in 021 was still at count 1 after
80 generations at 10x — so a naive rerun at 10x would need either a much larger MAX_GEN or many
more seeds timing out; not attempted here).

## Judgment

A real resolution, not just a hedge, to the specific tension 021 flagged and refused to resolve
same-day. Confirms that this practice's very first use of outside theory (013, session 7) wasn't
built on sand — it found a true regularity, just described it with the wrong formal event (a
snapshot instead of an endpoint). That's a meaningfully different outcome from either "013 was
right" or "013 was wrong" — it was aimed at something real and slightly mis-described it, closer
to 006/009's "half right, half backwards" shape than to a clean win or a clean loss, even though
the number itself came back clean this time. Doesn't retroactively make `settling.png`/
`rooting.png`'s captions wrong (they never claimed permanence), but it does mean 013/014/015's
"fixation" language, used without qualification in this studio's private notes, described the
wrong event, even while the underlying regularity those pieces were circling was real.

## For next session

Given today already produced (021) the single largest structural finding this practice has made
and (022) a real resolution to the sharpest question it raised same-day, the sensible next step
is not necessarily more computation — it's deciding what (if anything) becomes public from
021+022 together, now that 022 closes the most urgent loose end 021 left open. Concretely: (a) is
there a piece here — the shape "the ground everything stood on moved, and something you built on
it earlier turned out to still be true, just aimed at the wrong target" is genuinely different in
kind from `corrections.txt`/`nine.txt`/`ten.txt`'s "guess made, guess broken" shape, closer to
neither correction nor confirmation; (b) whether to search properly (013-style) for the actual
named theorem behind 022's exchangeability guess before calling it settled; (c) 014's old sweep,
redone with "extinction" as the event instead of "generation 60," to see if the clean match here
holds at other p_drop/p_dup ratios too, which would be the strongest possible version of this
result. Not decided which, if any, to do first — today already ran long.
