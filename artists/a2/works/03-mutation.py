import random

random.seed(916)

# Public domain source, unrelated to this studio or its charter.
# Opening lines of Moby-Dick, Herman Melville, 1851 (US public domain).
source = (
    "Call me Ishmael. Some years ago never mind how long precisely "
    "having little or no money in my purse, and nothing particular "
    "to interest me on shore, I thought I would sail about a little "
    "and see the watery part of the world."
)

seed = "call me ishmael"

# vocabulary pool drawn only from the source passage itself
pool = [w.strip(".,").lower() for w in source.split()]
pool = list(dict.fromkeys(pool))  # dedupe, keep order

def mutate(words, rate):
    out = []
    for w in words:
        if random.random() < rate:
            out.append(random.choice(pool))
        else:
            out.append(w)
    return out

words = seed.split()
lines = [seed]
for step in range(1, 13):
    rate = step / 12
    current = mutate(words, rate)
    lines.append(" ".join(current))

with open("out3.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
