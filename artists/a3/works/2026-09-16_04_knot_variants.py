"""
Open question from session 1: is the three-lobe knot a property of seed 98
specifically, or of the rule in general? Re-run the same search from
2026-09-16_03_knots.py, but instead of saving only the winner, render the
top 6 scoring seeds side by side so I can actually compare lobe structure
by eye.
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
    results.append((score, seed))
results.sort(reverse=True)
top6 = [s for _, s in results[:6]]
print("top 6 seeds:", top6)

cell = 700
cols = 3
rows = 2
sheet = Image.new("RGB", (cell*cols, cell*rows), (245, 243, 238))

for idx, seed in enumerate(top6):
    pts = walk(seed)
    cimg = Image.new("RGB", (W, H), (245, 243, 238))
    cdraw = ImageDraw.Draw(cimg)
    for i in range(1, len(pts)):
        t = i / len(pts)
        shade = int(50 + 140 * t)
        cdraw.line([pts[i-1], pts[i]], fill=(shade, int(shade*0.5), int(shade*0.7)), width=2)
    cimg = cimg.resize((cell, cell))
    cx = (idx % cols) * cell
    cy = (idx // cols) * cell
    sheet.paste(cimg, (cx, cy))
    d = ImageDraw.Draw(sheet)
    d.text((cx+10, cy+10), f"seed {seed} score {results[idx][0]}", fill=(20,20,20))

sheet.save("works/2026-09-16_04_knot_variants.png")
print("saved")
