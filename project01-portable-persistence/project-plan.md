# Project01 — Portable LibreChat persistence

| Metadata | Value |
|---|---|
| Project | project01-portable-persistence |
| Status | Active — Slice02 contract design; Slice01 acceptance pending; no conversion implementation assigned |
| Depends on | Source/build revalidation in `billo-guildhall`; upstream dev lineage now resolved |
| Blocks | A validated Mongo-free LibreChat deployment through the new boundary |
| Related | Billo Guildhall; CCDP; memory research; AI Engineering concept cards and ontology work |
| Design | [Interface proposal](interface-design.md), [backend proposal](backend-decision.md) |
| Evidence | [Reconnaissance](research.md) |

## Goal and boundaries

Deliver the Operator's three practical objectives: design our own persistence interface with room for Guildhall's eventual data architecture; convert LibreChat to that interface while retaining MongoDB; implement one first non-Mongo backend and establish an iterative path forward.

“Future-oriented” means explicit, evolvable semantic contracts and independently testable adapters. It cannot mean a guarantee that every future requirement fits an unchanged API. We should expect additive operations, versioned changes, and new domain services.

In scope: application persistence and its lifecycle, identity and tenant semantics, contract isolation, Mongo compatibility, a Rust-hosted SQLite implementation, data migration and rollback, and complete selected-backend startup. The proposed SQLite deployment target is a local service with a single owner for writes. This proposal does not reduce LibreChat's existing tenant or authorization obligations.

Outside this project's delivery: a general-purpose memory protocol, ontology extraction, replacing existing knowledge graphs, an HTN planner, a CCDP dispatcher, a ratatui client, Lance projections, vector-search redesign, replacing every external search/RAG/file service, or making Node-based LibreChat itself a Rust application. Those directions inform boundaries without becoming prerequisites.

## Initial corpus — Operator addition, 2026-09-20

Use the Operator's historical **Claude conversations as the initial LibreChat dataset**. Account for the complete Claude corpus in SQLite before proceeding to an **OpenAI/GPT log import** as the next dataset. SQLite is now the named target in the Operator's requested sequence; the Rust-service architecture remains a proposal.

The Operator has located the Claude archive and extracted JSON and reports importing it successfully through local Mongo-backed LibreChat on 2026-09-20. The route is therefore Claude export → LibreChat/Mongo → SQLite migration → OpenAI/GPT import. See [corpus-baseline.md](corpus-baseline.md) for exact source fingerprints, counts, observed content kinds, and the distinction between the reported UI result and pending database reconciliation. No corrective import or migration has been performed by this contributor.

Arc01 must characterize the existing Claude importer alongside the ordinary-save pilot before freezing the contract. This does not automatically make the whole importer part of the first code slice. Determine whether import requirements alter that slice's boundary, and record the reason if they do. The corpus becomes a concrete migration/reload acceptance dataset in Arc04; the later OpenAI/GPT import exercises the same boundary after Claude acceptance.

Preserve the original export as a local source artifact outside version-controlled planning/source trees. Record source identity and fingerprints, original IDs and timestamps, relationships, and the mapping to LibreChat IDs. Inventory content kinds present in the actual export, including any attachments, artifacts, tools, or branching metadata, before deciding their storage representation. Distinguish what is absent from the export from what a converter cannot represent. Preserve source material and report unsupported items explicitly; a successful import notification or matching conversation count alone does not establish fidelity.

Define repeat-import behavior, duplicate detection, resumable progress, and complete population accounting. Start with a representative isolated rehearsal, then process and reconcile the full corpus. Use sanitized fixtures in committed tests; keep private raw conversations out of repository evidence. Do not initiate the OpenAI/GPT batch until the Claude population has been accounted for and its agreed acceptance checks pass in SQLite.

## Definition of done

