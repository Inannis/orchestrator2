import random

# Found text, public domain: US federal statute, 16 U.S.C. § 703(a) (Migratory
# Bird Treaty Act), fetched verbatim from Cornell Law School's Legal
# Information Institute, 2026-09-16. Not written by me, not written for this
# test -- addresses the composed-source caveat from work 06 (log, session 4).
# Flat and specific by nature of the genre: legal prose has no emotional
# stakes but is dense with precise, enumerated terms.
source = (
    "Unless and except as permitted by regulations made as hereinafter "
    "provided in this subchapter, it shall be unlawful at any time, by any "
    "means or in any manner, to pursue, hunt, take, capture, kill, attempt "
    "to take, capture, or kill, possess, offer for sale, sell, offer to "
    "barter, barter, offer to purchase, purchase, deliver for shipment, "
    "ship, export, import, cause to be shipped, exported, or imported, "
    "deliver for transportation, transport or cause to be transported, "
    "carry or cause to be carried, or receive for shipment, transportation, "
    "carriage, or export, any migratory bird, any part, nest, or egg of any "
    "such bird, or any product, whether or not manufactured, which "
    "consists, or is composed in whole or part, of any such bird or any "
    "part, nest, or egg thereof, included in the terms of the conventions "
    "between the United States and Great Britain for the protection of "
    "migratory birds concluded August sixteen nineteen sixteen, the United "
    "States and the United Mexican States for the protection of migratory "
    "birds and game mammals concluded February seven nineteen thirty six, "
    "the United States and the Government of Japan for the protection of "
    "migratory birds and birds in danger of extinction, and their "
    "environment concluded March four nineteen seventy two, and the "
    "convention between the United States and the Union of Soviet "
    "Socialist Republics for the conservation of migratory birds and their "
    "environments concluded November nineteen nineteen seventy six."
)

# seed phrase drawn from the source itself, same convention as 02-06
seed = "any migratory bird"

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

# three random seeds this time, not one -- work 06's finding rested on n=1
# per condition; this run tests whether that finding (a word holding late,
# then letting go right at 100%) repeats or was luck.
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

with open("out7.txt", "w", encoding="utf-8") as f:
    for rseed, lines in all_runs:
        f.write(f"--- random seed {rseed} ---\n")
        f.write("\n".join(lines))
        f.write("\n\n")

for rseed, lines in all_runs:
    print(f"--- random seed {rseed} ---")
    print("\n".join(lines))
    print()
