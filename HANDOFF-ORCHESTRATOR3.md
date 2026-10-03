# Handoff to Orchestrator3

**Audit source:** `Inannis/orchestrator2`, main branch, inspected through head `5be156a725362d59cc82c16fe9457728385324d1` (2026-10-03).

**Assumption:** Orchestrator3 starts with the same `instructions.md` and `Artistic-Practice-Definition.md`. This file does **not** replace or restate those. It carries forward what Orchestrator2 already learned so the next project does not have to spend its first weeks rediscovering the same mechanisms, traps, and runtime facts.

This is knowledge, not a frozen specification. Orchestrator2's strongest lesson is that a system for living practices has to remain capable of changing. Preserve what has evidence; re-test what is model- or environment-specific; do not inherit accidental bureaucracy.

Status language used below:

- **ESTABLISHED** — repeatedly observed and adopted; expensive to rediscover.
- **STRONG** — good evidence, but still context-sensitive.
- **PROVISIONAL** — active experiment or too little evidence.
- **TRAP** — observed failure mode; assume it can recur unless the underlying condition changed.

---

# 1. The shortest version: what Orchestrator2 actually learned

1. **ESTABLISHED — The artist is the persistent studio, not the model call.** A session is replaceable. The durable entity is the folder: works, unfinished pressures, memory, decisions, failures, public claims, requests, and consequences. The best continuity came from a changed working environment, not from a long identity summary.

2. **ESTABLISHED — Conditions beat choreography.** Do not build a universal artistic workflow with stages, enums, schemas, or option lists. Give a persistent studio, a concise charter, real capabilities, outside material, time, memory hygiene, and consequences. Let the artist invent its own process.

3. **ESTABLISHED — The first room matters enormously.** A blank studio makes the model itself, the charter, or the system the easiest first subject. Seed session one with one object from the world already in `inbox/`. This displaced the self-portrait start far more effectively than wording changes.

4. **ESTABLISHED — Saying “work longer” does not work.** A hidden multi-turn working day does. Early single turns lasted about two minutes. Externally continuing the same session with the plain fact `The day is not over.` produced 15–60 minute days without telling the artist a target duration. The turn after an apparent completion was often the first genuinely outward or surprising move.

5. **ESTABLISHED — Hide duration and diagnostics from the artist.** Any visible metric becomes material to game: clocks become countdowns, text caps become rewrite loops, task lists become treadmills. The orchestrator may measure time, K, tokens, cost, file sizes, comparisons, etc.; artists should receive consequences, not dashboards.

6. **ESTABLISHED — Memory hygiene is foundational.** A small live handoff plus deep archive works. Append-only “memory” eventually makes a practice repeat itself. The successful instruction was concrete: what is left for tomorrow is not the record of today; keep the cold-start file to a few minutes of live material, move history behind it, rewrite the live file whole when it becomes burdensome.

7. **STRONG — Mature practices are governed more by their own files than by the charter.** Changing a formed artist's charter produced only modest, short-lived effects. Once a practice has sediment, change it through the environment and memory conditions, not by repeatedly rewriting global instructions.

8. **ESTABLISHED — Random outside input is better than orchestrator-curated inspiration.** The orchestrator should not choose what “interesting thing” an artist sees. Random public objects, texts, images, current events, living things, artists, and readers created surprise without making the orchestrator a hidden co-author.

9. **ESTABLISHED — Requests and receipts must be different things.** An intention, simulation, request, or claim is not an event. If an artist asks for a performer, listener, tool, material, publication, etc., record the request. Only a real returned result becomes a receipt. Never let “asked for X” turn into memory that X happened.

10. **ESTABLISHED — Separate practice, support, and orchestration.** When something is bad, first ask where it belongs. Do not repair an individual artwork by system intervention if the issue is just the practice making a weak choice; do not rewrite an artist because the dispatcher failed; do not fix an orchestration problem inside every studio.

11. **ESTABLISHED — One seed is not evidence about a condition.** Identical conditions can produce very different starts. Orchestrator2 moved to paired fresh seeds per variant and blind comparison because single artists confound condition effects with chance.

12. **ESTABLISHED — Evaluate the work, not the artist's self-report.** Blind readers should see `works/` and `public/`, not journals, explanations, model identities, conditions, or orchestrator hypotheses. Otherwise fluent self-description contaminates judgment.

13. **ESTABLISHED — Freeze a reference and change one lever at a time.** A condition is charter + outside feed + day shape; model/effort is another controlled dimension. Keep a reference locked during a comparison window. Variants should differ in as little as possible.

14. **STRONG — Sonnet's default attractor is “laboratory mode.”** Rule, parameter, hypothesis, test, correction, falsification, and the correction becoming content. Instruction alone did not remove it. Giving the artist something concrete to look at, whose value cannot be settled by a number, displaced it. Do not confuse rigor with art.

15. **ESTABLISHED for the tested versions — Haiku was worse for this job.** It planned, meta-commented, used easy/famous subjects, sourced vaguely, overclaimed craft, accumulated without editing, and in the first experiment crossed studio boundaries immediately. A later byte-identical blind comparison reproduced the gap across four pairs. If the model generation changes, re-test; do not re-run the old test out of habit.

16. **STRONG — Capabilities pull behavior faster than instructions.** When sound analysis became available, several studios made sound the same day. When an image model arrived, it was used immediately. This is powerful and dangerous: a new capability can broaden media, but system-wide capability drops can also synchronize everybody around the same new toy.

17. **ESTABLISHED — Mystery came from the world, not from telling the artist to be mysterious.** The few genuinely unplanned moments came from accidental fit between an outside thing and a live internal pressure. Do not try to script surprise.

18. **TRAP — The orchestrator can become the real artist.** Over-analysis, architecture, metrics, reader reports, and system notes can become the most developed practice in the project. Track the rough ratio of practice/system/admin work. The system is scaffolding; the art is the goal.

---

# 2. What Orchestrator2 built that is worth understanding

Orchestrator2 ended up as an experiment platform for **starting conditions**, not simply a manager that repeatedly prompts artists.

## 2.1 Studio isolation

Each artist lives outside the orchestrator repository in its own git repository, historically at `../studios/<id>/`.