1. Application consumers use explicit portable operations; engine types and query languages remain inside the relevant adapter. Any remaining Mongo dependency is classified and cannot run on the SQLite-selected path.
2. Mongo preserves characterized user-visible behavior and data compatibility through that boundary. Changes to semantics are separately documented and reviewed.
3. SQLite implements the required capability set through a local Rust service; the same behavioral conformance cases exercise both adapters. No Docker is required by the new service.
4. A documented migration rehearsal preserves identities, tenant boundaries, relationships, temporal metadata, supported content, and deletion semantics, with mismatch accounting and a demonstrated rollback strategy.
5. A representative enabled-feature deployment starts, authenticates, saves and reloads conversations, and performs its background work without a Mongo service or URI. The enabled-feature matrix is explicit; omitted features are not counted as supported. Project closure requires resolving every Mongo-dependent default feature, not disabling defaults to make a smoke test pass.
6. Relevant regression, recovery, isolation, latency, and packaging checks pass with retained evidence and reviewer reproduction. See [ledger.md](ledger.md).
7. The full initial Claude corpus is reconciled in SQLite with explicit transformations and unresolved items visible; then perform and evaluate the subsequent OpenAI/GPT import when its source export is available.

## Arc roadmap

| Arc | Capability | Depends on | Current state |
|---|---|---|---|
| [Arc01 — Contract and first Mongo conversion](arc01-contract-and-mongo-pilot/arc-plan.md) | Characterize ordinary saves and Claude import requirements; establish portable contracts and real-database conformance; convert one bounded application path with Mongo underneath | Reconciliation complete; concrete design and source branch resolution before code | Active: Slice02 contract design using Slice01 attested evidence |
| Arc02 — Complete Mongo boundary | Migrate the remaining persistence families and startup/lifecycle wiring; make bypasses and supported capabilities explicit | Arc01 | Not detailed |
| Arc03 — Rust service and SQLite adapter | Implement the second adapter and transport, using the established contract and Mongo behavioral reference | Arc01 contract; Arc02 coverage before full integration acceptance | Not detailed |
| Arc04 — Migration and complete cutover | Rehearse migration/rollback, validate full selected-backend composition, recovery, and native operation | Arc02 and Arc03 | Not detailed |

These arcs describe capabilities, not estimated sprint sizes. Arc02 in particular may need several slices and revised decomposition after the dependency inventory. Arc03's earliest bounded conformance work may begin after Arc01; the roadmap should not postpone discovering portability failures until the entire Mongo conversion is finished. No parallel execution is currently assigned.

## Immediate design work

The recommended first conversion is the ordinary message-save/conversation-update path. It is recognizable to the user and its save helper accepts injected methods, but BaseClient itself still imports the database singleton. Its retention, provenance, logical/storage IDs, and partial-failure semantics have been characterized in Slice01 and now constrain the contract; the earlier claim of an already-injected store was too broad. Arc01 must scope ordinary turns explicitly and preserve compatibility with other callers; it cannot silently absorb all subagent scheduling and import workflows.

Before issuing its first implementation slice:

1. Use the resolved `billo-guildhall` worktree from upstream dev and refresh source/build evidence and applicable current instructions; see [Operator decisions](operator-decisions.md).
2. Trace all callers and lifecycle effects of the selected methods; identify which remain behind compatibility adapters.
3. Finalize concrete operation and result schemas, ID translation, omission/clearing semantics, error mappings, and module exports.
4. Specify real-Mongo characterization and portable conformance tests with cases that fail on incorrect tenant scope, null handling, identity translation, or lost metadata.
5. Create Arc01's plan/ledger and the first slice's complete open set using the framework's implementation-prompt readiness guide.

There is no implementation estimate yet. Import counts are reconnaissance measurements, not a count of edits or an estimate of effort.

## Workflow and authority

The Operator selected **One-Contributor Workflow for investigation** on 2026-09-20. This assistant works directly with the Operator on research, design, and planning, and reports its checks as self-checks. No separate CC or CRC context is assigned, and no synthetic implementation or verification handoff is required for this investigation.

The Operator's intended progression is:

| Stage | Workflow | Transition condition |
|---|---|---|
| Current focused investigation | One contributor | Active now; characterize the pilot and resolve design questions |
| Deeper design and bounded implementation work | Two contributors: CDC + CC | Record the effective scope and assign a separate contributor when that separation becomes useful |
| Well-defined implementation programme | Three contributors: CDC + CRC + CC | Once the implementation is concrete, record activation, actual contexts, reviewer authority, and the first handoff |

