# Field, patch and write-outcome mapping — current pilot

Source: Guildhall `fe79265b2f47937051625719f3ba5080189912c1`. This refines the [historical contract draft](../contract-design.md); it is not a complete executable DTO schema. The [census](field-census.json) carries exact field definitions and source lines. The current handle and observations are described in the [decision](decision.md).

## Inventory boundaries

| Surface | Declared schema fields | Direct interface members | Observed differences |
|---|---:|---:|---|
| Message | 44 | 48 | Interface-only `plugin`, `plugins`, `createdAt`, `updatedAt` |
| Conversation, expanded preset | 73 | 75 | Schema-only `thinkingLevel`; interface-only `isShared`, `createdAt`, `updatedAt`; schema overrides preset `agent_id` and `tags` |

This is a top-level AST inventory. It excludes inherited Mongoose Document members, implicit `_id`/`__v`, plugin-added paths and runtime casting. Nested definitions are retained as source text, not recursively certified as a portable codec. Timestamps are enabled by both schemas; their absence from direct schema keys is explained. `IConversation` documents `isShared` as request-derived. Message plugin fields and conversation `thinkingLevel` still require consumer reconciliation before choosing their contract status.

Named projections must differ. The schemas mark these fields `select:false`:

- Message: `_meiliIndex`, `subagentTranscript`, `subagentActivityProjection`, `subagentTriggerProjection`, `subagentTask`.
- Conversation: `initial_agent_id`, `subagentThreadLease`, `agentEventBinding`, `agentEventActor`, `agentEventActorCleanup`, `agentEventActorReconciliations`, `agentEventActorEpoch`, `agentEventActorLegacyTurn`, `agentEventActorSuspension`.

That declaration is evidence about query selection, not permission to serialize a returned write object. A newly written record, an explicit projection and a default query can expose different fields. Do not implement the public DTO with `{ _id, ...rest }`, or use the full persistence interface as the browser message type.

Keep the existing logical message ID scoped by owner/tenant; conversation membership is a relationship. Preserve source/import identities separately. Physical message linkage is private to the handle. `chatProjectId` is currently an ObjectId-shaped public string: preserving its existing string value is different from exposing a Mongoose ObjectId instance. Its access check and project-statistics side effects remain in the adapter.

## Concrete compatibility rules

| Input/state | Current source behavior to preserve | Portable boundary consequence |
|---|---|---|
| `resolvedConversation` property absent | Retention/helper may perform a read | Use an explicit unread state, not null-coalescing all states |
| Property present with `null` | Known absent; helper does not reread | Keep distinct from unread |
| Property present with `undefined` | Own-property test marks cache known; load helper yields null | Preserve locally; a future JSON codec cannot convey this with omission alone |
| Cached conversation object | Supplies retention and unset-key decisions | Preserve the required fields and key presence; not just the display summary |
| `contextMeta` omitted | Message update preserves stored value | No inferred clear |
| `contextMeta:null` | `saveMessage` builds an unset | Translate to a field-specific clear intent; null is not a universal delete operator |
| `contextMeta` populated | Existing message update/validation applies | Preserve nested policy; do not broaden acceptance |
| Endpoint option absent/undefined | Helper may unset an existing non-excluded key | Retain its actual key enumeration and excluded/kept-field rules |
| Endpoint option null, false, zero, empty string/list | Not `undefined`, so helper does not mark it unset for that reason | Keep these states distinct; runtime casting/validators still apply |
| `endpointOptions.conversationId` non-null | Overrides conversation update target | Do not silently require equality with the saved message's conversation ID |
| Observed message locator | Append that observed row | Handle-owned; no current-row lookup fallback |
| Saved result absent or locator absent | Omit append metadata; old conversation method reconciles messages by query | Preserve this branch; missing result is not an empty append set |
| Seed's explicit empty append set | No append/reconciliation query from this metadata branch | Seed stays separate from message handoff |
| Retention fields in message/conversation payload | Ordinary methods remove payload fields and apply write-context retention rules | Scope and retention are trusted context, not generic patch fields |
| Initial agent, code environment/workspaces, actor checkpoint fields | Existing conversation method protects, seeds or strips these through specialized rules | Generic set/clear cannot override those ownership rules |
| Truthy invalid/unowned `chatProjectId` | Existing method removes update value and requests unset | Preserve ownership query and resulting clear; no invented public ObjectId type |
| Message provenance paths | Existing normalization, bounded merging and CAS path | Do not replace with ordinary array assignment |
| `newMessageId` / `newConversationId` | Existing identity-changing paths remain | No new rename/move capability in the ordinary pilot; classify callers before restricting accepted fields |

