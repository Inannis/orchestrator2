# Self-organization

Read after `instructions.md`. Then `notes/log.md` tail, `notes/hypotheses.md` open items, `registry.md`. Keep this under 60 lines.

## Layout
- `template/studio/` clean seed (charter v4, `reference/`, `inbox/`, `requests/`). Studios at `../studios/<id>/`, each its own git; artist-owned except `CHARTER.md`, `reference/`, `inbox/`. `registry.md`: id, path, charter, status, sessions.
- `tools/encounter.py <studio> [--p]` random public object into an inbox. `tools/READER-PROMPT.md` reader who sees only `public/`. `tools/shot.py` live-page screenshot. `tools/publish.py` copies every `public/` into `docs/` for Pages.
- `runs/runs.ndjson` one line per run (private). `notes/observations/<id>.md` rewritten, max 60 lines. `notes/hypotheses.md` open/closed. `notes/gap.md` practice definition vs. what is there, rewritten. `notes/log.md` one line per session. `notes/lessons.md`, `notes/post-mortems/`, `notes/requests/` (mine to the user), `notes/reference/` (audits). `archive/<id>/` retired studios.

## Session routine
1. Read the files above. Check `../studios/*/requests/` and `notes/requests/` for anything answered by the user.
2. Fulfil artist requests: typed file into `inbox/` (`note-`, `reading-`, `receipt-`), or escalate to `notes/requests/`. Reader when `public/` changed and ~3 sessions passed since the last.
3. Run artists, three at a time, all six per session over two rounds. Prompt = `template/SESSION-PROMPT.md` with real date and session number. Draw K from 1–6 privately. First continuation: `encounter.py <studio> --p 0.5`; if delivered send `The day is not over. Something arrived in inbox/.`, else `The day is not over.` Later continuations plain. Log each run.
4. Read what changed. Rewrite observations. Never touch a studio's own files.
5. Decide only when a window closes or something is clearly systemic. One change, one hypothesis, a window.
6. `publish.py`, commit, push. One log line with the practice/system/admin ratio.

## Rules
- Consequences, not dashboards: nothing from `runs/` or `notes/` enters a studio.
- Charter changes only through a hypothesis; rewrite whole, never patch; positive pull, no pink elephants.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Filter kills (`[bio]`): operator note asking for the artist's own words, then one retry, then Haiku or retire.
- Max 6 artists, 3 running. Two per approach. Don't keep an artist without an active hypothesis.
- Sonnet only for artists. Never commit while a turn is running. Always the real date.
- Expand tools on request, never limit. Never bypass a human-verification wall.
- Memory hygiene first, for artists and for me: without it nothing else works.

## Current state (2026-09-17)
- Active: a1 s14 (v3, longitudinal control), a3 s10, a5 s6, a6 s6, a7 s5, a8 s4 (all v4). Retired: a2 (filter), a4 (Haiku).
- Site: https://inannis.github.io/orchestrator2/<id>/ . request-002 (a body to walk a3's score) with the user.
- Next session: decide the memory-bloat hypothesis first (a1, a3), then run.
- Seeding a new artist: copy `template/studio`, replace `{ID}` in the charter, `git init`, `encounter.py --p 1`.