The later modes are not active merely because they appear in this table. Use the Operator-selected progression, record the transition when its condition is met, and establish actual context assignments before dependent work. Adding a reviewer does not retroactively turn this investigation's self-checks into independent evidence.

The Operator has authorized research/design/planning and the standard planning worktree. The implementation objectives and Claude-first/SQLite-before-GPT sequence are established; the Rust service and detailed interface design remain proposals. Ordinary planning preparation proceeds under existing authorization. Record a settled backend or architecture choice before issuing dependent implementation work.

During one-contributor investigation, unresolved design and scope questions return directly to the Operator. Once multiple contributors are active, scope, architecture, acceptance, or cross-arc changes return through CDC and the Operator. Preserve any issued prompts and use the framework's iteration filenames and assignment history.

Current investigation checks are recorded in the owning research/planning documents without fictional independent-verification files. Later use `cdc-verification.md` for two-contributor slice review and `crc-verification.md` for three-contributor slice review; three-contributor arc/project closure retains both records as required by the framework. Existing independent and Operator acceptance requirements remain in force. Detailed slice artifacts live under their owning slice unless an explicit override is recorded.

### Expedited Mode — enabled 2026-09-20

The Operator explicitly requested Expedited Mode and project-relative prompt paths in chat. It applies to Project01, including the current Arc01 investigation, and remains independent of contributor count. One-contributor investigation is still active; no CC or CRC context is assigned by enabling this mode.

- Commit completed planning/review updates with explicit path allowlists and concise reports. When CC is assigned, its instructions likewise require explicit-path commits of its work before reviewer acceptance; those commits remain proposed-done.
- Close a slice as soon as its full evidence, required review, and Operator gates permit; immediately open the next planned slice. At the last slice, perform formal arc closure and open the next arc/first slice when the roadmap and required gates permit. Preserve the designated contributor's authority for each action.
- Report every newly issued initial or iteration prompt in chat as a plain copy/paste path relative to `project01-portable-persistence/`, including its full arc/slice path. A Markdown link may supplement the path but does not replace it. Identify the assigned role and current assignment; do not report a nonexistent or superseded prompt as actionable.
- While this investigation uses one contributor, the current slice plan is the assignment. No synthetic CC prompt is required. When a real contributor handoff is ready, complete the existing readiness and workflow-transition requirements and report the resulting prompt path.
- No shortcuts, skipped validation, weaker evidence/review, inferred source scope, scope reduction/change, timeline interpretation, or override of explicit Operator gates. Unresolved escalations and required independent/Operator gates still stop affected advancement; unaffected authorized work can continue.

Activation state: planning baseline `e4f437873`; Arc01/Slice01 open with all acceptance rows open; no implementation prompt issued and no application test baseline run. This policy changes cadence and reporting, not the acceptance state.

### Transition record — 2026-09-20

- Prior state: default two-contributor planning, initialized at planning commit `c90d56654`; no CC assignment or reviewer acceptance issued.
- Effective state: one contributor for investigation and design preparation, authorized by the Operator's latest message. This conversation owns the next action.
- Application baseline: `ba44443fdb232bbe6d4977e2619774b5a72586ac`, unchanged and clean at transition.
- Evidence: source reconnaissance and document self-checks only; no runtime tests or benchmarks. All project ledger rows remain open.
- Open findings owned by this contributor: pilot caller/lifecycle coverage, exact contract semantics, executable baseline evidence, and the required implementation branch baseline.
- Open design decisions: service architecture, concrete operation schemas, and initial Claude import route remain unresolved. The Operator subsequently named SQLite as the Claude corpus target; workflow selection alone did not settle those design questions.
- Current prompt: none. No receiving contributor exists yet; record acknowledgement when a future handoff occurs.

## Arc01 readiness assessment — 2026-09-20

**Ready to begin focused Arc01 investigation and detailed planning; not yet ready to implement the Mongo conversion.** The current evidence supports the direction and a candidate pilot. It does not yet establish that the pilot is a complete, bounded change with a proven behavior baseline.

The recommended opening work has four concrete outputs:

