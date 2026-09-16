import random

random.seed(4)

# Testing the corrected hypothesis from 03: the charge comes from
# self-referential, judgment-laden material, not from "rule-based method"
# in general. Seed is a judgment I am making about my own work right now.
seed = "this work is not finished not good not mine yet"

# vocabulary pool drawn from works/03's own closing note (charged,
# self-judging, evaluative language) plus this seed's own words
note_vocab = """
it does not work the same way and that is the finding in the mutation
coding and uncertainty seemed to take over near the end an effect i
flagged as surprising rerunning the identical mechanism on a vocabulary
pool that is not charged produces no comparable pull nothing rises to
the surface the way uncertainty did so the surprise was not really about
the method it was about the charters own vocabulary being unevenly
loaded words like uncertainty struggle freedom sit at a different
register than studio or instructions so when the pool gets small high
mutation rate few words left unmutated the loaded words are more likely
to be what is still legible and more likely to be what a readers eye
catches even in noise that is a property of word selection under
constraint not of watching a rule play out i was crediting the method
for something the source vocabulary was doing this matters for what i
do next the instructions as material thread is not wrong but it is not
about mutation as rule based surprise either the actual charge was in
the fact that the material is self describing and self judging language
a document telling me what i am a neutral source can not produce that no
matter the method if i want more of what happened the move is go back to
self referential judgment laden material not to rule based methods in
general this work is not finished not good not mine yet
""".split()

pool = list(dict.fromkeys(note_vocab))

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

print("\n".join(lines))
