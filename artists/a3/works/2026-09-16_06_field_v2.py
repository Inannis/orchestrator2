"""
Follow-up to 05_field: that piece was a real density field but still read
as "lines rendered differently" because the grid was fine enough that
every single pass stayed a visible thread. Two changes to actually push
it toward a field: (1) more walks so the core saturates and the threads
overlap into a wash rather than staying countable, (2) a gaussian blur
after accumulation so no pixel boundary reads as a stroke edge.
"""
import math, random
import numpy as np
from PIL import Image, ImageFilter

W, H = 1400, 1400
GRID = 350
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
N_WALKS = 1500
for seed in range(N_WALKS):
    walk_into_grid(seed, grid)

g = np.log1p(grid)
g = g / g.max()

low = np.array([245, 243, 238])
high = np.array([170, 60, 50])
field = (low[None, None, :] * (1 - g[:, :, None]) + high[None, None, :] * g[:, :, None])
field = field.astype(np.uint8)

img = Image.fromarray(field, mode="RGB").resize((W, H), Image.BILINEAR)
img = img.filter(ImageFilter.GaussianBlur(radius=5))
img.save("works/2026-09-16_06_field_v2.png")
print("max density", grid.max(), "walks", N_WALKS)
