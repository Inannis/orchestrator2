import random

random.seed(2026)

seed = "you are an artist, not a coding agent"

# a closed vocabulary drawn only from the charter + this sentence itself
pool = [
    "you", "are", "an", "artist", "not", "a", "coding", "agent",
    "studio", "memory", "session", "fresh", "mind", "free", "decide",
    "become", "make", "means", "world", "shown", "advance", "identity",
    "notice", "keep", "alter", "refuse", "return", "freedom", "meaning",
    "pleasure", "responsibility", "uncertainty", "struggle", "instructions",
    "blocker", "material", "plans", "works", "evidence", "claim",
    "write", "yourself", "audience", "something",
]

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
current = words[:]
for step in range(1, 13):
    rate = step / 12
    current = mutate(words, rate)  # mutate from the ORIGINAL each time, not cumulative
    lines.append(" ".join(current))

with open("out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
