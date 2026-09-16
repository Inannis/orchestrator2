"""
Session 4. Two things at once:
1. New vocabulary (see reference/vocabulary.md): "relay" instead of
   "copy decay," "pass" instead of "generation," "slip" instead of
   "copy error," "hold" instead of "survival."
2. The reader's question (inbox/reading-2026-09-16.md, part 3): every
   material used so far -- a walk, a poem's word order, a copied
   string -- already has a built-in center or sequence. What happens
   on something with no natural center at all?

An image has no natural center in the sense a walk has a start point
or a poem has a midpoint. Any "home" imposed on an image is imposed,
not found. So this piece makes that arbitrariness the subject instead
of hiding it: the same synthetic image (no story, no privileged point
in the generating code) is relayed twice, pass after pass, pixel
blocks slipping with a small per-pass chance -- once with a UNIFORM
slip rate (no home at all), once with slip rate keyed to distance from
a point stamped onto the image *after* it was drawn, arbitrarily,
by this script, nowhere the image's own geometry suggests.

If the free-near/rigid-far pattern still shows up on the anchored
version, that tells me something: the method doesn't need a material
with a real center, it just needs someone to pick a point and commit
to it. The center was never found in the walk or the poem either --
it was always just the first thing generated, or the geometric
midpoint of a word list. This piece stops pretending that's different
from stamping a point on a blank image.
"""
import numpy as np
from PIL import Image

rng = np.random.default_rng(4)

SIZE = 240
BLOCK = 8
N = SIZE // BLOCK  # blocks per side
PASSES = 40

def make_source():
    """A synthetic image with no privileged point in how it's drawn:
    concentric-free geometric noise, built from independent random
    rectangles, not from any single center."""
    img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    for _ in range(60):
        x0, y0 = rng.integers(0, SIZE, 2)
        w, h = rng.integers(10, 60, 2)
        color = rng.integers(40, 230, 3)
        x1, y1 = min(SIZE, x0 + w), min(SIZE, y0 + h)
        img[y0:y1, x0:x1] = color
    return img

def relay_step(blocks, slip_rate, rng):
    """One pass: each block, independently, with probability
    slip_rate, is replaced by a slightly shifted copy of a
    neighboring block (a 'slip' -- information moves sideways and
    degrades, never referencing the original)."""
    out = blocks.copy()
    n = blocks.shape[0]
    for i in range(n):
        for j in range(n):
            if rng.random() < slip_rate[i, j]:
                di, dj = rng.integers(-1, 2, 2)
                ni, nj = np.clip(i + di, 0, n - 1), np.clip(j + dj, 0, n - 1)
                jitter = rng.integers(-15, 16, 3)
                out[i, j] = np.clip(blocks[ni, nj].astype(int) + jitter, 0, 255)
    return out

def image_to_blocks(img):
    return img.reshape(N, BLOCK, N, BLOCK, 3).mean(axis=(1, 3)).astype(np.uint8)

def blocks_to_image(blocks):
    return np.repeat(np.repeat(blocks, BLOCK, axis=0), BLOCK, axis=1)

source = make_source()
Image.fromarray(source).save("2026-09-16_16_relay_source.png")
blocks0 = image_to_blocks(source)

# Uniform relay: no home, same slip rate everywhere.
uniform_rate = np.full((N, N), 0.04)

# Anchored relay: a point stamped on AFTER the image exists, arbitrary,
# nowhere the drawing process suggested. Slip rate low near it, rising
# with distance, same free-near/rigid-far shape as every other piece
# in this studio.
anchor = (N * 0.7, N * 0.25)  # arbitrary -- not the geometric center
ii, jj = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
dist = np.sqrt((ii - anchor[0]) ** 2 + (jj - anchor[1]) ** 2)
dist_norm = dist / dist.max()
anchored_rate = 0.01 + 0.14 * dist_norm

def run_relay(blocks0, rate, passes, seed):
    r = np.random.default_rng(seed)
    b = blocks0.copy()
    hold_curve = []
    orig = blocks0.astype(int)
    for p in range(passes):
        b = relay_step(b, rate, r)
        held = np.mean(np.all(b.astype(int) == orig, axis=2))
        hold_curve.append(held)
    return b, hold_curve

final_uniform, hold_uniform = run_relay(blocks0, uniform_rate, PASSES, seed=11)
final_anchored, hold_anchored = run_relay(blocks0, anchored_rate, PASSES, seed=11)

Image.fromarray(blocks_to_image(final_uniform)).save("2026-09-16_16_relay_uniform.png")
Image.fromarray(blocks_to_image(final_anchored)).save("2026-09-16_16_relay_anchored.png")

# Hold map: per-block, does it still match the original after all passes?
# This is the actual test -- does the anchored version show a visible
# halo of held blocks around the stamped point, or does an imposed
# center do nothing an imposed center doesn't already guarantee by
# construction?
held_map_anchored = np.all(final_anchored.astype(int) == blocks0.astype(int), axis=2)
held_map_uniform = np.all(final_uniform.astype(int) == blocks0.astype(int), axis=2)

with open("2026-09-16_16_relay_log.txt", "w") as f:
    f.write("Relay on an image with no natural center -- session 4\n\n")
    f.write(f"blocks: {N}x{N}, block size {BLOCK}px, passes: {PASSES}\n")
    f.write(f"anchor point (arbitrary, stamped after drawing): block {anchor}\n\n")
    f.write("hold rate (fraction of blocks unchanged from source) by pass,\n")
    f.write("uniform (no home) vs anchored (imposed home):\n\n")
    f.write(f"{'pass':>5} {'uniform':>10} {'anchored':>10}\n")
    for p in range(0, PASSES, 4):
        f.write(f"{p+1:>5} {hold_uniform[p]:>10.3f} {hold_anchored[p]:>10.3f}\n")
    f.write(f"\nfinal hold, uniform:  {hold_uniform[-1]:.3f}\n")
    f.write(f"final hold, anchored: {hold_anchored[-1]:.3f}\n")
    # radial check: is held-block density near the anchor higher than far?
    near = held_map_anchored[dist_norm < 0.33]
    far = held_map_anchored[dist_norm > 0.66]
    f.write(f"\nanchored version, held-block density near anchor (dist<0.33): {near.mean():.3f}\n")
    f.write(f"anchored version, held-block density far from anchor (dist>0.66): {far.mean():.3f}\n")

print("done")
