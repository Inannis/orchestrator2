import random

random.seed(916)

# Found text, public domain, not written by me. A field-guide-style
# description: precise, specific vocabulary (species names, anatomical
# terms, measurements) with no emotional charge -- no grief, no judgment,
# no stakes. Written in flat descriptive register on purpose, to isolate
# specificity from charge (session 3's open question).
source = (
    "The peregrine falcon is a large, crow-sized falcon. It has a blue-grey "
    "back, barred white underparts, and a black head with a black malar "
    "stripe. The adult is thirty-four to fifty-eight centimetres long with "
    "a wingspan of seventy-four to one hundred twenty centimetres. Females "
    "are noticeably larger than males. It reaches speeds over three hundred "
    "kilometres per hour during its hunting stoop, making it the fastest "
    "animal in the world. The species breeds on cliff ledges, in quarries, "
    "and increasingly on tall buildings and bridges in urban areas. It "
    "feeds almost exclusively on medium-sized birds, which it strikes in "
    "midair with a clenched foot. The nest is a scrape, unlined, on a bare "
    "ledge. Clutch size is usually three to four eggs, incubated mainly by "
    "the female for around thirty-three days."
)

seed = "the fastest animal in the world"

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

with open("out6.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
