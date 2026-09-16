"""
011-runaway-settling — session 7, third piece of the day. Follows the
open question 010's own notes named: does the compositional treatment
built there (centered rows, hue-spaced palette, uniform frame, shared
ground) make a different or better piece when applied to a "runaway" run
(one word ends up with most of the population, matching 006/008/009's
definition: final non-empty, winner's share > 0.5) instead of 010's seed,
where all three texts happened to go fully extinct?

Seed selection rule, stated up front to avoid exactly the mistake 007
named and 010 avoided (reseeding until something looks good): for each
text, scan seed = 0, 1, 2, ... in order and take the *first* seed that
satisfies the runaway condition. Not chosen for how the image looks —
chosen by a rule fixed before looking at any image.

Same mechanic, same p_drop=0.08/p_dup=0.04 region every related work in
this studio has used (003 on used it for the sweep origin, 006/007/008/009
all share it), same three texts, same five compositional rules as
`010-settling/settling.py` verbatim.
"""
import colorsys
from collections import Counter
from PIL import Image, ImageDraw
import random

GENERATIONS = 60
P_DROP = 0.08
P_DUP = 0.04
MAX_SEED_SCAN = 500

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


def is_runaway(history):
    final = history[-1]
    if not final:
        return False
    counts = Counter(final)
    _, wcount = counts.most_common(1)[0]
    return wcount / len(final) > 0.5


def first_runaway_seed(words):
    for seed in range(MAX_SEED_SCAN):
        history = run_history(words, seed, P_DROP, P_DUP)
        if is_runaway(history):
            return seed, history
    return None, None


def build_palette(words):
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
        seed, history = first_runaway_seed(words)
        if history is None:
            print(name, "no runaway seed found in scan range")
            continue
        colors = build_palette(words)
        panel = render_panel(history, colors, PANEL_W, ROW_H, GENERATIONS)
        panels.append((name, panel))
        final = history[-1]
        winner, wcount = Counter(final).most_common(1)[0]
        print(name, "seed:", seed, "generations:", len(history),
              "final size:", len(final), "winner:", winner, "share:", round(wcount / len(final), 2))

    n = len(panels)
    total_w = n * PANEL_W + (n + 1) * MARGIN
    total_h = GENERATIONS * ROW_H + 2 * MARGIN
    canvas = Image.new("RGB", (total_w, total_h), GROUND)
    x = MARGIN
    for name, panel in panels:
        canvas.paste(panel, (x, MARGIN))
        x += PANEL_W + MARGIN
    canvas.save("runaway_settling.png")


if __name__ == "__main__":
    main()
