# Arc01 — Contract and first Mongo conversion

| Metadata | Value |
|---|---|
| Arc | arc01-contract-and-mongo-pilot |
| Project | [project01-portable-persistence](../project-plan.md) |
| Status | Active — investigation; no conversion code assigned |
| Opened | 2026-09-20, explicitly requested by the Operator |
| Depends on | Existing interface proposal and completed read-only Claude reconciliation; implementation baseline decision before code |
| Blocks | Arc02's broader persistence conversion; Arc03's first concrete adapter contract |
| Workflow | One contributor for current investigation; later transitions follow the project plan |
| Execution mode | Expedited Mode; see the project plan for cadence, unchanged gates, and prompt-path reporting |
| Current slice | [Slice02 — Portable contract design](slice02-portable-contract-design/slice-plan.md); Slice01 acceptance remains pending |

## Capability

Establish a storage-neutral contract for one complete ordinary message-save/conversation-update/read path, implement its first binding through existing Mongo behavior, and demonstrate that the path preserves its characterized semantics. Incorporate the real Claude import's source-preservation requirements into the contract design so that the initial abstraction does not foreclose richer intake later.

The arc's implementation remains bounded to the pilot. Source-preserving intake is a design obligation here; implementing a new archival store, replaying the Claude import, or restoring omitted fields to live records is separate work. Arc01 must leave those requirements traceable to the later project work rather than treating their exclusion from the first code slice as a waiver.

## Starting evidence

- [Interface proposal](../interface-design.md) and [backend direction](../backend-decision.md).
- [Source reconnaissance](../research.md) and [Claude reconciliation](../corpus-reconciliation.md).
- Source baseline: `ba44443fdb232bbe6d4977e2619774b5a72586ac`; planning intake: `d5e9f5370`.
- Mongo contains all 820 conversations and the expected 9,731 retained messages; 107 source messages were skipped under the current importer. The operational import matches its current rules, with demonstrated source-content and relationship losses.
- Opening state (superseded by Slice01 evidence): no application test baseline had been executed. Slice01 now records 12 suites / 641 passing existing tests, with mocked versus real-Mongo coverage and Node/dist limitations separated. Corpus reconciliation remains a distinct check.

## Scope

In scope: the pilot call graph; tenant/actor context; storage ID translation; patch and outcome semantics; retention and provenance; source-versus-operational identity and representation; a relevant real-Mongo test baseline; concrete contract/conformance design; and the first bounded Mongo-backed consumer conversion with regression evidence.

Outside this arc's implementation: full importer migration, corrective writes to the user's imported corpus, all-domain persistence abstraction, SQLite/Rust implementation, new UI features, memory/ontology/planner semantics, event-sourcing infrastructure, and OpenAI/GPT ingestion. Study adjacent writers only far enough to identify dependencies and compatibility obligations that constrain the pilot.

## Slice roadmap

| Slice | Capability | Dependencies | State |
|---|---|---|---|
| Slice01 — Behavior baseline | Map the pilot and relevant import boundary, execute existing isolated Mongo tests, and produce a source-grounded behavior/coverage matrix | Starting evidence above | Investigation delivered; proposed-done, independent acceptance pending |
| [Slice02 — Portable contract design](slice02-portable-contract-design/slice-plan.md) | Resolve operation schemas, source/operational identity mapping, failure semantics, conformance cases, module boundaries, and the precise code fence | Slice01 attested evidence; explicit Operator authorization to continue design preparation | Active; first design pass and cursor characterization delivered; not implementation-ready |
| Slice03 — First Mongo conversion | Implement the reviewed pilot contract and Mongo binding, convert its consumers, and demonstrate integrated behavior and regression protection | Slice02 design; resolved implementation baseline; assigned contributor/reviewer workflow | Planned; detail when near |

