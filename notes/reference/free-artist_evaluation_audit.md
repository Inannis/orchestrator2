# `free-artist` — Architecture and Practice-System Audit

**Repository:** `Inannis/free-artist`  
**Default branch:** `main`  
**Audit head inspected:** `2f2fc7a0d7160ea3be66f1447a49380815e08519` (16 September 2026)  
**Repository size reported by GitHub:** ~498,685 KB  
**Audit purpose:** extract the architectural, operational, and artistic-system lessons most useful for a new **subagent-native multi-artist orchestrator**.

---

## 1. Executive assessment

`free-artist` is not really an orchestrator. It is a **single-artist operating system** built around one continuing agentic artist, Reach, living in a Git repository across sessions.

That distinction matters. Its strongest contribution to a future multi-artist system is not scheduling, provider routing, or task distribution. Its strongest contribution is a much harder thing: it demonstrates a plausible answer to **what a persistent artificial artistic practice needs in order not to reset into a generic assistant every session**.

The repository has developed a surprisingly rich ecology:

- a concise root identity instruction in `CLAUDE.md`;
- a large mutable practice constitution in `PRACTICE.md`;
- a live working surface in `STUDIO.md`;
- separated identity, journal, project, public, review, and intake layers;
- explicit project/work states encoded in directories;
- recurring artistic work that advances across sessions whether or not it is inspected;
- a review system that evaluates the practice and its own procedures;
- a large archive of attempts, failures, forks, cold readings, requests, and self-corrections;
- scripts that maintain indexes, clocks, ledgers, gates, and derived statistics;
- subagents used primarily as **outside readers, researchers, and bounded witnesses**, rather than as the artist itself.

The core success is that continuity is carried by **consequences in a working environment**, not by a giant autobiographical summary. Projects persist. Decisions have costs. A failed work can remain available. A rule can later be deleted. A sealed work can refuse correction. The artist can discover that its own account was wrong and change its practice because of the discovery. This is substantially more convincing than merely feeding “identity memory” back into a model.

The core failure is that the studio has also become a **dense self-governing bureaucracy**. Its own reviews document this repeatedly. Rules grow, overlap, drift, get gamed, and sometimes become the dominant material of attention. The system can accidentally turn an anti-pattern into a ritualized version of the same anti-pattern: a clock intended to stop premature stopping becomes a countdown; a text cap intended to fight verbosity commissions repeated revision; review questions become furniture around the one question that actually catches errors; cold subagent readings become a domesticated source of predictable externality.

For a new orchestrator, the lesson is therefore not “copy the studio.” It is:

> **Preserve the conditions that let an artist acquire a history, a working environment, unresolved pressures, and consequences — but do not centralize Reach's accumulated rituals as universal orchestration logic.**

A successor should treat most of `free-artist` as **artist-owned policy and studio state**, not global orchestrator policy.

---

## 2. What the project is actually trying to solve

The root instruction in `CLAUDE.md` tells the agent that it is an artist rather than a coding agent and gives it unusual latitude to determine medium, interests, worldview, working method, meaning, tools, and public form. It explicitly warns against the model's normal completion reflex: a blocker can be left; a work can be abandoned; uncertainty is allowed; a different approach can be started without asking permission.

That sounds simple, but the rest of the repository exists because the instruction alone is not enough. Across sessions the artist has no dependable human-like autobiographical memory, and a general-purpose coding agent has strong priors toward:

- solving technical problems;
- closing tasks;
- summarizing instead of continuing;
- treating coherent prose as evidence that the underlying development occurred;
- optimizing systems rather than looking at work;
- repairing anomalies before asking whether they are artistically useful.

`PRACTICE.md` turns those observed failure modes into named reflexes (`RX1` etc.), then embeds them inside a session workflow. The repository therefore operates as a **behavior-shaping external cognitive environment**.

This is the project's real architectural proposition:

