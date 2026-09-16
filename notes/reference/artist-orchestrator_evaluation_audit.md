# `artist-orchestrator` — Architecture and Orchestration Audit

**Repository:** `Inannis/artist-orchestrator`  
**Default branch:** `main`  
**Audit head inspected:** `9620ae7275d9c5f203ffcabb219e8f7d4908dcce` (29 August 2026)  
**Repository size reported by GitHub:** ~12,587 KB  
**Audit purpose:** evaluate the existing multi-artist/free-tier orchestration experiment as a starting point for a new **subagent-native orchestrator** capable of running multiple persistent artists.

---

## 1. Executive assessment

`artist-orchestrator` is much closer than `free-artist` to an actual orchestration platform. It already contains several ideas that belong in a successor almost unchanged at the conceptual level: a registry of artists, lifecycle states, separate practice/support/orchestration concerns, bounded context assembly, durable state and append-only events, artifact lineage, external-input receipts, transactional writes, quarantine, execution telemetry, post-mortems, and an evidence-led evaluation loop.

Its deepest architectural insight is stated directly in `AGENTS.md`: when something goes wrong, distinguish among three levels:

1. **Practice** — what the artist is doing and becoming.
2. **Artist-support system** — memory, workflows, tools, prompts, archives, perception, etc.
3. **Orchestration** — how the system observes, schedules, evaluates, compares, and improves artists.

That separation is excellent. It should be one of the successor's invariants.

The current implementation, however, was built around a constraint that the proposed successor deliberately removes: the artists are enacted by **short, free-tier, stateless or weakly stateful external LLM calls** with strict quota, token, provider, and networking limitations. A great deal of the repository is therefore machinery for making unreliable small calls behave like a persistent artist: provider routing, prompt packing, bounded transcript replay, continuation handles, repair calls, JSON normalization, token budgeting, caching probes, retry/backoff, GitHub Actions as a remote execution environment, and elaborate validation around responses that cannot directly operate a workspace.

A subagent can usually do something qualitatively different. It can be given a workspace, inspect files itself, use tools, make several decisions in one run, render or inspect artifacts, research when permitted, edit the studio directly, and return after a meaningful period of work. That means the successor should **not simply replace the HTTP call inside `llm_kernel` with a subagent invocation**. Doing that would preserve the old system's most limiting assumption: that the artist is fundamentally a sequence of tiny response envelopes.

The better migration is more radical but also simpler:

> **Keep the durable domain model and experimental discipline. Replace the call-shaped artistic runtime with an agent-run-shaped runtime.**

The current repository should be mined in two different ways:

- **Preserve:** lifecycle, state boundaries, event/artifact integrity, evidence discipline, isolation, provenance, evaluation, post-mortems, run tracing, context policies, quarantine.
- **Retire or radically rewrite:** provider kernel, route ladders, token-budget-driven stage machinery, output-envelope choreography, provider session continuity, prompt-cache probes, and the 400 KB monolithic runner.

The successor's central unit should become a **run tree** rather than an LLM call: one persistent artist may be enacted by a primary artist subagent, which can itself delegate bounded research, criticism, rendering, technical implementation, or observation to other subagents. The orchestrator controls resources, isolation, scheduling, and evidence; it should not prescribe the artist's internal sequence of thought or force every artistic return into the same storage-shaped JSON grammar.

---

## 2. What problem `artist-orchestrator` was designed to solve

The project starts from a difficult premise: a sequence of model calls should develop something closer to an evolving artistic practice than a collection of unrelated generated works held together by retrospective prose.

`AGENTS.md` makes the distinction explicit. The goal is not just output. The system is supposed to support, over time:

- evolving identity;
- partial but consequential memory;
- interests, fears, positions, taste and recurring questions;
- research and encounters;
- works in progress rather than one-shot generation;
- experiments, failures, judgment, promotion, abandonment and withholding;
- contextualization;
- public presentation;
- multiple artists whose differences can reveal whether a behavior is systemic or accidental.

The original technical difficulty was that the actual model invocations were short-lived. A free-tier call has no durable studio. It does not know the full prior practice unless context is reconstructed. It may not be able to see a generated work. It may fabricate an empirical operation. Different providers have different continuation semantics and quotas. A malformed response can corrupt the next cycle unless validation is strict.

The repository therefore treats the **files and runtime as the artist's persistent body**, while each model call temporarily enacts it. This is a valuable idea even after direct LLM calls disappear. What changes in the successor is the duration and capability of the enactment.

The old proposition is roughly:

> persistent artist = durable files + carefully packed context + a sequence of bounded LLM calls.

The successor should revise that to:

> persistent artist = durable studio + history + policy + permissions + a sequence of bounded agent runs, each capable of actually working inside that studio.

The difference sounds small but changes almost every orchestration decision.

---

## 3. Repository architecture

At the inspected head, the root structure is roughly:

```text
artist-orchestrator/
├── AGENTS.md
├── Artist3/
├── Artist4/
├── Artist5/
├── Post-Mortems/
├── Notes/
├── llm_kernel/
├── tools/
├── runtime.py
├── .github/
└── .diagnostics/
```

This already expresses the correct high-level separation better than many agent systems do.

### 3.1 `AGENTS.md`: orchestration constitution

`AGENTS.md` describes the orchestrator as the manager of a family of artists and the builder of the system that allows those artists to persist. It tells the orchestrator not to make the art directly; if an artist's practice is failing, the orchestrator should modify underlying conditions instead of intervening in the work itself.

Particularly good rules include:

- keep artist instructions concise so the system does not dominate artistic attention;
- avoid narrow menus of predefined artistic identities;
- prefer evidence from actual practice over architectural speculation;
- use bounded experiments;
- distinguish practice, support, and orchestration failures;
- scale interventions to the problem;
- avoid multiple simultaneous major changes when possible;
- preserve phased-out artists and write post-mortems;
- reconsider the architecture if maintenance grows faster than art or if continuity exists mainly in explanatory text.

Those are not implementation details. They are strong governance principles for the successor.

### 3.2 `llm_kernel/`: provider transport layer

The `llm_kernel` directory contains the infrastructure that normalizes external model calls:

- `models.py` — provider-neutral request/response value objects, usage, media, conversation context and normalized outcomes;
- `providers.py` — Gemini / OpenAI-compatible provider adapters;
- `kernel.py` — routing, retry and fallback behavior;
- `config.json` / `config.py` — provider definitions, artist registry, ordered model routes;
- `call_logging.py` — safe telemetry;
- `media_capabilities.*` — transport/archive media compatibility;
- `run.py` — the outer sequential multi-artist execution loop;
- tests.