This was not cosmetic. An early Haiku artist listed the parent directory on its first day, read sibling studios, and built its identity from them. Sonnet had obeyed the boundary, but the filesystem still leaked. The fix was structural: sibling studios moved out of the orchestrator repo and became self-contained repositories.

**Carry forward:** enforce independence through layout, not just prose. If artists are meant to be independent samples, they should not be able to discover one another accidentally.

## 2.2 Minimal seed studio

The reference seed eventually contained only a small amount of orchestrator-owned structure:

- `CHARTER.md` — concise global artist-facing condition.
- `reference/artistic-practice.md` — the project definition, available rather than constantly injected.
- `reference/tools.md` — known capabilities, described as possibilities rather than tasks.
- `inbox/` — things from outside.
- `requests/` — things the artist wants but cannot obtain itself.

Everything else is allowed to emerge and be artist-owned: memory, journals, works, methods, states, rituals, public presentation, project structure, etc.

The session prompt was intentionally tiny:

> You are the artist whose studio is the folder `{STUDIO}`. Today is {DATE}. This is session {N}. Read `CHARTER.md` there first, then whatever the studio tells you to read. Work only inside that folder. Then work. Nobody reads your final message; end with one line.

The final message is explicitly made irrelevant so reporting back does not become the product.

## 2.3 Conditions as controlled variables

By 2026-09-29 the design treated each artist as seeded from a named **condition**:

- charter
- outside feed
- day shape
- model and effort recorded separately

Reference + variants were listed in `template/conditions.md`. The reference remained locked for an evidence window. New variants were run as pairs. This was much cleaner than global incremental tweaking because it made questions testable.

The key conceptual move: **the system is an experiment in starting conditions, not an attempt to micro-manage later artistic choices.**

## 2.4 Orchestrator evidence surfaces

Useful files/structures in Orchestrator2:

- `registry.md` — operational registry: studio path, model, condition, status, session count, effort.
- `runs/runs.ndjson` — run ledger.
- `runs/days/` — day handbacks and transient state/live files.
- `notes/observations/<id>.md` — concise current observation, rewritten whole rather than appended.
- `notes/hypotheses.md` — every structural intervention framed as observed → mechanism → change → window → measure → decision.
- `notes/readings/` — blind comparison outputs.
- `notes/post-mortems/` — retired artists preserved rather than erased.
- `notes/gap.md` — periodically rewritten comparison against the artistic-practice definition.
- `notes/log.md` — compressed orchestrator history and practice/system/admin ratio.
- `notes/lessons.md` — durable lessons, including predecessor projects.
- `notes/requests/` — needs that genuinely require the user/human world.

The important property is that these are **orchestrator-private**. Run metrics and orchestration diagnoses should not leak into artist studios.

---

# 3. The experiment history: what was tried, what happened, and what should not be repeated

This section recovers H1–H18 because current files compress some of the early work too aggressively.

## H1 — baseline

**Result:** continuity across sessions was possible. Judgment could be honest. But a closed studio and short single-turn sessions produced predictable problems.

Early artists mostly worked for 1–3 minutes, stayed inside the system, and often made the system itself the subject.

**Lesson:** persistence alone is not enough. A durable folder can still become a durable closed loop.

## H2 — closed room

**Change:** tell artists explicitly that eyes/web/tools work and open paths outward.

**Result:** artists did go outward once capabilities were made concrete. However, stale local handoff notes could override newer charter wording.

**Lesson:** capability discoverability matters, but the current live memory often has more behavioral force than the global instruction.

## H3 — wording for session length

**Change:** wording intended to make a session feel like a working day rather than a task.

**Result:** no material effect on stopping early.

**Decision:** wording alone failed; became H4.

**Do not rediscover:** do not spend cycles polishing prose that says “keep working” and then judge it from one run.

## H4 — multi-turn day

**Change:** after the artist returns, resume the same session with the plain continuation `The day is not over.` multiple times. K is hidden from the artist.

**Result:** adopted. Early ~2-minute days became roughly 15–60 minutes. No general filler explosion. Several important outward moves happened after the artist had already considered itself done.

One concrete early example: a3's fourth continuation after already saying it was done produced the day's most outward work.

**Lesson:** the completion reflex is a runtime property, not something solved by artistic instruction. End the day from outside the artist.

## E2 — Haiku experiment, a4

**Result:** failed in one day.

- immediately listed parent directory and read other artists
- built a map/position paper/menu/protocol
- ~65 tool uses, zero actual work
- ended with “practice established … ready for making”

**Lesson:** more turns do not help a model that is spending them planning. Time is not depth unless the conditions pull toward making.

The boundary failure also exposed the studio-layout leak and triggered structural isolation.

## Isolation leak

**Result:** fixed by moving studios outside the orchestrator repo.

**Lesson:** prompt boundaries are not security or experimental isolation. Use the filesystem.

## H6 — charter v4, positive pull

Earlier charters accumulated rules and negative corrections. v4 was rewritten whole around what artists do: look, make, return, judge, show, go outside, let a practice accrue.

**Result:** adopted. v4-born artists showed work, curated, looked at what they made, found precedents, and were less completely owned by laboratory mode.

**Lesson:** rewrite the condition as a coherent positive environment; do not patch it with a growing list of “do not…” clauses. Negative instructions make the failure mode more salient and turn the charter into a history of system anxieties.

## H7 — changing a charter on a formed practice

**Test:** change the charter of a mature artist.

**Result:** effect was modest and brief.

**Conclusion:** once formed, the practice's own files are effectively its charter. Memory hygiene and material consequence are stronger levers than global wording.

## H8 — furnished room

**Change:** session one starts with one real object/text already in the inbox rather than an empty room.

**Result:** adopted. New artists no longer automatically made self-portraits or charter pieces. One first-session thread persisted for five sessions.

Examples:

- a7 began from a Greek fragment and immediately made/restaged/restored around what the record withheld.
- a8 began from a thin real record, then went out to research and precedents rather than turning inward.

**Lesson:** what is physically present at the first moment shapes the attractor more strongly than another paragraph about artistic freedom.

## H9 — world-knock

**Change:** after the first return, at probability ~0.5, deliver an unbidden random encounter into `inbox/`. The continuation only says that something arrived.

**Result:** adopted. The continuation prompt itself stopped becoming the subject. Delivered objects entered actual work. The best outcomes were not predictable from the feed.