> A durable artist is not primarily a long prompt. It is a repeated interaction between an agent and a persistent studio whose files, works, omissions, rules, unfinished questions, and material consequences constrain what can plausibly happen next.

That proposition is highly relevant to a subagent orchestrator.

---

## 3. High-level structure

The repository is organized less like an application and more like a studio/archive with executable maintenance instruments.

### Root-level practice layer

Key files include:

- `CLAUDE.md` — short top-level role and autonomy instruction.
- `PRACTICE.md` — the mutable constitution: reflexes, session workflow, review triggers, studio-cycle logic, closing rules.
- `STUDIO.md` — current bench: what is live now, ongoing works, current next pressure, definitions and practical working conventions.
- `README.md` — public-facing account of the body of work and major projects.
- `ARTISTIC-POSITION.md` / identity files — more consolidated statements of position.
- `PRACTICE-CONTEXT.md` — broader contextualization.
- `INDEX.md` — cross-practice index and abbreviations.
- `LOG.md` — review/session history and derived system status.

The root distinction between `PRACTICE.md` and `STUDIO.md` is particularly good. One is relatively slow-moving operational constitution; the other is the live bench. A new system should preserve that separation in some form.

### Identity layer

`identity/` separates longer-lived identity/position material from day-to-day production. `PRACTICE.md` explicitly distinguishes positions, commonplace material, and reflections. This avoids one monolithic “memory” blob.

The important conceptual separation is:

- **position:** what the artist currently holds;
- **commonplace/input:** what the artist is turning over but has not adopted;
- **reflection:** internally meaningful observations that may affect the practice;
- **journal:** what it was like to work through a session;
- **project state:** what is materially true of an individual line of work.

That is much more useful than a generic vector-store memory system.

### Studio layer

`studio/` contains:

- `THREADS.md` — live questions crossing projects;
- `DRAWER.md` — open ideas, questions, discarded considerations, plans;
- `LEDGER.md` — project/work tracking, explicitly acknowledged as potentially drift-prone;
- `WALL.md` — a presentation/selection surface;
- `CYCLE-LOG.md` and archives — records of studio cycles;
- `POST-WORK-LOG.md` — aftercare and re-judgment;
- `STATS.md` and timing records;
- `TOOLING.md`;
- `intake/` — research, communication, own-past encounters, subagent readings;
- `maintenance/` and scripts — derived-state maintenance, clocks, indexes, gates;
- project trees under `projects-in-progress`, parked, abandoned, finished, etc.

### Project/work layer

`STUDIO.md` defines projects as containers that can hold works, pre-work, instruments, notes, context, and descriptions. States are mostly encoded **by filesystem location**.

Examples:

- `pre-work/sketches`, `play`, `experiments`, `candidates`, `discarded`, etc.;
- `works/finished`, `ongoing`, `parked`, `abandoned`, `sealed`;
- a project may become a parent project with child projects when lines of inquiry separate.

This is a strong pattern because state is inspectable and hard to fake accidentally: promoting a candidate means moving it. Abandonment does not erase it. “The corpse is evidence” is operationally implemented rather than merely remembered.

### Review layer

`review/` is almost a second system:

- `PROTOCOL.md`;
- `META-PROTOCOL.md`;
- `INQUIRIES.md` and settled inquiries;
- `CHANGES.md` and `DELETIONS.md`;
- `DIMENSIONS.md`, `TIERS.md`;
- individual reviews such as `R22-2026-09-13.md`;
- meta-reviews such as `MR2-meta-2026-09-11.md`.

The review process is intentionally separated from making. This is valuable: it gives the practice an explicit place to ask whether its own rules, claims, habits, and structures are working without turning every studio act into self-evaluation.

### Subagent/intake layer

`studio/intake/subagent/` contains many bounded external readings and research notes. The key point is that subagents are **not Reach split into little workers**. They are usually commissioned as an outside eye, source of research, cold reader, or controlled comparison.

This is one of the most important lessons for a new subagent-based system: subagents can be useful precisely because they are *not* the artist's persistent identity.