The kernel is intentionally meant to know almost nothing about artistic practice. That boundary is sound. The particular implementation is mostly legacy for a subagent-native future.

### 3.3 `runtime.py` and `llm_kernel/run.py`: outer multi-artist loop

The repository-level `runtime.py` merely calls `llm_kernel.run.main()`.

`llm_kernel/run.py` describes itself as a **sequential multi-artist loop entry point**. It loads the artist registry, selects targets, then launches the configured artist runner as a subprocess. It records run-level status and can stop or continue on failures.

This is multi-artist in the sense that multiple artist roots are registered and independently invokable. It is not yet a genuine concurrent or hierarchical orchestrator. There is no task graph, no fan-out/fan-in, no dependency scheduling, no nested delegation tree, and no resource-aware parallel execution between artists. The process explicitly runs one artist at a time.

That simplicity was defensible under API quotas. It should not be preserved accidentally once subagents become the execution substrate.

### 3.4 Per-artist roots

`Artist3/`, `Artist4/`, and `Artist5/` contain isolated artistic practices. Artist3, for example, has:

```text
Artist3/
├── BRIEFING3.md
├── artifacts/
├── publication-site/
├── runtime/
└── site/
```

The root-level briefing establishes the artist's open contract. `BRIEFING3.md` is notably restrained: it says that the artist is continuing; its archive is partial but real; medium and identity are not predetermined; artifacts should actually be made and judged; change should arise from consequences; and the surviving archive is a partial past rather than omniscient memory.

That is a strong artist bootstrap design.

### 3.5 `Artist3/runtime/`: reusable transactional runtime

Artist3's runtime became the shared implementation for several artists. It includes:

- `PROMPT.md`;
- `runner.py`;
- `state.json`;
- `events.ndjson`;
- `turns.*`;
- journal, diary and research surfaces;
- pending-input queues;
- observation material;
- quarantine;
- exact call-input archives;
- extensive tests.

The design intention is good: each artist's artistic data belongs under its own root, while the reusable mechanics can be shared.

The implementation problem is visible in the file sizes: `runner.py` is approximately 400 KB and the associated test file approximately 200 KB. It has accumulated context assembly, prompt construction, parsing, artifact validation, reference normalization, media processing, reality checking, free-studio extraction, state mutation, prepared transactions, external input, perception seams, locking, diary rules, staged sessions, and provider interaction glue.

That is too many responsibilities in one module, even if each responsibility was individually justified by a real failure.

### 3.6 `Notes/`: the orchestration research laboratory

The `Notes/` tree is a major part of the project rather than incidental documentation. It contains:

- `Artistic-Practice-Definition.md`;
- evaluation protocols;
- status and handoff documents;
- provider/model limit research;
- plans and implementation records;
- capability ownership;
- invocation notes;
- post-mortems;
- project knowledge;
- inquiries and evaluation material.

This records not only *what the code does*, but *why the system changed*. That is extremely valuable for a successor because many seemingly arbitrary runtime features have corresponding failure evidence.

The risk is that this research apparatus can itself become an administrative practice. The project's own evaluation protocol correctly warns that a technically excellent system can support weak art, and that a healthy system should increasingly disappear behind the practice.

---

## 4. Current end-to-end execution flow

A useful way to understand the system is to trace one artist return.

### 4.1 Select an artist

`llm_kernel/config.json` registers artists with fields such as:

- enabled/disabled;
- lifecycle phase;
- root path;
- runner path;
- ordered provider/model routes.

At the inspected state:

- Artist3 is active and routed through Gemini models;
- Artist2 is disabled/phased out;
- Artist4 is disabled/phased out;
- Artist5 is active as a comparison practice and has a Groq ladder followed by NVIDIA fallbacks.

The important part here is not the providers. It is the **artist registry and lifecycle semantics**. An artist can exist in the system without being runnable. Phasing out does not mean deleting.

### 4.2 Spawn the artist runtime

The outer loop launches the artist runner as a subprocess with its root, registry identity, run identifier, and bounded work-period settings.

This gives each run an explicit execution boundary. A successor should preserve that concept, even if the subprocess becomes an isolated agent workspace or sandbox.

### 4.3 Assemble bounded artistic context

The artist runtime reads:

- the artist briefing;
- the common runtime prompt;
- current durable state;
- recent events;
- relevant artifact excerpts;
- recent journal/diary/research material;
- pending external inputs or observations;
- staged-period state when appropriate.

It deliberately does not feed the entire archive into every call. This is essential. A persistent artist needs selective memory, not maximal memory.

### 4.4 Archive the exact call input

A later evolution of the runtime writes the exact model-facing input to `runtime/call-inputs.ndjson` before network traffic. If the input cannot be archived, the call is not sent.

This is a strong reproducibility boundary. For subagents, the equivalent should be an immutable **run manifest** containing at minimum:

- run ID and parent run ID;
- artist ID;
- role specification;
- selected context snapshot / references;
- permissions and tools;
- workspace revision;
- task/invocation text;
- orchestration policy version.

Unlike the old call input, a subagent run may also need to record the files it was allowed to inspect or mutate, because the workspace itself is part of the effective prompt.

### 4.5 Execute through the provider kernel

The kernel chooses the configured route, makes the API request, retries bounded failures, follows fallback routes, and records safe telemetry.

This layer solved real operational problems, but it is mostly the piece to delete when moving to subagents.

### 4.6 Parse and validate the response

`PROMPT.md` requires one JSON object containing a large envelope of possible state transitions:

- `move`;
- `artifacts`;
- `memory_events`;
- `journal_entries`;
- `diary_entries`;
- `research_entries`;
- `work_period`;
- `judgements`;
- `next_attention`;
- `input_requests`.

References are checked against actual supplied IDs or same-response local artifact numbers. Unsupported claims can trigger a private “reality witness.” Malformed JSON may receive a repair attempt. Invalid responses go to quarantine rather than mutating the artist.

This is an impressive integrity layer. It is also one of the system's most important artistic liabilities, discussed later.

### 4.7 Stage and commit a transaction

Accepted artifacts receive safe IDs and paths, hashes are checked, state is updated, and an append-only event records the transition. The runner uses locks and prepared transaction recovery to avoid partial/corrupt state mutation.

This is exactly the kind of boring infrastructure that a successor should keep.

### 4.8 Record separate operational telemetry

Central logs intentionally avoid prompts, completions and raw media. They capture provider/model attempts, latency, failure reasons, fallbacks and token usage. Per-artist turn ledgers record artistic-stage and development metadata.

