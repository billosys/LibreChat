# Portable persistence interface — initial design proposal

Status: **initial design proposal for discussion, not a frozen API or implementation assignment**. Current one-contributor refinement lives in the [Slice02 contract draft](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/contract-design.md). Source observations refer to the baseline in [research.md](research.md).

## The boundary we want

Define persistence in terms of application operations and their observable outcomes. A conversation save should have a contract describing identity, ownership, patches, ordering, retention, and failure. It should not require a consumer to understand a Mongoose document or compose a Mongo update expression.

LibreChat already has injectable method factories. We should use them as the initial implementation seam, while replacing their exposed engine-specific contracts deliberately. Renaming `createMethods` or putting a generic `find(collection, filter)` wrapper in front of it would leave the difficult coupling intact.

The immediate interface is for operational application persistence. Guildhall memory, ontology, and planning APIs will be separate domain contracts using compatible identity and provenance conventions. We should avoid naming this interface as if it were the entire Guildhall API.

```text
FIRST CONVERSION

LibreChat application logic
          |
    portable domain ports                 plain, validated contracts
          |
    Mongo compatibility adapter           ID/error/value translation
          |
    existing data-schemas methods          preserve characterized policy
          |
    Mongoose / MongoDB

SECOND BACKEND

LibreChat application logic
          |
    same portable domain ports
          |
    TypeScript service client
          |  versioned local protocol
          v
    Rust persistence service               canonical SQLite write owner
          |
    SQLite adapter / migrations
          |
    local SQLite database
```

Mongo initially remains in the existing Node process. Reimplementing its behavior in Rust at the same time as introducing the abstraction would multiply the changes we need to verify. Rust owns the new SQLite service; moving Mongo into that service is not a prerequisite or promised deliverable.

## Current preferences, hypotheses, and open decisions

**Strong current preferences:** domain-oriented operations; explicit tenant/actor context; storage-neutral identifiers and values; Mongo compatibility first; a native local Rust service for the new backend; one authority for each canonical write; no Docker requirement introduced by our service; small conversions with real-backend checks.

**Working hypotheses:** the existing method factories are sufficient foundations for the first migration; ordinary turn persistence makes a tractable first slice after characterization; SQLite fits the local workload; an explicit operation log/outbox will eventually connect operational changes to cognitive projections.

**Open decisions before implementation:** exact operation names and DTO schemas; minimum pilot surface; service transport and authentication; version-negotiation rules; crate and SQLite build selection; capability grouping; supported deployment/feature matrix; precise atomicity and retry policy for each mutation. This draft specifies constraints on those choices without pretending they have been resolved.

## Module and ownership proposal

Follow the repository's existing rule that database contracts live in `packages/data-schemas`. Introduce a deliberately narrow contract entrypoint there, with plain types and runtime validation that do not pull model registration, Mongoose, or Node-only side effects into consumers. Verify its dependency graph; a new directory alone does not create isolation.

Mongo implementations remain in that package alongside existing schemas and methods. Application orchestration and the future service client belong in `packages/api`; `/api` stays composition and legacy wiring. Frontend API models remain in `packages/data-provider`; the browser must not gain a persistence or privileged service connection.

That placement is a compatibility choice for the LibreChat fork. Later extraction into a separately maintained Guildhall contract package is plausible, but it should preserve the same schemas and conformance obligations rather than start a competing API. A Rust service may consume an independently portable wire schema with generated or checked language bindings. Select the schema format before implementing transport, not by exporting TypeScript types and assuming Rust sees the same contract.

Proposed ownership: keep LibreChat's TypeScript adapter/client in this fork and house the Rust service in Guildhall, subject to confirming that repository's layout. Do not insert a Rust backend into LibreChat in conflict with its TypeScript workspace rules. This planning pass creates no Guildhall repository or service source tree; coordinate its eventual implementation assignment explicitly with this project's contract and acceptance criteria.

## Semantics to make explicit

