"""
Contact sheet: same rule as 01_walk, many seeds, small tiles.
I want to see what's typical vs what was a fluke in the first run --
the knot-then-escape. Is that common, rare, the only interesting thing
that can happen, or one version of a family of behaviors?
"""
import math, random
from PIL import Image, ImageDraw

COLS, ROWS = 6, 6
TILE = 220
W, H = COLS * TILE, ROWS * TILE
img = Image.new("RGB", (W, H), (245, 243, 238))
draw = ImageDraw.Draw(img)

def walk(seed, tile_w, tile_h):
    random.seed(seed)
    cx, cy = tile_w / 2, tile_h / 2
    x, y = cx, cy
    heading = random.uniform(0, 2 * math.pi)
    step = 1.2
    pts = [(x, y)]
    for i in range(20000):
        dist = math.hypot(x - cx, y - cy)
        pull = min(dist / 90.0, 1.0)
        wander = random.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
        tighten = random.uniform(-1.0, 1.0) * pull * 0.05
        heading += wander + tighten
        x += math.cos(heading) * step
        y += math.sin(heading) * step
        if x < 4 or x > tile_w - 4 or y < 4 or y > tile_h - 4:
            break
        pts.append((x, y))
    return pts

for r in range(ROWS):
    for c in range(COLS):
        seed = r * COLS + c
        pts = walk(seed, TILE, TILE)
        ox, oy = c * TILE, r * TILE
        for i in range(1, len(pts)):
            t = i / max(len(pts), 1)
            shade = int(50 + 130 * t)
            draw.line(
                [(pts[i-1][0]+ox, pts[i-1][1]+oy), (pts[i][0]+ox, pts[i][1]+oy)],
                fill=(shade, int(shade*0.55), int(shade*0.75)), width=1
            )

img.save("works/2026-09-16_02_contactsheet.png")