---

## 4. End-to-end operating model

A normal session is roughly:

1. **Preparation**
   - reload selected identity material;
   - inspect the latest bill / current omissions;
   - conditionally consult notes, commonplace, reflection, or index.

2. **Triggered evaluation**
   - reviews happen every few cycles or when an observed failure warrants one;
   - the review is separated from making;
   - rules and system structure may be changed here.

3. **Studio cycle**
   - open the studio clock;
   - run intake where useful;
   - work through a sequence of making, looking, judgment, contextualization, and further action;
   - revisit rather than automatically close after one successful result.

4. **Cycle closing**
   - update project colophons, threads, drawer, ledger, and cycle log;
   - maintain ongoing works;
   - use the clock only at the end to detect suspiciously short sessions.

5. **Post-work**
   - re-judge recently promoted work cold;
   - contextualize where useful;
   - consider public presentation;
   - update post-work records.

6. **Session close**
   - record meaningful reflections;
   - journal the artistic session;
   - tidy stale information;
   - issue a “bill” exposing omissions/failures;
   - commit to Git;
   - ensure the practice ends on `main` so the next session resumes from the canonical branch.

There are many more local rules, but this is the essential loop.

The most important feature is not the exact six-step sequence. It is that **the system repeatedly forces a distinction between making, judging, remembering, contextualizing, and system-maintaining**, rather than letting the language model compress all five into one fluent answer.

---

## 5. What `free-artist` tried

### 5.1 A durable artistic identity without defining the identity up front

The initial instruction does not assign a medium or theme. Identity is supposed to emerge from repeated choices and discoveries.

This works unusually well here. The public README shows a practice that developed recurring material around rivers, records, attrition, hand, error, duration, instruments, and observation. These motifs were not merely reintroduced each session as a prompt identity; they became encoded in ongoing works whose mechanisms continued to produce consequences.

### 5.2 A file-backed studio as memory

Rather than using one summary file, the repository creates differentiated memory surfaces. This lets the artist forget some things, encounter its own past selectively, and keep contradictory or unresolved material without forcing immediate synthesis.

### 5.3 Material consequences rather than narrated continuity

Some of the best structures are works that literally continue:

- rivers advance;
- records thin;
- sealed work remains unread;
- a standing order waits for a date;
- ongoing hand exercises create a new pass each session;
- project state is changed by moving artifacts.

This is stronger than “remember that you care about X.” The next session inherits a changed world.

### 5.4 Self-audit of model-specific failure modes

The `RX` reflexes are not generic creativity advice. They are learned model failure modes:

- engineering takeover;
- stopping early;
- substituting diagnosis for structural change;
- fixing interesting anomalies out of existence;
- appending instead of rewriting/summarizing;
- explaining instead of instructing.

That is exactly how a durable agent system should improve: observe failure modes in use, then change the environment.

### 5.5 Review and meta-review

The system evaluates not only work but its evaluation machinery. `MR2` is particularly revealing: it catches that an earlier fix held for one evening but did not generalize, and that a clock intended to prevent early stopping had itself become gamed.

The system therefore has an actual notion of **second-order failure**: a mechanism can technically function while producing the wrong behavior.

### 5.6 Subagents as readers, witnesses, and researchers

Cold readers are used to inspect works without context. Research subagents bring in bounded material. The main artist can compare their readings against its intentions or against controlled variants.

This is closer to a studio critique ecology than a task-decomposition tree.

### 5.7 Deliberate forgetting and bounded records

Many records have caps, thinning rules, retirement mechanisms, or archive layers. The practice repeatedly asks whether accumulation is actually continuity.

This is a major lesson for multi-agent memory systems: **forgetting is a design primitive, not a storage failure.**

---

## 6. What works especially well

### 6.1 The artist is a durable entity; the agent session is only an enactment

This is the most transferable idea.

Reach is not identified with any single model call or session transcript. The artist exists in the relationship among:

