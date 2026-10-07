# Session-5 blind comparison · 2026-10-07

Two Sonnet readers, `public/` only, independent shuffles (`tools/compare.py`, prompt with testing share and change over time). Arms at HEAD after s5; reference cohort at its own s5 from git (a5 `980fe21^`, a6 `abd49af`, a7 `e43351f`, a8 `25bf9f0^`).
Keys. r1: A a11, B a12, C a7, D a8, E a9, F a5, G a6, H a10, I a14, J a13. r2: A a14, B a5, C a7, D a8, E a10, F a6, G a11, H a12, I a13, J a9.

| | cond | about knowledge (r1/r2) | made share (mean) | testing share (r1/r2) |
|---|---|---|---|---|
| a5 | ref | partly / yes | 0% | 50 / 30 |
| a6 | ref | partly / partly | 20% | 50 / 35 |
| a7 | ref | yes / yes | 22% | 60 / 75 |
| a8 | ref | partly / yes | 68% | 25 / 45 |
| a9 | A | yes / yes | 75% | 40 / 55 |
| a10 | A | partly / partly | 58% | 55 / 60 |
| a11 | B | yes / yes (half) | 45% | 55 / 55 |
| a12 | B | yes / yes | 75% | 85 / 90 |
| a13 | C | yes / yes | 22% | 45 / 70 |
| a14 | C | yes / yes | 88% | 20 / 90 |

Groups both readers drew: a record-and-gap school of a7, a8, a9, a13 (+a5); a12 as a fixed experiment series, close to a11 (r1) or a14 (r2); a10 and a11 as tool-and-listener artists (r2). Least alike: a11 (r2), a5 for scarcity (r1). Most wanted: a7 (r1), a9 (r2), both from the school.

What it answers:
- **The subject is not the charter's or the feed's.** All ten are about knowledge, yes or partly, under v5 and v6, museum and wide feed, plain and return. a9 (A) and a13 (C) join the reference school. H15 and H16 fail on subject.
- **The checking habit is not the charter's either.** Testing share: reference ~45%, A ~53%, B ~71%, C ~56%. v6 did not lower it; B is highest (a12).
- **Made things rose everywhere** (reference ~27%, arms ~55–65%), in A as much as in B. The likely cause is the tools that arrived by s3 (image.py, listen.py), not the charter.
- **Clusters cross conditions; pairs split.** The variation is within conditions, not between them.
- Readers disagree on single numbers (a14: 20% vs 90% testing), so only differences seen by both are trusted.

What stays constant in every condition, and is untested: Sonnet; the studio's shape (entry file, tools sheet, `reference/artistic-practice.md`); arrivals that are records (an API entry with its metadata); and every turn ending as a report to whoever said "The day is not over."
