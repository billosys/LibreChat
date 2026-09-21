# Pilot dependency and lifecycle map

Source paths below are relative to LibreChat source commit `ba44443fdb232bbe6d4977e2619774b5a72586ac`. Line ranges describe inspected symbols, not a full audit of their surrounding large files. The [callsite inventory](callsite-candidates.json) and [all lexical references](symbol-references.json) are retained with their [query](inventory-command.json).

## Ordinary turn and reload

```text
BaseClient.sendMessage
  user-message admission / deferral / Stop
    optional seedTurnConversation -> getConvo -> saveConvo (append [])
    runAfterSeed orders deferred persistence after seed
  saveMessageToDatabase
    snapshot request/options; enforce client user when set
    optional retained-conversation lookup; construct authoritative write context
    saveMessage -----------------------> Message upsert / provenance CAS
    skipSaveConvo? return message
    saveTurnConversation
      reuse cached lookup OR getConvo
      endpoint patch + insert metadata + child-thread no-upsert rule
      saveConvo -----------------------> Conversation update/upsert
        append stored message ID OR rebuild references from Message query
        retention / immutable attribution / project ownership
        project statistics and retained-state backfills
  response persistence promise (may outlive client disposal)

server context reload: BaseClient.loadHistory
  getMessages(owner, conversation) -> walk logical parent IDs
  optional checkpoint summary boundary -> authorized attachment hydration

browser reload: GET /api/messages/:conversationId
  ownership/retention/child-thread validation --------+
  owner-scoped getMessages(CLIENT_MESSAGE_SELECT) ----+ -> gated response

query read: GET /api/messages?conversationId=...
  same ownership probe + public single-message or cursor read
```

There is no transaction spanning message and conversation writes. A seed may precede a deferred message; ordinary message persistence otherwise precedes conversation persistence. A successful message write does not prove conversation metadata/project-stat maintenance succeeded.

## Concrete edges

| Source symbol / extent | Responsibility and edge |
|---|---|
| `api/app/clients/BaseClient.js:54, 912–1003` | Module-level `db = require('~/models')`, not an injected class store today. Deferred persistence has pending/started/cancelled states; admission rejection cancels it; Stop starts the parent write. Seed errors settle; user-save rejection is logged and converted to `{}`. |
| `BaseClient.js:1238–1253, 1332–1415` | Optional terminal-ownership hook can prevent response persistence. `saveMessageToDatabase` snapshots options before awaiting; disposed-before-call returns `{}`; saved message's `_id` is passed to turn helper; missing `_id` leaves the rebuild fallback. `updateMessageInDatabase` is an adjacent operation, outside the proposed first conversion. |
| `packages/api/src/conversations/save.ts:1–229` | Fully inspected. Request property **presence** distinguishes unread from cached-null. Retention precedence is bound event context, loaded conversation, then request body. `initialized` means an earlier existing row was observed, not simply successful insertion. Unsets depend on excluded endpoint keys. Insert creation time is parsed and ignored if invalid. Subagent binding sets `noUpsert`. |
| `api/models/index.js:1–26`; `api/db/index.js:1–15`; `methods/index.ts:314–346` | Wiring constructs methods with Mongoose and cache helpers; model registration occurs before index-sync import. Conversation methods receive message methods and adjacent deletion hooks. Deletion/queue/trigger hooks are not executed by the ordinary save and remain separate compatibility operations. |
| `packages/data-schemas/src/methods/message.ts:848–1056` | User required before write; UUID-shaped conversation ID required; owner overridden from context. Main upsert keyed by logical message ID + owner, with tenant added by plugin. Retention from context; `contextMeta: null` clears atomically. NaN token count becomes zero. Returns plain object containing storage `_id`, or null/undefined in distinct cases; most errors throw. Duplicate-key recovery can return the existing row without proving the attempted fields won. |
| `message.ts:17–108, 196–374` | Normalizes/deduplicates provenance, preserves unknown versus explicit flags, captures steer paths; caps whole paths at 256 and promotes whole-message provenance on overflow. Exact-field paths have their own bound. Compare-and-set merge retries eight times, then throws. This is data policy plus concurrency behavior, not a generic CRUD detail. |
| `methods/conversation.ts:525–539, 567–576, 2148–2557` | `getConvo` reads by owner + logical ID. `saveConvo` needs injected message methods; absent append option rebuilds message references, present empty skips the read, nonempty uses set-union append. Protects initial agent, code-environment decision, actor checkpoint fields; checks project ownership. Retention/code-decision backfills and project-stat updates may occur after the main write. A missing no-upsert match returns null. Caught exceptions return `{message: 'Error saving conversation'}`. |
| `methods/chatProject.ts:187–332` | Owner-scoped visibility predicate; refresh reads project stats, conversation count/latest and compare-and-sets the snapshot; can exhaust retries and throw. Incremental pointer update rechecks visibility afterward. Failure can therefore follow a committed conversation update. |
| `BaseClient.js:1256–1324, 1437–1508`; `message.ts:2397–2421` | Full owner/conversation query, default createdAt ascending without a tie-breaker. Logical-ID map walks parent chain with a visited-set guard, reverses it, optionally cuts at a summary. Root sentinel skips DB. This is server context assembly, distinct from display projection. |
| `api/server/routes/messages.js:93–217, 492–519`; `api/server/middleware/messageValidation.js:1–16` | Public read starts scoped message query and ownership probe concurrently, but releases data only after validation. Middleware's injected method named `getConvo` is actually **getConvoOwnership**, an important alias that lexical call-name counts alone miss. |
| `methods/conversation.ts:2060–2081`; `message.ts:456–482, 3583–3619` | Ownership probe hides expired conversations before TTL cleanup and identifies child threads. Public projection strips `_id`, user, contextMeta, trace routing and private task fields. Cursor method uses a strict bound on only the selected sort field, with no identity tie-breaker. Equal-value page completeness needs characterization. |