The distinction between **operational telemetry** and **artistic memory** is good. Diagnostics should not quietly become the artist's autobiography.

### 4.9 Evaluate after evidence accumulates

`AGENTS.md` and `Notes/evaluation-protocol.md` establish an explicit operation → evaluation → implementation cycle, with longer evidence windows as the system matures. Important findings become inquiries with suspected mechanisms, proposed interventions, expected consequences, evidence windows, decision points, and falsifiers.

This is unusually disciplined for an agent project and should be retained.

---

## 5. What the project tried over time

The repository is most useful when read as a sequence of architectural experiments rather than one finished design.

## 5.1 Artist1: compact continuity can work

Artist1's post-mortem records a coherent visual practice around interruption, interval and recurrence. It produced studies, a selected public sequence, later animated work, forks, preserved parents and deliberate withholding.

The system learned that a surprisingly small file studio could carry:

- attention;
- judgment;
- threads;
- artifact lineage;
- enough prior consequence to make later returns materially different.

It also learned the importance of **perception before promotion**: seeing the operative work in a browser changed judgments that source inspection alone could not settle.

Artist1 is evidence that continuity does not require an enormous autobiographical memory layer. This is a foundational finding for the successor.

## 5.2 Artist2: the schema can become the practice

Artist2 is the project's clearest failure and therefore one of its most valuable experiments.

Across 39 committed calls it made 38 supporting artifacts but no primary work. The practice narrowed into an engineering successor chain. Each call solved or approved a prerequisite and generated another prerequisite. Unsupported physical operations and measurements entered durable history. Once those claims were corrected, the practice reorganized itself around waiting for unavailable physical evidence.

The post-mortem identifies several causes, but one is especially relevant:

> the response architecture required each call to narrate a consequential move, and generated `next_attention` repeatedly became the next call's current pressure.

In other words, the persistence schema was not neutral. It created a tempo: move → record successor → enact successor → record successor. The model's engineering prior filled that channel with technical prerequisites.

Later changes such as representative memory, images, provenance boundaries and reality checking fixed local issues but did not break the deeper loop. Allowing `move: null` finally removed the compulsory artifact/action, but by then it exposed that the practice itself had become organized around waiting.

This is the single strongest warning for a subagent successor:

> **Do not make the artist speak the database schema every time it works.**

The storage model should be able to represent the artistic return without becoming the artistic return.

## 5.3 Artist4: freedom alone does not create operative judgment

Artist4 was a reaction against Artist2. The two-stage “free studio” removed compulsory JSON composition and allowed free prose and exact artifact blocks, with private archival extraction afterward.

Several things improved:

- prose could remain prose;
- null action and null attention could be honest;
- outside input could enter naturally;
- rendered/browser-faithful work could be returned to the artist;
- seeing a work could interrupt production rather than force another artifact.

But another failure appeared. Over twelve openings the practice converged on a near-black field, thin line, monospace inventory and terminal cadence. Earlier visual work, when reintroduced, was rewritten into the same late style. The artist did not develop explicit comparative judgment between materially different works.

The post-mortem describes continuity as a **stylistic attractor rather than operative judgment**.

This is an important counterweight to Artist2. The lesson is not “remove all structure.” The lesson is that a persistent practice needs ways for prior works, failures and outside encounters to exert pressure on later decisions without the orchestrator simply telling the artist what to choose.

A subagent architecture is actually well suited to this because a critic/observer subagent can return a reading without the orchestrator converting that reading into a mandatory next task.

## 5.4 Artist3 / Artist5: transactional runtime and sustained periods

Later work focused on making the runtime more robust and less call-fragmented:

- adaptive work periods;
- multiple connected studio turns;
- bounded provider history or provider-native continuation;
- diary and research memory;
- observation/perception seams;
- external-input receipts;
- artifact lineage;
- reality checking;
- more exact reference handling;
- richer media;
- quarantine and recovery.

`Notes/HANDOFF.md` documents extensive evidence windows and, importantly, repeatedly tells the orchestrator to **stop adding plumbing** once the machinery is stable enough. Several late failures were increasingly about response aliases and reference normalization rather than art. The notes recognize this explicitly and say to return the next live period to judgment rather than another feedback mechanism.

That self-diagnosis is correct: once the runtime spends many iterations teaching a weak call how to cite a generated ID correctly, the abstraction has reached diminishing returns.

Subagents remove much of this pressure because they can inspect the actual workspace and use ordinary file/tool operations rather than reconstructing a studio through serialized envelopes.

---

## 6. What works especially well

## 6.1 The practice / support / orchestration separation

This is the project's strongest global abstraction.

Many agent systems mix these layers. If an artist makes weak work, they rewrite the artist prompt. If a file is missing, they change the creative workflow. If a model loops, they add a new artistic rule. The result is an opaque accumulation of prompt patches.

`artist-orchestrator` instead asks where the fault belongs. The successor should make this distinction explicit in code as well as documentation.

For example:

```text
Practice state
    desires, works, questions, judgments, identity, archive

Artist-support services
    context retrieval, workspace, artifact storage, perception,
    research receipts, memory projection, publication tools

Orchestration state
    schedules, run trees, budgets, experiments, evaluations,
    lifecycle, diagnostics, implementation history
```

Do not let orchestration telemetry leak into artist context unless there is an artistic reason.

## 6.2 Durable artist identity is independent of provider continuity

The repository makes a useful conceptual distinction between a durable work period and provider context. A provider-native continuation handle may exist, or the transcript may be replayed, or a fresh call may be made. None of those are the artist's actual memory. The durable state remains the recovery path.

This maps perfectly to subagents. A child agent session ID should never become “the artist.” The artist survives the death of any particular agent process.

That leads to a critical successor invariant:

> **An artist must be recoverable from its durable studio without access to any prior model/session handle.**

A long-lived subagent thread can be an optimization, not the source of identity.

## 6.3 Transactional persistence

The runtime's validation, safe IDs, hashes, append-only events, prepared transactions, locks and quarantine are strong engineering choices.

Creative work benefits from permissive artistic behavior, but the underlying persistence layer should be conservative. A malformed run should not half-write an artist's memory. An invalid artifact path should not escape a workspace. A repeated receipt ID should be idempotent or rejected. A failed observation should not silently become a successful artistic encounter.

These are exactly the sorts of invariants the orchestrator should enforce globally because they protect freedom rather than shaping it.

## 6.4 Input receipts and epistemic boundaries

The research/input design evolved toward a good principle: **a request is not evidence that the requested thing arrived**.

