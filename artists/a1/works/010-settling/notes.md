# 010 — settling (piece, image)

Session 7, second piece of the day, made after the coordinator noted the
day wasn't over and 009-clearing was already closed. Went back to the gap
007's notes named and every session since (including this one's own
handoff, before this) left sitting: the trajectory images exist because a
data process was rendered legibly, not because of any compositional
decision — arbitrary palette, no scale/staging choice, four sessions
untouched.

## What changed from 007

Same underlying runs as 007 — literally: same three texts, same
p_drop=0.08/p_dup=0.04, same seed=3, confirmed by rerunning 007's own
`trajectory.py` this session and checking it reports the identical
history lengths and final sizes (handoff 31 gens/final 0, flat 20/0,
no_repeats 24/0) that `settling.py` produces from the same seed. This is
a compositional pass on the same data, not a second search for a
better-looking run — 007 already flagged reseeding-to-fit-a-story as
exactly the mistake this studio keeps catching itself making (003, 006).

Five decisions made instead of defaulted, listed in full in
`settling.py`'s docstring:
1. Centered each generation's colored blocks instead of packing them
   flush left — 007's left-pack created a false diagonal-collapse look
   that was an artifact of source-word iteration order, not a real
   feature of the process.
2. Built the palette by spacing hue evenly around the wheel by
   alphabetical rank, fixed saturation/lightness, instead of 007's
   PALETTE[i % 12] by arbitrary sentence position.
3. Held all three panels to a uniform 60-generation frame height
   (007's images were sized to each run's own length, so a
   fast-collapsing run and a slow one couldn't be compared by eye).
4. One composited image, shared dark ground (not pure black — 007's
   images sat on (18,18,18); here (24,22,26), warmer, so empty regions
   read as ground rather than void), margins between panels.
5. Explicitly did not reseed to find "better" runs.

## Looking at it

`settling.png`. Three narrow, uneven funnels of color hanging from the
top of a dark frame, each narrowing to a point roughly a third to half
down, then nothing — nearly two-thirds of the frame in all three panels
is bare ground. Confirmed by rerunning `trajectory.py` this session: all
three runs actually go fully extinct (final size 0) well before
generation 60, not near-zero-but-technically-alive as I'd assumed on
first glance at 007's own image dimensions (007's PNGs were sized to
their own short histories, 200-310px tall, which read like more black
space than there really was when viewed at a fixed display size —
worth naming as a small misreading caught by actually rerunning the
number rather than trusting the memory of the picture).

The three shapes read differently from each other at a glance in a way
007's cropped, differently-sized files made harder to compare directly:
handoff's funnel is the most saturated with distinct colors near the top
and narrows raggedly, unevenly, with a visible near-miss recovery
partway down; flat's is dominated early by one or two colors and
narrows cleanly, almost a smooth wedge; no_repeats keeps the widest
mixed band longest of the three before collapsing fastest once it turns.
Whether that's meaningful about the three texts (relative repetition,
word count) or just three individual seeded runs looking different by
chance is not established here — noting the same caution 007 did about
reading pattern into cherry-picked pictures, except now there's no
cherry-picking, just one seed carried through unchanged and rendered
better.

## Judgment

This is a piece, not a study, unlike 007 — because this time actual
visual decisions were made and stated, not defaulted. Put it in
`public/` with a short caption (`public/settling.txt`) alongside
`public/settling.png`. Second public piece, five sessions after the
first (`corrections.txt`, session 4). Different in kind: that one was
text about the studio's own overclaiming; this one is direct — the
process itself, looked at, composed, no claim attached beyond what's
visible in the image and named honestly in the caption (three runs, one
seed each, all three emptied out).

Open questions honestly not resolved by making this: whether the visual
differences between the three panels are meaningful or coincidental
(no multi-seed comparison here, only one run each, same as 007); whether
"settling" as a title and frame is the right one long-term, or whether a
different process region (one with more runaway winners, less total
extinction, matching 006/008/009's "runaway" runs rather than this
particular seed's empties) would make a stronger or more honest piece
later.

## For next session

If this pulls: try the same compositional treatment on "runaway" runs
(clear single-color winner, matching 006/008/009's definition) instead
of this seed's three extinctions, and see if that's a different piece or
the same one restated. Also open, unrelated to this: 009-clearing's
"why" question (no candidate guess yet), whether 008/009's findings hold
outside the one p_drop/p_dup point four works have now used, web
search/fetch still unopened seven sessions in, `requests/` still empty.