1. **Pilot dependency map:** all callers of the selected operations, ownership/tenant context, plugin and background effects, and explicit compatibility boundaries for writers outside the pilot.
2. **Behavior matrix:** identities and relationship translation; absent/null/empty/clear states; provenance and retention; ordering; duplicate saves; and failure between message and conversation writes. Include Claude import transformations, source-to-target mapping, non-text content, repeat-import behavior, and population accounting. Link each behavior to source and existing or needed tests.
3. **Executed baseline:** run the relevant existing Mongo tests in an isolated test environment, retain results including failures or unavailable prerequisites, and distinguish pre-existing problems from new changes. No application database mutation is needed for this baseline.
4. **Implementation-ready contract and slice boundary:** precise inputs/outcomes, module ownership, adapter translation, discriminating acceptance cases, and the resolved source branch baseline.

These outputs have a stopping rule: the first conversion must be describable without leaving consequential behavior choices to its implementer. Then deepen the contributor workflow and prepare the implementation assignment. Broader database comparison is not a prerequisite for this Mongo-focused work. The named SQLite target does not require settling the Rust-service transport or initial import route before source characterization.

## Current status

[Arc01](arc01-contract-and-mongo-pilot/arc-plan.md) is open at the Operator's request, with [Slice02](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/slice-plan.md) active under one-contributor design preparation. The Operator explicitly authorized continuation after reading Slice01’s report; this permits preparatory work without representing Slice01 as independently accepted. The arc and slice ledgers remain open for acceptance; Slice01’s evidence-production work is proposed-done in its [closing packet](arc01-contract-and-mongo-pilot/slice01-behavior-baseline/closing-report.md). No CC prompt or implementation assignment is issued. The earlier fork-only query found no dev ref; that branch blocker is now resolved by fetching upstream dev and creating `billo-guildhall` from it. Main is a pristine upstream release checkout. See [repository workflow](../repository-workflow.md) and [Operator decisions](operator-decisions.md); earlier test results remain pinned to the historical baseline. The orphan planning checkout and initial design inputs exist. The Operator reports successful local startup and Claude import into Mongo. Read-only source inventory confirms 820 conversations and 9,838 messages in the archive-matching JSON, including content the importer does not carry through. No arc or slice is accepted and no application source behavior has changed. The earlier tests-pending state is superseded by Slice01’s [attested baseline](arc01-contract-and-mongo-pilot/slice01-behavior-baseline/artifacts/test-baseline.md): 641 tests passed across 12 suites. No new-interface tests or benchmarks have been run; Node 22 versus pinned Node 24 and installed-dist provenance remain explicit limits. Read-only reconciliation now confirms every conversation and retained message matches the current importer representation: 820 conversations, 9,731 retained messages, and 107 explained skips. It also confirms source-content loss and 95 changed retained parent relationships across 55 conversations. Source preservation, richer intake design, and every project composition criterion remain open; this does not accept SQLite migration. See [corpus-baseline.md](corpus-baseline.md) and [corpus-reconciliation.md](corpus-reconciliation.md).

Arc01/Slice02 has now supplied a [first contract draft](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/contract-design.md) and a [bounded synthetic cursor experiment](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/pagination-findings.md): 6/6 unique-time records returned, but only 4/6 equal-time records, despite cursor exhaustion. This finding is separate from the earlier 641-test baseline. A corrective pagination change requires separate scope; it is not silently included in compatibility work. The current draft leaves relationship translation, field-level schema/projection mapping and exact code fence open. No SQLite migration or implementation-readiness claim follows from this design pass.