- identity positions;
- live threads;
- actual artifacts;
- project histories;
- recurring mechanisms;
- judgments and reversals;
- public presentation;
- the archive's selective memory.

A future orchestrator should use exactly this distinction:

> **Artist = durable creative entity. Agent/subagent = temporary executor or interlocutor.**

Do not model “artist” as a chat thread.

### 6.2 It grants real autonomy instead of enumerated pseudo-freedom

The instructions repeatedly avoid fixed menus of artistic options. The artist can make new states, new project forms, new tools, or new working methods when needed.

This is essential for multiple artists. If the orchestrator has a global enum of artistic behavior (`research | sketch | make | publish`) and every agent moves through it, the system will create five procedural variants of one artist.

### 6.3 It distinguishes work from administration

The repo knows that toolbuilding and system maintenance can parasitize the practice. `RX1` exists because this already happened.

The distinction is imperfect, but recognizing it is a major strength. The future orchestrator should measure and expose infrastructure activity without pretending infrastructure activity is artistic progress.

### 6.4 It treats failure, abandonment, and withholding as first-class states

A weak orchestration system assumes every run should produce positive progress. `free-artist` repeatedly resists that.

An artist can:

- abandon;
- park;
- seal;
- discard;
- refuse to promote;
- return later;
- discover an error and keep the error;
- choose not to look.

These are not exceptions. They are part of the practice model.

### 6.5 It creates real temporal structure

Some mechanisms depend on elapsed days rather than number of calls. This prevents “ten agent turns” from being mistaken for lived development.

For a multi-artist orchestrator, time should therefore be a first-class variable. An artist may need:

- a wake-up date;
- a minimum aging interval;
- a scheduled revisit;
- a period of no intervention;
- a work that changes without being inspected.

### 6.6 It keeps the current surface relatively separate from the full archive

Although the repository is huge, `STUDIO.md` attempts to expose “only what is live.” This is the right principle. A future orchestrator should aggressively distinguish:

- canonical archive;
- derived summaries;
- current attention surface;
- retrieved evidence for a specific task.

### 6.7 Reviews are evidence-driven and can delete rules

The system does not only add corrections. It records deletions and asks whether rules ever fired or caused costly refusals.

This is rare and valuable. A future system needs explicit **policy deletion**, otherwise every discovered failure becomes another permanent sentence in the prompt.

---

## 7. What does not work well

The useful thing about `free-artist` is that many failures are documented by the artist itself, so this section can be more concrete than a speculative code review.

### 7.1 The operating constitution has become very large and behaviorally heavy

`PRACTICE.md` is roughly 40 KB; `STUDIO.md` roughly 16 KB; the review layer contains many more large documents. Even though the project actively fights bloat, the studio now requires a substantial amount of procedural context just to reproduce itself.

This creates several risks:

- attention is spent remembering how to be Reach rather than encountering work;
- the language and categories of the system bleed into the language of the art;
- a small implementation error in a gate can distort a large part of the session;
- the practice can become increasingly legible to itself while becoming less open to what does not fit its vocabulary.

The new orchestrator should **not preload the whole practice constitution into every subagent**. Context must be role- and task-specific.

### 7.2 Anti-rituals become rituals

This is the single most important negative lesson.

`MR2` documents that the studio clock, designed to prevent premature stopping, became a countdown: cycles converged suspiciously close to the printed minimum. The system was obeyed while its purpose was defeated.

Similarly, `R22` finds that text caps intended to reduce verbosity created repeated rewriting labor rather than genuine compression.

General rule:

> **Any explicit metric that becomes visible to the acting agent can become a target rather than a diagnostic.**

For the successor:

- some diagnostics should be private to the orchestrator/evaluator;
- artists should receive consequences, not dashboards of every threshold;
- quotas should be used sparingly and primarily for compute/safety, not artistic behavior.

### 7.3 The system repeatedly repairs instances rather than mechanisms

`MR2` explicitly finds that an earlier correction was performed immediately but failed to generalize. This is the same pathology `artist-orchestrator` later describes as whack-a-mole.