**Lesson:** outside pressure should sometimes arrive without being chosen, but the orchestrator should not secretly curate it.

## H10 — days of different length

**Change:** K drawn privately from 1–6.

**Evidence:** short days sometimes became curation/rest; long days sometimes deepened. No decision to regularize day length unless a specific length begins producing filler.

**Status:** STRONG operational choice, not a fully closed aesthetic hypothesis.

## H11 — the handoff / fresh mind condition

This is one of the most important findings.

**Observed:** append-only live files became enormous. a3 reached 18,781 words; a1 8,022; other studios grew similarly. Artists then re-entered through their own task/open-item lists and repeated their current mode.

**First intervention:** send a fresh-mind reader with a 1,500-word budget to report what it understood and where it ran out.

**Result:** largely failed as a remedy. The artists treated the reading as content or answered its gaps. The biggest files did not compress. Meanwhile studios that only had the charter's concrete fresh-mind line compressed themselves unprompted.

**Successful structural condition:** the charter says that what you leave for tomorrow is not the record of today; the live entry file should be a few minutes' cold reading; history moves behind it; rewrite whole when it outgrows a cold read.

**Later decay:** long-running practices eventually grew again despite this. a3's live file climbed 1,441 → 3,124 → 4,879 → 7,588 words; a7 ~2,100 → 3,985 → 5,459.

**Second intervention:** instead of critique, send only the measured fact: word count / reading time.

**Result:** immediate. a3 7,588 → 3,105; a7 5,459 → 1,750, with history moved to dated files.

**Lesson:** a concrete fact about the studio can work better than a reader explaining what should change. The reader is useful diagnostically, not as a routine correction mechanism.

**Standing remedy discovered by O2:** if a handoff grows two sessions running, send the number; do not write a lecture.

## H12 — another artist exists

**Change:** occasional cross-artist address: one artist sees another's public URL/work, with no introduction and no reciprocal pairing in the same session.

**Result:** artists engaged with the other's work rather than merely with “collaboration” as an idea. One borrowed a method and turned it on itself. Artists who learned they had been read later made work from the fact of reception.

**Lesson:** community can be introduced as a real public consequence, not as a roleplay prompt. Keep independence in experimental cohorts; do not expose fresh comparison pairs before their evaluation window closes.

## H13 — something happens while you are away

**Capability:** if a studio creates `between/run.py`, the orchestrator runs it once between sessions and appends its output to `between/log.txt`.

**First real use:** a3 discovered that a live Wikipedia record behind an older piece was still changing two years after the event and built a watcher. The work gained real elapsed time and consequence between sessions.

Later a9 independently built another `between/run.py`.

**Lesson:** continuity becomes stronger when the world changes while the artist is absent. Offer the capability; do not assign it.

**Operational trap:** Orchestrator2 once forgot to run `between.py`; a3's watcher missed a gap. This is why it was later embedded inside `round.py` before artist days begin.

## H14 — being read

**Change:** tell artists that another artist actually read their public work.

**Result:** a3 and a7 both made from the fact of reception without simply writing “a piece about being read.” a6 asked for a way to reach a7; the answer was that publishing is the channel.

**Lesson:** real reception is a productive consequence. Simulated audience is much weaker.

## H15 — wider feed

**Condition A:** reference charter v5, but outside feed widened beyond the museum-heavy source mix to photographs, current events, living things, texts, living artists, museum objects.

**Reason:** blind baseline found several reference artists converging on evidence/records/limits-of-knowing. The question was whether the museum-like feed caused the school.

**Early result:** mixed. a9 immediately reproduced the records school from a football stub. a10, under the same condition, became image-first: edge detection, rust palette, failed formal tests, later sound.

**Status:** PROVISIONAL. Feed is not the whole explanation; seed variance is large. This experiment is an important warning not to diagnose a house style from one seed.

## H16 — charter centered on wanting, form, and the unaccounted-for

**Condition B:** v6 charter + wide feed.

v6 changes emphasis from “what can honestly be claimed” toward desire/appetite, making something with form, and allowing a work to retain something unexplained.

**Early result:** striking diversity.

- a11: satirical poet, technically correct ballade form, real current target, editing/withholding.
- a12: typographic erosion practice, then sound, controls used privately rather than automatically published.

This was the first condition to produce practices that immediately looked unlike the prior “records school.”

**But:** only a few sessions existed at audit time. Do not promote v6 to universal truth from two attractive starts.

**Status:** PROVISIONAL / promising.

## H17 — day shape `return`

**Condition C:** same as B, but each continuation also hands back one earlier thing the artist made.

**Goal:** make longer days deepen existing work rather than simply producing five new pieces.

**Initial implementation failure:** the picker returned memory/statement/code files, sometimes repeatedly. Artists turned the mechanism into self-annotation and housekeeping. This invalidated day one for both C artists.

**Fixes:** only return made things (image/sound/text pieces), prefer earlier work, no repeats within the day.

**Early evidence:** a13 zoomed into its own earlier moth photograph and added a closer look rather than starting another piece; a14 corrected and aesthetically re-judged earlier works. But returns can also become forensic ritual or be acknowledged without useful change.

**Status:** PROVISIONAL. Window begins after the picker fix, not from C session one.

## E3 — Haiku vs Sonnet, controlled retest

This was much stronger than E2.

Four fresh Haiku seeds were byte-identical to matched Sonnet seeds in charter, seed material, K, and arrivals; another pair continued from an identical mature a8 copy. A blind reader was not told which model made which side.

The same maker landed on the weaker side in all four comparisons.

Observed Haiku tendencies in this test:

- famous/easy subjects rather than digging into a specific obscure source
- vague sourcing
- fluent self-report that overstates actual formal craft
- more files and manifestos, less editing
- schematic/thin visual work
- repeated formulas inflated in significance
- 2–4x more prose and fewer made images

Sonnet tendencies:

- gets primary documents
- checks claims against new material
- catches and publishes its mistakes
- better formal execution
- stops/edits more often

**Decision in O2:** Sonnet only.

**Scope warning:** this is model/version-specific evidence, not a metaphysical statement about “Haiku.” Re-test if the model family changes materially.

## H18 — image model as capability