| Concern | Proposed contract rule | Compatibility obligation |
|---|---|---|
| Identity | Opaque logical string IDs and scoped references; immutable except an explicitly named identity-changing operation | Preserve existing public IDs, including historically ObjectId-shaped strings. Keep internal row/ObjectId mappings private |
| Scope | Trusted server-derived tenant, actor, and authority context on operations | Preserve the current legacy unscoped/system policy where compatibility requires it; never accept elevated scope solely because a remote caller supplied it |
| Values | Plain structured values with documented timestamp, numeric, and binary encodings | Preserve supported message content and metadata; no silent precision loss or dropped unknown supported content |
| Patches | Per-field set/clear/unchanged rules; omitted fields are not silently converted into null | `contextMeta: null` currently clears while omission preserves. Empty string/list/object may have distinct meaning |
| Writes | Distinguish create, patch, conditional update, and upsert | A portable call must not accidentally create rows where old behavior used no-upsert |
| Results | Domain outcomes such as saved, absent, rejected, conflict, or unavailable, with operation-specific payloads | Preserve existing caller outcomes through a compatibility mapping; do not collapse undefined/no-op, absent, and backend failure without reviewing the call path |
| Pagination | Opaque cursor tied to sort, scope, filters, and contract version; deterministic tie-breaking | Existing `_id` tie-breaking needs a stable equivalent across migration. Reusing an unrelated row order is insufficient |
| Filtering | Named filters and projections for real use cases; bounded result sizes | Keep Mongo operators and arbitrary SQL outside the contract. Capture needed aggregates explicitly |
| Concurrency | Named compare-and-set/claim operations with documented preconditions and outcomes | Cover leases, queue ordering, conditional ownership, and retries; CRUD alone cannot express these correctly |
| Retention | Authoritative write context, explicit expiration semantics, eventual deletion behavior documented | Preserve temporary/general retention, insertion behavior, and indexes/workers needed to enforce expiry |
| Provenance | Preserve supplied and derived origin metadata with defined merge rules | Normalized provenance and user-submitted paths must survive edits, imports, and re-saves |
| Search | Explicit search capability with declared result semantics and indexing consistency | Existing Meili indexing is a lifecycle integration. A database swap does not automatically replace it |
| Lifecycle | Explicit initialize, migrate, health, flush/drain, and close responsibilities | Registration order, seeds, reconciliation, cache setup, and background workers remain part of backend selection |

Storage neutrality does not mean every engine supports every optional capability. Required capabilities must be checked at startup; an unsupported operation must fail explicitly. Capabilities cannot be an excuse to disable existing default behavior and call migration complete.

## The first application path

`BaseClient.saveMessageToDatabase` currently uses the imported `~/models` singleton. It saves a message and then calls `saveTurnConversation`; that helper accepts injected `getConvo`/`saveConvo` methods. The earlier proposal incorrectly described the whole BaseClient path as already injected; conversion must introduce and verify that dependency boundary. This is a promising first visible path because a user can save a turn, reload it, and inspect its conversation.

The seam is not portable today: `savedMessage._id` crosses into conversation persistence, and `appendMessageIds` carries Mongoose ObjectIds. The proposal is to return a logical saved-message reference. The Mongo adapter translates that reference to its existing storage identity internally, preserving ownership checks and avoiding an unnecessary read where feasible. Whether the reference uses the existing scoped message ID alone or an additional opaque relationship token needs the call-graph review.

A candidate pilot operation set is: look up a conversation for an actor; persist a message with explicit write context; update the conversation after a saved message; read the saved conversation and its messages. These are descriptive names, not final signatures. Define the exact supported filters and projections from callers before freezing them.

Tests must distinguish at least: a first turn from a later turn; absent conversation from not-yet-read request cache; omitted metadata from explicit clear; temporary from persistent retention; duplicate logical IDs across users/tenants; invalid conversation IDs; updated provenance; equal-timestamp ordering; and failure between message save and conversation update. Preserve the behavior of `skipSaveConvo` and disposed clients where that path uses them.

This pilot is not the full conversation lifecycle. Deletion, imports, sharing, subagent threads, queued deliveries, and other writers must remain correctly routed through existing behavior until migrated. The first slice must identify its boundary rather than rewrite a many-thousand-line module wholesale.

## Working identity direction toward the cognitive data plane

**Status: lightweight design hypothesis, 2026-09-20.** This follows the Operator's clarification that denormalization was an option, not a recommendation. It draws on this document's Guildhall direction and the [backend proposal](backend-decision.md); it is not a survey of current LanceDB APIs or a commitment to particular tables, graph products, UUID formats or storage features.

The useful long-lived commitment is to semantic identity and provenance. A message, memory assertion, concept or project should remain addressable when its physical representation changes. Mongo, SQLite and possible Lance/graph views can locate the same entity differently. Existing ontology identifiers retain their own authority; a shared reference convention need not mean one universal entity table or one ID issuer.