## Storage bindings and side effects

`models/message.ts` and `models/convo.ts` register tenant isolation, optionally register mongoMeili only when host/key exist, and reuse existing models. `schema/message.ts:310–362` and `schema/convo.ts:392–432` declare expiry TTL and compound identity indexes; uniqueness is `(logical ID, user, tenantId)`, not globally unique logical ID. Mongoose supplies casting, schema strictness, defaults, timestamps, and private `select:false` behavior. These responsibilities cannot disappear when removing Mongoose from a future backend.

`tenant/policy.ts` and `models/plugins/tenantIsolation.ts` were read completely. AsyncLocalStorage determines scoped/system/unscoped context. Strict mode rejects missing scope; non-strict absence deliberately retains legacy unscoped behavior. Query hooks inject tenant predicates; update guards reject reassignment and strip protected fields; sanitized empty updates cannot upsert. The policy uses plain types but still accepts Mongo-style operators; do not publish that mutation shape as the new portable API.

`utils/tenantBulkWrite.ts` is a separate path because model bulk writes bypass ordinary query middleware. It strips caller tenant updates and stamps operation filters/documents, including distinct system-scope behavior. Keeping the query plugin alone is insufficient for import compatibility.

`utils/tempChatRetention.ts` defines precedence, hours bounds, general/temporary policy and clock-derived expiration. `utils/retention.ts` defines expiry/visibility predicates. Retention is more than a TTL index: reads must hide expired records while Mongo's asynchronous cleanup has not run.

`models/plugins/mongoMeili.ts:1132–1170, 1237–1293` adds write-version metadata and detached indexing after `findOneAndUpdate`, unwrapping result metadata for conversation saves. It rereads the latest row and handles indexing failure separately. Those selected hooks were inspected, not the entire search engine integration. The baseline did not run an external Meili service; no indexing-availability guarantee is inferred from passing persistence tests.

## Import boundary

`api/server/utils/import/importers.js:202–279` builds the Claude operational view: fresh IDs, extracted text/thinking, skipped unrendered content, linear parents, monotonic timestamp adjustment, and configured model label. The source comment about tree ordering is not a fidelity requirement: executed `convoStructure.spec.ts` reconstructs parent graphs despite scrambled timestamps.

