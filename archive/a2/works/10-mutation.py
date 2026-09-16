import random

# Direct response to work 09's mechanism audit. 02-08's mutate() gave
# every word identical replacement probability regardless of content --
# no code in this studio had ever actually tested whether a word's
# properties affect its durability under substitution. This is a new
# mechanism, not a rerun of the old one: replacement probability is now
# explicitly weighted by word length, used here as a crude, declared-
# up-front proxy for "specificity" (longer words in English skew rarer
# and more semantically specific -- function words are short, content
# words tend longer -- this is a real but weak correlation, not a
# measurement of specificity itself, and it says nothing about charge).
# Being upfront about the proxy's crudeness is the point: 09's whole
# complaint was claims outrunning what the mechanism actually measured.

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
pool = list(dict.fromkeys(pool))

def resistance(word, max_len=12):
    # 0 (no resistance, replaced at the base rate) to ~0.6 (strong
    # resistance) scaled by word length. Capped so nothing is immune.
    return min(len(word), max_len) / max_len * 0.6

def mutate(words, rate, rng):
    out = []
    for w in words:
        effective_rate = rate * (1 - resistance(w))
        if rng.random() < effective_rate:
            out.append(rng.choice(pool))
        else:
            out.append(w)
    return out

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

with open("out10.txt", "w", encoding="utf-8") as f:
    for rseed, lines in all_runs:
        f.write(f"--- random seed {rseed} ---\n")
        f.write("\n".join(lines))
        f.write("\n\n")

for rseed, lines in all_runs:
    print(f"--- random seed {rseed} ---")
    print("\n".join(lines))
    print()

print("word lengths / resistance:")
for w in seed.split():
    print(f"  {w}: len={len(w)} resistance={resistance(w):.2f}")
