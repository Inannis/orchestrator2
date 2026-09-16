"""
Session 4, third and last test tonight. The reader's third suggestion,
after image (no center) and graph (a center available but not
required): a crowd. The difference that matters isn't spatial, it's
agency -- a pixel and a graph node just hold whatever value they're
given. A person can refuse.

Setup: N agents scattered on a plane, each with a fixed, randomly
assigned STUBBORNNESS in [0, 1] -- not tied to position, not tied to
distance from the anchor, just a private property each agent has
independent of the rule being imposed on it. Same relay mechanism as
before (each pass, probability of slipping to a neighbor's value
instead of holding), same distance-keyed base slip rate (low near an
arbitrary anchor point, high far from it) -- but now each agent's
actual slip probability is the base rate MULTIPLIED by (1 -
stubbornness). A stubborn agent resists the imposed rule regardless of
where it stands. A compliant agent (stubbornness near 0) follows the
spatial rule exactly, same as a pixel or graph node would.

Question: does agency (independent of position) break the
free-near/rigid-far pattern, weaken it, or leave it untouched? Unlike
the graph piece, this is the first test where something in the
material can act *against* the rule rather than just having or
lacking a privileged position.
"""
import numpy as np
from PIL import Image, ImageDraw

rng = np.random.default_rng(4)

N_AGENTS = 300
PASSES = 40
FIELD = 400

pos = rng.uniform(0, FIELD, (N_AGENTS, 2))
stubbornness = rng.uniform(0, 1, N_AGENTS)  # agency, independent of position

anchor = np.array([FIELD * 0.7, FIELD * 0.25])  # arbitrary, as before
dist = np.linalg.norm(pos - anchor, axis=1)
dist_norm = dist / dist.max()
base_rate = 0.01 + 0.35 * dist_norm  # same shape as prior pieces

# neighbors: k-nearest for the relay to draw a slipped value from
# (plain numpy pairwise distance -- N_AGENTS is small enough this is fine)
pairwise = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=2)
neighbor_idx = np.argsort(pairwise, axis=1)[:, :6]  # includes self at [:,0]

def run_relay(effective_rate, seed):
    r = np.random.default_rng(seed)
    values = np.arange(N_AGENTS)
    original = values.copy()
    hold_curve = []
    for p in range(PASSES):
        new_values = values.copy()
        roll = r.random(N_AGENTS)
        slip_mask = roll < effective_rate
        for i in np.where(slip_mask)[0]:
            choices = neighbor_idx[i][1:]
            new_values[i] = values[r.choice(choices)]
        values = new_values
        hold_curve.append(np.mean(values == original))
    return values, hold_curve

rate_agentic = base_rate * (1 - stubbornness)
rate_compliant = base_rate  # control: no agency, pure spatial rule (like the graph piece)

final_agentic, hold_agentic = run_relay(rate_agentic, seed=11)
final_compliant, hold_compliant = run_relay(rate_compliant, seed=11)

held_agentic = (final_agentic == np.arange(N_AGENTS))
held_compliant = (final_compliant == np.arange(N_AGENTS))

def near_far(held, dist_norm):
    near = held[dist_norm < 0.33]
    far = held[dist_norm > 0.66]
    return near.mean(), far.mean()

na, fa = near_far(held_agentic, dist_norm)
nc, fc = near_far(held_compliant, dist_norm)

# Does stubbornness alone (ignoring position) predict holding, in the agentic run?
stub_held = stubbornness[held_agentic]
stub_slipped = stubbornness[~held_agentic]

with open("2026-09-16_18_relay_crowd_log.txt", "w") as f:
    f.write("Relay on a crowd -- agency vs pure spatial rule, session 4\n\n")
    f.write(f"agents: {N_AGENTS}, field: {FIELD}x{FIELD}, passes: {PASSES}\n")
    f.write(f"anchor (arbitrary): {anchor.tolist()}\n\n")
    f.write("hold rate by pass, agentic (rate * (1-stubbornness)) vs compliant control:\n")
    f.write(f"{'pass':>5} {'agentic':>10} {'compliant':>10}\n")
    for p in range(0, PASSES, 4):
        f.write(f"{p+1:>5} {hold_agentic[p]:>10.3f} {hold_compliant[p]:>10.3f}\n")
    f.write(f"\nfinal hold, agentic:   {hold_agentic[-1]:.3f}\n")
    f.write(f"final hold, compliant: {hold_compliant[-1]:.3f}\n\n")
    f.write(f"agentic   -- near-anchor hold: {na:.3f}, far-anchor hold: {fa:.3f}\n")
    f.write(f"compliant -- near-anchor hold: {nc:.3f}, far-anchor hold: {fc:.3f}\n\n")
    f.write(f"mean stubbornness of held agents (agentic run):    {stub_held.mean():.3f}\n")
    f.write(f"mean stubbornness of slipped agents (agentic run): {stub_slipped.mean():.3f}\n")
    corr = np.corrcoef(dist_norm, stubbornness)[0, 1]
    f.write(f"\n(stubbornness assigned independent of position -- correlation with distance: {corr:.3f}, should be ~0)\n")

# Render: two panels, position = agent position, color = held/slipped,
# marker size in agentic panel scaled by stubbornness so agency is
# visible, not just inferred from the log.
img = Image.new("RGB", (FIELD * 2 + 40, FIELD), "#0b0f14")
draw = ImageDraw.Draw(img)

for offset, held, sizes_from_stub, title_anchor in [
    (0, held_compliant, False, anchor),
    (FIELD + 40, held_agentic, True, anchor),
]:
    for i in range(N_AGENTS):
        x, y = pos[i]
        r = 2 + (4 * stubbornness[i] if sizes_from_stub else 0)
        color = (232, 195, 74) if held[i] else (36, 52, 71)
        draw.ellipse([offset + x - r, y - r, offset + x + r, y + r], fill=color)
    ax, ay = title_anchor
    draw.ellipse([offset + ax - 6, ay - 6, offset + ax + 6, ay + 6], outline=(255, 60, 60), width=2)

img.save("2026-09-16_18_relay_crowd.png")
print("done")
