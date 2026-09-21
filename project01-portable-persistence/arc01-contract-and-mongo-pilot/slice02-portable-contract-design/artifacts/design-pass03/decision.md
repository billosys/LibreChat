# Logical identity and an observed write are different contracts

**Disposition:** reject pass 2's invisible WeakMap fast path with logical-lookup fallback. Keep the two-stage application ordering. Investigate a per-invocation turn-write handle that retains the observed row privately, with ordinary logical references remaining value-based. This is a contributor design recommendation, not an implemented or independently accepted interface.

## What the experiment established

The [predeclared protocol](protocol.md) and [harness](experiment.cjs) ran once against a fresh Mongo 8.2.1 instance using native driver 6.20.0. The harness used the exact memo declarations from the sealed [pass-2 experiment](../design-pass02/experiment.cjs). [Attempt](attempt-01.json), [raw output](output-01.log) and [structured results](result-01.json) preserve the run. Cleanup succeeded. No live database or private export was opened.

| Mutation between observation and resolution | Original reference object | JSON copy with identical values | Result |
|---|---|---|---|
| None | A | A | Equivalent |
| Content update in place | A | A | Equivalent |
| Delete | A | Unavailable | Different; A is dangling |
| Delete and recreate under same logical key | A | B | Different; A is dangling |
| Rename message ID | A | Unavailable | Different; A exists under another logical ID |
| Move conversation ID | A | Unavailable | Different; A exists in another conversation |

All six characterization cases matched their predeclared expectations: two equivalence controls and four counterexamples. Each original-object resolution used zero fallback reads; each copied-reference resolution used one. The actual synthetic conversation `$addToSet` operations confirmed dangling links for deletion/recreation and a reference mismatch for rename/move. The default-port guard rejected a live-style URI, and the forced always-lookup control was rejected by the zero-extra-read oracle despite returning the right ID.

The result is not “six cache tests passed.” The candidate's value-equivalence claim failed in four tested lifecycle conditions. Its earlier 28 mocked orchestration matches remain valid within their declared limits; they never proved freshness.

## Connection to current source

Pinned source: Guildhall `fe79265b2f47937051625719f3ba5080189912c1`. The result records hashes for the schema and both method files. Relevant observations:

- `packages/data-schemas/src/schema/message.ts:310–312` declares TTL expiry and a unique `(messageId,user,tenantId)` index. Conversation ID is not part of that uniqueness key.
- `packages/data-schemas/src/methods/message.ts:880–886` copies supplied fields and supports `newMessageId`; `deleteMessages` at 3570 delegates to `deleteMany`.
- `packages/data-schemas/src/methods/conversation.ts:2202–2206` distinguishes missing append metadata (reconcile by query) from supplied metadata; 2328–2329 builds the physical-ID `$addToSet` without verifying that each row still exists.
- `api/app/clients/BaseClient.js:1332–1386` saves a message, then reads application state and supplies the returned `_id` to the conversation helper. The current handoff is an observed physical row, not a fresh logical lookup. Its separate writes already permit a dangling relationship if deletion intervenes.

The fixture reproduces the relevant storage primitives, not those full methods. TTL scheduling, provenance CAS, tenant middleware, retention, duplicate recovery and the whole request pipeline were not executed. Ordered mutations exhibit possible interleavings; this is not a production race-frequency claim. Node 22.22.3 remains below the Node 24.16.0 pin. No application build, typecheck or integrated conformance acceptance is claimed.

## Decisions we can make now

1. A logical reference cannot silently switch between “the row once observed” and “the current row with these values” based on JavaScript object identity. Copying or serialization must not change its contract.
2. A request-scoped WeakMap or short TTL does not repair this: deletion can happen within the same request. Invalidation confined to this binding cannot cover legacy writers, database TTL deletion or another process. No such correctness guarantee is established.
3. The ordinary Mongo compatibility path should preserve its observed-row handoff without an extra resolution read. A deliberately named logical-resolution operation may query current storage; it must not be the fallback of an observed-write operation.
4. Keep durable message identity separate from incarnation, revision, representation and transient operation state. Preserve existing IDs; do not add incarnation columns, event sourcing or a denormalized schema solely to resolve this pilot seam.

