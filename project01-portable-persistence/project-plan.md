# Project01 — Portable LibreChat persistence

| Metadata | Value |
|---|---|
| Project | project01-portable-persistence |
| Status | Draft design and roadmap; no implementation arc active |
| Depends on | LibreChat source baseline; resolution of source `dev` branch before implementation |
| Blocks | A validated Mongo-free LibreChat deployment through the new boundary |
| Related | Billo Guildhall; CCDP; memory research; AI Engineering concept cards and ontology work |
| Design | [Interface proposal](interface-design.md), [backend proposal](backend-decision.md) |
| Evidence | [Reconnaissance](research.md) |

## Goal and boundaries

Deliver the Operator's three practical objectives: design our own persistence interface with room for Guildhall's eventual data architecture; convert LibreChat to that interface while retaining MongoDB; implement one first non-Mongo backend and establish an iterative path forward.

“Future-oriented” means explicit, evolvable semantic contracts and independently testable adapters. It cannot mean a guarantee that every future requirement fits an unchanged API. We should expect additive operations, versioned changes, and new domain services.

In scope: application persistence and its lifecycle, identity and tenant semantics, contract isolation, Mongo compatibility, a Rust-hosted SQLite implementation, data migration and rollback, and complete selected-backend startup. The proposed SQLite deployment target is a local service with a single owner for writes. This proposal does not reduce LibreChat's existing tenant or authorization obligations.

Outside this project's delivery: a general-purpose memory protocol, ontology extraction, replacing existing knowledge graphs, an HTN planner, a CCDP dispatcher, a ratatui client, Lance projections, vector-search redesign, replacing every external search/RAG/file service, or making Node-based LibreChat itself a Rust application. Those directions inform boundaries without becoming prerequisites.

## Definition of done

1. Application consumers use explicit portable operations; engine types and query languages remain inside the relevant adapter. Any remaining Mongo dependency is classified and cannot run on the SQLite-selected path.
2. Mongo preserves characterized user-visible behavior and data compatibility through that boundary. Changes to semantics are separately documented and reviewed.
3. SQLite implements the required capability set through a local Rust service; the same behavioral conformance cases exercise both adapters. No Docker is required by the new service.
4. A documented migration rehearsal preserves identities, tenant boundaries, relationships, temporal metadata, supported content, and deletion semantics, with mismatch accounting and a demonstrated rollback strategy.
5. A representative enabled-feature deployment starts, authenticates, saves and reloads conversations, and performs its background work without a Mongo service or URI. The enabled-feature matrix is explicit; omitted features are not counted as supported. Project closure requires resolving every Mongo-dependent default feature, not disabling defaults to make a smoke test pass.
6. Relevant regression, recovery, isolation, latency, and packaging checks pass with retained evidence and reviewer reproduction. See [ledger.md](ledger.md).

## Arc roadmap

| Arc | Capability | Depends on | Current state |
|---|---|---|---|
| Arc01 — Contract and first Mongo conversion | Establish portable contract conventions and real-database conformance; convert one complete, bounded application path with Mongo underneath | Operator design review; current source branch resolved | Candidate scope only |
| Arc02 — Complete Mongo boundary | Migrate the remaining persistence families and startup/lifecycle wiring; make bypasses and supported capabilities explicit | Arc01 | Not detailed |
| Arc03 — Rust service and SQLite adapter | Implement the second adapter and transport, using the established contract and Mongo behavioral reference | Arc01 contract; Arc02 coverage before full integration acceptance | Not detailed |
| Arc04 — Migration and complete cutover | Rehearse migration/rollback, validate full selected-backend composition, recovery, and native operation | Arc02 and Arc03 | Not detailed |

These arcs describe capabilities, not estimated sprint sizes. Arc02 in particular may need several slices and revised decomposition after the dependency inventory. Arc03's earliest bounded conformance work may begin after Arc01; the roadmap should not postpone discovering portability failures until the entire Mongo conversion is finished. No parallel execution is currently assigned.

## Immediate design work

The recommended first conversion is the ordinary message-save/conversation-update path. It is recognizable to the user and already has an injected store, but its retention, provenance, logical/storage IDs, and partial-failure semantics require careful characterization. Arc01 must scope ordinary turns explicitly and preserve compatibility with other callers; it cannot silently absorb all subagent scheduling and import workflows.

Before issuing its first slice:

1. Resolve the source branch baseline and read applicable current instructions.
2. Trace all callers and lifecycle effects of the selected methods; identify which remain behind compatibility adapters.
3. Finalize concrete operation and result schemas, ID translation, omission/clearing semantics, error mappings, and module exports.
4. Specify real-Mongo characterization and portable conformance tests with cases that fail on incorrect tenant scope, null handling, identity translation, or lost metadata.
5. Create Arc01's plan/ledger and the first slice's complete open set using the framework's implementation-prompt readiness guide.

There is no implementation estimate yet. Import counts are reconnaissance measurements, not a count of edits or an estimate of effort.

## Workflow and authority

Use the collaboration framework's **Two-Contributor Workflow**. This conversation is CDC; the Operator reviews consequential design choices. CC will be a separately assigned implementation context. CDC performs source-grounded review and required reproduction. No CRC context has been appointed.

The Operator has authorized research/design/planning and the standard planning worktree. The implementation objectives are established; the design alternatives here have not yet been selected by the Operator. Ordinary planning preparation proceeds under existing authorization. Record a settled backend or architecture choice before issuing dependent implementation work.

Scope, architecture, acceptance, or cross-arc changes return to CDC and the Operator. Preserve issued prompts; use the framework's iteration filenames and assignment history. Verification filenames use `cdc-verification.md` in the default workflow; contributor reports alone do not close reviewer-owned acceptance. Detailed slice artifacts live under their owning slice unless an explicit override is recorded.

## Current status

The orphan planning checkout and initial design inputs exist. No arc or slice is accepted, no source behavior has changed, and no runtime tests or benchmarks have been run for this project. Every project composition criterion remains open.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-09-20 | Initial proposed roadmap from the Operator's three persistence objectives and pinned LibreChat reconnaissance. No arc-close bubble-up yet. |