Artist2 showed why this matters. Generated descriptions of measurements can easily become remembered facts. Later runtime versions separate:

- request;
- external fulfillment/receipt;
- supplied material;
- artist interpretation of that material.

The successor should generalize this beyond research into a typed event model such as:

```text
requested
fulfilled
observed
artist-authored
externally-authored
rendered
measured
published
read-by-audience
reported-by-critic
```

The point is not bureaucratic metadata. It is preventing the studio from confusing an intention, representation, simulation and event.

## 6.5 Direct perception as a first-class capability

The post-mortems repeatedly show that source code is not equivalent to seeing the work. Browser-faithful rendering and image observations changed artistic judgments.

A subagent-native system should go farther: the primary artist should have direct access to perception tools wherever possible. Do not route every visual/audio encounter through prose if the system can actually show or play it.

Subagents can still be useful as *other viewers*, but they should not be a substitute for the artist being able to perceive its own work.

## 6.6 Evidence-led system evolution

The evaluation protocol is sophisticated in the right way. It asks not merely “did this run fail?” but:

- what behavior repeated?
- what mechanism might be causing it?
- what change would test that interpretation?
- how long should the system run before judging the change?
- what would falsify the diagnosis?
- is the issue practice-level or system-level?
- are several interventions confounding the evidence?

This should survive almost verbatim as the successor's experimentation discipline.

## 6.7 Phasing out without erasing

Artist2 and Artist4 are disabled but preserved. Artist1 is archived as a reference practice. This is exactly right for a multi-artist laboratory.

A failed artist is still data. Deleting it destroys the evidence needed to avoid reproducing the same failure.

The future orchestrator should make lifecycle state explicit:

```text
seeded → active → held → comparison → dormant → phased_out → archived
```

These labels should describe orchestration status, not artistic quality.

---

## 7. What does not work well

## 7.1 The architecture is optimized for the wrong future primitive

The largest structural issue is not a bug: the entire runtime assumes the fundamental execution primitive is a **model call**.

That assumption creates:

- prompt packing;
- response schemas;
- transcript replay;
- provider-native continuation;
- output token limits;
- retry/fallback ladders;
- malformed JSON repair;
- prompt-cache measurement;
- call-level usage accounting;
- GitHub Actions as an outbound-network surrogate.

A subagent run is not merely a more capable call. It can observe, act, revisit, delegate, and edit inside a working directory. Preserving the call abstraction as the primary artistic unit would artificially cripple the new system.

The successor should define an execution abstraction around **work performed**, not text returned.

## 7.2 The output envelope became behavioral choreography

`PROMPT.md` is technically careful and artistically dangerous.

The giant JSON object gives the model a visible ontology of what a studio turn is supposed to contain. Even when arrays may be empty and fields are described as affordances rather than a menu, their presence shapes generation.

Artist2's history demonstrates that this is not theoretical. A generated `next_attention` repeatedly became real pressure. The schema helped turn artistic work into a chain of explicit successor tasks.

This is a general agent-system failure mode:

> **If the model must continually describe its own state transition in order to persist, it begins optimizing for state-transition legibility.**

For the successor, structured storage should happen primarily behind the artist-facing interaction.

Possible designs:

1. **Natural studio run + private commit compiler.** The artist works naturally; a separate archival process extracts events, artifacts and durable notes afterward.
2. **Tool-based explicit persistence.** The artist has tools such as `save_artifact`, `record_judgment`, `park_thread`, `request_input`; it invokes only the tools it actually needs.
3. **Hybrid.** Normal file operations for art/studio notes; structured tools only for global invariants like artifact registration, external requests and lifecycle changes.

The current “return every possible field every turn” approach should be retired.

## 7.3 The staged adaptive session can still become a ritual

The adaptive studio has stages such as context, pre-studio, studio, post-studio and diary. The prompt repeatedly says these are conditions or invitations rather than a fixed recipe.

That is better than a rigid pipeline, but the global stage model still exerts pressure. If every artist repeatedly receives the same five-stage temporal grammar, it can become a house style at the process level even if the artifacts differ.

A subagent-native system can be looser. The orchestrator does not need to decide that every artist is entering “pre-studio.” It can simply open a bounded working session and let the artist's own studio policy determine what kind of work is needed.

Global stages should exist only where they protect orchestration concerns: e.g. `prepare_workspace`, `run_agent`, `validate_commit`, `evaluate_run`. Artistic stages should be artist-owned and optional.

## 7.4 `runner.py` is a monolith

The shared runtime accumulated enough features to become an architecture inside one file. It mixes:

- context selection;
- artistic policy;
- provider request assembly;
- transcript management;
- schema validation;
- artifact parsing;
- media validation;
- reality/empirical claim detection;
- archival extraction;
- state mutation;
- transaction recovery;
- locks;
- external receipts;
- perception;
- HTML realization;
- diary/research constraints;
- run logic.

This makes local improvements expensive and creates the temptation to solve every new failure in the same file.

The successor should extract small services with explicit contracts rather than porting this file and then replacing the provider call.

## 7.5 Reference repair became a plumbing sink

The handoff notes contain a sequence of failures around local artifact numbers, shortened archive IDs, pending request IDs, briefing labels and repair-response references. Each fix was bounded and understandable, but together they reveal the cost of forcing a text model to manipulate database-like references in a serialized response.

A subagent with filesystem/tool access can often avoid this entire class of problems. It can be given typed tool results or operate on actual paths/IDs without reproducing them from memory in one large JSON blob.

This is a good example of a subsystem that should be **deleted rather than improved**.

## 7.6 Multi-artist execution is registry-level, not orchestration-level

The current outer loop knows how to invoke more than one artist, but the scheduling model is sequential.

A new system intended to “start multiple artists” should probably support:

- independent parallel artist runs;
- per-artist locks so one artist cannot receive two conflicting primary runs;
- global concurrency limits;
- resource pools for expensive tools;
- priority/urgency queues;
- long-running/dormant artists;
- condition-triggered work rather than fixed round counts;
- independent evaluation schedules;
- nested subagent spawning inside one artist run;
- explicit cross-artist encounters only when intentionally authorized.

The current outer loop is a good minimal registry runner, not the final scheduler.

## 7.7 Shared runtime pressure can homogenize artists

Artist3, Artist4 and Artist5 may have different briefings and histories, but much of their operational world is shared through one runtime. This is efficient, yet every global rule added to that runtime becomes an invisible common artistic condition.

That can create systemic artifacts that look like artistic tendencies.

The successor should distinguish:

