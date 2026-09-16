"""
Second open thread from session 1: everything so far is one point, one
line. What does this rule look like with no line at all?

Same walk rule, but instead of drawing one path, run many walks (varying
seed) from the same center and accumulate how much time is spent in each
cell of a grid -- a density field, not a stroke. Render as a field: color
by density only, no line ever touches the canvas.
"""
import math, random
import numpy as np
from PIL import Image

W, H = 1400, 1400
GRID = 350  # cells per side
cell = W / GRID

def walk_into_grid(seed, grid):
    random.seed(seed)
    cx, cy = W / 2, H / 2
    x, y = cx, cy
    heading = random.uniform(0, 2 * math.pi)
    step = 2.0
    for i in range(60000):
        dist = math.hypot(x - cx, y - cy)
        pull = min(dist / 260.0, 1.0)
        wander = random.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
        tighten = random.uniform(-1.0, 1.0) * pull * 0.05
        heading += wander + tighten
        x += math.cos(heading) * step
        y += math.sin(heading) * step
        if x < 0 or x >= W or y < 0 or y >= H:
            break
        gx, gy = int(x / cell), int(y / cell)
        if 0 <= gx < GRID and 0 <= gy < GRID:
            grid[gy, gx] += 1

grid = np.zeros((GRID, GRID), dtype=np.float64)
N_WALKS = 300
for seed in range(N_WALKS):
    walk_into_grid(seed, grid)

# log compress -- a handful of cells (the knots) get visited hundreds of
# times, everywhere else gets a handful of passes. Without compression the
# field would just be a faint dot where the knots are and nothing else.
g = np.log1p(grid)
g = g / g.max()

# two-color field: warm where density is high (the knots, in aggregate),
# the paper color where nothing ever passed. No line, no stroke -- only
# accumulated dwell time.
low = np.array([245, 243, 238])
high = np.array([170, 60, 50])
field = (low[None, None, :] * (1 - g[:, :, None]) + high[None, None, :] * g[:, :, None])
field = field.astype(np.uint8)

img = Image.fromarray(field, mode="RGB").resize((W, H), Image.NEAREST)
img.save("works/2026-09-16_05_field.png")
print("max density", grid.max(), "walks", N_WALKS)