Anchors: `packages/api/src/conversations/save.ts` (cache, unset, retention and seed orchestration); `packages/data-schemas/src/methods/message.ts:848–1060` (auth/ID checks, contextMeta, provenance, duplicate recovery); `packages/data-schemas/src/methods/conversation.ts:2187–2558` (link intent, protected fields, project membership, secondary writes).

The initial local boundary may preserve Date values for compatibility; this packet does not claim they are JSON strings or choose a future Rust timestamp codec. Expiry nullability and nested dates must be captured explicitly when that codec is specified. Schema Mixed fields need an observed-value/consumer census before promising lossless JSON transport.

## Outcome and partial-commit rules

Keep “observed a row” separate from “this attempt applied every requested change.” In particular, duplicate recovery can return a pre-existing message without applying the desired update. A portable result must not call that proven applied/successful mutation merely because it contains a record.

| Stage and legacy outcome | Knowledge available at the boundary | Continuation/compatibility rule |
|---|---|---|
| Pre-write owner mismatch or disposed client | Current application rejected/skipped before save | Preserve existing thrown error or `{}` result; no handle/store dispatch |
| Retention read throws | Message method not dispatched | Propagate current error; no writes initiated by this invocation |
| Message method returns a record | A row was observed; full requested mutation not proved | Retain locator privately; expose typed observed data; continue unless live skip flag says otherwise |
| Message method returns undefined | No row returned; invalid conversation ID or duplicate-recovery absence/error are possible | Do not invent one cause or claim no commit; preserve later reconciliation behavior |
| Message method throws | Could include a failure after an earlier write in the method | Propagate; no conversation stage; no automatic retry or rollback claim |
| Post-message helper read throws | Message may already be persisted; conversation method not dispatched | Propagate; release handle; preserve partial outcome |
| Conversation method returns a row | It observed a row and completed its method path | Update request cache and return normal conversation; handle terminal |
| Conversation method returns null | No row returned by its update/read path | Preserve null, especially no-upsert; do not turn into error or create a row |
| Conversation method returns `{message:'Error saving conversation'}` | Caught failure, possibly after main write/retention/project-statistics work | Preserve distinguishable error outcome; do not report rollback or untouched state |
| Conversation dependency throws | Earlier message may remain; conversation effect uncertain | Propagate current thrown behavior; no hidden retry |
| Seed catches failure | Existing helper logs and settles | Preserve swallowing and subsequent seed-ordering contract |

Suggested result vocabulary for eventual types is `observed`, `notReturned`, and `legacyFailure`, with commit knowledge separately `unknown` unless a specific pre-dispatch guard proves no write was dispatched. These are semantic dispositions, not a requirement to change existing caller return shapes in the same edit. First introduce the envelope behind an application compatibility mapper and test the mapper against all consumers. A raw exception is not by itself proof of “nothing happened.”

## Remaining concrete work

Reconcile the 117 schema fields, direct interfaces, provider/browser types, named read projections and ordinary write callers before freezing allowlists. Explicitly resolve `thinkingLevel`, message plugin fields, inherited/implicit fields, nested Mixed values and dates. Preserve the server/private versus public distinction and cache key-presence requirements. Then define typed mutations, errors and exact source file fence; run pinned-runtime source builds and real-adapter conformance before implementation acceptance. The inventory and these source-derived mappings do not close those obligations.
