import random

# Same source and seed as work 05 (Lincoln's letter to Mrs. Bixby,
# Nov 21 1864 -- public domain, found, not written by me). 05's result
# ("bereavement" surviving to full/100% mutation) is the one claim in
# the whole mutation set never replicated across seeds -- everything
# else has now been checked against multiple seeds (07) or reasoned
# about directly (06). This closes that gap: same source and seed,
# three random seeds instead of one.
source = (
    "I have been shown in the files of the War Department a statement "
    "of the Adjutant General of Massachusetts that you are the mother "
    "of five sons who have died gloriously on the field of battle. "
    "I feel how weak and fruitless must be any words of mine which "
    "should attempt to beguile you from the grief of a loss so "
    "overwhelming. But I cannot refrain from tendering to you the "
    "consolation that may be found in the thanks of the Republic they "
    "died to save. I pray that our Heavenly Father may assuage the "
    "anguish of your bereavement, and leave you only the cherished "
    "memory of the loved and lost, and the solemn pride that must be "
    "yours to have laid so costly a sacrifice upon the altar of freedom."
)

seed = "the anguish of your bereavement"

pool = [w.strip(".,").lower() for w in source.split()]
pool = list(dict.fromkeys(pool))  # dedupe, keep order

def mutate(words, rate, rng):
    out = []
    for w in words:
        if rng.random() < rate:
            out.append(rng.choice(pool))
        else:
            out.append(w)
    return out

# 916 is 05's original seed, kept for continuity; 42 and 7 match the
# other two seeds used in 07, so results are directly comparable across
# both replication runs.
random_seeds = [916, 42, 7]

all_runs = []
for rseed in random_seeds:
    rng = random.Random(rseed)
    words = seed.split()
    lines = [seed]
    for step in range(1, 13):
        rate = step / 12
        current = mutate(words, rate, rng)
        lines.append(" ".join(current))
    all_runs.append((rseed, lines))

with open("out8.txt", "w", encoding="utf-8") as f:
    for rseed, lines in all_runs:
        f.write(f"--- random seed {rseed} ---\n")
        f.write("\n".join(lines))
        f.write("\n\n")

for rseed, lines in all_runs:
    print(f"--- random seed {rseed} ---")
    print("\n".join(lines))
    print()
