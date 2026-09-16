"""
Follow-up to 08_color_study: chose weight-by-pull (D) on seed 98 alone.
Flagged as open: does it hold up on a walk with a different lobe count,
and on a walk that never knots at all? Testing three: seed 98 (3 lobes,
already seen), seed 104 (1 lobe, from the 04 comparison), and a seed that
scored ~0 in the knot search -- i.e. a walk that just leaves.
"""
import math, random
from PIL import Image, ImageDraw

W, H = 1400, 1400
paper = (245, 243, 238)

def walk(seed):
    random.seed(seed)
    cx, cy = W / 2, H / 2
    x, y = cx, cy
    heading = random.uniform(0, 2 * math.pi)
    step = 2.0
    pts = [(x, y, 0.0)]
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
        pts.append((x, y, pull))
    return pts

def render(seed):
    pts = walk(seed)
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    for i in range(1, len(pts)):
        x0, y0, _ = pts[i-1]
        x1, y1, pull1 = pts[i]
        width = max(1, int(1 + pull1 * 4))
        d.line([(x0, y0), (x1, y1)], fill=(90, 40, 50), width=width)
    return img

# find a low-scoring (non-knotting) seed quickly
def score(pts):
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

low_seed = None
for s in range(200):
    p = walk(s)
    if len(p) > 400 and score(p) == 0:
        low_seed = s
        break

seeds = [98, 104, low_seed]
cell = 700
sheet = Image.new("RGB", (cell*3, cell), paper)
for idx, s in enumerate(seeds):
    im = render(s).resize((cell, cell))
    sheet.paste(im, (idx*cell, 0))
    label = f"seed {s}" + (" (no knot)" if idx == 2 else "")
    ImageDraw.Draw(sheet).text((idx*cell+10, 10), label, fill=(20,20,20))

sheet.save("works/2026-09-16_09_weight_check.png")
print("no-knot seed used:", low_seed)
