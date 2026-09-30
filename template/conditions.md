# Conditions

Every artist is seeded from one condition (`tools/seed.py <id> <condition>`). The reference is locked: it changes only by adopting a variant that beat it over its window. A variant differs from the reference in as few things as possible and runs as a pair. `tools/encounter.py` reads the feed from here via the registry.

| name | charter | feed | shape | notes |
|---|---|---|---|---|
| ref | v5 | museum | plain | Reference, locked 2026-09-29. `template/studio/` as is. Running: a3, a7. |
| A | v5 | wide | plain | H15, the world sends the present: news, a living thing seen this week, a photograph, a little museum. |
| B | v6 | wide | plain | H16, charter v6 (desire and form at the centre, honesty one line) on top of A. B vs A isolates the charter. |
| C | v6 | wide | return | H17, the day shape: each continuation also hands back one of the artist's own earlier files. C vs B isolates the shape. |

- **charter** `v5` is `template/studio/CHARTER.md`; anything else overlays `template/variants/<charter>/` on it.
- **feed** `museum`: Met, Art Institute, Gutenberg, Wikipedia, living artists (x2). `wide`: Commons photograph, Wikipedia current events, iNaturalist, Gutenberg, Wikipedia, living artist, Met.
- **shape** is how the day is kept going after the artist reports back (`tools/day.py`). `plain`: "The day is not over." K times, K private, 1–6, plus "Something arrived in inbox/." when the first draw delivers. `return`: the same, plus one of the artist's own earlier files drawn at random.
- **model** is per artist, in `registry.md`.
- **seeding** is the same for all: one encounter at p=1 before session one.