The Operator clarified that denormalization was only an option, not a recommendation. D02 now follows the [working Guildhall/Lance identity direction](interface-design.md#working-identity-direction-toward-the-cognitive-data-plane): stable scoped logical references, distinct entity/revision/representation identities and adapter-private physical mappings. The initial compound-first hypothesis has been refined by [Slice02 pass 2](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/design-pass02/decision.md): preserve staged writes, pass logical references and investigate an adapter-private locator hint. Its 28 source-based comparisons passed with mocked stores; real database/lifetime validation and concrete schemas remain open. Project02 separately tracks memory/project UI imports; those additions do not broaden the current persistence pilot.

**Pass-3 correction (supersedes the private-hint recommendation above):** the [real-Mongo lifecycle fixture](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/design-pass03/decision.md) produced two equivalence controls and four counterexamples: deletion, recreation, rename and conversation move make original-object and copied-reference resolution disagree. Reject the invisible-cache contract. Keep staged application decisions and investigate a per-invocation adapter-owned turn-write handle for the observed-row handoff; keep ordinary logical references value-based. This is bounded Slice02 design refinement, with no source implementation, workflow transition or roadmap expansion. DTO, failure, scope and handle lifecycle validation remain open.

**Pass-4 progress:** [Arc01/Slice02 handle and contract evidence](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/design-pass04/decision.md) supports per-invocation observed-write ownership: 28 mocked orchestration comparisons, 26 lifecycle/scope cases using actual tenant policy, and five detected mutants. A source AST census records 44 message and 73 conversation fields and exposes schema/interface differences; patch and partial-commit mappings are recorded. This establishes the working handoff direction, not full conformance. Named projections/consumers, concrete DTOs, validation ordering and pinned-runtime source builds remain open. No new source scope or contributor assignment.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.13 | 2026-09-20 | Arc01/Slice02 pass 4 supported the explicit turn-write handle and advanced field/partial-outcome mapping; retained actual scope, DTO and integration limits. |
| v1.12 | 2026-09-20 | Arc01/Slice02 pass 3 falsified invisible-cache reference equivalence in four Mongo lifecycle cases; superseded the hint candidate with explicit observed-write ownership for further comparison. |
| v1.11 | 2026-09-20 | Incorporated Arc01/Slice02 pass 2 evidence and the refined staged-write/logical-reference candidate; no implementation, conformance acceptance or roadmap change. |
| v1.10 | 2026-09-20 | Incorporated the Operator clarification: treat denormalization as an option and guide D02 with lightweight future cognitive-data-plane models, without freezing schemas or expanding implementation scope. |
| v1.9 | 2026-09-20 | Recorded Operator-approved denormalization options and separate Guildhall/features worktrees; resolved D06 using upstream dev, preserved historical evidence and separated Project02 feature scope. |
| v1.8 | 2026-09-20 | Arc01/Slice02 opened for explicitly authorized design continuation; recorded first contract pass, confirmed cursor gap and corrected singleton/injection premise. Slice01 review and all implementation gates remain pending; roadmap unchanged. |
| v1.7 | 2026-09-20 | Slice01 delivered its attested 641-test baseline and bounded source/behavior/design package. Updated current evidence status; preserved all acceptance gates, roadmap and implementation boundaries. |
| v1.6 | 2026-09-20 | Enabled Operator-requested Expedited Mode and exact project-relative prompt reporting; retained one-contributor investigation and all existing scope, evidence, and review gates. |
| v1.5 | 2026-09-20 | Opened Arc01 and its first investigation slice at the Operator's request; recorded the three-slice roadmap, ledgers, artifact home, and confirmed remote dev-branch absence. No implementation or acceptance claim. |
| v1.4 | 2026-09-20 | Recorded authorized read-only Mongo reconciliation with complete population accounting, retained failed/corrected oracle attempts, concrete source fidelity losses, and unchanged open SQLite acceptance. |
| v1.3 | 2026-09-20 | Recorded Operator-reported local Mongo startup/import, resolved initial route and source location, verified archive/JSON identity and source counts, and identified concrete structured-content preservation requirements. |
| v1.2 | 2026-09-20 | Added Operator-requested Claude initial corpus, full SQLite reconciliation before OpenAI/GPT import, and import fidelity questions surfaced by source inspection. Initial import route and export location remain pending. |
| v1.1 | 2026-09-20 | Recorded Operator-selected one-contributor investigation, intended later workflow progression, transition state, and bounded Arc01 readiness work. No implementation or acceptance scope changed. |
| v1.0 | 2026-09-20 | Initial proposed roadmap from the Operator's three persistence objectives and pinned LibreChat reconnaissance. No arc-close bubble-up yet. |