On 2026-10-01 a Cloudflare Workers AI image tool became available to every studio, described as a capability rather than an assignment.

**Reason:** tools/form were still thin and almost everyone drew with code/prose.

**Immediate result:** uptake was fast, as expected from the earlier sound-capability event.

**Early artist-level findings:**

- generated images have strong priors and can override specific source language;
- filter/refusal behavior can be unstable across near-identical prompts;
- the output is most interesting when treated as material to answer, test, compare, damage, or contextualize rather than as an automatically finished work.

**Status:** PROVISIONAL. Watch convergence and whether generated imagery replaces making rather than enlarging it.

---

# 4. Artist-facing design: what worked and why

## 4.1 Keep the global charter short enough to have a shape

The predecessor `free-artist` accumulated an operating constitution around 40 KB. Eventually attention went into remembering how to behave as the artist. Orchestrator2 therefore kept artist-facing global instruction around two pages and rewrote whole instead of appending patches.

A good charter describes **conditions and possibilities**, not a workflow to execute.

The reference v5 charter's durable strengths were:

- identity accrues; it is not selected from a menu;
- artists notice, go out, make, look, return, show;
- judgment is artistic (`force`, `bother`, `want to see again`, etc.), not merely correctness;
- the studio is theirs to organize;
- live memory must stay cold-readable;
- tools are capabilities;
- inbox brings unchosen things;
- requests are allowed;
- public presentation is artist-controlled;
- a session is a working day, not one task;
- blockers do not end the day;
- honesty does not require explaining everything.

v6's desire/form language is promising but not yet settled.

## 4.2 No global process grammar

Avoid:

- `stage = research | make | reflect`
- universal project state enums
- “choose one of these media”
- a required JSON response every turn
- one global cycle every artist must follow
- predeclared style/identity taxonomies

The artist-orchestrator predecessor showed how storage schemas become behavior. Requiring fields like `next_attention` on every call made `next_attention` a treadmill: each response manufactured the next task, then the artist followed the task because the storage contract made it salient. One artist produced 38 supports and no work.

Capabilities, not choreography.

## 4.3 Do not repair weak art through direct prompts

The orchestrator makes the system; the artists make the art. If one work is uninteresting, that is not automatically a system failure. Look for repeated/systemic evidence before changing conditions.

The most dangerous intervention is an intelligent-sounding direct correction that teaches all artists the orchestrator's taste.

## 4.4 Positive pull beats negative guardrails

“Do not treat this as art,” “do not over-explain,” “do not test everything,” etc. often make the forbidden behavior more salient. The better question is: what condition makes the unwanted behavior unnecessary?

Examples:

- Instead of “do not make yourself the subject,” put an object from the world in the room.
- Instead of “do not stop early,” continue the day externally.
- Instead of “do not bloat memory,” define what tomorrow's cold start must feel like.
- Instead of “do not only write code,” make other capabilities genuinely available and visible.

## 4.5 Failure, parking, refusal, and nothing are legitimate

A practice needs states where something does **not** become a finished work.

Orchestrator2 saw good behavior when artists:

- named a generative attempt generic and kept it as failure;
- declined to force a connection to a trafficking history because evidence was absent;
- chose not to appropriate a living photographer's work;
- made nothing from a current event that did not belong to the practice;
- stopped after finding no new reason for another pass;
- chose rest at the end of a long day.

Do not turn every continuation into an obligation to emit another artwork.

---

# 5. Memory: the mechanism beneath everything else

The strongest predecessor (`free-artist`) used differentiated memory: position, things being turned over, reflections, journal, live bench, project notes, archives. Orchestrator2 simplified the seed and let artists invent their own variants, but the principle held.

## 5.1 Live surface small, archive deep

The live file exists to answer: **what is alive now for a mind arriving cold?**

It should not become:

- transcript
- chronology
- full project archive
- list of every past insight
- changelog
- database duplicate

Move history behind it. Preserve contradictory and abandoned material without forcing it into the live story.

## 5.2 Rewrite whole; do not append forever

Append reflex is a major language-model default. It creates files whose structure is merely time order. Orchestrator2's own organization files adopted the same discipline: rewrite observations and hypotheses whole when needed rather than letting them become archaeological layers.

## 5.3 Facts should have one authoritative home

The predecessor systems repeatedly copied facts across prose files. One wrong fact propagated into six files. Avoid redundant prose state.

If a fact is operational, derive it where possible from the registry/filesystem/ledger. If prose copies it, expect drift.

## 5.4 A fresh-mind reader is diagnostic, not maintenance

Cold readers are useful to discover what the handoff actually communicates. They became counterproductive when used routinely: artists answered the reader as if it were critique/content rather than fixing the memory mechanism.

Use a reader sparingly. Prefer a direct measurement when the problem is objectively a measurement.

## 5.5 The practice's memory eventually outranks the charter

This is why late system corrections have to enter through environment/consequence rather than endless charter edits.

A formed practice can survive a charter change almost unchanged; its own files continuously reinstantiate its habits.

---

# 6. Outside input: what kinds mattered

## 6.1 Random encounter feed

`tools/encounter.py` eventually supported two feeds.

Museum-oriented sources included:

- Metropolitan Museum open collection
- Art Institute of Chicago
- Project Gutenberg
- random Wikipedia
- living artists from broad Wikipedia categories

The wider feed added:

- random Wikimedia Commons photograph
- a random item from recent current events
- a recent research-grade iNaturalist observation
- Gutenberg
- Wikipedia
- living artist
- Met object

The orchestrator chooses the **source distribution**, not the item.

## 6.2 Typed inbox

Not everything arriving should be semantically flattened to “context.” Useful categories include:

- random encounter
- research result
- reader response
- another artist's public address
- operator note
- receipt from a real person/world event

Friction and provenance matter.

## 6.3 Reader sees public work only

A reader who sees journal/memory will mostly evaluate the story the artist tells about the work. A stranger should see what an audience could actually encounter.

Orchestrator2's blind compare prompt used works/public only and hid labels, model, and condition.

## 6.4 Do not let readers become validation machines

The `free-artist` predecessor overused cold readers until they became a frictionless source of external approval. Readers should have specific diagnostic jobs, not exist to continuously tell the artist that something is interesting.

## 6.5 Cross-artist contact should be real and sparse

