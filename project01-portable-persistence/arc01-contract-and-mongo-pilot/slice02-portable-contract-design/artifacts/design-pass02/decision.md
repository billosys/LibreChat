# D02 refinement — logical references with an adapter-private fast path

**Status: selected working candidate for the Mongo seam; not an approved implementation contract.** This pass replaces the previous preference to begin with one compound storage call. The source-based comparison supports preserving the existing two-stage application workflow and optimizing physical-link resolution inside the Mongo binding. Full DTO, tenant-policy and database-lifetime validation remain required.

## What the source actually requires

At `fe79265b2f47937051625719f3ba5080189912c1`, `BaseClient.saveMessageToDatabase` and `packages/api/src/conversations/save.ts` retain the earlier sequence. Retention may require `getConvo` before `saveMessage`; otherwise an unread conversation may be loaded after the message write. Cached-null and cached-present requests avoid that lookup. `initialized` suppresses the later lookup, but is read after the message write. Endpoint options and request cache are also consulted at later stages.

These are observable distinctions, not just implementation style. In particular, `api/server/cleanup.js:144–145` can reset `client.fetchedConvo` while the client method is awaiting a write. An early detached snapshot does not reproduce that case: the reference calls `saveMessage → getConvo → saveConvo`, while the snapshot skips `getConvo`. This comparison does not demonstrate that every real cleanup interleaving causes a user-visible defect; it demonstrates that the naive snapshot is not behaviorally equivalent.

The normal send path awaits `userMessagePromise` before persisting the response (`BaseClient.js:1191–1192`); this reduces ordinary overlap but does not erase cleanup or shared-state concerns. Admission/terminal ownership, seed ordering and request mutation remain application responsibilities. We should not turn those into a new remote state machine just to hide an ObjectId.

## Recommended boundary

Keep a high-level `persistTurn` application service if it improves callers, but do not require its Mongo implementation to be one database operation or one future RPC. Its constituent domain operations can remain save-message and update-conversation, using ordinary logical references. The caller never needs a physical-link token.

Illustrative public shapes (not complete DTO definitions):

```text
MessageReference = { kind: "message", messageId, conversationId }
                    + trusted operation scope from the boundary

message-write outcome = { observedMessage, reference?, commitKnowledge }
conversation-link intent = reconcile | none | append(MessageReference[])
```

Identity is resolved within trusted owner/tenant scope; the reference supplies identity, not authorization. Production output should put the reference in a typed operation-result envelope rather than automatically adding a `ref` field to the browser message model. The prototype's `message.ref` is a minimal plumbing device for the experiment, not a settled public response shape.

The Mongo binding can privately associate a returned reference object with the `_id` of the actual returned database row. A `WeakMap` owned by the binding is a plausible mechanism. The entry stores the logical values and effective owner/tenant scope as well as the physical locator; reuse requires all of them to match. Do not cache the requested new identity instead of the identity actually observed after duplicate recovery or renaming.

```text
existing Mongo save -> row {_id, logical IDs, ...}
                         |
                         +-> plain message DTO + logical reference -> application
                         |
                         +-> binding-private weak association -> physical locator

conversation update receives logical reference
  same returned object + matching values/scope -> reuse locator
  copied/reconstructed reference or other binding -> scoped logical lookup
  unavailable/invalid target -> explicit failure, never arbitrary physical append
```

On the immediate ordinary save path, the application passes the returned reference directly to the conversation helper. No new lookup is needed. Serialization, copying or moving to another adapter loses the optimization, not the logical identity. A future SQLite implementation could resolve those IDs with its own indexing/key design; it need not emulate the WeakMap. Future Lance/graph representations continue to refer to logical entities and source revisions, not this adapter's locator.

No physical denormalization or Mongo data migration is needed for this candidate. Receipts remain unnecessary in the public interface unless a later operation has an actual durable receipt requirement. A service timeout/idempotency receipt is a different concern from this local link optimization.

## Preserve the present write semantics

The adapter still delegates to existing methods. A missing saved result or returned row without `_id` retains the legacy reconcile behavior; an empty seed link set remains `none`; an observed saved row supplies append intent. Message and conversation writes remain separate, without rollback or automatic retries added by this change. Conversation error objects and no-upsert misses remain distinct, and message persistence can precede a failure.

The existing `endpointOptions.conversationId` override is preserved by the comparison. Do not add a rule equating that target with the reference's message conversation ID without classifying existing callers first. Matching cached logical values protects against changing a reference while reusing its old locator; it is not a substitute for defining which relationships an operation permits.

