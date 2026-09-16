"""
010-settling — session 7 (second piece this session). Addresses the gap
007's notes named and left open for four sessions: the trajectory images
existed because a process was rendered legibly, not because of any actual
compositional decision. This script makes those decisions instead of
routing around them again.

Same underlying mechanic as 007 (unchanged: independent per-word
drop/dup, p_drop=0.08/p_dup=0.04, same three source texts, same seed=3
per text so the underlying runs are identical to 007's — only how they're
drawn changes). Five specific decisions 007 didn't make:

1. Centered, not left-packed. 007 packed each generation's colored blocks
   flush left in original-word order, which reads as a diagonal collapse
   toward the top-left — that diagonal is an artifact of iteration order,
   not a real feature of the process. Centering each row removes that
   false directionality and lets the actual width (population size) and
   actual composition (which colors, how much) read as the content.

2. A built palette, not arbitrary RGB. 007 assigned PALETTE[i % 12] by
   each word's position in the source sentence — meaningless order.
   Here each word gets a hue evenly spaced around the color wheel by its
   sorted-alphabetical rank (a real, if arbitrary-in-a-different-way,
   ordering rule stated outright), fixed saturation and lightness so the
   set reads as one family rather than 12 unrelated swatches.

3. Uniform frame height across all three (60 generations, always,
   regardless of when a run empties out) so the three panels are
   honestly comparable as a set — how much of the frame is black tells
   you how early each collapsed, which was true information 007's
   variable-height files didn't preserve side by side.

4. A margin and a shared dark ground (not pure black, so lost/empty
   regions read as "ground," not "void") between and around the three
   panels, composited as one image, one piece, not three separate files.

5. Left as run, not staged: still seed=3 for all three, same as 007 —
   picked in 007 "only so there'd be something to look at," not because
   the specific seed matters, and re-used here rather than re-cherry-
   picked, so this is a compositional pass on the same data, not a
   second search for a better-looking run.

Output: `settling.png`, one triptych.
"""
import colorsys
from collections import Counter
from PIL import Image, ImageDraw

GENERATIONS = 60
P_DROP = 0.08
P_DUP = 0.04
SEED = 3

ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}

GROUND = (24, 22, 26)
MARGIN = 24
PANEL_W = 480
ROW_H = 8


def run_history(words, seed, p_drop, p_dup):
    import random
    rng = random.Random(seed)
    words = list(words)
    history = [list(words)]
    for gen in range(GENERATIONS):
        out = []
        for w in words:
            r = rng.random()
            if r < p_drop:
                continue
            out.append(w)
            if p_drop <= r < p_drop + p_dup:
                out.append(w)
        words = out
        history.append(list(words))
        if not words or len(words) > 4000:
            break
    return history


def build_palette(words):
    """Hue evenly spaced by alphabetical rank, fixed sat/light -- one
    family of color, not arbitrary swatches."""
    uniq = sorted(set(words))
    n = len(uniq)
    colors = {}
    for i, w in enumerate(uniq):
        h = i / n
        r, g, b = colorsys.hls_to_rgb(h, 0.55, 0.65)
        colors[w] = (int(r * 255), int(g * 255), int(b * 255))
    return colors


def render_panel(history, colors, width, row_h, generations):
    img = Image.new("RGB", (width, row_h * generations), GROUND)
    draw = ImageDraw.Draw(img)
    max_pop = max((len(gen) for gen in history), default=1) or 1
    for row in range(generations):
        if row >= len(history):
            break
        gen = history[row]
        counts = Counter(gen)
        total_px = 0
        widths = {}
        for w, c in counts.items():
            wpx = max(1, int(c / max_pop * width)) if c else 0
            widths[w] = wpx
            total_px += wpx
        x = (width - total_px) // 2
        for w in sorted(counts, key=lambda w: -counts[w]):
            wpx = widths[w]
            if wpx <= 0:
                continue
            draw.rectangle([x, row * row_h, x + wpx, row * row_h + row_h - 1], fill=colors[w])
            x += wpx
    return img


def main():
    panels = []
    for name, text in ORIGINS.items():
        words = text.split()
        history = run_history(words, SEED, P_DROP, P_DUP)
        colors = build_palette(words)
        panel = render_panel(history, colors, PANEL_W, ROW_H, GENERATIONS)
        panels.append((name, panel))
        print(name, "generations rendered:", GENERATIONS, "history len:", len(history))

    n = len(panels)
    total_w = n * PANEL_W + (n + 1) * MARGIN
    total_h = GENERATIONS * ROW_H + 2 * MARGIN
    canvas = Image.new("RGB", (total_w, total_h), GROUND)
    x = MARGIN
    for name, panel in panels:
        canvas.paste(panel, (x, MARGIN))
        x += PANEL_W + MARGIN
    canvas.save("settling.png")


if __name__ == "__main__":
    main()
