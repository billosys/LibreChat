# Inputs to Slice02 portable contract design

This is the completed one-contributor investigation's recommendation, **not an implementation assignment or approved API**. The map and [behavior matrix](behavior-matrix.md) identify observed behavior and test limits. All design decisions below have an owner and a re-entry point before code.

## Recommended pilot

Keep the first binding thin: delegate to existing Mongo methods so retention, provenance CAS, tenant middleware, schema behavior, project statistics and search hooks continue to run. Introduce plain exported contracts in `packages/data-schemas`; expose a supplied port to application orchestration in `packages/api`; retain CJS files as wiring. Do not wrap arbitrary Mongoose query/update operators and call the result portable.

Candidate operations to resolve in Slice02:

| Candidate operation | Inputs/outcomes to specify | Exact current consumers |
|---|---|---|
| Read conversation for turn | Actor/scope + logical conversation ID; absent vs loaded result, server retention/config fields | BaseClient retention lookup; `save.ts` load/seed helpers |
| Save turn message | Trusted actor/scope, message content/provenance/retention intent, field presence operations; persisted/rejected/recovered/error semantics | `BaseClient.saveMessageToDatabase` user and response saves |
| Write turn conversation | Logical ID, endpoint metadata patch, protected insert metadata, insert permission, logical message-link intent; absent/error/persisted outcome | `saveTurnConversation`, `seedTurnConversation` |
| Read server conversation messages | Owner/scope + logical conversation ID; full server shape and defined ordering | `BaseClient.loadHistory` (parent walk stays above storage) |
| Probe public-read authorization | Owner/scope + ID; absent/expired/child discriminator without full document | `messageValidation.js` supplies `getConvoOwnership`; query GET route |
| Read public messages | Owner/scope + conversation/message selection and public projection; list/cursor semantics only if query route is included | `routes/messages.js` ordinary reload and query-read paths |

Names are provisional. This list intentionally reveals that one ordinary visible save/reload path is more than a generic save/get pair. The request's active-job fallback and admission/terminal ownership remain application rules; the store must not take over the generation manager.

**Logical identity preference:** use existing logical conversation/message IDs at the boundary. An adapter should resolve any physical link internally or use a nonserialized internal receipt; exposing `_id` as a “generic string” is not sufficient storage independence. Decide how to retain the current append fast path without adding a serial query per save. Do not copy `IMessage`, `IConversation`, `FilterQuery`, `Document`, or `Types.ObjectId` into the public contract just because they already exist.

**Failure preference:** typed outcomes should make absence, skipped/rejected input, recovered existing record and partial persistence distinguishable. Legacy callers may initially translate these outcomes back to their present shapes; semantics must not change invisibly. In particular, the current message→conversation→project-stats sequence is not transactional. Making it atomic would be a separately reviewed behavior change.

## Proposed code fence and sizing

Candidate source fence for a later reviewed implementation: new contract/adapter modules and exports in `packages/data-schemas`; turn orchestration in `packages/api/src/conversations/save.ts` (and a new TS helper if needed to keep CJS behavior out); narrow wiring in `api/models/index.js`, `api/app/clients/BaseClient.js`, `api/server/middleware/messageValidation.js`, and selected ordinary read handlers in `api/server/routes/messages.js`. Associated focused unit/conformance/integration tests belong to the same workspaces. These are **candidate paths**, not a source-write allowlist; Slice02 must name final files and consumers before issuing Slice03.

Keep existing message/conversation method implementations intact unless design proves a specific change unavoidable. Do not globally replace `createMethods`, migrate all adjacent agents/controllers, alter import mapping, redesign tenancy, or remove Mongo dependencies from every model in this pilot. Out-of-pilot writers in the dependency map retain their existing compatibility methods; the converted pilot must not silently bypass the supplied port.

**Sizing judgment:** one implementation slice still appears feasible for a delegating Mongo adapter and this bounded consumer set. It is not yet implementation-ready. If solving logical message-link receipts, public cursor behavior, or post-write partial failures demands rewriting shared methods, split Slice03 before assignment. Slice02 owns this decision; the roadmap is not amended by this recommendation.

## Decision register

During the current workflow, “design owner” is this contributor working with the Operator. At a recorded two-contributor transition it becomes the actual assigned CDC; do not invent a reviewer or silently transfer authority.

| ID | Decision / owner | Required resolution before implementation |
|---|---|---|
| D01 | Pilot read surface — design owner | Freeze inclusion of full reload, query pagination and ownership probe; account for both server/private and public views. Keep mutation/search handlers outside the code fence unless specifically needed. |
| D02 | IDs, DTOs and links — design owner | Specify owner/tenant namespaces, storage-neutral temporal encoding, field presence, plain DTO extension policy and message-link receipt. Show source and destination shapes; prove no per-message lookup regression. |
| D03 | Error/partial-success contract — design owner | Enumerate invalid message ID, disposed client, noUpsert miss, duplicate recovery, message failure, conversation failure, post-write stats/backfill failure, and retry ownership. Define legacy translations and negative tests. |
| D04 | Context and patch policy — design owner | Freeze explicit trusted scope, cache-state representation, retention precedence, protected insert metadata, and keep/set/clear semantics. Resolve any new fail-closed policy as a deliberate change. |
| D05 | Message cursor finding — design owner | Characterize equal-key page boundaries with a real DB oracle. Decide preserve/document versus separately scoped fix; do not infer message coverage from conversation-pagination tests. |
| D06 | Source branch baseline — Operator with design owner | Source instructions require `dev`; explicit remote query found only `main` at the inspected commit. Establish the intended fork dev lineage before source branching. No branch was created and `main` was not silently substituted. |
| D07 | Runtime/build provenance — implementation author and reviewer | Reproduce on pinned Node 24.16.0, build affected packages from the claimed source and record resolved artifacts. This run used Node 22 and installed dist, explicitly limited. |
| D08 | Review/acceptance — Operator and actual separate reviewer | Investigative results are proposed-done. Preserve existing independent gates before formal close/advance; record actual workflow transition. Self-checking this packet is not independent review. |
| D09 | Service/SQLite architecture — Operator with design owner | SQLite is selected as first alternative. Rust single-writer service and transport remain proposals for later arc design; do not embed an irreversible RPC or Rust dependency into the TS port now. |