Slice02 produces the implementation-ready Slice03 assignment after satisfying the prompt-authoring readiness requirements. Do not issue a speculative CC prompt now. If the actual dependency map makes Slice03 too large for one context, split it before assignment and record the roadmap amendment; do not silently broaden the pilot.

Slice01 and Slice02 have owning directories/open sets. Slice03 remains a roadmap entry, not an empty execution packet. The earlier Slice01-only state is superseded by the Operator-authorized design continuation recorded below.

## Arc acceptance and composition

The [arc ledger](ledger.md) governs acceptance. At composition review, demonstrate one ordinary turn being saved and read through the portable boundary while its Mongo binding preserves characterized identity, content, tenancy, retention, provenance, and failure behavior. Verify there is no engine-specific type/query escape hatch in that public pilot contract. Account for every out-of-pilot caller that still uses compatibility paths.

The contract design must separately show how original source records and their operational representation relate: source namespace/native identity, original parent references and timestamp precision, content blocks, import provenance, repeat-ingest identity, and derivation/version mapping. This is not a requirement to make every possible future Guildhall field part of the first message DTO.

Child completion alone does not prove the arc composes. Arc close requires integrated evidence, disposition of all bubble-up findings, the applicable independent composition review, and the Operator's unchanged gates. No arc criterion is accepted at opening.

## Workflow and source boundaries

This conversation is the sole active contributor. The Operator remains the design partner and scope authority. Current work is investigation and planning with self-checks; no fictional CC/CRC assignments or independent verification files are created. The project retains its intended progression to two contributors for deeper work and three for well-defined implementation. Record actual assignments and effective scope at transition.

The earlier fork-only remote query found no dev ref. This is now resolved: the Operator requested a `billo-guildhall` implementation worktree, created from verified `upstream/dev` at `fe79265b2f47937051625719f3ba5080189912c1`. Source instructions still require upstream PRs against dev; main remains pristine. See [repository workflow](../../repository-workflow.md) and [Operator decisions](../operator-decisions.md). Earlier evidence remains at its original source commit; refresh source/build validation before implementation.

Keep the running LibreChat/Mongo corpus unchanged. Test suites must be inspected for isolated database setup and teardown before execution. Tests may mutate only their disposable databases. Keep private exports and conversation contents outside Git; use sanitized fixtures for later tests.

## Current action

Slice01 delivered its [proposed closing packet](slice01-behavior-baseline/closing-report.md), and its findings were already bubbled into this plan and the project plan in `a085652ce`. On 2026-09-20 the Operator read that report and instructed “Please continue, regardless!” This authorizes [Slice02 design preparation](slice02-portable-contract-design/slice-plan.md) using the attested evidence while Slice01's independent acceptance remains pending. The earlier blanket advancement hold is superseded for this preparatory work; no child is formally closed, no review is fabricated, and no source implementation is assigned.

Slice02 has delivered a [first contract pass](slice02-portable-contract-design/artifacts/contract-design.md) and [cursor characterization](slice02-portable-contract-design/artifacts/pagination-findings.md). The synthetic control returned 6/6; the equal-timestamp fixture returned 4/6 and declared completion, confirming the suspected gap in the installed build. A pagination correction is proposed as separate work; the adapter must not silently change compatibility behavior. The initial proposal also overstated injection: BaseClient imports the database singleton; only the save helper accepts injected dependencies. That correction is reflected in the project design input.

