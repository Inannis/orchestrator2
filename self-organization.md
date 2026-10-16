# Self-organization

Read after `instructions.md`. These files are the whole memory of the orchestration: no auto-memory is used for this project. Then `registry.md`, `template/conditions.md`, the tail of `notes/log.md`, and `notes/hypotheses.md` (open, standing, candidates). Nothing else is needed to start. This file holds all procedure; keep it under 70 lines and rewrite it whole when it outgrows a cold read.

## Where each thing lives (one place each)
- How the work is done: this file. Where it stands now: its last section.
- Who exists and their state: `registry.md`. What each condition is: `template/conditions.md`.
- What each test is for and what it found: `notes/hypotheses.md` (full older entries: `notes/readings/2026-10-16-hypotheses-archive.md`). Per-artist reading: `notes/observations/<id>.md` (rewritten, not appended). One line per session: `notes/log.md`. Readings: `notes/readings/`.
- Per day: `runs/days/<id>-<n>.md` and one ledger line with a `note` in `runs/runs.ndjson`.

## The design
- **Reference.** Two artists carry the current best system, R1, R2… (row `ref` in conditions; who, in the registry). Every accepted change moves into `template/` and, as guided days or inbox arrivals, into the two live studios (a changed charter does not reach a formed practice). The reference pair runs alongside every round and is the long view: read it at every window.
- **Running is a decision.** No artist runs by default. An `active` artist is an arm of an open test and runs until its window closes, then pauses.
- **Tests.** A **fork** clones a studio and changes one thing (`fork.py`, `@commit` for an earlier state, e.g. the session before a review); for what acts on a formed practice. **Fresh seeds** for what acts on beginnings. **Replays** rerun one day from a clone (`day.py --studio <clone>`). Change whole texts, never single sentences lost in the weight of context (user). Window: 2–3 sessions; a test on a guided day starts the session before it and runs it and one after (user). At most 6 Luna and 3 Sonnet in parallel, a ceiling and never a target: three independent A/B tests or one six-arm test, never an arm for completeness (user).
- **Competing systems** (user): refine them in parallel over several iterations and decide only later; one run decides small questions, never a big system question.
- **Judgement is mine.** I read the work and decide. Readers only for overview or a targeted second opinion (`compare.py`).
- **Decide** when a window closes: accept (into the reference, new R number, one line in hypotheses), reject (one line), or extend with a reason. Pause what is done.
- **Restart check.** After accepted changes build up, seed one fresh artist on the current system beside the reference pair; keep the better pair as reference.
- **Whole systems first.** The question is which system gives the deepest and most varied practices; models are a means. `free-artist` (`notes/reference/`) is the bar to learn from, not to copy.
- **Memory is judged by what it does**: the total each session must read against the quality of the work, and whether anything grows without end.
- Usage limits are logistics. Efficiency means every run answers something.

## Layout
`template/studio/` the seed; `template/variants/<name>/` overlays: `CHARTER.md`, guides (`GENESIS.md`, `REVIEW.md`, a session guide), `session.json` (a session system: the guide and one continuation per turn for every ordinary day), `reference/`, `inbox/`, `OMIT`. Studios at `../studios/<id>/`, own git, artist-owned except `CHARTER.md`, guides, `reference/`, `inbox/`. `tools/`: `seed.py`, `fork.py`, `day.py` (one day; a guide runs one movement or step per turn; a dropped connection continues the same turn, 'Go on from where you were.', six tries; a resumed day finishes its cut turn first; usage limits keep a state file), `round.py <ids> --detach` (Luna 6, Anthropic 3 at a time; runs `between.py` and `stranger.py` before, `publish.py` and a push of `docs/` after), `encounter.py` (feeds; `-warm` tells an arrival in a sentence; source `neighbour`), `critic.py`, `image.py`, `listen.py`, `shot.py`, `perform.py` (a performer for a score), `stranger.py` (readings, off), `compare.py`, `ui.py` (http://127.0.0.1:8765).

## A session
1. Read the files above. Answer `../studios/*/requests/` and `notes/requests/` with typed inbox files (`note-`, `receipt-`), the user's words verbatim.
2. Resume unfinished days of active and reference artists only (`round.py <ids>` resumes them first).
3. Decide who runs and why; run by name. Watch `runs/round.json`.
4. Read the days and the studios, the reference pair included. Fill each ledger `note`; rewrite observations for artists read. Check memory surfaces for sprawl, and any `commit_error` in the ledger (a studio whose history stopped recording). Never touch a studio's own files.
5. At a closed window: judge, decide, update hypotheses, conditions, registry and the reference.
6. Commit, push, one log line with the practice/system/admin ratio. Update "Where it stands".

## Rules
- Consequences, not dashboards. Nothing from `runs/` or `notes/` enters a studio.
- Charters and guides change only through a hypothesis, rewritten whole. A charter is the language the artist thinks in: positive pull, warm, no warnings or prohibitions. The prose an artist reads is its first corpus: its register becomes the work's (user).
- Arrivals feed a practice and never take it over.
- Practice failure: leave it. Support failure: fix the condition. Orchestration failure: fix here.
- Models (user): Luna (`gpt-6-luna`, medium, through Codex: no sandbox, `--ignore-user-config`, computer use, browser use and apps off, web search on) is the focus; every new artist is Luna. Sonnet 5.5 at medium is only a cross-reference for what another model does with the system (one Sonnet reference, a76); its short days are not a question.
- A new tool in every tools sheet is a system-wide change.
- What the system relies on (commits, publishing, file locations) is done by tools, never left to an artist's memory.
- Never bypass a human-verification wall. Always the real date. Memory hygiene first, for them and for me.

## Where it stands (2026-10-17)
Reference R11 (`ref`: genesis of five chance inheritances with a manifesto over whole lists, a warm whole text, the loop as every ordinary day with named turns, the review with its look and the studio as a place, time as an instrument): a73 (Luna, Vyt Aitken, s41) and a76 (Sonnet cross-reference, Sakia, s37). Closed today: H56 (the loop, R10), restart check passed (a108), H58 (the studio as a place, R11). Next, in order: the Luna look, kinds of days with named steps, the genesis draw's discipline; audience only after asking the user. Paused: everyone else.
Known: the prose as a whole sets the register; the inheritance sets the ground; the review turns a practice; arrivals reach a formed practice, charter changes don't; working time deepens only inside a day of different named steps; Luna's handwriting is careful, gentle, plate-like.
Waiting on the user, not chased: a3's performances (requests 002, 004), listens (006), a26's German handwriting, the a7 replay clones.