`importBatchBuilder.js:176–245` validates size/content, then invokes conversation bulk write, message bulk write preserving timestamps, and tag updates through `packages/api/src/conversations/import.ts`. Failure cleanup is compensating deletion, not a multi-collection transaction. `ImportBatchBuilder.saveMessage` is an in-memory builder method, **not** the data-schemas `saveMessage`. The importer must not be counted as an ordinary-save consumer merely because the names coincide.

`methods/message.ts:1061–1104` and `methods/conversation.ts:2623–2747` are the bulk paths. They normalize provenance, apply tenant-safe bulk writes, preserve/import selected timestamps, protect server-owned conversation fields, and refresh project stats. Source IDs/parents/blocks are already transformed before these methods see them. The [completed corpus reconciliation](../../../corpus-reconciliation.md) remains the source-preservation evidence; no private corpus was reread for this slice.

## Caller coverage and first-conversion boundary

The reproducible lexical scan found **305 reference lines in 60 files; 155 call-like candidate lines in 43 files** across production `api`, `packages/api/src`, and `packages/data-schemas/src`. Candidates include declarations and builder namesakes, so **155 is not a count of distinct runtime database calls**. References passed as dependencies are retained in the larger inventory; arbitrary computed property access and renamed aliases are not a complete whole-program proof. The ownership alias above was resolved by following wiring.

The classified table below accounts for every candidate file. Only the ordinary turn, seed helper, server-history read and selected public reload wiring are proposed first-conversion consumers. The other classes remain explicit compatibility callers of current methods. Narrow wrapper insertion must not globally replace `createMethods` or change methods shared by these callers.