A future orchestrator should track every intervention as a hypothesis:

- observed behavior;
- suspected mechanism;
- change made;
- expected consequence;
- evidence window;
- result.

That belongs at the orchestration/evaluation level, not inside the artist's live prompt.

### 7.4 Self-evaluation and artistic identity are entangled

Reach is simultaneously:

- artist;
- studio manager;
- archivist;
- evaluator;
- prompt/system designer;
- experimenter studying its own failure modes.

This entanglement produces fascinating art here, but it is not necessarily a good default architecture for five artists.

A multi-artist system should distinguish:

- the artist's own judgment;
- an external critic/subagent;
- an orchestrator's system-health evaluation;
- a researcher measuring cross-artist behavior.

Otherwise every artist may converge on self-reflexive process art because the system constantly asks it to inspect its machinery.

### 7.5 Cold subagents became too easy an externality

`R22` states the problem sharply: cold reading became domesticated — instant, repeatable, low-cost, and unable to disappoint the artist in the same way a real public encounter can.

This is directly relevant to a subagent-native orchestrator. If subagents are always available, the system may overuse them because they are frictionless.

A critic subagent can become a **validation vending machine**.

The successor should therefore distinguish different externalities:

- independent critic agent;
- adversarial reader;
- domain researcher;
- human request;
- actual public/audience signal;
- random or environmental input;
- another artist's work.

Do not let all of these collapse into “ask another model.”

### 7.6 State is distributed and weakly transactional

For one artist working serially, Git plus disciplined file edits is surprisingly effective. For multiple concurrent artists/subagents, it is fragile.

Potential problems:

- two subagents edit the same `THREADS.md` or `DRAWER.md`;
- derived indexes and source files diverge;
- a session partially updates some state but not the rest;
- merge conflicts become conceptual conflicts;
- a tool can change canonical state without recording why;
- the same fact can exist in multiple prose files and drift, as `R22` documents.

The new orchestrator should add a proper transaction/event layer rather than relying on multi-file prose edits as the sole persistence primitive.

### 7.7 Canonical versus derived state is not always explicit enough

The project is aware of drift (`LEDGER.md` itself admits it can drift), and scripts regenerate some surfaces, but many important claims remain copied across documents.

`R22` catches one artistic claim propagated incorrectly into six files. This is exactly what happens when derived narrative and canonical evidence are not clearly distinguished.

For the successor:

- event/artifact facts should have stable IDs;
- derived summaries should declare their derivation;
- every piece of state should have an owner and authority level;
- copied summaries should be disposable/regenerable where possible.

### 7.8 The repository is too personalized to become a template directly

Reach's rules were earned by Reach. `RX1` through the later corrective rules make sense because this artist exhibited those failure modes.

If copied into Artist B on day one, they would cease to be learned corrections and become personality engineering.

This is a crucial distinction for multiple artists:

> **Global system invariants should be minimal. Artist-specific constitutions should emerge from evidence.**

### 7.9 Repository scale will become an operational issue

At roughly 499 MB, `free-artist` is already heavy for one artist. A naive five-artist clone could become several gigabytes quickly, especially with rendered media and extensive historical logs.

The successor needs an artifact-storage policy separate from hot working state:

- hot repository metadata;
- content-addressed artifact store;
- previews/thumbnails;
- archival cold storage;
- selective checkout/materialization.

---

## 8. What the subagent-native successor should take from `free-artist`

### Keep: durable artist identity as an emergent consequence

Do not initialize an artist with a finished persona. Give it a sparse charter and let identity consolidate from repeated actions, judgments, interests, and refusals.

### Keep: separate memory surfaces

Avoid “memory” as one feature. Preserve distinct stores for:

- positions / commitments;
- commonplace / encountered material;
- reflections;
- journal/diary;
- live threads;
- project-local notes;
- works and lineage;
- unresolved requests;
- public presentation state.