**Strong working preference:** use scoped, typed logical references at domain boundaries; keep storage addresses private. Preserve existing LibreChat IDs and separately map original import identities. The authenticated context governs access: knowing or supplying a reference never grants authority.

**Plausible future model, subject to revision:**

| Meaning | Illustrative shape | Why preserve the distinction |
|---|---|---|
| Entity identity | `(namespace, kind, logical_id)` with explicit ownership/scope policy | Survives movement between physical stores; namespace rules need not duplicate tenant in every payload |
| Entity revision | `(entity_ref, revision_ref)` | Identifies the specific state from which a claim, summary or trace was derived; do not assume existing Mongo `__v` provides this contract |
| Source identity | `(source_namespace/account, kind, native_id)` plus export/version evidence | Preserves external identity and repeat-import mapping without replacing operational IDs |
| Derived representation | Own representation ID, source revision refs, derivation/version metadata | Allows multiple chunks, embeddings or views of one entity, and eventual rebuilds without changing that entity's ID |
| Relationship | Typed endpoints plus supporting provenance and validity where needed | Supports parentage, project membership and evidential links without assuming a particular graph engine or physical join |

For example, message `m17` could have revision `r3`, with two retrieval chunks referring to `(m17,r3)`. An assertion extracted from it would be a distinct entity with its own identity and an evidence link to that message revision. A rebuild could replace the chunks while preserving `m17` and the assertion's identity. This is a conceptual example, not permission to add a revision column or emit assertions during an ordinary chat save.

Our tentative Lance role remains a cognitive data plane: reusable source/derived material and appropriate query views, alongside operational storage where useful. Candidate message/content, representation, relationship and trace datasets could share these references. Their exact partitioning, mutation strategy and physical schema remain open. Some content and derived artifacts may be authoritative within their own domains; do not assume that all Lance data is a disposable copy of SQLite, or that every row is immutable and append-only.

Embedding rows, chunk positions, internal Mongo IDs and graph indices must not become the public identity of a memory or concept. Derivation needs enough version/provenance information to recognize stale material. Retention, deletion and access rules must follow referenced and derived data; rebuilding a projection is not a substitute for those rules. Full event sourcing and eagerly materializing every possible view remain unnecessary for the current pilot.

### Consequence for the immediate Mongo seam

The initial candidate was a named ordinary-turn operation. [Pass 2](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/design-pass02/decision.md) favored staged writes with plain references and an invisible physical-locator hint after 28 mocked orchestration comparisons. **That hint preference is superseded:** [pass 3](arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/design-pass03/decision.md) found four lifecycle counterexamples in real Mongo. Copying a reference changed which row it identified, or whether it resolved at all.

**Current working direction:** preserve the staged application sequence, but distinguish ordinary value-based logical references from an observed-write handoff. Investigate one adapter-owned turn-write handle per save invocation: retain the returned row privately, expose a plain message DTO, accept the later conversation update after the application reads its live state, and release in `finally`. No implicit logical lookup substitutes for a lost observation. This is a local operation dependency, not an entity ID, generic transaction callback, rollback guarantee or settled Rust wire protocol.

The candidate must preserve retention pre-reads, cache distinctions, seed order, protected fields, skip behavior and partial outcomes. It avoids an extra Mongo resolution query without pretending that the legacy physical link is a fresh logical lookup. Intervening deletion can still produce the legacy dangling link; stronger referential integrity requires a separately reviewed behavior change. Scope enforcement, lifecycle/overlap tests, full DTOs and failure mapping remain open. The current Mongo uniqueness key is `(messageId,user,tenantId)`; conversation membership must not silently become universal entity identity merely because the prototype reference carried it.

Future SQLite and cognitive-data-plane mappings should agree on domain meanings without copying Mongo's physical arrays or this local coordination mechanism. No new Lance schema, incarnation column, event log, graph implementation or RPC receipt registry is required now.

## Transactions, retries, and events

Do not promise that saving a message and updating its conversation is already one atomic transaction. The observed path performs separate calls, and the source has explicit transaction-capability probing. Characterize the actual deployment-dependent behavior before assigning stronger guarantees.

Prefer named atomic operations over a public `transaction(callback)` API: an arbitrary in-process callback is not a portable remote contract. Operations that require claims, ordering, or compare-and-set must specify their atomic boundary. Adding stronger atomicity is a separate behavior change, not an incidental benefit we can claim from switching engines.

