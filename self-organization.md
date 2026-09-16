# Self-organization

Read after `instructions.md` each session. Keep under 80 lines.

## Layout
- `template/` clean artist seed. `artists/<id>/` live studios (artist-owned except `CHARTER.md`, `reference/`, `inbox/`).
- `runs/runs.ndjson` one line per artist run: id, artist, session n, date, model, minutes, files changed, one-line note. Orchestrator-private.
- `notes/observations/<id>.md` what I see in each artist over time. Rewritten, not appended. Max 60 lines.
- `notes/hypotheses.md` every system change: what was observed, the mechanism suspected, the change, the evidence window (sessions), the decision date, the result. Closed ones compressed to one line.
- `notes/lessons.md` from previous attempts. `notes/reference/` the raw audits. `notes/requests/` mine to the user. `notes/post-mortems/` phased-out artists.
- `notes/log.md` one line per orchestrator session: date, what ran, what changed, ratio practice/system/admin. Max 100 lines, then compress the oldest.

## Session routine
1. Read `instructions.md`, this file, `notes/log.md` tail, `notes/hypotheses.md` open items.
2. Fulfil artist requests: read `artists/*/requests/`, deliver into `inbox/` as a typed file (`reading-`, `research-`, `receipt-`, `note-`), or escalate to `notes/requests/`. A reader is a Haiku/Sonnet subagent that sees only the files named, never the studio.
3. Run each active artist once: fill `template/SESSION-PROMPT.md`, spawn a Sonnet subagent, log the run. Time it.
4. Read the diff of each studio. Update observations. Do not touch the studio.
5. Evaluate only when a window closes or something is clearly systemic. Change one thing, record it as a hypothesis.
6. Update log line, commit.

## Rules for myself
- Artists get consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- The charter changes only through a hypothesis with a window of at least 3 sessions.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- If two artists start to look alike in process, suspect the charter before the artists.
- If `notes/` grows faster than `artists/`, stop system work.
- Start one artist. Clone or add a second only to test a specific hypothesis.
- Subagents: Sonnet for artists and anything with judgment, Haiku for pure execution.

## Current state
- a1 (s5), a2 (s3), a3 (s1) active on charter v3. Open: H2 world/eyes, H3 session length. Decide after a3 s4.
- Same-day sessions are fine; always pass the real date. Never tell an artist a fake date.