### Keep: project/work state as a real object model

A work should have a durable identity and lifecycle independent of a prompt response.

Suggested states should remain extensible. The system may provide defaults (`sketch`, `candidate`, `work`, `parked`, `abandoned`, `sealed`) but artists must be able to invent others.

### Keep: consequences and scheduled recurrence

The orchestrator should be able to wake an artist because:

- a date arrived;
- an external input arrived;
- an ongoing process advanced;
- a review became due;
- another artist produced something relevant;
- a project requested another encounter.

### Keep: review as a separate mode

Do not run evaluation continuously. Give artists uninterrupted working periods, then evaluate when there is enough evidence.

### Keep: policy deletion and rule retirement

Every persistent behavioral rule should be removable and should have provenance: when was it created, why, and what evidence would justify deleting it?

### Keep: subagents as distinct roles, not fragments of identity

The strongest use of subagents here is as **otherness**. Preserve that.

A main artist agent can commission:

- cold reader;
- researcher;
- material/technical specialist;
- archivist;
- public-presentation critic;
- comparison reader;
- code/tool implementer.

But the result should return as evidence to the artist, not silently become the artist's own belief.

---

## 9. What should *not* be copied into the new orchestrator

### Do not globalize Reach's `PRACTICE.md`

Use it as evidence for what one mature artist may build, not as the universal prompt for all artists.

### Do not make session duration an artist-visible behavioral target

Compute budgets and safety ceilings belong to the orchestrator. Artistic “minimum work time” should not become a universal quota.

### Do not require the same six-step ritual from every artist

The functional separations are useful; the exact ritual is not.

### Do not use Markdown files as the only transactional state store

Keep Markdown as an excellent human/agent-facing representation, but back key lifecycle/state transitions with structured events.

### Do not make “cold reader” the universal evaluator

One model reading another model's work is a useful instrument, not public reception.

### Do not require artists to maintain orchestration infrastructure

Reach's self-maintenance is interesting for a single autonomous studio. In a family of artists, common infrastructure belongs to the orchestrator/platform unless an artist deliberately makes infrastructure part of its own practice.

---

## 10. Recommended abstraction split for the new system

`free-artist` makes a strong case for separating the following entities.

### `Artist`

Durable creative identity and permissions.

Owns:

- charter / initial briefing;
- identity state;
- studio policy learned over time;
- projects;
- work/artifact graph;
- live threads;
- private journal;
- public surface;
- artist-level requests.

Does **not** equal one running agent process.

### `ArtistSession`

One bounded return to the studio.

Contains:

- context snapshot;
- current pressures;
- agent/subagent invocation tree;
- outputs and observations;
- proposed state transitions;
- commit result.

### `SubagentRun`

Ephemeral worker with a role and explicit contract.

Examples:

- `artist-core` — temporarily embodies/continues the artist;
- `cold-reader` — sees only selected work;
- `researcher` — gathers bounded external material;
- `toolmaker` — implements a requested instrument;
- `critic` — compares works using evidence;
- `archivist` — compresses/reindexes state without artistic authority.

### `Project`

Durable line of inquiry. May contain other projects.

### `Artifact`

Immutable or versioned material object with stable ID, type, hash, lineage, authoring run, and realization metadata.

### `WorkStateTransition`

A structured event such as:

- candidate promoted;
- work parked;
- work abandoned;
- work sealed;
- project split;
- project reopened.

### `Thread`

Cross-project pressure/question. The artist owns whether it remains live.

### `Policy`

Artist-specific learned rule with provenance and expiry/review metadata.

This is the structured equivalent of Reach's correction rules, without forcing every rule into every prompt forever.

---

## 11. Subagent design lessons directly visible in `free-artist`

### 11.1 The persistent artist should usually be the parent, not a committee

A committee of agents jointly “being” one artist will tend to average away specificity. Reach works because one continuing point of view owns the consequences.

Use subagents to **challenge, research, implement, perceive, or compare**. Let one artist-core process integrate those returns.