A service boundary introduces timeout ambiguity: a caller can lose the response after a commit. Mutations requiring retry must define an idempotency key, its scope/lifetime, duplicate outcome, and conflict behavior. Cancellation must distinguish “request cancelled” from “write definitely not committed.” Resolve these before the affected operation moves across a process boundary.

Append-oriented events remain attractive for traceability and future projection. We should first decide what is authoritative. A practical later pattern is an operational transaction committing both state and an outbox entry, followed by retryable projection delivery. It avoids independent best-effort writes to SQLite and Lance being mistaken for one durable operation. Outbox availability on each Mongo deployment needs design and verification; it is not assumed here.

Full event sourcing is not required for the first adapter. A transactional WAL, an audit log, a domain event stream, and an event-sourced system are different mechanisms. Retention/deletion and sensitive-data policy must also govern exported events and derived projections; retaining a tombstone does not automatically satisfy erasure.

## Complete boundary inventory

The first inventory found 47 registered models and 45 named domain method factories, plus storage outside that naming pattern. Before Mongo-free acceptance, account for at least:

- Conversations, messages, imports, tags, projects, sharing, and tool-call records.
- Users, sessions, tokens, identity refresh coordination, groups, roles, ACLs, keys, and auth-related cache invalidation.
- Agents, assistants, prompts, presets, skills, MCP configuration/authority, and preferences.
- Files and storage metadata, GridFS-backed facilities, caches, checkpoints, and search-index synchronization.
- Schedules, queued turns, trigger delivery/ordering, purge/retirement work, code environments, and reconciliation.
- Balances, transaction/metering records, audit, insights, banners, configuration, seeds, migrations, and existing LibreChat memory records.

Existing LibreChat memory records are application data to preserve; they are not by themselves Guildhall's research-grounded memory system. Likewise metering “transactions” are a domain name, not evidence of database atomicity.

Each family needs a coverage row linking entrypoints, contract operations, policy/lifecycle effects, adapters, and tests. A family is migrated only when its consumers and background paths are accounted for. Direct import counts are useful signals; indirect model access can remain even when those counts shrink.

## Toward Guildhall

```text
LibreChat     ratatui / tools / agents (future clients)
    |                  |
    +------ native domain APIs -------------------------+
               |                |               |       |
        operational       memory/knowledge   planning   |
        persistence        services          services   |
               |                |               |       |
         Rust / SQLite     protocol-neutral artifacts   |
               |                |               |       |
          future exports / projections / stable references
                                |
                     cognitive data plane
                   Lance + appropriate views

CCDP: optional first-class adapter to governed multi-service workflows.
Direct native API access remains available; routine chat saves need no CCDP hop.
```

Stable references should permit linking a message or observation to a concept, assertion, episode, procedure, or trace without flattening these into one entity type. Existing ontology graphs keep their semantic authority. No operation should assume a concept ID is a Lance row offset, a petgraph index, or a Mongo primary key.

Lance/LanceDB, graph views including possible Lance Graph or petgraph, DuckDB, DataFusion, and Arrow remain future storage/query/interchange candidates. Their evaluation belongs to the relevant Guildhall capabilities, not to the definition of a LibreChat message-save operation. SQLite could continue to serve operational workloads alongside that cognitive data plane; eventual evolution need not mean replacing it everywhere.

The memory API can later expose search, retrieve, assert, revise, invalidate, link, explain, consolidate, and audit, with research-derived semantics and lazy materialization. HTN/planner integrations can refer to procedures, world assertions, and execution traces through their own contracts. This persistence project prepares identity, provenance, and transport boundaries that make those integrations possible; it does not prematurely define their semantics.

## Revision history

| Date | Change |
|---|---|
| 2026-09-20 | Slice02 pass 3 rejected invisible logical-reference caching using real-Mongo lifecycle counterexamples; explicit per-invocation ownership of the observed write is the next candidate. |
| 2026-09-20 | Slice02 pass 2 refined the immediate boundary using source-executed comparison: staged operations with logical references and a private locator hint are preferred for further validation; prior compound-first hypothesis retained as history. |
| 2026-09-20 | Added lightweight Guildhall/Lance-oriented identity hypotheses after the Operator clarified that denormalization is not a recommendation; prefer investigating a named turn operation before a public physical-link receipt. |
| 2026-09-20 | Slice02 corrected the initial injection claim using `BaseClient.js:54,1332–1388` and `save.ts:124–187`; linked the current refinement. No API or implementation scope was frozen. The earlier document remains the architectural starting proposal. |