## Source-preservation obligations

Every row below refers to the prior complete [Claude reconciliation](../../../corpus-reconciliation.md); no new corpus content is stored here. Arc01/Slice02 owns semantic design; the later intake/migration work owns implementation and full-population verification. Excluding richer intake from the pilot never waives it.

| Evidence | Required retained meaning and later check |
|---|---|
| 820 source conversations; 9,838 source messages; 9,731 operational messages; 107 skipped, 66 carrying file/attachment metadata | Account for **every** source message with a preservation record and explicit operational disposition. Skipped does not mean empty, invalid, or safe to erase. |
| Source conversation/message UUIDs replaced; no durable source mapping | Stable `(source namespace/account, entity kind, native ID)` plus import batch/fingerprint and versioned source→operational mapping. Define repeated/overlapping export dedup and revisions, not fresh-ID duplication. |
| 95 retained parent links changed across 55 conversations; 52 source branch points in 47 | Preserve original parent/root markers and topology, including skipped ancestors. Keep operational display ordering separately; never reconstruct source graph solely from timestamps. |
| 8,609 tool-use, 8,532 tool-result, 2,388 token-budget blocks not represented structurally | Preserve ordered typed source blocks and unrecognized fields; explicitly derive a display projection. Token budgets are source assertions, not automatically observed usage. |
| 329 thinking blocks concatenated into 140 assistant messages | Keep block boundaries, types and order alongside the rendered text; classify privacy/exposure in DTO views. |
| Attachments on 287 messages, files on 583 (overlap) absent from stored messages | Preserve metadata and references with explicit availability states. These counts do not prove file bytes exist in the archive; byte recovery is an independent later investigation. |
| 446 nonempty conversation summaries omitted | Preserve source-authored summary and provenance separately from generated memory/concept summaries. |
| Conversation update timestamps reset (819 distinct source update times); 161 retained messages had distinct source update times omitted | Keep original creation/update strings and temporal precision, separate from ingest/storage/update times. |
| 9,719 retained creation timestamps lose submillisecond precision | Retain exact source time representation; normalized millisecond values are a projection. Version any timestamp/order adjustment and do not overwrite source evidence. |
| One import-assigned `claude-fable-5-1` model label; no model field supplied by export | Distinguish configured operational label from historical model evidence; unknown historical model stays unknown. |
| Empty embedded message arrays on all 820 conversations; all 9,731 message rows linked | Treat operational row relationships as authoritative history; migration must not count empty embedded arrays as missing all messages. |
| Full raw source remains outside Git with recorded fingerprint | Preserve access-controlled original artifact and derivation provenance; committed tests use sanitized fixtures. Reconcile source fidelity and current-Mongo compatibility as separate obligations before GPT intake. |

Stable concept IDs, memory assertions, procedures/plans and cognitive traces remain future domain contracts. This pilot must preserve extension/provenance space and avoid making LibreChat model shapes the universal Guildhall ontology. It does not implement CCDP, an event log, memory API, Lance or a planner.

## Discriminating future acceptance cases

1. Write/read a turn through **only** the supplied port; fail the test if a converted consumer touches the old singleton. Exercise real Mongo and then the eventual SQLite harness with the same plain inputs and normalized outcomes.
2. Colliding logical IDs for two owners and two tenants; deny spoofed scope, preserve explicit system authority rules, distinguish absent and unknown records without leakage.
3. Seed a nonempty contextMeta/endpoint field, clear it, assert physical absence and protected-field survival; omission leaves it unchanged. Include zero/missing measurements and unknown structured fields.
4. Duplicate/retried/concurrent saves preserve one scoped row and all intended provenance; stale snapshot retries and exhausted contention have observable outcomes. Failed update recovery must not masquerade as new content persisted.
5. Separate unread, cached-null and cached-row request cases. Assert lookup counts and seed→message ordering; test Stop, admission denial, terminal ownership denial and mid-await disposal.
6. Inject failures after message commit, after conversation commit and inside project-stat/backfill work. Inspect durable state and retry behavior; reject false all-or-nothing claims.
7. Preserve bound deadlines despite spoofed payloads; hide expired records before TTL cleanup; test public projection does not return private context or trace fields. Assert parent walk and summary behavior after reload.
8. Equal-timestamp page-edge messages and scrambled parent/child creation times. Require the chosen ordering/pagination promise explicitly; this is distinct from the already passing conversation pagination suite.
9. Sanitized Claude fixture with branching, nonrendered messages, tools, multiple thinking blocks, source summaries, exact timestamps and overlapping second export. Verify source archive, derived view, mappings and population accounting separately.

These are requirements for Slice02 to turn into concrete input/output oracles, not permission to let the implementer resolve the choices. No new implementation tests were added in this investigation. The source's typecheck, relevant workspace regressions and message-loading Lighthouse gates remain required for the later conversion.
