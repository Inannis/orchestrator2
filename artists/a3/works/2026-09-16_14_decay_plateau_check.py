"""
Follow-up to 2026-09-16_12_copy_decay.py: is the ~5-9% plateau seen by
generation 30 a real fixed point, or just slow decay that hadn't
finished by generation 30? Same rule, same seed, run to 300
generations instead of 30, tracking exact-word-survival every
generation. No image -- this is a check, not a piece.
"""
import random

SEED = 3
random.seed(SEED)

SRC_LINES = [
    "Once upon a midnight dreary, while I pondered, weak and weary,",
    "Over many a quaint and curious volume of forgotten lore—",
    "While I nodded, nearly napping, suddenly there came a tapping,",
    "As of some one gently rapping, rapping at my chamber door.",
    "’Tis some visiter,” I muttered, “tapping at my chamber door—",
    "                                   Only this and nothing more.”",
]
gen0 = "\n".join(SRC_LINES)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
P_SUB, P_DEL, P_DUP = 0.012, 0.006, 0.006

def copy_once(text):
    out = []
    for ch in text:
        r = random.random()
        if r < P_DEL:
            continue
        elif r < P_DEL + P_SUB:
            out.append(random.choice(ALPHABET) if ch.isalpha() else ch)
        elif r < P_DEL + P_SUB + P_DUP:
            out.append(ch); out.append(ch)
        else:
            out.append(ch)
    return "".join(out)

ref_words = [w.strip(".,—“”’").lower() for w in gen0.split()]

cur = gen0
fracs = []
for i in range(301):
    words = cur.split()
    hits = sum(1 for w in words if w.strip(".,—“”’").lower() in ref_words)
    fracs.append(hits / len(ref_words))
    cur = copy_once(cur)

# report every 10th generation
for i in range(0, 301, 10):
    print(i, f"{fracs[i]*100:.1f}%")

print("min over last 100 gens:", f"{min(fracs[200:])*100:.1f}%")
print("max over last 100 gens:", f"{max(fracs[200:])*100:.1f}%")
print("final text length:", len(cur), "vs original", len(gen0))