The candidate reference included `conversationId`; the fixture deliberately preserves that lookup constraint. Since the source's unique key omits it, the DTO census must label conversation membership as relationship context/expected membership rather than silently declaring it part of universal message identity. This does not authorize changing legacy move/rename behavior.

## Next candidate: a local turn-write handle

Prefer explicit bounded ownership over a global receipt registry. One `saveMessageToDatabase` invocation obtains one adapter-owned handle. It can save one message and then update one conversation using the observed write internally. It is a local dependency interface, not a serializable entity DTO, durable identifier, database transaction or generic callback API.

```text
application                         adapter-owned turn handle
  retention/cache decisions
  beginTurnWrite(trustedScope)  ---> private state, no DB read
  saveMessage(fields, metadata) ---> save through legacy method; retain returned row
                              <--- plain observed-message DTO
  read live skip/initialized/
    request/endpoint state
  updateConversation(fields,    ---> append retained locator, or legacy reconcile
    updateOptions)                  if the save returned no usable row/locator
                              <--- existing conversation outcome
  release in finally           ---> discard retained row; no rollback
```

The handle is the named local continuation of an observed write. It never accepts a caller-supplied Mongo locator and never resolves a copied logical reference to replace a missing observation. Keep physical objects in the data-schemas implementation; application code receives the portable DTO and method surface. Exact type names remain draft until the field/result census.

Proposed lifetime rules for the next comparison:

- Scope is bound from trusted effective tenant/owner policy. Every operation still enforces that policy; a changed effective scope fails before any write. Do not treat possession of the handle as authorization. Test strict, unscoped and system modes explicitly.
- One handle per invocation, never one per client or conversation. Reject concurrent/repeated use of the same stage. In-flight calls retain their own state; release discards retained data when they finish and rejects new stages. It does not cancel or undo a write already dispatched.
- No eager snapshot of mutable application policy. Compute conversation fields and read `skipSaveConvo`/`fetchedConvo` at the current source's points after awaiting the message. This avoids the pass-2 early-snapshot defect.
- A successful message method may return `undefined` or an observed row without a locator; keep the current reconciliation branch. A thrown message write stops the workflow. Conversation errors/null results retain their existing distinctions. There is no hidden retry or transaction promise; a failed conversation write may follow a persisted message.
- Seed writes remain a separate path with their existing empty append intent. Skip/disposal/failure paths release the handle in `finally`. A later application retry creates a fresh invocation; handles do not become retry tokens.
- Intervening deletion does not silently redirect to a replacement row. Mongo's compatibility implementation keeps the observed locator, even where legacy behavior can leave a dangling link. Improving referential integrity is a separately reviewed behavior change. This does not mandate dangling physical arrays in SQLite or Lance.

This candidate avoids exporting receipts just to hide `_id`, while preserving staged application decisions. A future Node-to-Rust adapter must decide how the service owns continuation state or combines commands; this local handle is not an approved remote protocol. Durability, timeout recovery and idempotency remain D09 work. Do not add an RPC session registry now.

## Next bounded work and remaining gates

D02's semantic ambiguity is resolved against invisible-cache resolution. Its concrete handle implementation, scope enforcement and lifecycle proof remain open. Compare this candidate against the same 28 source-based scenarios, then test illegal lifecycle transitions and two independent overlapping handles; include a negative control that re-resolves after recreation. Complete the DTO/projection census and D03/D04 result/field-state mapping before issuing an implementation prompt. These are refinements inside Slice02, not new roadmap scope.

The parent plans and ledger carry this disposition. Earlier packets remain sealed. No source conversion, Slice02 closure, reviewer assignment or new contributor prompt occurred.