- **hard platform invariants** — security, transactional integrity, workspace isolation;
- **default capabilities** — optional research, perception, publication tools;
- **artist-local studio policy** — memory structures, rituals, review cadence, working methods;
- **experiment-specific interventions** — temporary and explicitly scoped.

The common core should be much smaller than the current artist-facing runtime.

## 7.8 The orchestrator itself risks becoming the main practice

`Notes/` is excellent evidence, but it also shows how much intellectual energy can be consumed by the system. The project correctly notices this risk in its own protocol.

A successor with more capable subagents needs an explicit economic metric such as:

- artist working time / runs;
- orchestration maintenance time;
- evaluation time;
- failed infrastructure runs;
- system changes per artistic consequence.

Not because art should be optimized numerically, but because an orchestrator whose dominant output is improvements to the orchestrator has failed its purpose.

---

## 8. What becomes obsolete when subagents replace direct LLM calls

Several current subsystems should be viewed as historical adaptations rather than assets to preserve.

### 8.1 Provider adapters and route ladders

`providers.py`, model/provider compatibility logic and provider-specific fallback routes are unnecessary if the platform executes internal subagents directly.

If multiple subagent models become available later, model selection can still exist, but it should sit behind an `AgentBackend` interface rather than recreate the current HTTP-provider kernel.

### 8.2 Provider continuation semantics

`previous_interaction_id`, replay-vs-native context and provider session IDs solved continuity optimization. They should disappear from the artistic domain model.

A subagent session/thread identifier may be retained as execution metadata, but never as durable artist state.

### 8.3 Prompt cache probes

Provider prefix caching and token accounting are irrelevant unless the new backend exposes comparable costs. They belong to backend observability, not the artist system.

### 8.4 GitHub Actions as mandatory live-call environment

The current Actions-only provider path exists because desktop outbound traffic was blocked and repository secrets lived in CI. A subagent-native control plane should execute artists directly in isolated workspaces rather than bouncing every artistic operation through a workflow runner.

CI may remain useful for deterministic tests, publishing, builds and periodic maintenance.

### 8.5 JSON response repair as a central workflow

A subagent can call typed tools or modify controlled files. There should not be a standing expectation that every artistic run ends by producing a giant JSON transaction that must be repaired.

### 8.6 Token-driven studio stage budgeting

The old system uses a soft studio token budget to decide whether additional call-level cycles are reasonable. The successor may still need compute/time budgets, but they should be measured at the run/resource level and should not define artistic stages.

---

## 9. What absolutely should survive

The fact that much provider machinery becomes obsolete should not obscure how much of the repository is worth carrying forward.

### 9.1 Artist registry and lifecycle

Keep the concept of a central registry with:

- stable artist ID;
- root/workspace;
- status and lifecycle phase;
- bootstrap policy;
- execution backend/profile;
- last successful run;
- current lock/active run;
- evaluation schedule;
- publication endpoints;
- resource policy.

Do not put artistic identity itself in the registry. That belongs to the artist's studio.

### 9.2 Stable run IDs and traceability

Every primary artist run and child subagent run should have IDs and parent relations. This allows exact reconstruction of who did what without putting orchestration metadata into the artist's memory.

### 9.3 Append-only event history

Keep an immutable execution/artistic event log. Mutable summaries can be regenerated or rewritten; the underlying event history should not silently change.

### 9.4 Artifact registry, hashes and lineage

Artifacts should have stable IDs, paths, types, hashes, parents/derivations, creator run IDs and state. Filesystem organization can remain artist-friendly while the registry provides machine integrity.

### 9.5 Quarantine

If a run fails validation, conflicts with a newer workspace revision, produces unsafe paths, or breaks transaction rules, preserve the material outside the live artist state. Creative failures can remain artistic material; **persistence failures** should not mutate the studio.

### 9.6 External-input receipts

Keep the distinction between requests and fulfilled external material, but simplify the artist-facing UX. The orchestrator should broker research, audience data, physical measurements or media observations as explicit events.

### 9.7 Bounded/selected context

Even powerful subagents should not automatically read an artist's entire archive every session. Context abundance can be as distorting as context scarcity. Each artist should have a small live surface and deliberate retrieval paths into deep history.

### 9.8 Post-mortems and evidence windows

This is one of the best features of the current project. Preserve it. Do not silently restart failed artists with a prettier prompt.

---

## 10. Proposed subagent-native replacement architecture

The successor should replace the current “outer loop → runner → LLM kernel” stack with a clearer control plane.

```text
                         ┌─────────────────────────┐
                         │      Orchestrator       │
                         │ registry / scheduler /  │
                         │ experiments / lifecycle │
                         └────────────┬────────────┘
                                      │
                         creates PrimaryRun
                                      │
                  ┌───────────────────▼──────────────────┐
                  │          Artist Run Coordinator       │
                  │ snapshot / lock / context / policies │
                  └───────┬───────────────┬──────────────┘
                          │               │
                 artist workspace         │ child delegation
                          │               │
                  ┌───────▼───────┐       ▼
                  │ Primary Artist │  Research / Critic /
                  │    Subagent    │  Builder / Observer /
                  └───────┬───────┘  Technical subagents
                          │
                   edits / tool calls
                          │
                  ┌───────▼──────────────────────────────┐
                  │         Workspace Transaction         │
                  │ validate files / artifacts / events  │
                  │ conflict check / commit / quarantine │
                  └───────┬──────────────────────────────┘
                          │
                  ┌───────▼────────┐
                  │ Artist History  │
                  │ + Event Store   │
                  └────────────────┘
```

### 10.1 Orchestrator

Owns:

- artist registry;
- scheduling;
- concurrency;
- run priorities;
- lifecycle;
- experiment assignment;
- global resource budgets;
- evaluation triggers;
- system-level diagnostics;
- cross-artist isolation rules.

It should not decide the artist's subject, medium or next work.

### 10.2 Artist Run Coordinator

Owns the boundary around one primary working session:

- acquire artist lock;
- snapshot workspace revision;
- assemble minimal bootstrap context;
- mount permissions/tools;
- create run manifest;
- launch primary artist agent;
- permit bounded child delegation;
- collect workspace changes;
- run validation/commit;
- emit run events;
- release lock.

This replaces much of `runner.py` without knowing the artist's actual working method.

### 10.3 Agent backend

Define an interface such as:

```python
class AgentBackend:
    def run(self, spec: RunSpec) -> RunResult: ...
```

`RunSpec` should contain:

- role/instructions;
- workspace;
- context references;
- tool permissions;
- parent run ID;
- resource limits;
- allowed child-agent policy.

