"""
Session 4, closing the loop. Tonight's crowd piece
(2026-09-16_18_relay_crowd.py) added a private property -- stubbornness,
assigned independent of position -- that resists the rule without
following it, and found it doesn't cancel the spatial pattern, it adds
a second axis on top. Open item from that piece: try the same idea on
the ORIGINAL material, the walk from session 1, untouched since. Full
circle -- three sessions of moving the rule onto new material, now one
piece moving new material's finding back onto the oldest material.

The original walk (2026-09-16_01_walk.py): heading changes by
"wander" near the start point, by "tighten" (the pull toward an arc)
far from it. Here each walk gets a fixed stubbornness in [0,1],
independent of anything about its own run (assigned before the walk
starts), that scales down how much the tighten term can act --
same mechanism as the crowd piece's (1 - stubbornness) multiplier.
A stubborn walk resists arcing even once it's far from home; a
compliant one (stubbornness 0) is identical to the session-1 rule.

Measure: does a walk with high stubbornness actually escape the frame
differently than a low-stubbornness walk -- more steps taken, less
tightly arced, straighter? Run a grid (10 seeds x 5 stubbornness
levels) and compare, the same experimental shape as the crowd piece's
agentic-vs-compliant comparison.
"""
import math, random
from PIL import Image, ImageDraw

W, H = 1400, 1400
cx, cy = W / 2, H / 2
STEP = 2.2
STUBBORNNESS_LEVELS = [0.0, 0.25, 0.5, 0.75, 0.95]
SEEDS = range(10)

def run_walk(seed, stubbornness, max_steps=30000):
    rng = random.Random(seed)
    x, y = cx, cy
    heading = rng.uniform(0, 2 * math.pi)
    points = [(x, y)]
    total_turn = 0.0
    for i in range(max_steps):
        dist = math.hypot(x - cx, y - cy)
        pull = min(dist / 500.0, 1.0)
        wander = rng.uniform(-1.0, 1.0) * (1.0 - pull) * 0.6
        tighten = rng.uniform(-1.0, 1.0) * pull * 0.05 * (1.0 - stubbornness)
        d_heading = wander + tighten
        heading += d_heading
        total_turn += abs(d_heading)
        x += math.cos(heading) * STEP
        y += math.sin(heading) * STEP
        if x < 20 or x > W - 20 or y < 20 or y > H - 20:
            break
        points.append((x, y))
    return points, dist, total_turn

results = {}
for s in STUBBORNNESS_LEVELS:
    steps_list, dist_list = [], []
    for seed in SEEDS:
        pts, final_dist, total_turn = run_walk(seed * 7 + 1, s)
        steps_list.append(len(pts))
        dist_list.append(final_dist)
    results[s] = {
        "mean_steps": sum(steps_list) / len(steps_list),
        "mean_final_dist": sum(dist_list) / len(dist_list),
    }

with open("2026-09-16_19_walk_stubbornness_log.txt", "w") as f:
    f.write("Stubbornness on the original walk -- session 4\n\n")
    f.write("Each walk's 'tighten' response to distance-from-start is scaled\n")
    f.write("by (1 - stubbornness); 'wander' is untouched. 10 seeds per level.\n\n")
    f.write(f"{'stubbornness':>13} {'mean steps to exit':>20} {'mean exit distance':>20}\n")
    for s in STUBBORNNESS_LEVELS:
        r = results[s]
        f.write(f"{s:>13.2f} {r['mean_steps']:>20.0f} {r['mean_final_dist']:>20.1f}\n")

# Render: one walk per stubbornness level, same seed, side by side,
# so the difference is visible as line shape, not just numbers.
PANEL = 320
img = Image.new("RGB", (PANEL * len(STUBBORNNESS_LEVELS), PANEL), (245, 243, 238))
draw = ImageDraw.Draw(img)
SEED_FOR_RENDER = 3 * 7 + 1

for idx, s in enumerate(STUBBORNNESS_LEVELS):
    pts, _, _ = run_walk(SEED_FOR_RENDER, s, max_steps=30000)
    ox = idx * PANEL
    # scale to fit panel
    scale = PANEL / W
    scaled = [(ox + (x) * scale, (y) * scale) for x, y in pts]
    for i in range(1, len(scaled)):
        t = i / len(scaled)
        shade = int(60 + 120 * t)
        draw.line([scaled[i - 1], scaled[i]], fill=(shade, int(shade * 0.6), int(shade * 0.75)), width=1)
    draw.text((ox + 6, 6), f"stub={s}", fill=(20, 20, 20))

img.save("2026-09-16_19_walk_stubbornness.png")
print("done")