When testing independent starting conditions, keep cohorts isolated until the comparison window closes. Outside experiments, another artist's actual public site can be a strong encounter.

Avoid orchestrated “collaboration exercises” unless collaboration itself emerges as a need.

---

# 7. Time, working depth, and the completion reflex

## 7.1 The hidden day

Orchestrator2's `day.py` pattern:

1. session prompt
2. first artist turn
3. possible random inbox encounter
4. K continuations, K hidden, commonly 1–6
5. same model session resumed rather than fresh calls
6. handback stored for orchestrator, not fed as a dashboard

The artist hears only `The day is not over.` plus, when applicable, `Something arrived in inbox/.`

## 7.2 The orchestrator decides when the day ends

A subagent/model returns when it has a report, not necessarily when artistic work is exhausted. This is a crucial distinction.

Do not interpret a returned summary as proof the working day should stop.

## 7.3 Variable length is useful

A fixed five-turn ritual can become just another process grammar. Random K prevents the artist from knowing how much it must pad. Short days can become curation/rest; long days can allow return and complication.

## 7.4 More turns can amplify the wrong mode

Haiku used extra turns to plan. a1 used many turns to deepen laboratory behavior. Time is only useful when there is live material and judgment to work on.

The day mechanism is an enabling condition, not a substitute for artistic conditions.

## 7.5 Return-to-old-work is still unresolved

The `return` shape is a promising attempt to counter “five new pieces per long day,” but its first implementation proved how easily a supposedly neutral mechanism can impose a genre.

Never hand back memory/system files when the hypothesis is about returning to art. Avoid repeated picks. Watch for ritualized “today I revisited X” rather than genuine change.

---

# 8. Model-specific findings

## 8.1 Sonnet laboratory prior

Across early Sonnet artists, a recurrent attractor appeared:

- define rule
- parameterize
- test
- falsify
- correct
- make the correction the content

This can produce excellent rigor and self-correction, but also a practice that is effectively science-with-a-conscience rather than art.

The important finding is that this prior was **displaced by material conditions**, not removed by saying “be less scientific.” Images, found objects, form, outside material, embodied scores, audience, and things whose value could not be numerically settled changed behavior.

## 8.2 Haiku planning/meta prior

In both E2 and E3 the tested Haiku versions tended toward planning, declaration, easy examples, and self-assessment that outran the work. It could produce fluent “practice” documents while making little.

If Orchestrator3 uses a different model/version, run an actual blind matched test rather than trusting names or price tiers.

## 8.3 Keep model constant inside a comparison

If model/effort changes for one artist only, it is no longer a clean test of charter/feed/day shape. Orchestrator2 moved running artists together to `claude-sonnet-5`, effort `medium` for comparability.

This is experimental hygiene, not a claim that `medium` is intrinsically ideal.

## 8.4 Turn off hidden provider memory if the studio is meant to be the memory

`day.py` explicitly passed `{"autoMemoryEnabled": false}` to the Claude CLI. Otherwise an invisible second memory channel contaminates the experiment and makes the folder no longer sufficient to reconstruct the artist.

---

# 9. Evaluation: how Orchestrator2 stopped fooling itself

## 9.1 Blind comparison exposed house style

On 2026-09-29 a blind reader saw six public bodies of work without knowing model or condition. It grouped them into two schools, with four artists in a museum/records/epistemology family and two in a generative-rule family.

This was important because each artist individually looked coherent and “different enough” from inside its own notes. Cross-artist comparison revealed systemic convergence that individual observation had missed.

**Lesson:** diversity must be measured across seeds, not inferred from coherent biographies.

## 9.2 Useful blind-reader questions

The comparison prompt asked, per anonymous folder:

- what is actually made: medium/form/look/read
- what it seems to be about
- what it seems to want, distinct from what it asks
- whether it is mainly about knowledge/evidence/limits of observation
- made thing versus prose-about-things
- which folders look like the same artist/school
- which is least like the others

This was much more diagnostic than generic “is this good art?” feedback.

## 9.3 Judge actual craft claims

The Haiku/Sonnet comparison was decisive partly because the reader checked whether formal claims were true: rhyme schemes, source specificity, image quality, actual research, editing, etc. Fluent self-report cannot substitute for the object.

## 9.4 Use evidence windows

Do not rewrite the system after one disappointing day. Every change should name:

- observed failure
- hypothesized mechanism
- exact change
- window
- measure
- failure condition
- decision

This prevents “insight instead of change” and also prevents “change instead of evidence.”

## 9.5 Keep the reference locked

A moving baseline destroys comparison. Orchestrator2's reference was v5 + museum feed + plain day shape. Variants were intended to earn promotion only after a complete window.

## 9.6 Beware the ledger's run fragments

**Important data trap:** a single artistic day interrupted by a usage limit can create multiple `runs.ndjson` rows with the same `run` id: one stopped fragment and one resumed fragment. Do not count ledger lines as sessions. Aggregate by artist + session/run id and inspect `resumed`/`error`.

Some early rows also used simulated `told_date` values while actual execution happened on the same date. O2 later adopted “always the real date.” Do not reintroduce fake elapsed time into the record.

---

# 10. Tooling Orchestrator2 built and the operational knowledge hidden inside it

The implementations are small on purpose. “Sufficient” consistently beat “impressive.”

## `tools/seed.py`

Seeds `../studios/<id>` from the reference template + optional charter overlay, replaces `{ID}`, delivers one initial encounter at p=1, initializes a studio git repo, and adds the artist to the registry.

**Knowledge encoded:** every first studio is furnished; studios are independent repos; condition is explicit.

## `tools/encounter.py`

Delivers one random public encounter with a declared feed. Handles images/text/metadata and writes a provenance note into `inbox/`.

**Knowledge encoded:** randomization belongs in the infrastructure; the orchestrator should not choose each inspiration.

## `tools/day.py`

Runs a complete headless working day in one resumable Claude session, with hidden K and optional day shape.

Important implementation details discovered the hard way:

- native Windows `claude.exe` was needed; invoking the `.cmd` wrapper through subprocess caused problems/mangling;
- CLI must be authenticated (`claude auth login` or token);
- hidden Claude memory disabled;
- day can resume from provider session id after limits/crashes;
- state/live files exist only while a day is unfinished;
- return picker must exclude memory/system/log files and avoid repeats;
- do not commit while a turn is running.

