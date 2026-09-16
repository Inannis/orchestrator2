"""
First mark. No plan beyond: a single process, watched, not designed for prettiness.

A point walks. At each step it turns by an angle that depends on how far it
already is from where it started -- so early steps are freer, and as it
drifts outward the walk tightens into arcs, like something learning
gravity it didn't have at the start.
"""
import math, random
from PIL import Image, ImageDraw

random.seed(16)

W, H = 1400, 1400
img = Image.new("RGB", (W, H), (245, 243, 238))
draw = ImageDraw.Draw(img)

cx, cy = W / 2, H / 2
x, y = cx, cy
heading = random.uniform(0, 2 * math.pi)
step = 2.2

points = [(x, y)]
for i in range(30000):
    dist = math.hypot(x - cx, y - cy)
    pull = min(dist / 500.0, 1.0)          # 0 near center, 1 far out
    wander = random.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
    tighten = random.uniform(-1.0, 1.0) * pull * 0.05
    heading += wander + tighten
    x += math.cos(heading) * step
    y += math.sin(heading) * step
    if x < 20 or x > W - 20 or y < 20 or y > H - 20:
        break
    points.append((x, y))

for i in range(1, len(points)):
    t = i / len(points)
    shade = int(60 + 120 * t)
    draw.line([points[i - 1], points[i]], fill=(shade, int(shade*0.6), int(shade*0.75)), width=1)

img.save("works/2026-09-16_01_walk.png")
print(f"{len(points)} points, ended at distance {math.hypot(x-cx,y-cy):.1f} from center")
