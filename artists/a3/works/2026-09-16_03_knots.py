"""
Following the contact sheet: the moment I kept looking at was the knot --
where pull gets strong enough that the walk coils before it finds a
straight line out. Most seeds don't knot; they just leave. So: search
many seeds at full scale, keep only the ones that coil (i.e. that
revisit their own neighborhood) before they escape the frame.
A rule about what counts as "escape" makes this a bit stricter and less
forgiving than the contact sheet -- I want fewer, more considered results,
not a bigger bucket.
"""
import math, random
from PIL import Image, ImageDraw

W, H = 1400, 1400

def walk(seed):
    random.seed(seed)
    cx, cy = W / 2, H / 2
    x, y = cx, cy
    heading = random.uniform(0, 2 * math.pi)
    step = 2.0
    pts = [(x, y)]
    max_dist_reached_early = 0
    for i in range(60000):
        dist = math.hypot(x - cx, y - cy)
        pull = min(dist / 260.0, 1.0)
        wander = random.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
        tighten = random.uniform(-1.0, 1.0) * pull * 0.05
        heading += wander + tighten
        x += math.cos(heading) * step
        y += math.sin(heading) * step
        if x < 30 or x > W - 30 or y < 30 or y > H - 30:
            break
        pts.append((x, y))
    return pts

def self_proximity_score(pts):
    # crude: sample every 8th point, count close non-adjacent pairs
    sample = pts[::8]
    n = len(sample)
    if n < 20:
        return 0
    close = 0
    for i in range(n):
        for j in range(i + 15, n):
            dx = sample[i][0] - sample[j][0]
            dy = sample[i][1] - sample[j][1]
            if dx*dx + dy*dy < 25*25:
                close += 1
    return close

results = []
for seed in range(200):
    pts = walk(seed)
    if len(pts) < 400:
        continue
    score = self_proximity_score(pts)
    results.append((score, seed, len(pts)))

results.sort(reverse=True)
print("top candidates (score, seed, n_points):")
for r in results[:8]:
    print(r)

best_score, best_seed, _ = results[0]
pts = walk(best_seed)
img = Image.new("RGB", (W, H), (245, 243, 238))
draw = ImageDraw.Draw(img)
for i in range(1, len(pts)):
    t = i / len(pts)
    shade = int(50 + 140 * t)
    draw.line([pts[i-1], pts[i]], fill=(shade, int(shade*0.5), int(shade*0.7)), width=2)
img.save(f"works/2026-09-16_03_knot_seed{best_seed}.png")
print("saved seed", best_seed)