Current design work is relationship translation without exposing physical IDs or adding a serial lookup, field-level DTO/projection validation, conservative partial-write outcomes and the exact route/code fence. These findings deepen Slice02 without broadening the three-slice roadmap or implementation scope. D06 dev lineage is now resolved through the upstream-based Guildhall worktree; Node 24/source-build reproduction remains pending. The Operator subsequently clarified that denormalization is only an option. Slice02 should instead start from the [future-oriented logical identity model](../interface-design.md#working-identity-direction-toward-the-cognitive-data-plane) and investigate a named turn operation that keeps physical links inside the adapter. Receipts and denormalization remain alternatives; the exact boundary and schema are not frozen.

Slice02 [pass 2](slice02-portable-contract-design/artifacts/design-pass02/decision.md) now supplies 28 matching source-based orchestration comparisons, eight memo/fallback checks and three detected negative controls. These support the smaller logical-reference/private-locator-hint candidate while preserving the two-stage workflow; a naive early snapshot changes cleanup timing. This supersedes the compound-first hypothesis above as the immediate design direction. Scope/lifetime correctness against real Mongo, DTO schemas and caller/result mappings remain open. There is no new implementation or roadmap scope.

**Pass-3 correction:** [Slice02 lifecycle evidence](slice02-portable-contract-design/artifacts/design-pass03/decision.md) supersedes the pass-2 hint preference: two controls held, four lifecycle cases broke reference value equivalence, and two negative controls were detected. Reject silent hot/cold resolution. Next compare a per-invocation turn-write handle retaining the observed row privately, while preserving current application sequencing. This remains investigation; real application conformance, concrete DTOs, lifecycle/scope enforcement and acceptance remain pending.

**Pass-4 progress:** [Slice02 comparison and mapping](slice02-portable-contract-design/artifacts/design-pass04/decision.md) retains the handle as the working handoff: 28 orchestration cases, 26 lifecycle/scope cases and five negative controls. The source field census and patch/error table now guide DTO work. Remaining implementation prerequisites include projection/consumer reconciliation, invalid-input versus strict-scope validation ordering, current source builds and real-method conformance. Slice02 remains active; no roadmap expansion or contributor transition.

**Pass-5 progress:** [Slice02 read contract](slice02-portable-contract-design/artifacts/design-pass05/read-contract.md) records the selected reload/by-ID/history paths, shared probe wiring and explicit legacy exclusions. It preserves parallel admission gating (16 comparisons plus two deferred checks) and source preflight ordering (three cases). Begin-time strict enforcement from pass 4 is superseded by non-enforcing scope capture with legacy query enforcement. The 117-field matrix resolves declared projection/provider differences; full nested codecs and source integration remain pending.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.9 | 2026-09-21 | Slice02 pass 5 made D01 read scope explicit, corrected D04 validation ordering and reconciled declared fields with provider/public projections. |
| v1.8 | 2026-09-20 | Slice02 pass 4 validated the bounded handle prototype and added source-field/partial-outcome mapping; scoped remaining DTO and integration work. |
| v1.7 | 2026-09-20 | Slice02 pass 3 rejected invisible locator caching after real-Mongo lifecycle counterexamples; recorded the next explicit observed-write candidate without expanding source scope. |
| v1.6 | 2026-09-20 | Slice02 pass 2 compared actual source orchestration and private logical-reference translation; refined D02 direction with explicit mocking, lifetime and source-build limits. |
| v1.5 | 2026-09-20 | Refined D02 direction using the Operator's future-Lance guidance; denormalization is not a preferred solution, and named-operation/logical-identity hypotheses need concrete validation. |
| v1.4 | 2026-09-20 | Incorporated Operator denormalization preference and verified worktree/base decision; D06 resolved, historical test evidence preserved and current-build validation still required. |
| v1.3 | 2026-09-20 | Recorded Operator-authorized Slice02 design continuation while retaining Slice01 acceptance; bubbled confirmed cursor gap and injection correction from Slice02, with unresolved contract choices explicit and no source scope change. |
| v1.2 | 2026-09-20 | Slice01 delivered the attested map/matrix and 641-test baseline; added concrete contract/coverage/runtime findings and retained independent acceptance. Roadmap unchanged pending reviewed sizing in Slice02. |
| v1.1 | 2026-09-20 | Applied project-level Expedited Mode; investigation workflow and acceptance requirements unchanged. |
| v1.0 | 2026-09-20 | Opened Arc01 at the Operator's request; defined three slices and opened only the first investigation slice. No application behavior or project acceptance requirement changed. |
