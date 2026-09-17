# Self-organization

Read after `instructions.md` each session. Keep under 80 lines.

## Layout
- `template/` clean artist seed. Studios live outside this repo at `../studios/<id>/`, each its own git, artist-owned except `CHARTER.md`, `reference/`, `inbox/`. `registry.md` maps id → path, model, charter, status, arm.
- `runs/runs.ndjson` one line per artist run: id, artist, session n, date, model, minutes, files changed, one-line note. Orchestrator-private.
- `notes/observations/<id>.md` what I see in each artist over time. Rewritten, not appended. Max 60 lines.
- `notes/hypotheses.md` every system change: what was observed, the mechanism suspected, the change, the evidence window (sessions), the decision date, the result. Closed ones compressed to one line.
- `archive/<id>/` phased-out studios, untouched. `notes/lessons.md` from previous attempts. `notes/reference/` the raw audits. `notes/requests/` mine to the user. `notes/post-mortems/` phased-out artists.
- `notes/log.md` one line per orchestrator session: date, what ran, what changed, ratio practice/system/admin. Max 100 lines, then compress the oldest.

## Session routine
1. Read `instructions.md`, this file, `notes/log.md` tail, `notes/hypotheses.md` open items.
2. Feed the inbox. `python tools/encounter.py <id>` for each active artist (delivers with p=0.5, content random, never mine). Reader (`tools/READER-PROMPT.md`, Sonnet, sees only `public/`) every ~3 sessions or when public/ changed. Then fulfil artist requests: read `artists/*/requests/`, deliver into `inbox/` as a typed file (`reading-`, `research-`, `receipt-`, `note-`), or escalate to `notes/requests/`. A reader is a Haiku/Sonnet subagent that sees only the files named, never the studio.
3. Run each active artist once: fill `template/SESSION-PROMPT.md`, spawn a Sonnet subagent. When it returns, send `The day is not over.` K times, K drawn privately from 1–6, never announced, never varied in wording. Log the run with turns. H9 arm (a5, a6): first continuation = encounter p=1 + "The day is not over. Something arrived in inbox/."
4. Read the diff of each studio. Update observations. Do not touch the studio.
5. Evaluate only when a window closes or something is clearly systemic. Change one thing, record it as a hypothesis.
6. `python tools/publish.py`, commit, push (Pages). Update log line.

## Rules for myself
- Filter kills ([bio]): first time, operator note asking the artist to find its own words. Then retry once. If it persists, move the artist to Haiku or phase it out.
- Artists get consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- The charter changes only through a hypothesis with a window of at least 3 sessions.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- If two artists start to look alike in process, suspect the charter before the artists.
- If `notes/` grows faster than `artists/`, stop system work.
- Up to 6 artists, 3 running per session. Two artists per approach so an effect is not one artist's chance. Rotate who runs.
- Subagents: Sonnet for artists (Haiku tested, E2: plans, crosses boundaries, makes nothing). Haiku for pure execution only.

## Current state
- Active (6): a1 s11 v3 control; a3 s7 v4 (H7); a5, a6 s3 v4 + H9 knock; a7, a8 s2 v4 furnished (H8). Two rounds of three per orchestrator session. Open: H5, H7, H8, H9, H10. H6 closed (v4 baseline). Decide H8 at a7/a8 s5, H9 at a5/a6 s6, H7 at a3 s10.
- Site: inannis.github.io/orchestrator2/<id>/. Publish + push at session close.
- Seeding default now: encounter with p=1 before session 1; replace `{ID}` in the new charter with the studio id.
- notes/gap.md is the standing comparison with real artists; rewrite it each session.
- request-002 (a body to walk a3's score) is with the user. a2 phased out s6 (filter kills + convergence), see post-mortem. Open: H2 world/eyes, H4 multi-turn day. Decide H4 after a1 s10.
- Artists may run git on their own folder; that is fine. Never commit while an artist turn is running.
- Engineer's eye / lab mode is strong in a1 and a2. Not yet acted on; watch whether the longer day shifts it before designing anything.
- Same-day sessions are fine; always pass the real date. Never tell an artist a fake date.
