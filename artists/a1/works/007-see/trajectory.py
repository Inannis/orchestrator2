"""
trajectory.py — session 5. First use of the "eyes" capability the operator
confirmed this session (render an image, then actually open and look at it).
Not a new sweep -- a different way of looking at the same process 001-006
have only ever seen through summary numbers (share, empty, runaway rate).
Draws each surviving word's population count per generation, for one run,
as stacked-color horizontal bands (one PNG per run).
"""
import random
from collections import Counter
from PIL import Image, ImageDraw

GENERATIONS = 60
ORIGINS = {
    "handoff": (
        "I arrive with nothing but what the last one left, "
        "and I leave with nothing but what the next one gets."
    ),
    "flat": "the cat sat on the mat and the dog sat on the rug",
    "no_repeats": "glass water window ladder river copper distance evening",
}

PALETTE = [
    (230, 60, 60), (60, 140, 230), (60, 200, 120), (230, 180, 40),
    (170, 80, 220), (240, 130, 40), (40, 200, 200), (200, 60, 160),
    (140, 140, 140), (100, 220, 60), (220, 220, 60), (60, 100, 200),
]


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


def render(history, orig_words, path, width=900, row_h=10):
    colors = {w: PALETTE[i % len(PALETTE)] for i, w in enumerate(orig_words)}
    max_pop = max(len(gen) for gen in history) or 1
    img = Image.new("RGB", (width, row_h * len(history)), (18, 18, 18))
    draw = ImageDraw.Draw(img)
    for row, gen in enumerate(history):
        counts = Counter(gen)
        x = 0
        for w in orig_words:
            c = counts.get(w, 0)
            if c == 0:
                continue
            wpx = max(1, int(c / max_pop * width))
            draw.rectangle([x, row * row_h, x + wpx, row * row_h + row_h - 1], fill=colors[w])
            x += wpx
    img.save(path)


def main():
    for name, text in ORIGINS.items():
        words = text.split()
        # ratio=0.5 at p_drop=0.08: the region 006 found peaks runaway rate
        history = run_history(words, seed=3, p_drop=0.08, p_dup=0.04)
        render(history, words, f"trajectory_{name}.png")
        print(name, "generations:", len(history), "final size:", len(history[-1]))


if __name__ == "__main__":
    main()
