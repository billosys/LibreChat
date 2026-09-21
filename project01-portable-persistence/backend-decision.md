# First non-Mongo backend — SQLite proposal

Status: **SQLite named by the Operator as the initial Claude corpus target; Rust-service architecture remains proposed**. Date: 2026-09-20. No backend benchmark, migration, or application acceptance test has been performed.

## Recommendation

Choose **SQLite**, accessed through the portable domain interface and hosted by a **local Rust service**. First establish the Mongo-backed interface in the existing LibreChat process; then implement the SQLite service client as another binding of that interface.

This recommendation assumes local/native operation, a single service owning canonical writes, and a workload that can tolerate serialized write transactions. It does not assume one human user, waive tenant isolation, or require a separate database per tenant. Those are independent design choices.

SQLite's own guidance describes both local application storage and an application-specific server that accepts higher-level requests. It also documents the single-writer constraint and reasons to choose a client/server engine when writers cannot queue. Those properties match the proposed service boundary, subject to workload validation. [SQLite: appropriate uses](https://www.sqlite.org/whentouse.html).

WAL mode offers a reader/writer concurrency mechanism, but checkpointing, long-lived readers, busy handling, and durability settings still require operational design. We should pin and test an appropriate SQLite build instead of treating a mode flag as proof of suitability. [SQLite: write-ahead logging](https://www.sqlite.org/wal.html).

The architectural reason to start here is that a second engine with different data and query semantics will exercise the abstraction. A successful adapter must reproduce the domain contract rather than forward Mongo operators to another server.

## What the first SQLite implementation should look like

- A Rust process owns schema migration and writes to a local database. LibreChat connects through a versioned, authenticated local protocol; clients do not open the file directly.
- Use explicit tables and constraints for identities, ownership, relationships, and frequently queried state. Structured content can retain nested representation where its semantics warrant it. Do not make one opaque document column the universal schema merely to mimic Mongo.
- Implement transaction boundaries per domain operation. Keep write transactions short; establish bounded queue/busy behavior and observability. Numerical targets follow representative workload measurement.
- Preserve historical IDs and maintain private mappings where necessary. Schema design must distinguish missing, null, and explicitly cleared state when the domain does.
- Own expiry scheduling and recovery deliberately. The presence of an expiration timestamp is not a working equivalent of Mongo TTL behavior.
- Treat search and blob/checkpoint/cache facilities as explicit migration surfaces. Preserve required external integrations until their replacement is separately designed.

SQLite FTS5 is a potential local full-text facility. Its existence does not establish compatibility with LibreChat's Meili query, ranking, filtering, or indexing behavior; do not bundle a search-engine swap into the initial persistence work. [SQLite: FTS5](https://www.sqlite.org/fts5.html).

The concrete SQLite schema, Rust crates, protocol, supervisor/launch mechanism, runtime version, durability profile, and backup tooling remain to be selected during detailed design. The existing Node runtime remains part of LibreChat. “Rust-first” here governs the new service, not a rewrite of the application.

## Alternatives and why they are not the initial recommendation

The following is a scope/architecture comparison, not a measured product ranking.

| Candidate | Why consider it | Current disposition |
|---|---|---|
| PostgreSQL | Appropriate alternative if service deployment and independent concurrent writers become the primary target | Reconsider if the local single-owner assumption changes; not a second simultaneous backend assignment |
| FerretDB / Mongo-compatible replacement | Could reduce application changes by retaining the existing wire/query contract; the repository contains an earlier investigation | Useful separate migration strategy, but retaining Mongo semantics does not demonstrate our desired portable boundary |
| Lance / LanceDB first | Closest to an important proposed cognitive substrate | Defer as the operational starting point: we would need to validate all current mutation, identity, auth, lifecycle, and concurrency semantics at the same time as the interface |
| DuckDB first | Already part of the envisioned analytical toolset | Reserve evaluation for analytical views; this proposal gives it no operational compatibility claim |
| SurrealDB or another combined document/graph engine | Could be evaluated if concrete multi-model operations justify it | No source-backed compatibility case established in this reconnaissance; broader engine features alone do not resolve application contracts |

Deferring a candidate is not rejecting it from Guildhall. SQLite can remain an operational component while Lance supports a growing cognitive corpus and other engines provide specialized views.

## Evidence needed to confirm the choice

1. Run the agreed conformance cases against real Mongo and the real Rust/SQLite adapter, with mismatches recorded by domain outcome rather than physical document equality.
2. Exercise representative ordinary chat, imports, concurrent background work, and long histories. Measure latency and queue contention on the intended machine; include service transport cost.
3. Test competing claims, stale revisions, retried requests, process termination around commit/response, expiry, schema upgrade, and backup/restore. Confirm that a lost response cannot cause an unsafe blind replay.
4. Rehearse migration from a defined Mongo snapshot with preserved IDs, explicit field transforms, relationship checks, rejection accounting, and restartable progress. Prefer a write-quiesced first cutover; online replication is a separate scope expansion.
5. Define rollback for both pre-cutover and post-cutover writes. Keeping an old Mongo snapshot alone cannot recover new SQLite-only writes.
6. Start and exercise the supported LibreChat deployment without Mongo. Keep the feature matrix visible and account for caches, checkpoints, startup probes, seeds, and background workers.

Decision triggers: move toward PostgreSQL if required write concurrency or deployment topology invalidates the single-owner local model; revise contract boundaries if a second adapter needs engine-specific escape hatches in routine operations; revise migration scope if data cannot be mapped without losing meaning. These are reasons to update the plan, not to quietly relax acceptance.
