"""
Flagged three times now: color and line weight have never been a
decision, just a default (time-gradient, or whatever ramp made a field
legible). This is the study to actually make that call, instead of
flagging it a fourth time.

Same seed-98 knot path. Four treatments, each testing a different idea
of what the color/weight *should represent*, not just look nice:

  A. time (what I've done every time so far) -- color = when.
  B. speed of turning -- color = how sharply heading is changing, i.e.
     visualize "pull" itself, the actual mechanic of the rule.
  C. single flat ink, weight constant -- the null hypothesis: what if
     color was never doing anything and the line alone carries it.
  D. weight by pull, flat color -- thickness = how constrained the walk
     is right now, thin when free, thick when tightening.

I'm not picking the prettiest. I'm picking whichever one makes the
mechanic of the rule (free near home, constrained far out, knot,
escape) legible to someone who's never read the code.
"""
import math, random
from PIL import Image, ImageDraw

W, H = 1400, 1400
SEED = 98

def walk(seed):
    random.seed(seed)
    cx, cy = W / 2, H / 2
    x, y = cx, cy
    heading = random.uniform(0, 2 * math.pi)
    step = 2.0
    pts = [(x, y, 0.0, 0.0)]  # x, y, pull, turn_amount
    prev_heading = heading
    for i in range(60000):
        dist = math.hypot(x - cx, y - cy)
        pull = min(dist / 260.0, 1.0)
        wander = random.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
        tighten = random.uniform(-1.0, 1.0) * pull * 0.05
        heading += wander + tighten
        turn = abs(heading - prev_heading)
        prev_heading = heading
        x += math.cos(heading) * step
        y += math.sin(heading) * step
        if x < 30 or x > W - 30 or y < 30 or y > H - 30:
            break
        pts.append((x, y, pull, turn))
    return pts

pts = walk(SEED)
paper = (245, 243, 238)

def render(mode):
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    max_turn = max(p[3] for p in pts) or 1.0
    for i in range(1, len(pts)):
        x0, y0, pull0, turn0 = pts[i-1]
        x1, y1, pull1, turn1 = pts[i]
        if mode == "A":  # time
            t = i / len(pts)
            shade = int(50 + 140 * t)
            color = (shade, int(shade*0.5), int(shade*0.7))
            width = 2
        elif mode == "B":  # turn rate = pull, made visible directly
            tnorm = min(turn1 / (max_turn * 0.6), 1.0)
            color = (int(40 + 180*tnorm), int(40 + 40*(1-tnorm)), int(60 + 20*(1-tnorm)))
            width = 2
        elif mode == "C":  # null: flat ink, constant weight
            color = (35, 35, 40)
            width = 2
        elif mode == "D":  # weight by pull, flat color
            color = (90, 40, 50)
            width = max(1, int(1 + pull1 * 4))
        d.line([(x0, y0), (x1, y1)], fill=color, width=width)
    return img

cell = 700
sheet = Image.new("RGB", (cell*2, cell*2), paper)
labels = {"A": "A: color = time", "B": "B: color = turn rate (pull, made visible)",
          "C": "C: flat ink, constant weight (null)", "D": "D: weight = pull, flat color"}
for idx, mode in enumerate(["A", "B", "C", "D"]):
    im = render(mode).resize((cell, cell))
    cx, cy = (idx % 2) * cell, (idx // 2) * cell
    sheet.paste(im, (cx, cy))
    ImageDraw.Draw(sheet).text((cx+10, cy+10), labels[mode], fill=(20, 20, 20))

sheet.save("works/2026-09-16_08_color_study_sheet.png")

# the actual decision, made after looking at the sheet, not before:
# B (turn-rate color) turned out to saturate almost everywhere except the
# escape line, so it reads as barely-two-tone -- the mechanic it was
# supposed to expose got flattened out by my own scaling choice.
# D (weight = pull) is the one that's actually legible without the code:
# thin where the walk is free, visibly thickening exactly where it starts
# committing to the escape. That's the rule, seen, not just colored.
CHOSEN = "D"
render(CHOSEN).save(f"works/2026-09-16_08_color_study_chosen_{CHOSEN}.png")
print("saved sheet and chosen:", CHOSEN)