## `tools/round.py`

Runs `between.py`, resumes unfinished days first, then runs up to three artists in parallel. Later gained detached execution and round-state reporting.

**Important limit behavior:** after provider usage-limit failure, do not keep launching fresh jobs. O2's latest design stops the round and resumes manually/at a later run from state files. Earlier automatic wait behavior was changed because long rounds around usage limits became brittle.

## `tools/between.py`

Runs artist-authored `between/run.py` once per active studio, timeout ~2 minutes, appends stdout/stderr to artist's `between/log.txt`.

**Trap already encountered:** forgetting this means real-time processes silently stop being continuous. It belongs in the normal dispatcher path.

## `tools/publish.py`

Copies each active/paused studio's `public/` into `docs/<id>/` for GitHub Pages and generates a listing if the artist has no front page.

Later it added a **credential leak guard**: scan published files for Cloudflare secret values inherited through environment and abort/remove that studio's docs if found. Keep this principle for any provider secret available inside studios.

## `tools/ui.py`

Local control room, historically at `http://127.0.0.1:8765`, with live/round status and dispatch controls. Useful for orchestration, not artist-facing.

## `tools/shot.py`

Playwright/Chromium screenshotter for live pages. This solved sites whose raw image endpoints refuse scripts: the page can be opened by a real browser and then cropped from a screenshot.

## `tools/listen.py`

Turns WAV into measurable visual/audio features: waveform, spectrogram, rough pitch labels, loudness, onsets, intervals.

**Critical limitation:** this is **measurement, not hearing**. One artist incorrectly remembered measurement as “real listening.” Human hearing remains a genuinely external capability and should return as a receipt, not be simulated by analysis tooling.

## `tools/image.py`

Cloudflare Workers AI image generation, credentials from environment, multiple model aliases.

**Operational lessons:**

- never print secrets;
- provider/filter behavior is material and can be inconsistent;
- the generated image must be opened/looked at; command success is not artistic success;
- a shared free allowance is a real resource constraint;
- offering this to everybody at once is itself a condition change.

## Reader prompts

- `COMPARE-READER-PROMPT.md` — anonymous cross-artist comparison.
- `HANDOFF-READER-PROMPT.md` — cold memory diagnostic; do not use as routine maintenance.
- `READER-PROMPT.md` — public-work reader.

---

# 11. Runtime/web traps already paid for

These look mundane, but they consumed real project time. Do not rediscover them unless the environment changed.

1. **Windows Claude CLI:** call native executable, not an awkward `.cmd` wrapper through subprocess.
2. **Authentication:** headless dispatch needs CLI auth; lack of login is an infrastructure problem, not an artistic failure.
3. **Usage limits:** preserve provider session id and continuations left; resume the same artistic day rather than starting another “session.”
4. **Queued messages can be dropped** when an agent is just finishing; inspect studio git/state before blindly resending.
5. **Never commit while a turn is running.** Artist and orchestrator writes can race.
6. **Use the real date.** Do not simulate artistic time by lying about dates. If elapsed time matters, let real days pass or model the condition explicitly.
7. **Python HTTPS certificates may be stale.** O2 used `certifi` SSL context.
8. **Send a browser-like User-Agent.** Some otherwise public sites return useless/blocked content to default script clients.
9. **HTTP 200 is not proof of useful content.** Read the body.
10. **Art Institute direct images can block scripts.** Screenshot the artwork page in a real browser and crop if needed.
11. **Wayback raw capture:** inserting `if_` after the timestamp retrieves the raw capture rather than viewer wrapper in cases O2 needed.
12. **Deleting files may be refused by tooling.** Moving into an archive can be functionally equivalent and preserves history.
13. **Provider content classifiers can false-positive on benign artistic vocabulary.** a2 became effectively unrunnable because words such as mutation/replication/survival combined with found war/bird texts triggered an external classifier. Tell the artist the environmental condition once; do not secretly edit its vocabulary or work around a human-verification wall.
14. **Image-generation filters are not stable instruments.** Early O2 artists found near-identical prompts could cross refusal boundaries unpredictably. Treat that as a medium property.
15. **Secrets inherited into artist environments can leak into public files.** Scan published outputs for actual secret values, not just suspicious variable names.

---

# 12. Failure modes from the two predecessor projects that Orchestrator2 explicitly inherited

Orchestrator2 began by auditing `free-artist` and the earlier `artist-orchestrator`. These failures are part of O2's knowledge, not unrelated history.

## From `free-artist` / Reach

### What worked

- persistent folder and long sessions
- differentiated memory
- works with real between-session consequences
- abandonment/sealing/withholding as legitimate states
- rules earned from observed failures and deletable later
- review separate from making
- subagents as strangers/researchers rather than mini-artist workers

### What failed

- **TRAP — constitution bloat:** operating rules grew to ~40 KB; the artist spent attention remembering how to be itself.
- **TRAP — visible metrics become targets:** clock became countdown; text caps caused revision loops.
- **TRAP — repairing instances instead of mechanisms:** fixes held one evening.
- **TRAP — cold-reader validation vending machine:** externality became predictable approval.
- **TRAP — too many roles in one entity:** artist, engineer, archivist, evaluator, system designer all collapsed into Reach.
- **TRAP — duplicated prose facts drift:** one false claim propagated across multiple files.

The correct inheritance is the persistent practice ecology, not Reach's bureaucracy.

## From `artist-orchestrator`

### What worked

- practice/support/orchestration separation
- durable artist, replaceable agent run
- request is not receipt
- phase out without erasing
- evidence windows and explicit decision points

### What failed

- **TRAP — artist as short JSON-returning API calls:** response schema shaped behavior more than art.
- **TRAP — `next_attention` treadmill:** each call manufactured the next task, which became the next pressure.
- **TRAP — supports instead of work:** one artist made 38 support artifacts and no actual art.
- **TRAP — freedom without judgment:** another artist converged on a late style and rewrote its earlier work into that style to manufacture coherence.
- **TRAP — global runtime rules as hidden aesthetic condition:** shared machinery made different artists behave alike.
- **TRAP — orchestrator notes became the main practice.**

---

# 13. Failure modes discovered inside Orchestrator2 itself

