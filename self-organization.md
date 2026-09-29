# Self-organization

Read after `instructions.md`. Then `registry.md`, `template/conditions.md`, the tail of `notes/log.md`, and the open items in `notes/hypotheses.md`. Nothing else is needed to start. Keep this under 60 lines; rewrite it whole when it outgrows a cold read.

## The design
The system is an experiment in starting conditions. A **condition** is charter + feed + day shape (`template/conditions.md`); model and effort are per artist in `registry.md`. The reference condition is locked and carried by two long-running artists. The other four slots run variants as fresh pairs, judged against each other and against the reference cohort's own first sessions (`runs/runs.ndjson`). A variant that beats the reference over its window becomes the reference and frees its pair. The target: a condition that, seeded 10–20 times, gives practices that are deep and unlike each other. The blind comparison reader (`tools/COMPARE-READER-PROMPT.md`, labels shuffled, model and condition hidden) is how that gets judged.

## Layout
- `template/studio/` the reference seed (charter v5); `template/variants/<v>/` files that overlay it; `template/conditions.md`; `template/SESSION-PROMPT.md`.
- Studios at `../studios/<id>/`, each its own git, artist-owned except `CHARTER.md`, `reference/`, `inbox/`.
- `tools/`: `seed.py <id> <condition>` makes an artist; `day.py <id>` runs one whole day headless (first turn, encounter draw, K private continuations by the condition's shape, ledger line, handbacks to `runs/days/`); `round.py [ids]` three at a time; `ui.py` the control room at http://127.0.0.1:8765 (also `.claude/launch.json`); `encounter.py` reads the feed from the condition; `between.py`; `publish.py`; `shot.py`; reader prompts.
- `notes/`: `hypotheses.md`, `gap.md`, `observations/<id>.md` (rewritten, never appended), `readings/` (blind comparisons), `log.md`, `requests/`, `lessons.md`, `post-mortems/`.

## A session
1. Read the files above. Check `../studios/*/requests/` and `notes/requests/`.
2. Answer artist requests with a typed file in their `inbox/` (`note-`, `reading-`, `receipt-`), or escalate.
3. `python tools/between.py`.
4. `python tools/round.py` (all active), or dispatch from the UI. Read `runs/days/` and the studios, not the handbacks as they arrive. If the CLI is not logged in (`claude auth login`), fall back to subagents: same prompt, K drawn privately, `encounter.py` after the first return, "The day is not over." K times; queued messages to an agent that is just finishing get dropped, so check its git before resending.
5. Rewrite observations. Fill the ledger `note` for each run. Never touch a studio's own files.
6. Decide only when a window closes or something is systemic. One change, one hypothesis, one window.
7. `publish.py` (read anything about a real person before it goes out), commit, push, one log line with the practice/system/admin ratio.

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- Charters change only through a hypothesis, rewritten whole, positive pull. The reference stays locked.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Six active artists, three running. Two per variant. Paused studios are intact and do not count.
- Sonnet only (Haiku re-tested and rejected 2026-09-29). Never commit while a turn is running. Always the real date.
- Expand tools on request, never limit. Never bypass a human-verification wall.
- Memory hygiene first, for them and for me.

## Where it stands (2026-09-29, session 12)
Reference: a3, a7. Condition A (wide feed): a9, a10. Condition B (charter v6, desire and form first): a11, a12. Paused healthy: a1, a5, a6, a8.
A blind reader put four of the v4/v5-born artists in one school ("the record and what it withholds"); a1 and a3, born before v4's honesty paragraph, are a different family. After one session each: a9 (A) is that school again from a non-museum seed; a10 (A) is not; a11 and a12 (B) are unlike anything here, a satirical poet and a typographic practice, both with made form.
First moves next session: log the CLI in and test `day.py` on one artist; run session 2 for a9–a12 through `round.py`; read a3's `between/log.txt` (H13) and whether it answers its handoff reading (H11).
Open decision: a day-shape pair (`return`, `self`, `minimum`) needs a slot. Free one when A's direction is clear, or ask the user to raise the cap now that days run outside my context.
