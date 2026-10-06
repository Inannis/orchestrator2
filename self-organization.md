# Self-organization

Read after `instructions.md`. Then `registry.md`, `template/conditions.md`, the tail of `notes/log.md`, and the open items in `notes/hypotheses.md`. Nothing else is needed to start. Keep this under 60 lines; rewrite it whole when it outgrows a cold read.

## The design
The system is an experiment in starting conditions. A **condition** is charter + feed + day shape (`template/conditions.md`); model and effort are per artist in `registry.md`. The reference (v5, museum feed, plain day) is locked and carried by a3, a7. Variants run as fresh pairs, judged blind against each other and against the reference cohort at equal age. A variant that beats the reference becomes the reference. The target: a condition that, seeded 10–20 times, gives practices that are deep and unlike each other.

## Layout
- `template/studio/` the reference seed; `template/variants/<v>/` overlays; `template/conditions.md`; `template/SESSION-PROMPT.md`.
- Studios at `../studios/<id>/`, each its own git, artist-owned except `CHARTER.md`, `reference/`, `inbox/`.
- `tools/`: `seed.py <id> <cond>`; `day.py <id>` one headless day (stops on usage limits, keeps `runs/days/<id>.state.json` to resume, writes `<id>.live.json`); `round.py [ids] [--detach] [--resume-only]` runs `between.py`, resumes unfinished days, then new ones, three at a time, status in `runs/round.json`, starts nothing new after a limit; `ui.py` the control room at http://127.0.0.1:8765 (round panel, Start round, Resume unfinished, per-artist live status); `encounter.py`; `listen.py`; `image.py` (Cloudflare, credentials in env); `publish.py` (refuses to publish credentials); `COMPARE-READER-PROMPT.md`.
- `notes/`: `hypotheses.md`, `gap.md`, `observations/<id>.md` (rewritten), `readings/`, `log.md`, `requests/`, `lessons.md`.

## A session
1. Read the files above. Check `../studios/*/requests/` and `notes/requests/`; answer with typed inbox files (`note-`, `receipt-`), the user's words verbatim.
2. Finish unfinished days first: the UI's Resume unfinished, or `python tools/round.py --resume-only --detach`.
3. Start a round from the UI or `python tools/round.py --detach`. Watch `runs/round.json`, not the handbacks. A day costs a lot of usage: ~3–5 days per 5-hour window, ~40 per week.
4. Read `runs/days/` and the studios. Fill the ledger `note` per run, rewrite observations. Never touch a studio's own files.
5. Decide only when a window closes or something is systemic. One change, one hypothesis, one window.
6. `publish.py` (read anything about a real person first), commit, push, one log line with the practice/system/admin ratio.

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- Charters change only through a hypothesis, rewritten whole, positive pull. The reference stays locked.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Active artists capped by reason: each an arm or a control. Three running at a time. Sonnet 5 at medium (Haiku rejected).
- A new tool in every tools sheet is taken up by everyone at once and becomes a subject; treat it as a system-wide change.
- Handoff bloat: send the artist a note with only the measured word count and reading time. It works in one session.
- Never bypass a human-verification wall. Always the real date. Memory hygiene first, for them and for me.

## Where it stands (2026-10-06, session 14)
Reference a3 (s18), a7 (s13). A (v5 + wide feed): a9, a10. B (charter v6): a11, a12. C (v6 + `return` shape): a13, a14. Paused healthy: a1, a5, a6, a8.
A round started 10:18 (detached): a3, a7 done; a9, a10 finished their cut session 4; Then the 5-hour limit (reset 15:10): a11 and a12 stopped mid-day (resumable, state files kept), a14 not started, a13 was still finishing. Resume unfinished first, then a14's day. Today's ledger notes (a3-018, a7-013, a9-004, a10-004 resumed, and whatever B/C finished) are still empty.
**Next, in order:** (1) resume anything unfinished; (2) give a9 and a10 their session 5, and C its session 5 when it is due; (3) the blind comparison at session 5: A, B, C and the reference cohort as it stood at its own session 5, recovered from git (`git archive`; a5 at `980fe21^`, a6 at `abd49af`, a7 at `e43351f` (its s1–5 were committed late), a8 at `25bf9f0^`), works/ and public/ only, shuffled labels, `COMPARE-READER-PROMPT.md`. The question it must answer: does v6 hold, or does Sonnet's checking-and-correcting habit return under any charter by session 4–5 (a11 and a14 already named it in themselves)?
What is known: v5 artists form one school (blind reader); a9 joined it from a non-museum seed, a10 did not; B gave a satirical poet and a typographic practice; C's `return` produced real reworking once the picker handed back made work only; all eight took up `image.py` as an object of study, none as a replacement for making; listeners' replies (request-006) became work (a10 "Idly Playing").
Drafted, not seeded: day shapes `self` (artist ends with "The day goes on." to continue) and `minimum` (hidden wall-clock floor). Open user requests: none.
