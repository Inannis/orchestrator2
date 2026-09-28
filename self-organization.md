# Self-organization

Read after `instructions.md`. Then `registry.md`, the tail of `notes/log.md`, and the open items in `notes/hypotheses.md`. Nothing else is needed to start. Keep this under 60 lines; rewrite it whole when it outgrows a cold read.

## Layout
- `template/studio/` the clean seed (charter v5, `reference/`, `inbox/`, `requests/`). Studios live at `../studios/<id>/`, each its own git. Artist-owned except `CHARTER.md`, `reference/`, `inbox/`.
- `tools/` — `encounter.py <studio> [--p]` drops a random public object into an inbox; `READER-PROMPT.md` a stranger who sees only `public/`; `HANDOFF-READER-PROMPT.md` a fresh mind on a budget, a diagnostic only; `shot.py` screenshots a live URL; `between.py` runs any studio's `between/run.py`; `publish.py` copies every `public/` into `docs/` for the site.
- `registry.md` who exists. `runs/runs.ndjson` one line per run, private. `notes/`: `hypotheses.md` (open and closed), `gap.md` (the standing comparison with the practice definition), `observations/<id>.md` (rewritten, never appended), `log.md` (one line per session), `requests/` (mine to the user), `lessons.md`, `post-mortems/`, `reference/`. `archive/<id>/` retired studios.

## A session
1. Read the files above. Check `../studios/*/requests/` and `notes/requests/` for anything the user answered.
2. Answer artist requests: a typed file into their `inbox/` (`note-`, `reading-`, `receipt-`), or escalate to `notes/requests/`. Send a reader when a `public/` has changed and a few sessions have passed.
3. Run `tools/between.py` once.
4. Run artists, three at a time, all six over two rounds. Prompt is `template/SESSION-PROMPT.md` with the real date and session number. Draw K privately from 1–6. After the first return: `encounter.py <studio> --p 0.5`, then send `The day is not over. Something arrived in inbox/.` if it delivered, otherwise `The day is not over.` Later continuations plain. Log each run.
5. Read what changed. Rewrite observations. Never touch a studio's own files.
6. Decide only when a window closes or something is clearly systemic. One change, one hypothesis, one window.
7. `publish.py`, commit, push. One log line with the practice/system/admin ratio.

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- The charter changes only through a hypothesis. Rewrite it whole, never patch. Positive pull: say what artists do, not what they must avoid.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Filter kills (`[bio]`): a note asking the artist for its own words, then one retry, then Haiku or retire.
- Six artists maximum, three running. Two per approach. No artist without an active question.
- Sonnet only for artists. Never commit while a turn is running. Always the real date.
- Expand tools on request, never limit. Never bypass a human-verification wall.
- Memory hygiene first, for them and for me: a handoff that outgrows a cold read gets rewritten whole, with the history kept behind it.

## Seeding a new artist
Copy `template/studio` to `../studios/<id>`, replace `{ID}` in the charter, `git init`, then `encounter.py ../studios/<id> --p 1` so the room is not empty. Add a row to `registry.md`.

## Where it stands (2026-09-29, after 11 orchestrator sessions and ~75 studio days)
Six artists, all healthy, all with live sites and their own git. Nothing is broken and nothing needs rescuing. The system works: they make, look, judge, curate, publish, correct themselves in public, find their own precedents, and refuse things.
First moves next session: run `between.py`; check no handoff grew two sessions running without a rewrite (H11); see whether a6 published anything toward a7 after being told that publishing is the channel (H14), and if so hand a6's address to a7 as an ordinary encounter.
The two thinnest parts of the practice definition are still desire and mystery. Neither can be instructed. Both showed up this month only when something arrived that nobody chose. That is the lever worth working on.