| Candidate file | Lines | Classification |
|---|---|---|
| `api/app/clients/BaseClient.js` | 923, 932, 1263, 1349, 1352, 1368 | Pilot ordinary turn/history/seed |
| `api/server/controllers/agents/errors.js` | 132 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/controllers/agents/openai.js` | 458 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/controllers/agents/request.js` | 129, 425, 433, 458, 479, 530, 1726, 1899, 2703, 2729, 2940, 2959 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/controllers/agents/responses.js` | 326, 375, 426, 456, 700, 1755, 1768 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/controllers/agents/resume.js` | 255, 312, 517, 561, 1005, 1316 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/controllers/assistants/chatV1.js` | 257, 387 | Assistants/thread synchronization compatibility |
| `api/server/controllers/assistants/chatV2.js` | 264 | Assistants/thread synchronization compatibility |
| `api/server/controllers/assistants/errors.js` | 183 | Assistants/thread synchronization compatibility |
| `api/server/middleware/abortMiddleware.js` | 81, 93 | Authorization/abort/denial/error boundary; validate ownership alias separately |
| `api/server/middleware/abortRun.js` | 15 | Authorization/abort/denial/error boundary; validate ownership alias separately |
| `api/server/middleware/denyRequest.js` | 45 | Authorization/abort/denial/error boundary; validate ownership alias separately |
| `api/server/middleware/error.js` | 50, 69, 70 | Authorization/abort/denial/error boundary; validate ownership alias separately |
| `api/server/routes/agents/index.js` | 831, 842 | Adjacent API generation, recovery, error and agent controller compatibility |
| `api/server/routes/convos.js` | 214, 610, 712 | Conversation metadata/read compatibility |
| `api/server/routes/messages.js` | 71, 118, 177, 362, 453, 497, 540, 554, 568, 586 | Pilot reload candidate; edit/branch/delete/search remain compatibility paths |
| `api/server/services/Endpoints/agents/initialize.js` | 229 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `api/server/services/Endpoints/agents/title.js` | 161 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `api/server/services/Endpoints/assistants/title.js` | 77, 104 | Endpoint setup/title persistence compatibility |
| `api/server/services/Threads/manage.js` | 99, 100, 142, 161, 256, 363, 486 | Assistants/thread synchronization compatibility |
| `api/server/utils/import/fork.js` | 37, 73, 74, 132, 133, 463, 464, 495, 500, 528, 529 | Import/fork compatibility; builder saveMessage is an in-memory namesake |
| `api/server/utils/import/importBatchBuilder.js` | 126, 143, 222, 223, 254 | Import/fork compatibility; builder saveMessage is an in-memory namesake |
| `api/server/utils/import/importers.js` | 265, 535 | Import/fork compatibility; builder saveMessage is an in-memory namesake |
| `packages/api/src/agents/backgroundCompletionWakeup.ts` | 296, 304 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/control.ts` | 212 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/guard.ts` | 105, 135, 212 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/hitl/answers.ts` | 382 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/hitl/inspection.ts` | 294 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/hitl/protection.ts` | 1047 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/queuedTurnHttp.ts` | 172 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/queuedTurns.ts` | 507, 549 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/subagentActivity.ts` | 352 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/subagentCompletionWakeup.ts` | 275, 290, 409, 627, 628, 629, 675, 721 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/subagentThreads.ts` | 1540, 1568, 1569, 2199, 2756, 2757, 2857, 2920, 2981, 3007, 3106, 3152, 3221, 3258, 3259, 3316, 3360 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/triggers/bindingResolver.ts` | 82, 140 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/agents/triggers/bindings.ts` | 254, 305 | Background/subagent/queued turn/trigger/HITL lifecycle compatibility |
| `packages/api/src/conversations/save.ts` | 135, 146, 171, 185, 196 | Pilot ordinary turn/history/seed |
| `packages/api/src/files/retention.ts` | 139, 254 | File retention compatibility; some injected getConvo ports use projected alternatives |
| `packages/api/src/langfuse/session.ts` | 37 | Trace/session lookup compatibility |
| `packages/api/src/middleware/messageValidation.ts` | 147 | Authorization/abort/denial/error boundary; validate ownership alias separately |
| `packages/api/src/utils/message.ts` | 127 | Message identity helper compatibility |
| `packages/data-schemas/src/methods/conversation.ts` | 261, 294, 319, 567, 2148, 2203, 2623, 3101, 3166 | Storage implementations/declarations/internal calls, not external consumers |
| `packages/data-schemas/src/methods/message.ts` | 630, 703, 791, 848, 1061, 2397 | Storage implementations/declarations/internal calls, not external consumers |

This is a complete trace of the bounded path at the named symbols, with a lexical inventory and classification of adjacent callers. It is not a semantic audit of every agent, scheduler, import format, search route, or arbitrary model access in the repository.

### Passed references and renamed aliases

The remaining 17 reference-only files are accounted for as follows (they are not additional named callsite hits):

- `api/server/controllers/agents/client.js`, `api/server/services/Endpoints/agents/addedConvo.js`, and `packages/api/src/agents/initialize.ts` supply history/file context. The latter assigns `getThreadMessages = db.getMessages` at 1477 and invokes it at 1498; this is an actual renamed caller outside the literal call-name count. Its reduced file-provisioning query is not a model for the pilot's owner-scoped public read.
- `api/server/middleware/messageValidation.js` supplies **getConvoOwnership as getConvo**. `middleware/validate/subagentThreadTurn.js`, `routes/agents/openai.js` and `services/Endpoints/agents/subagentThreadStore.js` pass real store methods into subagent/API guards and lifecycle services.
- `api/server/routes/code-environments.js:24` supplies **getConvo as conversations.get** to the TS code-environment handlers. This compatibility consumer is outside the ordinary pilot.
- `api/server/routes/admin/langfuse.js`, `packages/api/src/admin/langfuse.ts`, `api/server/routes/share.js` and `packages/api/src/shared-links/session.ts` forward message reads to trace/session resolution. The share route also provides a locally implemented projected `Conversation.findOne` under the name getConvo (115–122): that is not a call to the same data-schemas method.
- `api/server/services/Files/retention.js:9` supplies getConvoRetention with getConvo as fallback, another reason to trace injected semantics rather than names alone.
- `packages/data-schemas/src/methods/index.ts` is the method factory wiring described above. `packages/api/src/schedules/fire.ts`, `schedules/types.ts` and `packages/data-schemas/src/models/plugins/mongoMeili.ts` contain documentation references, not direct named operation calls in the scan.

Every file in the final lexical inventory is thus classified. Dynamic dispatch and arbitrary model access remain outside this bounded inventory's completeness claim.
