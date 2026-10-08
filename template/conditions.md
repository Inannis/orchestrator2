# Conditions

What each condition is. Every studio is seeded (`tools/seed.py`) or forked (`tools/fork.py`) from one row; `day.py` and `encounter.py` read this table via the registry. How conditions are tested and decided is in `self-organization.md`; what each is for, in `notes/hypotheses.md`.

| name | charter | feed | shape | memory | notes |
|---|---|---|---|---|---|
| ref | deskw | objects | plain | deskw | R3 from 2026-10-08, the current reference system (a23 accumulated, a22 fresh). |
| R2 | desk | objects | plain | desk | 2026-10-07 to 10-08 (a16, paused). |
| R1 | v5 | museum | plain | own | The reference until 2026-10-07 (a3, a7, paused). |
| deskw | deskw | objects | plain | deskw | H23 accepted into R3. |
| rooms | rooms | museum | plain | rooms | H20 closed; its wants and studio day go on in `deskw` (a15 paused). |
| desk | desk | museum | plain | desk | H20 accepted into R2 (a16 now on `ref`). |
| min | v5 | museum | minimum | own | Closed 2026-10-07: padding (paused a17). |
| bare | v5 | objects-bare | plain | own | H19 closed (a18, a20 paused). |
| rec | v5 | objects | plain | own | H19 closed; H22 accepted `objects` into R2 (a19, a21 paused). |
| A | v5 | wide | plain | own | Closed 2026-10-07 (paused a9, a10). |
| B | v6 | wide | plain | own | Closed 2026-10-07 (paused a11, a12). |
| C | v6 | wide | return | own | Closed 2026-10-07 (paused a13, a14). |

- **charter** `v5` is `template/studio/CHARTER.md`; anything else overlays `template/variants/<charter>/`.
- **feed** `museum`: Met, Art Institute, Gutenberg, Wikipedia, living artists. `wide`: Commons photograph, current events, iNaturalist, Gutenberg, Wikipedia, living artist, Met. `objects`: Met objects with their image (twice as likely), Gutenberg passages: things, not texts about things. A `-bare` feed delivers the thing alone (picture, passage, text) without title, source or metadata; the record goes to `runs/encounters.ndjson` only.
- **shape** `plain`: "The day is not over." K times (K private, 1–6), plus "Something arrived in inbox/." when the first draw delivers. `return`: also one of the artist's earlier files. `minimum`: as plain, and the day goes on until it has lasted 20 minutes (never said).
- **memory** `own`: the artist organizes it, with the charter's one paragraph on the first file. `rooms`: furnished rooms, a letter moved to `days/` each morning, every fifth day a studio day. `desk`: notes live beside works, a letter moved to `days/` each morning, `DESK.md` laid out by `tools/desk.py`. `deskw`: desk plus `wants.md` and a studio day every fifth day (one continuation). The desk has no 'left alone longest' (H24).
- **model** is per artist in `registry.md`. **seeding**: one encounter at p=1 before session one (`--like <id>` gives the same object).