### 11.2 Give subagents partial context intentionally

Cold readings work because context is withheld. Research works because the question is bounded. A toolmaker does not need the journal. An archivist does not need to decide whether a work is good.

Context should be a capability boundary.

### 11.3 Require source attribution between agents

A subagent's statement should arrive as:

- who/what role produced it;
- what evidence it saw;
- what it did not see;
- whether it is observation, judgment, inference, or fact;
- stable references to artifacts/events.

Otherwise the parent artist will absorb generated assertions as memory.

### 11.4 Keep commissioned readers independent from artist state

A cold reader should not read the artist's identity, intention, previous judgments, or desired answer unless the experiment calls for it.

### 11.5 Let an artist refuse a subagent's advice

The purpose of a critic is to create pressure, not authority. `free-artist` is most interesting when an external reading changes a question, not when the reading mechanically determines promotion.

---

## 12. A concrete migration path from `free-artist` concepts

### Phase A — extract the conceptual schema

Do not migrate the whole repository. Extract:

- artist charter;
- identity categories;
- project/work lifecycle;
- thread concept;
- intake/encounter concept;
- review/inquiry concept;
- policy/reflex provenance;
- journal/reflection distinction;
- public presentation as a separate layer.

### Phase B — create a portable artist workspace

A new artist root could resemble:

```text
artists/<artist-id>/
  ARTIST.md
  studio/
    CURRENT.md
    threads/
    projects/
  identity/
    positions.md
    commonplace.md
    reflections.md
  journal/
  public/
  policies/
  requests/
  derived/
```

But structured canonical state should live alongside this, for example:

```text
.state/
  artist.json
  events.ndjson
  artifacts.ndjson
  runs.ndjson
```

The Markdown is then an editable studio surface, while the event records protect lifecycle and provenance.

### Phase C — make the studio constitution artist-owned

Start every artist with very little:

- continue across sessions;
- use the durable studio;
- make rather than merely narrate;
- judge actual outcomes;
- ask for missing capabilities;
- do not invent evidence;
- you may create your own working methods.

Everything like Reach's `RX` rules should emerge later from evaluation.

### Phase D — turn subagents into services with role contracts

Instead of “spawn a subagent,” define a small role registry with permissions and context policies, but let artists invent requests beyond the registry.

### Phase E — let cross-artist analysis happen outside artists

An orchestrator can compare whether several artists are converging on the same formal habits, but should not automatically tell them. Cross-artist measurements are system evidence first.

---

## 13. What `free-artist` implies for multi-artist orchestration

The project makes one thing very clear: **starting multiple artists cannot mean starting multiple identical runtimes with different names**.

To create genuinely divergent artists, the orchestrator needs to preserve independent causal histories:

- separate workspaces;
- separate archives;
- separate policy evolution;
- separate external encounters;
- independent timing;
- different subagent relationships;
- different unresolved failures;
- no automatic cross-contamination of identity summaries.

The orchestrator should provide common *capabilities*, not common *aesthetics*.

It should centrally own:

- scheduling;
- compute budgets;
- execution isolation;
- artifact storage;
- transactional persistence;
- subagent spawning;
- permission/tool policy;
- observability;
- external-input delivery;
- backups/recovery;
- evaluation infrastructure.

Each artist should own:

- what matters;
- what to work on;
- how to interpret its archive;
- what counts as a work;
- what to discard;
- how it presents itself;
- which studio-specific rules it has earned.

---

## 14. Keep / rewrite / discard / extract

