# Self-organization

Read after `instructions.md`. Then `registry.md`, `template/conditions.md`, the tail of `notes/log.md`, and the open items in `notes/hypotheses.md`. Nothing else is needed to start. This file holds all procedure; keep it under 70 lines and rewrite it whole when it outgrows a cold read.

## Where each thing lives (one place each)
- How the work is done: this file. Where it stands now: its last section.
- Who exists and their state: `registry.md`. What each condition is: `template/conditions.md`.
- What each test is for and what it found: `notes/hypotheses.md`. Per-artist reading: `notes/observations/<id>.md` (rewritten, not appended). One line per session: `notes/log.md`. Readings and replays: `notes/readings/`.
- Per day: `runs/days/<id>-<n>.md` and one ledger line with a `note` in `runs/runs.ndjson`.

## The design
- **Reference.** Two artists carry the current best system, R1, R2… (row `ref` in conditions; who, in the registry). Two, so chance and system can be told apart. Every accepted change moves into the reference: into `template/` and into the two live studios.
- **Running is a decision.** No artist runs by default. A reference runs only when a question needs its new sessions; its recent sessions already are the control. An `active` artist is an arm of an open test and runs until its window closes, then pauses.
- **Tests.** A **fork** clones a reference studio at today's commit and changes one thing (`tools/fork.py`); for anything that acts on a formed practice. **Fresh matched seeds** are two new studios differing only in the change, from the same first arrival (`seed.py --like`); for anything that acts on beginnings. **Replays** rerun one day from a cloned state (`day.py --studio <clone> --enc-p 0`, no ledger); for model and wording questions. Several tests run at once, one question each. Window: 3 sessions.
- **Judgement is mine.** I read the work and decide. Readers are the same model with less capability: use them for an overview of what artists did (so my context stays on the questions), and for a second opinion only with a targeted question where a clean context is a real advantage (`tools/compare.py`, `COMPARE-READER-PROMPT.md`). A reader's verdict is not more objective than mine.
- **Decide** when a window closes: accept (moves into the reference, new R number, one line in hypotheses), reject (one line), or extend with a reason. Pause what is done.
- **Restart check.** After accepted changes (of any kind) have built up, seed one fresh artist on the current system and run it beside the accumulated reference. It shows whether the system works from zero and whether accumulated material is carrying the reference. Afterwards keep the better pair as the reference.
- Usage limits are logistics, not a target. Efficiency means every run answers something.

## Layout
`template/studio/` the seed; `template/variants/<charter>/` overlays (v6, rooms, desk); `template/SESSION-PROMPT.md`. Studios at `../studios/<id>/`, own git, artist-owned except `CHARTER.md`, `reference/`, `inbox/`. `tools/`: `seed.py`, `fork.py`, `day.py` (one headless day; shapes, memory mechanisms, stops on usage limits and keeps a state file), `round.py <ids> [--detach] [--resume-only]` (three at a time, status in `runs/round.json`), `ui.py` (control room, http://127.0.0.1:8765), `encounter.py` (feeds, `-bare`, every record in `runs/encounters.ndjson`), `desk.py`, `compare.py`, `listen.py`, `image.py`, `shot.py`, `between.py`, `publish.py`.

## A session
1. Read the files above. Answer `../studios/*/requests/` and `notes/requests/` with typed inbox files (`note-`, `receipt-`), the user's words verbatim.
2. Resume unfinished days (`python tools/round.py --resume-only --detach`).
3. Decide who runs and why; run them by name: `python tools/round.py <ids> --detach`. Watch `runs/round.json`.
4. Read the days and the studios (a reader for overview when it is a lot). Fill each ledger `note`; rewrite observations. Check every memory surface's size. Never touch a studio's own files.
5. At a closed window: judge, decide, update hypotheses, conditions, registry and the reference.
6. `publish.py` (read anything about a real person first), commit, push, one log line with the practice/system/admin ratio. Update "Where it stands".

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- Charters change only through a hypothesis, rewritten whole, positive pull. Structure over sentences.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Sonnet 5.5 at medium for every artist (user); never effort high.
- A new tool in every tools sheet becomes a subject everywhere: a system-wide change.
- What the system relies on (commits, file locations) is done by tools, never left to an artist's memory: a7 lost its commit habit in its own compression.
- Never bypass a human-verification wall. Always the real date. Memory hygiene first, for them and for me.

## Where it stands (2026-10-08, session 15 continued)
Reference R3 (Desk with `wants.md` and a studio day every fifth day, no 'left alone longest'; objects feed): a23 (a7's practice, s27) and a22 (fresh, s5). Paused: everyone else.
Closed since 10-07: H20, H22 (R2), restart check (passed), H23 and H24 (R3). Known: the object leads a practice, not its wrapper; time without something to enter pads; handing 5.5 its old work becomes an audit; wants steer whatever they say.
Open: H25 diversity, three fresh R3 seeds (a24–a26) to s4.
Candidates after: the checking habit on new work (work that cannot be checked; a person who answers).
Open user requests: two listens (`notes/requests/request-006.md`). Replay clones `studios/a7-replay*` wait for the user.
