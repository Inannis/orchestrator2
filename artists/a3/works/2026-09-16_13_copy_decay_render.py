"""
Visual companion to 2026-09-16_12_copy_decay.py. Renders the 31
generations (0 through 30) as stacked rows of monospace text, one row
per generation, top to bottom. No color mapping to a rule this time --
just the text itself, getting visibly worse. The image IS the argument:
that copy error is a real different mechanism from the distance/pull
family the rest of the studio uses. There's no gradient to look
"correct"; there's only accumulated damage, and by the bottom rows it
plateaus into a noise floor rather than reaching zero -- short, common
words survive by having fewer characters exposed to error each
generation, not because any rule protects them.
"""
from PIL import Image, ImageDraw, ImageFont

with open("works/2026-09-16_12_copy_decay.txt", encoding="utf-8") as f:
    raw = f.read()

blocks = raw.split("--- generation ")[1:]
gens = []
for b in blocks:
    header, _, rest = b.partition("---\n")
    idx = int(header.split(" ")[0])
    text = rest.rstrip("\n")
    # collapse each generation's multi-line stanza to one row
    row = " / ".join(line.strip() for line in text.split("\n") if line.strip())
    gens.append((idx, row))

W, H = 1900, 40 * len(gens) + 60
img = Image.new("RGB", (W, H), (245, 243, 238))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("consola.ttf", 15)
except Exception:
    font = ImageFont.load_default()

for row_i, (gidx, text) in enumerate(gens):
    y = 30 + row_i * 40
    # damage increases with generation index, not distance from anything
    t = gidx / (len(gens) - 1)
    gray = int(20 + t * 90)
    color = (gray, gray, gray)
    draw.text((20, y), f"{gidx:02d}", font=font, fill=(160, 60, 40))
    draw.text((70, y), text[:210], font=font, fill=color)

img.save("works/2026-09-16_13_copy_decay_render.png")
print("saved", img.size)