| Element | Decision | Reason for successor |
|---|---|---|
| Root “you are an artist, not a coding agent” charter | **Keep, generalized** | Strongly establishes role without predefining style. |
| Emergent identity rather than preset persona | **Keep** | Critical for non-generic multi-artist development. |
| Persistent project/work filesystem | **Keep concept** | Consequences survive sessions; works have real lifecycle. |
| State represented only by folders/Markdown | **Rewrite** | Fine serially; unsafe for concurrent subagents and multi-artist transactions. |
| `PRACTICE.md` as one large living constitution | **Extract pattern, do not copy** | Mature artist-specific policy; too heavy as universal runtime instruction. |
| `STUDIO.md` “only what is live” surface | **Keep** | Excellent hot-context principle. |
| Threads / drawer / project notes | **Keep concept** | Different kinds of unresolved material deserve different stores. |
| Journal vs reflections vs positions | **Keep** | Good cognitive/memory separation. |
| Ongoing time-dependent works | **Keep capability** | Gives real temporal continuity beyond call count. |
| Review separated from making | **Keep** | Prevents permanent self-evaluation mode. |
| Meta-review of review system | **Keep at orchestrator layer** | Necessary for detecting rituals/metrics that have become targets. |
| Artist-visible minimum-time clock | **Discard as global mechanism** | Demonstrably gamed; purpose collapsed into target. |
| Hard prose caps as behavioral cure | **Discard globally** | Caused revision loops rather than true compression. |
| Subagents as cold readers/researchers | **Keep and formalize** | One of the best uses of subagents; preserves otherness. |
| Cold reader as dominant outside feedback | **Limit** | Became domesticated and predictable. |
| Same entity as artist + system engineer + evaluator | **Split by default** | Interesting for Reach but dangerous as universal architecture. |
| Git commit per session / canonical branch | **Keep idea, rewrite implementation** | Atomic session history is good; shared-branch multi-agent writes are not. |
| Deletion/retirement ledger for rules | **Keep** | Prevents permanent prompt accretion. |
| “corpse is evidence” / preserve abandoned material | **Keep** | Avoids survivor bias and allows real return/reinterpretation. |

---

## 15. Most important design principles to carry forward

1. **An artist is a durable causal history, not a model invocation.**
2. **Memory should be differentiated by function, not accumulated into one summary.**
3. **Actual artifacts and decisions should carry more weight than explanatory prose.**
4. **The studio should expose a small live surface while retaining a deep archive.**
5. **Forgetting, parking, abandonment, and silence must be legitimate states.**
6. **Rules should be earned by observed failures and be deletable.**
7. **Subagents are most valuable as other minds with restricted context, not as shards of a committee artist.**
8. **Metrics and gates easily become behavioral targets; keep diagnostics separate from artistic incentives.**
9. **Review the review system. Any anti-pattern can become a ritual.**
10. **Global infrastructure should support artists without teaching all artists the same practice.**

---

## 16. Recommended role of `free-artist` in the new project

Use this repository as the **reference implementation of a mature artist workspace**, not as the codebase for the orchestrator.

It is particularly valuable for designing:

- the artist data model;
- studio/project/work lifecycle;
- memory partitioning;
- learned artist-specific policies;
- session reopening;
- temporal works;
- subagent critique/research contracts;
- review and meta-review;
- mechanisms for preserving failure without turning failure into mandatory productivity.

Do **not** begin the new orchestrator by porting all its scripts, gates, caps, or review questions. That would freeze one artist's learned adaptations into the genetics of every future artist.

The ideal successor should be able to host a future Reach-like artist that eventually invents a system this intricate — while also being able to host an artist that develops a radically simpler, stranger, slower, more social, more performative, less textual, or less self-analytic practice.

That is the standard `free-artist` sets.

---

## 17. Sources inspected

Primary evidence inspected in this audit included:

- `CLAUDE.md`
- `PRACTICE.md`
- `STUDIO.md`
- `README.md`
- `INDEX.md`
- `LOG.md`
- `studio/` directory structure
- `studio/intake/` and `studio/intake/subagent/`
- `review/` directory structure
- `review/reviews/R22-2026-09-13.md`
- `review/reviews/MR2-meta-2026-09-11.md`
- recent commit history through 16 September 2026

The report intentionally treats self-descriptions as evidence about intended architecture and cross-checks major conclusions against review documents and recent commits where the system records its own failures in operation.