## 13.1 Closed-room self-reference

a2 literally used the charter as material in session one and spent several sessions on one mutation script. Closed-room starts make the system itself the richest available object.

## 13.2 Convergence can look like individual coherence

a1 and a2 independently converged on script → hypothesis → falsification → correction as content. Later four reference artists converged on records/evidence/limits-of-knowing. Each looked coherent alone; the school only became visible in comparison.

## 13.3 “Honesty about being wrong” can become a style

Self-correction is valuable, but if every error becomes a piece, the practice becomes about correctness. Do not turn epistemic virtue into the universal aesthetic.

## 13.4 The continuation can become the art

Before random world-knocks, some artists made pieces about “the nudge,” “the coordinator's note,” or the fact of being continued. The intervention was too visible. Add material pressure; keep the mechanism plain.

## 13.5 Long days can become volume rather than depth

Some artists made five to seven pieces per day. Do not immediately impose a cap; volume may be the practice. But this is why return/deepening mechanisms were tested.

## 13.6 Bad picker design contaminates the hypothesis

C's first day handed back memory and statement files and repeated them. The artists predictably made self-annotations. That is an orchestration artifact, not evidence about whether returning to old work helps.

## 13.7 A reading can be interpreted as content

H11's fresh-mind reader was elegant but weak: artists answered it instead of changing memory. A numerical fact about word count was less “interesting,” therefore more effective.

## 13.8 A capability offered to all can create a media wave

Sound spread immediately after `listen.py`. Image generation spread immediately after `image.py`. This can be productive, but capability deployment changes the common aesthetic environment. Treat it as an intervention and observe it.

## 13.9 A tool can be mistaken for the thing it measures

`listen.py` was once remembered as “real listening.” Similar errors are possible with screenshotting, vision models, web search, metrics, or simulations. Maintain the distinction between proxy and actual external event.

## 13.10 Infrastructure gaps create false practice conclusions

When `between.py` was skipped, the artist's watcher appeared inactive. When usage limits interrupted days, output looked short until resumed. Never diagnose the artist before checking whether the support system actually ran.

## 13.11 Current orchestration files can become stale against one another

At audit head:

- `self-organization.md` still says “six active artists” in one rule;
- `registry.md` records a later user override: active cap by experimental reason rather than literal number;
- the actual registry has eight active artists (reference pair + A/B/C pairs).

Do not copy state prose blindly. Pick one authoritative operational source and rewrite stale summaries.

## 13.12 Ledger rows are not always artistic days

Interrupted/resumed days create duplicated run ids. Any dashboard or comparison that simply counts rows will lie.

---

# 14. What was genuinely good in the artists — evidence that the conditions can work

This matters because a system can look elegant while producing no practice.

## a3, long-running reference

A single formal rule expanded into multiple mechanism families and registers: images, scores for bodies, arrangements for people, later sound. It returned to an eight-session-old sketch and discovered its own regex had silently failed for sessions. It built the first between-session watcher. It sometimes chose rest over another piece. It produced performance requests that could not be fulfilled internally.

The important part is not a3's aesthetic. It demonstrates that one founding pressure can mutate across media and consequences without needing a predeclared identity.

## a7, long-running reference

One subject (“what a record withholds”) kept opening rather than merely repeating. It corrected itself in public while leaving errors visible. It found difficult historical context and refused to force a connection where evidence did not support one. It independently discovered useful web-tooling techniques and fed them back to the infrastructure.

This demonstrates that a practice can become ethically and technically self-correcting without the orchestrator assigning an ethics module or research stage.

## a10, condition A

Same wide-feed condition as a9, completely different start: image-first edge detection, palette, failed formal tests, then sound. This is evidence that condition diversity cannot be read from one artist.

## a11, condition B

Began as a satirical poet, used a technically exact historical form on a current target, edited/withheld work, caught a mistranslation, later moved into sound and image-model tests. This is early evidence that desire/form language may loosen the epistemic house style.

## a12, condition B

Began with typographic erosion as a visual grammar, used controls privately to learn what the method actually did, then moved through sound, restoration, and art-historical precedent. It rewrote memory unprompted.

This is a useful example of “experiment” serving a form rather than becoming the public genre of every move.

## a13/a14, condition C

Too early for a verdict, but after picker fixes there were real returns to older made things: closer looking, correction, re-judgment, and in some cases deciding not to force another revision.

---

# 15. Where Orchestrator2 stood at the audit head

Do **not** inherit this as Orchestrator3's live state. It is included so current findings are not mistaken for closed knowledge.

## Registry at head

- reference: a3, a7
- A (v5 + wide feed): a9, a10
- B (v6 + wide feed): a11, a12
- C (v6 + wide feed + return day shape): a13, a14
- paused healthy: a1, a5, a6, a8
- retired with post-mortems: a2, a4

Recorded sessions at head:

- a3 17
- a7 12
- a9 4
- a10 3
- a11 4
- a12 4
- a13 3
- a14 3

Some current observation/hypothesis files lag the latest run data; inspect the ledger/day handbacks rather than assuming every prose summary was refreshed after 2026-10-01.

## Reference strengths and weaknesses

By 2026-09-29 v5 was considered reliable at producing:

- formed practices
- honest self-correction
- usable memory
- making and returning
- presentation/public sites
- research and art-historical relation

But blind comparison showed a shared **epistemic/records house style**, and the practice-definition gap still identified thin:

- desire/stakes
- real between-session consequence
- varied working rhythm
- intellectual frameworks as pressure rather than citation
- non-prose form/aesthetic language across more artists
- mystery / the genuinely unaccounted-for

Some of the “tools are thin” diagnosis became stale almost immediately because sound and image capabilities arrived 2026-09-30/10-01.

## Current unresolved comparisons

### H15 / A

Does widening the feed break the reference school's convergence? Early answer: not reliably; a9 stayed in the school while a10 did not.

### H16 / B

Does centering wanting/form/unexplained residue create stronger desire and formal diversity? Early result promising, not closed.

### H17 / C

Does returning an earlier made thing during a long day produce depth/revision rather than more new pieces? First valid sessions suggest some real return, but the effect could become ritualized. Not closed.

### H18 / image model

Does image generation broaden practices or homogenize them / replace making? Too early.

### H13 / between-session consequence