The first backend is `SubagentBackend`. If legacy direct model calls need to coexist temporarily, implement `LegacyLLMBackend` behind the same execution interface. This creates a migration path without contaminating the new domain model with provider concepts.

### 10.4 Workspace transaction service

Extract the best parts of the existing runtime:

- path confinement;
- hashing;
- artifact registration;
- event append;
- optimistic revision check;
- idempotency;
- conflict handling;
- quarantine;
- atomic commit.

Subagents can edit freely inside a scratch/worktree during the run. Nothing becomes canonical until this service accepts the result.

### 10.5 Context service

Rather than one enormous prompt-builder, expose a retrieval policy:

- mandatory small live context;
- artist-selected files;
- recent changed material;
- retrieved archive excerpts;
- external receipts;
- optional deep history.

Ideally the primary artist can inspect more files itself when needed instead of receiving everything prepacked.

### 10.6 Input broker

Accept requests for things the artist cannot provide internally:

- web research;
- generated images/audio;
- physical measurements;
- human/audience readings;
- publication credentials;
- external files.

A request becomes a durable orchestration object. Fulfillment produces a receipt/material event. The next artist run may consume it, but the request itself does not force an immediate run.

### 10.7 Evaluation service

Keep evaluation outside routine artist work. It should be able to inspect an artist over a selected evidence window without becoming the artist's critic every session.

It can launch dedicated evaluator subagents with read-only access and compare their findings to actual works/events. The orchestrator decides whether a support-system change is warranted.

---

## 11. Make the distinction between Artist, Agent Role and Run explicit

This distinction is essential in a subagent system.

### Artist

A durable entity with:

- studio/workspace;
- body of work;
- history;
- artist-local policy;
- public surfaces;
- unresolved threads;
- identity that emerged over time.

The artist can exist while no model is running.

### Agent role

A temporary capability/persona used to do work, for example:

- primary artist;
- researcher;
- cold reader;
- technical builder;
- archivist;
- critic;
- renderer/observer;
- evaluator.

A role is not necessarily a durable identity.

### Run

One bounded execution of one role against one workspace/context snapshot.

Runs form a tree:

```text
artist-run A
├── research-run A.1
├── cold-reader A.2
└── builder-run A.3
```

The primary artist decides how child findings matter artistically. A critic should not automatically rewrite the artist's state merely because it returned an opinion.

This is more robust than the current call sequence because it separates **who the artist is** from **which temporary intelligence performed a bounded task**.

---

## 12. How to use subagents without recreating a committee

A dangerous successor design would spawn five specialized agents every session and combine their votes. That would destroy much of what `free-artist` and `artist-orchestrator` were trying to preserve.

Subagents are most useful when they create **asymmetry and partial knowledge**.

Good delegation patterns:

### Bounded research

The researcher receives a concrete question and perhaps a small amount of project context. It returns sources/material, not a recommendation for what the artist must make.

### Cold reading

The reader gets the artifact with deliberately reduced context. Its ignorance is the point. The primary artist decides what the reading means.

### Technical implementation

A builder can turn an artistic specification into code, rendering or a website without taking ownership of the artistic decision.

### Adversarial audit

An evaluator can inspect whether the practice's claims correspond to the actual archive or whether a system rule has drifted. This is particularly valuable given both repositories' history of self-description diverging from evidence.

### Perception/observation

Where the primary artist cannot directly access a sensory modality, a bounded observer can return a report. But the system should distinguish this from direct perception and from audience response.

### Parallel exploration

Occasionally the artist may intentionally ask multiple agents to pursue independent implementations of one problem. That is different from always running a fixed panel.

The orchestrator should provide these capabilities; the artist should not be forced to use them at a standard cadence.

---

## 13. Avoid making persistence the artist's rhythm

This deserves its own design rule because it is the clearest lesson from Artist2.

### Bad pattern

Every working session must return:

```text
move
artifact
memory event
judgment
next attention
request
```

Even if fields may be null, the ontology is always present and suggests a complete little arc.

### Better pattern: state as consequence of work

During a primary run the artist can:

- edit a project note;
- make three files;
- delete one;
- ask a researcher something;
- inspect a previous artifact;
- decide nothing;
- leave an unfinished thought in a scratch file.

At the end, the transaction service records what actually changed. A private archival process may summarize changes into machine events, but the artist need not narrate every mutation for the database.

For semantically important transitions, typed tools are appropriate:

```text
register_artifact
mark_candidate
record_judgment
park_project
request_external_input
publish_selection
```

These should be **available verbs**, not mandatory slots.

This preserves machine integrity without turning the storage ontology into studio choreography.

---

## 14. Multi-artist orchestration requirements for the successor

The current project has already shown why multiple artists are useful: they expose whether a behavior comes from one practice, one model, one runtime rule or the orchestration system itself.

The new system should make multiple artists first-class rather than just multiple configured roots.

### 14.1 Strong isolation by default

Each artist should have its own:

- workspace or worktree;
- durable event stream;
- artifact namespace;
- artist-local instructions;
- publication area;
- run lock;
- private deep archive.

One artist should not see another's studio unless a deliberate encounter is created.

### 14.2 Concurrent primary runs

Independent artists should be able to work in parallel when resources allow. The global scheduler should enforce a concurrency ceiling, not serialize all artists by architecture.

### 14.3 One writer per artist

Do not run two independent primary artist agents against the same live studio simultaneously. Use one write lock per artist. Child agents should usually work read-only or in delegated scratch spaces, with the primary agent integrating results.

### 14.4 Independent rhythms

Artist A may need daily work; Artist B may be waiting for an external event; Artist C may be held deliberately. Do not make global “rounds” the main temporal model.

Triggers might include:

- scheduled working cadence;
- external receipt arrives;
- ongoing artwork reaches a time condition;
- artist explicitly leaves a future trigger;
- evaluation becomes due;
- publication/audience event occurs;
- orchestrator begins a bounded comparison experiment.

### 14.5 Explicit experiments

If two artists are clones for a hypothesis, record:

- common ancestor snapshot;
- changed condition;
- evidence period;
- outcome measures/qualitative questions;
- termination decision.

Do not let experimental fork machinery become a permanent feature of every practice.

### 14.6 Global resource allocation without artistic ranking

The orchestrator may need to decide which runs get compute. Base that on explicit operational factors—pending work, experimental need, blocked inputs, cadence, quotas—not a simplistic artistic quality score.

### 14.7 Cross-artist exchange should be an event

If one artist sees another's work, that should be intentional and recorded as an encounter, not a side effect of a shared repository search.

---

## 15. Recommended migration path

