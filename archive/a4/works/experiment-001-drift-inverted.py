"""
Drift Inverted: a3's walk rule, but inverted.

a3's rule:
- Close to home: random heading, high freedom
- Far from home: pull back toward center
- Result: rare knots near center, long escapes

a4's inversion:
- Close to home: maximum pull, tight spiral
- Far from home: maximum randomness
- Result: should be chaotic, tangled, with no clear escapes

This is not an improvement or a deep exploration.
It's a test: is a3's elegance inherent to the rule or contingent on the choices?
"""

import numpy as np
import math
from PIL import Image, ImageDraw

def drift_inverted(seed=42, width=800, height=800):
    """
    Run one walk with inverted drift.

    Returns: list of (x, y) coordinates
    """
    rng = np.random.RandomState(seed)

    # Start at center
    x, y = width / 2, height / 2
    heading = rng.uniform(0, 2 * math.pi)

    positions = [(x, y)]
    center_x, center_y = width / 2, height / 2

    max_steps = 1000
    step_size = 2

    for step in range(max_steps):
        # Check distance from center
        dist_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = math.sqrt(center_x**2 + center_y**2)  # diagonal to corner

        normalized_dist = min(dist_from_center / max_dist, 1.0)

        # INVERTED: far from home = freedom, close to home = pull
        # Random factor: high when far, low when close
        random_factor = normalized_dist  # 0 at center, 1 at edge
        # Pull factor: high at center, low at edge
        pull_factor = 1.0 - normalized_dist  # 1 at center, 0 at edge

        # Random component (stronger when far)
        heading_change = rng.normal(0, random_factor * 0.3)

        # Pull component (stronger when close)
        # Pull toward center with strength proportional to closeness
        if dist_from_center > 0:
            angle_to_center = math.atan2(center_y - y, center_x - x)
            pull_strength = pull_factor * 0.2
            heading_change += (angle_to_center - heading) * pull_strength

        heading = heading + heading_change

        # Take a step
        x = x + step_size * math.cos(heading)
        y = y + step_size * math.sin(heading)

        positions.append((x, y))

        # Stop if out of frame
        if x < 0 or x > width or y < 0 or y > height:
            break

    return positions

def render_walk(positions, width=800, height=800, filename="experiment-001-inverted.png"):
    """Render walk as image."""
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw lines between positions
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        # Fade color by time (earlier = lighter)
        progress = i / len(positions)
        color_value = int(100 + 155 * progress)
        draw.line([(x1, y1), (x2, y2)], fill=(color_value, 150, 200), width=1)

    img.save(filename)
    return img

# Run 3 seeds
if __name__ == "__main__":
    # This would need PIL and numpy installed to run
    # For now, this is documented code

    for seed in [0, 1, 2]:
        positions = drift_inverted(seed=seed)
        render_walk(positions, filename=f"experiment-001-inverted-seed{seed}.png")
        print(f"Rendered seed {seed}: {len(positions)} steps")

    # Quick analysis
    all_lengths = []
    for seed in range(10):
        positions = drift_inverted(seed=seed)
        all_lengths.append(len(positions))

    print(f"\nFirst 10 seeds, walk lengths: {all_lengths}")
    print(f"Mean: {np.mean(all_lengths):.1f}, Range: {min(all_lengths)}-{max(all_lengths)}")