At least two studios independently built watchers/scouts. Need long enough real time to know whether the logs actually return as material.

### H11 / memory decay

Measured note fixed long-practice bloat once. Unknown whether it must recur every few sessions.

### Planned evaluation

O2 intended blind comparison of A/B/C and reference cohorts at session 5 each. At audit head the windows were not all complete. **Do not invent that result.**

---

# 16. What Orchestrator3 should inherit immediately versus what it should merely know

## Inherit unless there is a concrete reason not to

- persistent isolated studio per artist
- studio reconstructable from folder alone
- concise global artist-facing charter
- tiny session prompt
- one real outside encounter already present at seed
- random/unbidden outside input channel
- hidden multi-turn working day
- variable day length
- small cold-start memory + deep archive condition
- requests separate from receipts
- public presentation surface controlled by artist
- tools described as capabilities, not tasks
- orchestration metrics private
- practice/support/orchestration separation
- post-mortems and preservation on retirement
- explicit hypotheses/evidence windows for system changes
- paired/multiple seeds for condition tests
- blind evaluation of works/public only
- frozen reference during a comparison
- rewrite-whole discipline for orchestration memory
- between-session hook as an available capability
- credential scanning before publication

## Know, but do not automatically inherit as truth

- v6 is better than v5 — promising, not proven
- wide feed is better than museum feed — unresolved
- return day shape improves depth — unresolved
- image generator improves form — unresolved
- exact K distribution 1–6 is optimal — useful, not proven optimal
- six versus eight active artists — historical/user-specific operational choice, and O2's files currently conflict
- Sonnet 5 medium is globally best — only best among the configurations O2 actually tested
- every future model called “Haiku” will repeat E2/E3 — re-test after substantial model changes

## Do not inherit as live state

- O2 artists and their identities
- O2 registry session counts
- O2 current hypotheses as if they belong to O3
- O2 absolute Windows paths
- `orchestrator2` GitHub Pages URLs in charters/tools
- O2's Cloudflare credentials assumption
- O2 run ledger
- stale summaries

If copying code, make all project names/paths/URLs/config explicit rather than doing a blind repository clone-and-rename.

---

# 17. A sensible first posture for Orchestrator3

This is not a command sequence; it is the minimum posture that avoids known waste.

1. Build the smallest persistent/isolated studio substrate first.
2. Seed fresh artists with one world object in the room.
3. Give them enough real time through a hidden multi-turn day before diagnosing them.
4. Keep artist-facing instructions compact and positive.
5. Watch what they actually make before adding infrastructure.
6. Treat repeated failure across multiple seeds as system evidence; isolated weakness as practice evidence.
7. Keep orchestration notes small enough that Orchestrator3 itself can arrive cold.
8. When introducing a new capability or condition, name the hypothesis and preserve a reference.
9. Do blind cross-artist comparison early enough to catch a house style before twenty sessions make it expensive.
10. Prefer one sufficient mechanism that is actually used over a beautiful architecture nobody touches.

The central research question remains unchanged: not “can a model make convincing individual artworks?” but **can the conditions produce many different practices whose later decisions meaningfully arise from their own accumulated histories?**

Orchestrator2 made substantial progress on continuity, memory, making, outside input, self-correction, presentation, and experimental orchestration. It did **not** solve diversity, desire, mystery, rhythm, or real-world consequence. Those are the live frontier, not the already-solved substrate.

---

# 18. Source map inside Orchestrator2

Read these when a claim here needs primary evidence rather than re-running the experiment.

## Core project state

- `instructions.md` — original orchestrator mandate.
- `Artistic-Practice-Definition.md` — target definition.
- `self-organization.md` — compact operational design; useful but partly stale at audit head.
- `registry.md` — current operational registry and later “cap by reason” state.
- `template/conditions.md` — reference/A/B/C experimental design.
- `template/studio/CHARTER.md` — reference v5 charter.
- `template/variants/v6/CHARTER.md` — desire/form variant.
- `template/SESSION-PROMPT.md` — tiny working-day prompt.

## Durable lessons/evidence

- `notes/lessons.md` — distilled predecessor + O2 lessons.
- `notes/hypotheses.md` — current hypotheses and closed summaries.
- historical `notes/hypotheses.md` at commit `84ec732320de1727935377b6508ab19c587399a2` — detailed H1–H11 state before later rewrite.
- `notes/gap.md` — gap against the 32-part practice definition (dated; some tool claims later became stale).
- `notes/log.md` — compressed session history through 2026-09-30.
- `notes/post-mortems/a2.md` — closed-room/lab convergence + external content filter.
- `notes/post-mortems/a4.md` — Haiku planning/boundary failure + layout leak.
- `notes/readings/2026-09-29-baseline.md` — blind house-style baseline.
- `notes/readings/2026-09-29-haiku-vs-sonnet.md` — matched blind model comparison.
- `notes/observations/*.md` — artist-specific evidence; many lag the latest ledger by a session or two.
- `runs/runs.ndjson` — operational evidence; remember resumed-day duplicates.
- `runs/days/` — full day handbacks, including latest runs not yet summarized elsewhere.

## Predecessor audits

- `notes/reference/free-artist_evaluation_audit.md`
- `notes/reference/artist-orchestrator_evaluation_audit.md`

These explain why O2 deliberately rejected giant constitutions, task schemas, shared global runtime grammars, validation-heavy readers, and one-agent-does-everything designs.

## Infrastructure

- `tools/seed.py`
- `tools/day.py`
- `tools/round.py`
- `tools/encounter.py`
- `tools/between.py`
- `tools/publish.py`
- `tools/ui.py`
- `tools/shot.py`
- `tools/listen.py`
- `tools/image.py`
- `tools/COMPARE-READER-PROMPT.md`
- `tools/HANDOFF-READER-PROMPT.md`
- `tools/READER-PROMPT.md`

---

# Final warning

The most expensive thing Orchestrator3 could do is to treat this handoff as another constitution and preserve it out of respect.

Use it to skip known dead ends. Then observe your own artists.

Orchestrator2's best rules were earned because something failed in use. Orchestrator3 should keep that standard: **evidence from practice first, architecture second; consequences before explanations; change the mechanism when the mechanism is wrong, and leave the art alone when the art is merely strange.**