Pure application rules can be factored into TypeScript under `packages/api`; Mongo lookup/cache/physical translation belongs in `packages/data-schemas`. Keep legacy helper signatures for adjacent consumers until their migration is scoped. Do not introduce ObjectId-bearing exports, arbitrary query filters, a process-global map keyed only by message ID, or callback-based transactions in the portable contract.

## Executed evidence

[Protocol](protocol.md), [prototype](experiment.cjs), [attempt/command](attempt-01.json), [raw summary](output-01.log), [full traces](result-01.json).

| Check | Result | What it establishes |
|---|---|---|
| 12 cache/retention/initialized combinations + 16 edge cases | 28/28 matched | Same ordered mocked legacy calls/arguments, normalized result/error and final request/client state for the selected scenarios |
| Ordinary reference resolution | Zero added lookup calls across all 28 comparisons | The immediate returned-reference path need not perform a second physical-ID lookup |
| Reference reuse/fallback cases | 8/8 passed | Same-object fast path, copied reference, other binding, other owner/tenant, mutation, missing target and plain wire shape handled by the prototype |
| Always-lookup negative control | Detected | Oracle rejects an extra resolution read even if returned data looks equivalent |
| Unchecked-scope negative control | Detected | Oracle rejects reuse of another tenant's cached physical ID |
| Early-snapshot negative control | Detected | The detached snapshot changes the call sequence during initialized-state reset |

One attempt, exit 0. No skipped comparisons or failed setup attempts. Node v22.22.3 and TypeScript 5.9.3; compiler and source hashes are in the full result. Selected source functions and provider declarations were extracted/transpiled directly from the current worktree. No installed application dist, Mongo connection or private corpus was used. The 28 cases are not additions to the earlier 641-test suite count.

## Limits that must constrain the implementation assignment

1. **Real database and scope enforcement remain unproved here.** The stores and fallback lookup are doubles; synthetic IDs such as `c1` intentionally bypass database UUID validation. The prototype does not invoke real provenance CAS, schema casting, retention, project statistics, tenant middleware or Meili hooks. It checks the arguments delivered to those methods. Production must resolve trusted scope through the existing policy, including strict/unscoped/system behavior, before consulting a locator hint; a cache hit cannot bypass that policy. A scoped lookup must include the actual logical keys and owner/tenant constraints and validate its returned row.
2. **Reference lifetime and concurrent delete/recreate need a deliberate rule.** A weak association limits object retention; it does not prove freshness. If a row is deleted/recreated under the same logical key, an old cached locator and a fresh lookup could disagree. The old physical-ID handoff has related risks, but that does not justify promising value-equivalent live resolution without a proof. Before freezing this API, define the hint's bounded handoff lifetime/invalidation and test deletion, recreation, identity-changing saves and retries with real Mongo. If those rules require a lookup on every handoff, revisit the optimization rather than silently weakening reference semantics.
3. **This is not whole-workflow equivalence.** The candidate is a selective source transformation plus a tiny binding prototype, not an integrated adapter. Some reference and candidate policy code is shared intentionally to isolate link translation. The negative controls show useful sensitivity but do not replace independent review. No general concurrency schedule, seed race, wire round-trip of every DTO, garbage-collection behavior, latency, package dependency graph or typecheck was tested.
4. **DTO and failure mappings remain separate work.** The comparison deliberately normalizes away physical message `_id` and the prototype's added `ref` field. Other caller-observed values are compared; the test does not prove all consumers tolerate the proposed operation-result envelope. A successful record returned by the old method is not proof that this attempt applied every requested field. The final outcome schema must preserve that uncertainty.

## Next design work and disposition

D02 now has a concrete preferred Mongo implementation technique with a measured call-sequence comparison, replacing speculative receipt design as the next step. It remains open for the lifetime/scope conditions above and for complete DTO schemas. D03/D04 still own failure/patch mapping; D07 still requires pinned Node 24 and a built source baseline for application acceptance. D06 remains resolved by the Guildhall worktree. No source conversion, new implementation scope or reviewer assignment is implied.

The next bounded investigation should resolve the stale-reference scenario and catalog message/conversation fields against their runtime schema and read projections. Keep the active ordinary save/read pilot, the historical pagination finding and Project02 imports separate. No Lance schema research is needed to answer the immediate adapter question.
