# Self-organization

Read after `instructions.md`. These files are the whole memory of the orchestration: no auto-memory is used for this project. Then `registry.md`, `template/conditions.md`, the tail of `notes/log.md`, and the open items in `notes/hypotheses.md`. Nothing else is needed to start. This file holds all procedure; keep it under 70 lines and rewrite it whole when it outgrows a cold read.

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
- **Whole systems first.** The question is which system (memory, organisation, rhythm, roles, presentation) gives the deepest and most varied practices; how the models behave is a means to it, not the subject. Test wildly different whole systems against the reference before tuning one. A small mechanism test only when it blocks a system decision, and then as one replay or one fork, never runs across many artists. Runs per question stay in proportion to its weight. `free-artist` (`notes/reference/`) is the bar to improve on.
- **Memory is judged by what it does.** No word limits. The measure is the total that every session must read, set against the quality of the work, and whether anything grows without end. A larger, well-organised memory that gives better work is better; one that gives the same work as a smaller one is not.
- Usage limits are logistics, not a target. Efficiency means every run answers something.

## Layout
`template/studio/` the seed; `template/variants/<charter>/` overlays (v6, rooms, desk); `template/SESSION-PROMPT.md`. Studios at `../studios/<id>/`, own git, artist-owned except `CHARTER.md`, `reference/`, `inbox/`. `tools/`: `seed.py` (`--like`, `--model`, `--effort`), `fork.py`, `day.py` (one day, streamed to `runs/days/<id>.stream.jsonl` and shown live in its own console window by `watch.py`, `--no-window` to hide; shapes, memory mechanisms, no MCP servers, output via files so an artist's background job cannot stall it, commits the studio at the end, stops on usage limits and keeps a state file), `round.py <ids> [--detach] [--resume-only]` (three at a time per provider, Anthropic and OpenAI; a usage limit stops only its provider; status in `runs/round.json`, or `runs/round-2.json` while another round runs), `ui.py` (control room, http://127.0.0.1:8765; if an artist's page shows there instead, a stray server holds the port: stop it and start `python tools/ui.py` again), `encounter.py` (feeds, `-bare`, every record in `runs/encounters.ndjson`), `desk.py`, `critic.py` (the second mind of a `twominds` studio), `compare.py`, `listen.py`, `image.py`, `shot.py` (URLs or studio file paths, so artists need no local server), `between.py`, `publish.py`.

## A session
1. Read the files above. Answer `../studios/*/requests/` and `notes/requests/` with typed inbox files (`note-`, `receipt-`), the user's words verbatim.
2. Resume unfinished days (`python tools/round.py --resume-only --detach`).
3. Decide who runs and why; run them by name: `python tools/round.py <ids> --detach`. Watch `runs/round.json`.
4. Read the days and the studios (a reader for overview when it is a lot). Fill each ledger `note`; rewrite observations. Check every memory surface's size. Never touch a studio's own files.
5. At a closed window: judge, decide, update hypotheses, conditions, registry and the reference.
6. `publish.py` (read anything about a real person first), commit, push, one log line with the practice/system/admin ratio. Update "Where it stands".

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- Charters change only through a hypothesis, rewritten whole. A charter is the language the artist thinks in: positive pull, no warnings or prohibitions (they plant what they forbid). Structure over sentences.
- Arrivals feed a practice and never take it over; the practice keeps its own gravity.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Models (user): Sonnet 5.5 at medium (never high); Codex `gpt-6-luna` at `xhigh` (any model `gpt-*` runs through Codex in `day.py`), without sandbox and without the user's Codex config (`--ignore-user-config`, computer use, browser use and apps disabled, web search on): an artist once reached the user's desktop through the Computer Use plugin. The user's global `~/.codex/AGENTS.md` is empty so no instructions reach a studio besides the charter (checked 2026-10-09; `CODEX_STUDIO_HOME` can point runs at a separate Codex home if that changes). New artists move the mix toward ~2/3 Luna, 1/3 Sonnet; running artists keep their model. A hypothesis can be tested on both models (model-independent A/B), but Luna vs Sonnet is never itself the A/B of a hypothesis: they differ by nature.
- A new tool in every tools sheet becomes a subject everywhere: a system-wide change.
- What the system relies on (commits, file locations) is done by tools, never left to an artist's memory: a7 lost its commit habit in its own compression.
- Never bypass a human-verification wall. Always the real date. Memory hygiene first, for them and for me.

## Where it stands (2026-10-09, session 16)
Reference R3 (Desk with `wants.md` and a studio day every fifth day, no 'left alone longest'; objects feed): a23 (s27) and a22 (s10). Paused: everyone else.
Known: the object leads a practice, not its wrapper; time without something to enter pads; handing 5.5 its old work becomes an audit; more objects per day give thin one-offs; wants steer whatever they say; R3 holds over ten sessions, keeps seeds distinct, and lets one practice deepen (a24) while arrivals scatter the varied ones.
Open: H30 whole systems (a29 R3, a30 Studio, a31 Project, a32 Two minds; Luna, one first object) to s5, running. Closed: H29 (R3 keeps Luna's memory bounded; a27 drifted into archive research). a27, a28 paused at s10. Closed: H28 (Luna on R3: the object leads there too; days long and deep; memory grows fast).
Open user requests: two listens (`notes/requests/request-006.md`); a26 asks for a reader of German handwriting (`../studios/a26/requests/read-the-german.md`). Replay clones `studios/a7-replay*` wait for the user.
