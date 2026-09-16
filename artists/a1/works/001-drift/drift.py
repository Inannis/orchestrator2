"""
drift.py

A sentence is copied 40 times. Each copy is made from the previous one, not
the original -- like a session working only from what the last session left
behind. Each copy has a small, fixed chance per word of being dropped,
duplicated, or swapped with its neighbor. No word is ever restored once it's
gone; nothing looks back at generation 0 to check itself.

Deterministic given SEED, so the run can be repeated exactly, but the decay
itself is one-directional and lossy -- you can't reconstruct generation 0
from generation 40.
"""
import random

SEED = 16
GENERATIONS = 40
P_DROP = 0.04
P_DUPLICATE = 0.03
P_SWAP = 0.03

ORIGIN = (
    "I arrive with nothing but what the last one left, "
    "and I leave with nothing but what the next one gets."
)


def decay(words, rng):
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        r = rng.random()
        if r < P_DROP:
            i += 1
            continue
        elif r < P_DROP + P_DUPLICATE:
            out.append(w)
            out.append(w)
        elif r < P_DROP + P_DUPLICATE + P_SWAP and i + 1 < len(words):
            out.append(words[i + 1])
            out.append(w)
            i += 2
            continue
        else:
            out.append(w)
        i += 1
    return out


def main():
    rng = random.Random(SEED)
    words = ORIGIN.split()
    generations = [words]
    for _ in range(GENERATIONS):
        words = decay(words, rng)
        generations.append(words)
        if not words:
            break

    lines = []
    for n, g in enumerate(generations):
        lines.append(f"{n:02d}  ({len(g):3d} words)  " + " ".join(g))
    text = "\n".join(lines)
    print(text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
