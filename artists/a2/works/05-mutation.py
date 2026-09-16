import random

random.seed(916)

# Found text, public domain, not written by me, not about me or this studio.
# Abraham Lincoln's letter to Mrs. Bixby, Nov 21 1864 (authorship of the
# letter itself is disputed by historians -- possibly ghostwritten by
# John Hay -- but the text is public domain either way and I did not
# write it). Emotionally loaded (grief, war, sacrifice), not
# self-referential in the way 02/04's source material was self-referential.
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

with open("out5.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