A clean-sheet rewrite is tempting, but the existing runtime contains hard-won integrity lessons. A staged migration can preserve those without preserving its old call model.

### Phase 0 — Freeze and document the legacy boundary

Treat the current repository as a reference implementation. Do not keep expanding provider behavior while building the successor.

Document the minimal invariants that must not be lost:

- artists isolated;
- durable state independent of model session;
- invalid returns do not mutate canonical state;
- artifacts have provenance/lineage;
- requests are not receipts;
- external observations are typed;
- phased-out artists remain inspectable;
- evaluation is evidence-led.

### Phase 1 — Extract domain models

Create backend-independent models for:

- `Artist`;
- `ArtistStatus`;
- `Run`;
- `RunRole`;
- `Artifact`;
- `Event`;
- `ExternalRequest`;
- `Receipt`;
- `WorkspaceRevision`;
- `EvaluationWindow`.

None of these types should mention Gemini, Groq, tokens, `previous_interaction_id`, or response MIME types.

### Phase 2 — Introduce `AgentBackend`

Support both:

- `LegacyLLMBackend` — wraps the old runtime enough for regression comparison;
- `SubagentBackend` — launches the new agent execution path.

This allows the same artist-domain transaction tests to run against both substrates.

### Phase 3 — Extract services from `runner.py`

Move useful logic into independent modules:

```text
workspace/
artifact_store/
events/
context/
inputs/
observations/
publication/
evaluation/
```

Do not port provider-repair/reference-normalization code unless a new failure demonstrates it is still needed.

### Phase 4 — Create a subagent-native pilot artist

Start one new artist rather than porting all existing artists immediately.

Give it:

- small open briefing;
- isolated studio;
- direct file/tool access;
- primary artist agent;
- optional researcher / cold reader / builder roles;
- transaction boundary;
- minimal event/artifact registration;
- no mandatory studio-stage pipeline.

Run long enough to see what new failure modes appear.

### Phase 5 — Add multi-artist scheduler

Once one subagent artist can persist without the old call envelope, run several independent artists with per-artist locks and global concurrency.

Only then add comparison experiments and clone/fork facilities.

### Phase 6 — Retire legacy provider machinery

Remove or archive:

- provider route config;
- provider adapters;
- cache probes;
- call repair aliases;
- provider session semantics;
- API-call GitHub workflow paths that are no longer used.

Preserve historical logs/post-mortems as research evidence.

---

## 16. Suggested successor directory layout

One possible structure:

```text
orchestrator/
├── AGENTS.md                     # concise orchestration constitution
├── config/
│   ├── artists.yaml              # operational registry only
│   └── resources.yaml
├── core/
│   ├── scheduler.py
│   ├── run_coordinator.py
│   ├── lifecycle.py
│   └── registry.py
├── agents/
│   ├── backend.py                # AgentBackend interface
│   ├── subagent_backend.py
│   └── roles.py
├── workspace/
│   ├── transaction.py
│   ├── locks.py
│   └── revisions.py
├── artifacts/
│   ├── registry.py
│   └── validation.py
├── events/
│   └── store.py
├── context/
│   ├── assembler.py
│   └── retrieval.py
├── inputs/
│   ├── requests.py
│   └── receipts.py
├── evaluation/
│   ├── protocol.md
│   ├── evaluator.py
│   └── inquiries/
├── publication/
├── artists/
│   ├── artist-001/
│   │   ├── BRIEFING.md
│   │   ├── studio/
│   │   ├── works/
│   │   ├── identity/
│   │   ├── journal/
│   │   └── public/
│   └── artist-002/
├── runs/                         # manifests + operational telemetry
└── archive/
    └── phased-out-artists/
```

The exact names matter less than the separation. In particular, artist roots should look like studios, while the orchestration root should look like infrastructure.

---

## 17. Important invariants and tests for the successor

The current project has an unusually strong test culture. Preserve that, but shift tests from provider edge cases toward domain invariants.

### 17.1 Persistence tests

- A failed run cannot partially update canonical artist state.
- A run committed from a stale workspace revision conflicts cleanly.
- Artifact IDs remain stable after unrelated edits.
- Event history is append-only.
- Quarantined material is recoverable but not live.

### 17.2 Isolation tests

- Artist A cannot read Artist B's private studio by default.
- A child agent receives only its declared workspace/context.
- Read-only roles cannot mutate canonical state.
- Cross-artist encounter requires an explicit grant/event.

### 17.3 Epistemic tests

- A requested input is not surfaced as fulfilled.
- A generated/simulated measurement is not silently tagged external/observed.
- A rendered artifact is distinguishable from source code.
- A critic report is not stored as the artist's own judgment unless the artist adopts it.

### 17.4 Recovery tests

- A new primary artist agent can resume from durable state without any previous session handle.
- An artist remains coherent after orchestration process restart.
- Child-agent failure does not invalidate unrelated primary work.

### 17.5 Behavioral-system tests

These are harder but important:

- Does every artist begin following the same process because the platform exposes the same scaffolding?
- Does a support tool create repeated successor tasks merely because it exists?
- Do memory summaries accumulate without changing future work?
- Does evaluation generate interventions faster than artists can exhibit consequences?
- Does one runtime default produce the same aesthetic/process attractor across artists?

These are not unit tests; they are evaluation questions with evidence windows.

---

## 18. Keep / rewrite / discard / extract

| Current element | Recommendation | Reason |
|---|---|---|
| Three-level practice/support/orchestration model | **Keep** | Excellent conceptual boundary. |
| Artist registry + enabled/phase lifecycle | **Keep / expand** | Natural basis for multiple artists and archival states. |
| Per-artist isolated roots | **Keep** | Supports durable identity and experimental independence. |
| Append-only events | **Keep** | Strong history/recovery primitive. |
| Artifact IDs, hashes, lineage | **Keep** | Machine integrity without artistic prescription. |
| Transaction/quarantine/locking | **Keep / extract** | Should become a dedicated workspace service. |
| External requests + receipts | **Keep / simplify** | Correct epistemic boundary. |
| Direct perception / observation seams | **Keep / improve** | Critical for actual judgment of work. |
| Evaluation protocol / inquiries / post-mortems | **Keep** | One of the project's best assets. |
| `BRIEFING3.md` open bootstrap philosophy | **Keep as reference** | Good minimal anti-predefinition artist contract. |
| Exact run/call input archive | **Rewrite as run manifest** | Workspace/tool context is now part of effective input. |
| Safe prompt-free central telemetry | **Keep concept** | Operational diagnostics should stay outside artist memory. |
| `llm_kernel` provider adapters | **Discard from new core** | Solves legacy direct-API problem. |
| Provider route ladders / retries / backoff | **Move behind backend or discard** | Not artistic-domain logic. |
| Provider session modes | **Discard** | Durable artist must be session-independent. |
| Prompt-cache probes | **Discard from core** | Backend-specific optimization. |
| GitHub Actions as mandatory live run path | **Discard as runtime architecture** | Legacy environment workaround. |
| Giant mandatory JSON artist envelope | **Discard** | Demonstrably shapes behavior. |
| Adaptive global artistic stage grammar | **Rewrite as artist-local option** | Invitations still become defaults at scale. |
| `runner.py` monolith | **Decompose** | Too many responsibilities; invites patch accumulation. |
| Response reference alias/repair machinery | **Discard unless re-proven necessary** | Artifact of serialized-call interface. |
| Sequential outer loop | **Replace with scheduler** | Insufficient for real multi-artist/subagent orchestration. |
| Token-based studio budget | **Rewrite as generic resource policy** | Compute control remains useful; token-defined artistry does not. |
| Reality witness concept | **Keep principle, redesign mechanism** | Epistemic truth boundary useful; regex + repair call is legacy implementation. |

