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
| Current slice | [Slice01 — Behavior baseline](slice01-behavior-baseline/slice-plan.md) |

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
| Slice02 — Portable contract design | Resolve operation schemas, source/operational identity mapping, failure semantics, conformance cases, module boundaries, and the precise code fence | Slice01 evidence and disposition of its findings | Planned; detail when near |
| Slice03 — First Mongo conversion | Implement the reviewed pilot contract and Mongo binding, convert its consumers, and demonstrate integrated behavior and regression protection | Slice02 design; resolved implementation baseline; assigned contributor/reviewer workflow | Planned; detail when near |

Slice02 produces the implementation-ready Slice03 assignment after satisfying the prompt-authoring readiness requirements. Do not issue a speculative CC prompt now. If the actual dependency map makes Slice03 too large for one context, split it before assignment and record the roadmap amendment; do not silently broaden the pilot.

Only Slice01 has a directory/open set. Later slices are roadmap entries, not empty execution packets.

## Arc acceptance and composition

The [arc ledger](ledger.md) governs acceptance. At composition review, demonstrate one ordinary turn being saved and read through the portable boundary while its Mongo binding preserves characterized identity, content, tenancy, retention, provenance, and failure behavior. Verify there is no engine-specific type/query escape hatch in that public pilot contract. Account for every out-of-pilot caller that still uses compatibility paths.

The contract design must separately show how original source records and their operational representation relate: source namespace/native identity, original parent references and timestamp precision, content blocks, import provenance, repeat-ingest identity, and derivation/version mapping. This is not a requirement to make every possible future Guildhall field part of the first message DTO.

Child completion alone does not prove the arc composes. Arc close requires integrated evidence, disposition of all bubble-up findings, the applicable independent composition review, and the Operator's unchanged gates. No arc criterion is accepted at opening.

## Workflow and source boundaries

This conversation is the sole active contributor. The Operator remains the design partner and scope authority. Current work is investigation and planning with self-checks; no fictional CC/CRC assignments or independent verification files are created. The project retains its intended progression to two contributors for deeper work and three for well-defined implementation. Record actual assignments and effective scope at transition.

The fork currently exposes `main` at the inspected source commit and no `dev` ref in the explicit remote query. Source instructions require implementation branches and PRs against `dev`. This does not block read-only investigation or isolated tests; resolve the implementation baseline with the Operator before creating an implementation branch. Do not silently retarget to `main` or fabricate an upstream lineage.

Keep the running LibreChat/Mongo corpus unchanged. Test suites must be inspected for isolated database setup and teardown before execution. Tests may mutate only their disposable databases. Keep private exports and conversation contents outside Git; use sanitized fixtures for later tests.

## Current action

Slice01 has delivered its [proposed closing packet](slice01-behavior-baseline/closing-report.md): source map, behavior/coverage matrix, 641-test baseline and design inputs. Evidence is attested; formal acceptance and advancement remain pending the existing separate-review gate. Findings for Slice02 include physical message-link IDs, cached-null lookup state, partial persistence/error-object outcomes, private versus public projections, weak unset coverage, and an uncharacterized equal-key message-cursor risk. The installed Node 22/dist baseline also needs pinned-runtime/source-build reproduction before implementation acceptance. These findings deepen the planned contract design; the three-slice roadmap and implementation scope are unchanged. The prior current action was execution of tracing/test preflight; it is now superseded by this delivered packet and its required review.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.2 | 2026-09-20 | Slice01 delivered the attested map/matrix and 641-test baseline; added concrete contract/coverage/runtime findings and retained independent acceptance. Roadmap unchanged pending reviewed sizing in Slice02. |
| v1.1 | 2026-09-20 | Applied project-level Expedited Mode; investigation workflow and acceptance requirements unchanged. |
| v1.0 | 2026-09-20 | Opened Arc01 at the Operator's request; defined three slices and opened only the first investigation slice. No application behavior or project acceptance requirement changed. |