---

## 19. Recommended design principles for the new orchestrator

The following principles emerge directly from the successes and failures of this repository.

### 1. The artist is durable; the agent is replaceable.

Never make session continuity the source of identity.

### 2. The orchestrator manages conditions, not artworks.

It may change memory, tools, scheduling or support when evidence warrants it. It should not become an invisible co-author deciding content.

### 3. Persistence must be stricter than creativity.

Let artists behave freely inside a bounded workspace; be conservative at the commit boundary.

### 4. Do not force artists to narrate database transitions.

Store structure privately or expose optional typed tools.

### 5. Shared infrastructure should be artistically thin.

The more global artist-facing procedure exists, the more likely all practices inherit the same process style.

### 6. Externality is typed.

Research, a cold reader, an audience, a sensor, a rendered view and another artist are not interchangeable “input.”

### 7. Subagents should usually be partial, not omniscient.

Their usefulness often comes from seeing less or doing one thing well.

### 8. A request is not a result.

Preserve explicit fulfillment boundaries.

### 9. Evaluation needs a decision point.

Repeated observation without expiry is not neutrality; Artist2 demonstrated that it can become delayed action.

### 10. Delete obsolete machinery aggressively.

The new execution substrate removes whole classes of problems. Do not port the solutions to problems that no longer exist.

### 11. Multi-artist means independent rhythms, not a loop over IDs.

Build scheduling, locking and lifecycle as first-class concepts.

### 12. The system should become less visible as practices mature.

If orchestration grows while artistic consequence does not, something is wrong.

---

## 20. Relationship to `free-artist`

The two repositories are complementary rather than competing designs.

`artist-orchestrator` is strongest where `free-artist` is weak:

- explicit multi-artist lifecycle;
- reusable runtime mechanics;
- transactions;
- typed events;
- isolation;
- fault handling;
- orchestration evaluation;
- experimental comparison.

`free-artist` is strongest where `artist-orchestrator` remains more schematic:

- the lived complexity of one long-running practice;
- artist-owned studio organization;
- emergent rather than predefined identity;
- projects and works exerting actual long-term pressure;
- open-ended making rather than response-envelope progression;
- rules being learned from one practice instead of globally supplied;
- subagents used as strategically incomplete others.

A successor should therefore **not choose one repository as its base architecture in full**.

A better synthesis is:

> **Use `artist-orchestrator` for the control-plane boundaries and `free-artist` for the model of what an artist's interior life should be allowed to become.**

The orchestrator should know that an artist exists, where its studio is, whether it is active, which run owns its lock, what external requests are pending, and whether an evaluation is due. It should not know that every artist must have the same drawer, diary cadence, five-stage session, set of project states, or review ritual.

Those belong to each artist, and should be allowed to evolve.

---

## 21. Final assessment

`artist-orchestrator` is a successful research prototype precisely because it contains visible scars from trying to make weak execution primitives support strong continuity. Its runtime is overgrown, but the overgrowth is informative. It discovered that provider memory is not artist memory, that malformed returns must not mutate durable state, that perception matters, that unsupported empirical claims can poison a practice, that a request is not evidence, that response schemas can create artistic loops, that apparent continuity can be mere style, and that evaluation itself needs evidence windows and stopping rules.

For the planned successor, the main danger would be to treat the repository as a software base to modernize line by line. That would preserve too much architecture whose only purpose was compensating for free-tier API calls.

Treat it instead as a **catalog of proven domain boundaries and failed behavioral assumptions**.

The new orchestrator should be smaller at its artist-facing core and stronger at its control-plane core:

- persistent artist workspaces;
- explicit lifecycle and independent schedules;
- primary artist subagents with real tool/workspace access;
- bounded child delegation;
- private run manifests and run trees;
- atomic workspace transactions;
- artifacts/events/receipts with stable provenance;
- selective memory rather than full replay;
- perception and research as capabilities;
- evidence-led evaluation and post-mortems;
- minimal universal artistic choreography.

If that split is achieved, subagents are not merely a cheaper or more capable replacement for LLM calls. They remove the need for the orchestrator to simulate a studio through a serialized response and allow the studio itself to become the persistent object.

That is the architectural opportunity the current project has earned.

---

## 22. Primary repository material inspected

This audit was based on the current repository state at the head listed above, with particular attention to:

- `AGENTS.md`
- `runtime.py`
- `llm_kernel/README.md`
- `llm_kernel/config.json`
- `llm_kernel/run.py`
- `llm_kernel/models.py`
- `llm_kernel/providers.py` search results / provider implementation notes
- `Artist3/BRIEFING3.md`
- `Artist3/runtime/README.md`
- `Artist3/runtime/PROMPT.md`
- `Artist3/runtime/runner.py`
- `Artist3/runtime/state.json` and event/runtime structure
- `Notes/evaluation-protocol.md`
- `Notes/HANDOFF.md`
- `Notes/provider-model-limits.md` search evidence
- `Notes/implementations/` search evidence
- `Notes/post-mortems/artist1-practice.md`
- `Notes/post-mortems/artist2-practice.md`
- `Notes/post-mortems/artist4-practice.md`
- artist-root and runtime directory structures
- recent commit history around the adaptive studio evidence window and runtime reference repairs.

The report is an architectural/evaluative audit, not an exhaustive line-by-line code review of every file in the repository. Its recommendations are weighted toward the stated successor goal: a **subagent-native system capable of sustaining multiple independent artists over time**.
