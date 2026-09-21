# Ordinary-turn persistence contract — design pass 1

Status: **working design, not a frozen API or implementation assignment**. This document develops Slice01's D01–D09 decisions. Recommendations below are the sole contributor's proposals. “Observed” refers to the pinned LibreChat source or retained experiment; it does not mean behavior has been implemented through the new interface.

Inputs: [dependency map](../../slice01-behavior-baseline/artifacts/dependency-map.md), [behavior matrix](../../slice01-behavior-baseline/artifacts/behavior-matrix.md), [decision and source-preservation inputs](../../slice01-behavior-baseline/artifacts/design-inputs.md). Source is `ba44443fdb232bbe6d4977e2619774b5a72586ac`. Existing tests passed 641/641 across 12 suites; those test existing code, not this contract. The bounded cursor experiment below uses installed dist under Node 22, not a rebuilt Node 24 baseline.

## 1. What belongs in this boundary

The boundary expresses owned conversations and messages, the intent of a turn write, and the outcomes the application can actually observe. It should be usable by a local Mongo adapter now and a service client later. It must not expose Mongoose documents, physical row identities, query operators, or callbacks whose behavior depends on sharing an address space.

```text
BaseClient / ordinary message read handlers
        | trusted request normalization + existing admission/cache rules
        v
Application turn orchestration (packages/api)
        | plain domain operations
        v
Portable contracts (isolated data-schemas export)
        |                            |
Mongo compatibility adapter     future service client
        |                            |
existing methods + hooks        Rust service -> SQLite

Unconverted writers -> existing methods (explicit compatibility paths)
```

**Correction to the initial proposal:** `BaseClient` imports the `~/models` singleton (`api/app/clients/BaseClient.js:54`). The `saveTurnConversation` helper accepts injected dependencies (`packages/api/src/conversations/save.ts`), but this does not mean the BaseClient path already has an injected portable store. Conversion must introduce and test the supplied port at the client boundary. Its test should fail if a converted consumer still accesses that singleton.

**Preferred pilot read scope (D01):** include BaseClient's server-history read, ordinary full-conversation reload, the conversation ownership/expiry probe used to authorize that reload, and the ordinary message-by-ID read. Account for the query route separately: its single-message branch and paginated branch currently share dispatch with search. Preserve existing query behavior via compatibility wiring until its precise inclusion and cursor change are settled. This is a proposed fence, not permission to leave the ordinary reload half-converted. The arc still owes one complete saved-and-reloaded turn.

The active-job exception to normal read admission, request caches, endpoint switching, seed ordering, Stop/disposal and terminal ownership are application rules. The adapter cannot infer authorization by seeing a record, and it must not consult the generation manager. Trusted tenancy, owner filtering, persistence-specific retention, provenance merge and schema effects remain enforced by the binding and existing methods.

## 2. Context, values and identity (D02/D04)

Use server-derived operation context. The proposed context carries actor/user identity, a tagged tenant scope (`tenant` with ID, or explicitly authorized legacy-unscoped mode), and separately issued system authority where the existing policy permits it. User JSON cannot select system authority. Do not change legacy tenant fallback into unconditional rejection during adapter introduction; first reproduce its policy matrix. Authenticated actor and record owner are distinct concepts even when ordinary saves require equality.

Identifiers are opaque strings in a named entity namespace and scope. Preserve the current logical `messageId`, `conversationId`, and parent/root markers exactly. A UUID-looking ID is not permission to regenerate it; an ObjectId-shaped public string is not automatically a physical row ID. Validation remains operation-specific: accepting historical reads need not imply accepting every string in a new-write operation. The current invalid-conversation-ID save behavior must remain visible in the compatibility mapping.

Proposed operational timestamps are UTC RFC 3339 strings with explicit millisecond precision. A Node compatibility facade converts to/from the Dates expected by existing consumers. Test actual Dates, null, absence and invalid values rather than relying on JSON serialization to define semantics. The future source archive preserves original timestamp strings and precision separately; it must not normalize away submilliseconds to fit operational DTOs.

Runtime payloads must be finite, plain structured data with explicit optional fields. Do not blindly serialize `IMessage extends Document` or coerce ObjectIds with `String(...)`. Date-bearing nested trace and claim fields need deliberate conversion even when they are private. Encoding undefined, nonfinite numbers, binary values and unknown structured content is a field-policy decision, not a generic stringify fallback.

### Message relationship translation — consequential choice still open

Observed: `BaseClient.saveMessageToDatabase` passes `savedMessage._id` into `saveTurnConversation`; the latter supplies `appendMessageIds` to `saveConvo`. The physical ID crosses application code to avoid re-reading all messages. Missing append metadata rebuilds links from a query; `[]` deliberately performs no link query; populated values append by set union.

| Alternative | Useful property | Unresolved cost or risk | Disposition |
|---|---|---|---|
| Logical message reference; adapter looks up its physical ID | Plain and portable; straightforward remote representation | Adds a serial read per ordinary message unless combined or optimized; duplicate recovery must still use the actual persisted row | Baseline correctness option; not accepted as a latency regression |
| Opaque adapter-issued link receipt plus logical reference | Can retain current append path without exposing `_id` | Receipt must bind adapter/version, tenant, owner, conversation and logical ID; define forgery/replay, lifecycle, serialization and retry behavior; it must never grant authorization | Investigate next; not frozen as a public type |
| One named save-message-and-update-conversation operation | Keeps physical link entirely inside binding; allows logical wire input | Must preserve separate writes, retention pre-read, cached-null behavior, endpoint decisions and partial outcomes without moving all application policy into the adapter | Viable alternative if its input can be resolved without changing query order |
| Rename `_id` to a generic string, public transaction callback, or process-global receipt cache | Small apparent edit | Leaks storage identity, couples address spaces, or creates hidden state/lifetime and memory-retention problems | Reject |

Current preference is to keep logical identity authoritative and any optimization wholly owned by the binding. A type-branded token alone is not a security contract. Before selecting a receipt, write success, wrong-scope, stale, replay and cross-binding examples and count serial reads. If that proves more complex than a named operation, choose the named operation explicitly. No implementer should have to invent this decision.

## 3. Operation inventory and observations

These are semantic operation names; exact signatures await the DTO and link decision. They are not a generic repository API.

| Operation | Input | Outcome / obligation | Source seam |
|---|---|---|---|
| `readConversationForTurn` | Trusted context + logical conversation ID | Server-only row or absent; retention/endpoint fields available; no automatic cache mutation | `getConvo`; BaseClient retention lookup and `save.ts` load/seed |
| `saveTurnMessage` | Context + message field intents + trusted retention/provenance input | Persisted/observed record or explicit skipped/failure mapping; relationship translation resolved within binding | `saveMessage`; BaseClient ordinary user/response saves |
| `writeTurnConversation` | Context, endpoint/config intents, insert permission, protected insert values, link intent | Row, no-upsert absence, or uncertain failure; preserve secondary effects | `saveConvo`; `saveTurnConversation` / seed |
| `readServerHistory` | Context + logical conversation ID | Internal DTOs with required summaries/private history data; existing order preserved | `getMessages`; BaseClient `loadHistory` |
| `probeConversationAccess` | Context + logical conversation ID | Minimal ownership/expiry/child classification; application decides active-job exception | `getConvoOwnership`; message validation |
| `readPublicMessages` | Context + logical conversation ID, optionally logical message ID | Public DTOs only, independent of server history shape; response is released only after admission | `getMessages` with `CLIENT_MESSAGE_SELECT`; ordinary reload and by-ID route |

Full-history reads are currently unpaginated. Preserve that for the pilot; switching them to pagination alters history assembly and is not an adapter refactor. Do not offer arbitrary `filter`, `sortField`, projection strings or SQL/Mongo fragments in these operations. A future pagination capability uses named order modes and a versioned cursor, with its own compatibility transition.

Existing seed behavior must remain: cached null is different from unread, an existing conversation is not seeded again, a seed uses an explicitly empty link intent, failure is logged and swallowed, and the subsequent write waits for the in-flight seed. These are orchestration tests as well as adapter tests.

## 4. Field policy and patch semantics

This is a **field-family census**, not yet a complete executable schema. Source anchors are `packages/data-schemas/src/types/message.ts`, `schema/message.ts`, `types/convo.ts`, `methods/message.ts`, `methods/conversation.ts`, and the exact client projection. The next pass must reconcile declared type, runtime schema, write filters, read projections and actual caller use field by field; their agreement cannot be assumed.

| Family | Examples that must be accounted for | Boundary policy |
|---|---|---|
| Identity/ownership | message/conversation/parent IDs, user, tenant | Context controls scope; scoped references preserve logical IDs; physical `_id`/`__v` never exported |
| Display/content | sender, text, content, model, endpoint, iconURL, files, attachments, plugin/plugins, thread_id, quotes | Preserve supported values and ordered blocks; use explicit validators per declared DTO, not a lossy text-only conversion |
| Message state | isCreatedByUser, unfinished, error, finish_reason, isTemporary, addedConvo | Keep existing defaults and BaseClient's forced unfinished=false; do not accept payload authority over retention |
| Provenance | isUserSubmitted, userSubmittedPaths, exact userSubmittedMessageFieldPaths | Preserve existing merge/CAS behavior and bounded path validation; no replacement by last-write-wins |
| Server history | summary, summaryTokenCount, tokenCount, contextMeta | Available to named server DTOs; field-specific null/omission rules and numeric handling |
| Trace/coordination | conversationSignature, clientId, invocationId, langfuse fields, subagent transcript/activity/task/trigger fields | Classify private fields and nested dates; preserve stored data when ordinary writes omit them; adjacent specialized writers remain legacy |
| UI/audit metadata | feedback, metadata, manualSkills, alwaysAppliedSkills | Preserve historical applied-skill values and existing nested field rules; audit content is not regenerated from present configuration |
| Lifecycle/internal | expiredAt, createdAt, updatedAt, _meiliIndex | Explicit temporal semantics; search bookkeeping is adapter-owned; expiry is distinct from physical deletion |
| Conversation policy | endpoint options, initial_agent_id, code/actor metadata, project relation, message membership | Protected fields and insert-only values cannot be overwritten through a general patch; project statistics remain a documented secondary effect |

Use omission for “leave unchanged” in wire objects; null is a value only where the field permits it. For clearable fields, prefer explicit typed mutation intent rather than assuming null has one universal meaning. The Node compatibility adapter translates the legacy cases, particularly `contextMeta: null` meaning unset, while omission means preserve. Empty string/list/object and zero stay distinct from null and absence. A set and clear on the same field must be invalid before mutation.

Link intent needs three distinct states: `reconcile` (legacy omitted append metadata), `none` (legacy empty append list), and `append` (specific saved references). Naming these states prevents an empty array from accidentally triggering a full message query. A missing field in an already validated public request must have one documented default, not be reinterpreted differently by each adapter.

Request cache is also three-state: unread, loaded-absent, loaded-present. It is application state, not a persisted field or a backend cache. `initialized` currently reflects the prior existing row, not simply that the latest write returned something; tests must preserve that distinction. Do not serialize a whole Express request into a storage operation.

## 5. Failure, commit knowledge and retry (D03)

The adapter must report only what the wrapped methods reveal. Returning a record after duplicate-key recovery does not establish that this attempt's requested content was written. Returning a generic conversation error object does not establish rollback. In particular, project/statistics or backfill work can fail after the conversation row was written.

Prefer operation-specific outcomes with separate **observed record** and **commit knowledge**. A useful vocabulary is `not-attempted`, `write-acknowledged`, and `unknown`; absence is a read/result state, not synonymous with failure. The existing thin adapter cannot always distinguish “newly saved” from “recovered existing.” Either conservatively report `observed` with uncertain application of the requested update, or instrument the underlying result seam in an explicitly reviewed change. Never manufacture a precise `recovered` status from a record's shape.

| Trigger | Current observable behavior | Compatibility requirement / proposed portable representation |
|---|---|---|
| Client disposed before save | `{}`; no write | Remain an orchestration skip; do not send a backend operation |
| Client user mismatch | Throws before write | Preserve rejection before mutation; actor cannot be overwritten by payload |
| Invalid conversation ID on message save | Message result may be undefined | Explicit skipped/invalid classification where knowable; preserve whether conversation path is subsequently attempted |
| Message write rejects | Later conversation update is not reached | Return/throw through facade as before; no claimed rollback of any uncertain database attempt |
| Message returns a record after duplicate-key recovery | Existing record available; requested new fields may not be applied | Do not attest update completion or blindly retry side effects; link the returned persisted identity |
| `skipSaveConvo` | Message-only result | Conversation `not-attempted`, not absent or failed |
| Conversation `noUpsert` misses | Null conversation | Message may already exist; distinguish no-upsert absence from error |
| Conversation error object | Message can already be durable; conversation durability uncertain | Preserve existing caller-visible error shape via facade; portable status cannot promise not-committed |
| Failure in post-conversation secondary work | Generic error may conceal a committed row | Unknown conversation/secondary completion unless explicitly instrumented; real state-inspection fault test required |
| Seed failure | Logged; seed settles without rejection | Preserve application sequencing; no automatic rollback or retry added |

No automatic retry policy is introduced by this pilot. Logical-ID upsert alone is not end-to-end idempotency: provenance merging, timestamps, conversation linkage, project statistics and hooks may have different replay effects. The eventual RPC version needs a scoped idempotency key, request fingerprint, durable outcome/replay rules, expiry and response-loss handling before writes cross a process boundary. A timeout cannot mean “did not commit.” These transport requirements belong to Arc03; the current contract must leave room for them without inventing a durable receipt service now.

## 6. Cursor finding and disposition (D05)

The [predeclared experiment](pagination-protocol.md) and [retained result](pagination-result.json) confirm the suspected defect in the installed message method. The unique-time control returned 6/6 with no duplicates. The tied-time case returned 4/6 with two missing IDs, no duplicates, and a null final cursor. Both fixtures stored all six rows. Exact tied IDs returned are not a stable ordering promise.

The defect follows from sorting on `createdAt` alone and advancing with a strict inequality on that value. This experiment uses whole-second timestamps; it does not characterize subsecond precision, descending order, concurrent mutation or authorization. Its successful harness exit means the planned defect reproduction matched, not that completeness passed.

**Recommendation:** preserve legacy behavior in any compatibility path converted during the adapter pilot, and track a separate reviewed pagination correction. Do not silently repair it while claiming Mongo-equivalent behavior. A new portable paginated capability should instead require a stable total order `(timestamp, logical tie key)` and an opaque cursor bound to version/order/filters/scope. Choose the logical tie key and ordering/migration behavior before implementation; replacing `_id` order with messageId order is a semantic change, not an automatic equivalence. A cursor is not authorization, and all its encoded fields must be revalidated against trusted context.

## 7. Source identity and archival obligations (D09 and A05)

Operational DTOs do not become the canonical representation of imported history. Keep separate source records, operational projections and derivation mappings. Suggested future source reference: namespace/account + entity kind + native ID, with export fingerprint, ingestion batch and revision/derivation version stored separately. Identical and overlapping exports need explicit dedup/revision semantics; none is implemented here.

All material obligations from the [full source-preservation table](../../slice01-behavior-baseline/artifacts/design-inputs.md#source-preservation-obligations) remain load-bearing:

- Account for all 9,838 source messages, including the 107 omitted from the 9,731-message operational import; 66 skipped messages carry file/attachment metadata.
- Preserve original IDs, parents and branching independently of display order; the existing import changed 95 retained parent links across 55 conversations, with 52 source branch points in 47 conversations.
- Preserve ordered tool-use (8,609), tool-result (8,532), token-budget (2,388) and thinking blocks (329 flattened into 140 messages), including unknown fields and explicit projection rules.
- Retain attachment/file metadata and availability separately from recoverable bytes (287/583 message populations overlap); byte presence has not been established by these counts.
- Preserve the 446 source summaries, original creation/update representations, 819 distinct conversation update times, 161 retained message update differences and 9,719 creation timestamps with submillisecond precision.
- Distinguish the configured import model label from unknown historical model evidence. Preserve access-controlled original artifacts outside Git and sanitized fixtures in tests.
- Reconstruct operational relationships from message rows, not the empty embedded arrays found on all 820 conversations. A SQLite copy of current Mongo cannot restore omitted source content.

Arc01 owns the semantic design; later intake/migration work owns implementation, repeat-ingest/recovery and full-population verification. Claude must be reconciled in SQLite before GPT intake. Concept IDs, world assertions, episodic memories, procedures and cognitive traces remain separate future domain contracts; no Mongo ID, SQLite rowid, Lance offset or graph index becomes their universal identity.

## 8. Discriminating conformance design

Each row below describes a future executable oracle, not an executed test. Use a real adapter database for durability/isolation effects and focused spies for dependency/query-order assertions. Keep the existing 641-test baseline distinct from these new cases.

| Case | Fixture/action | Required observation; incorrect behavior rejected |
|---|---|---|
| C01 Supplied port | Ordinary user+response save and reload; old singleton made unusable for converted calls | Saved text/IDs/parents reload; no singleton access; fails a cosmetic wrapper |
| C02 Scope collisions | Same logical IDs for two users in two tenants plus forged payload owner/tenant | Only authorized scoped records read/changed; independently exercise legacy-unscoped policy |
| C03 Presence | Existing nonempty contextMeta; omit, clear, empty-value and zero variants | Omit preserves, explicit clear physically unsets, allowed empties/zero survive; protected fields untouched |
| C04 Link intent | Existing messages then reconcile/none/append; duplicate append and foreign-scope reference | Correct set membership and exact read counts; none performs no rebuild; cross-scope reference cannot link |
| C05 Cache and seed | Unread/null/present cache; delayed seed; dispose before and during await | Required lookup counts and order; no accidental second write or rejected seed; options snapshot preserved |
| C06 No-upsert | Missing bound conversation after valid message write | Null/absent conversation without insert; message state accounted separately |
| C07 Recovery/provenance | Duplicate logical save, conflicting update and bounded CAS exhaustion | One scoped row; intended provenance preserved where acknowledged; no false claim new content saved on recovery |
| C08 Failure stages | Inject message failure, conversation failure, post-row statistics failure | Inspect stored rows; facade outcome matches baseline; no false all-or-nothing outcome |
| C09 Retention | Trusted temporary deadline and spoofed payload; expired row before TTL deletion | Bound deadline preserved; ordinary public read denied per policy before physical delete |
| C10 Projection | Private trace/context/summary fields and nested sensitive fields present | Server history keeps required data; public response exactly excludes protected fields, including nested projections |
| C11 History | Branching parents, summary and scrambled timestamps | Existing parent walk/context assembly preserved; no promise that chronological order repairs topology |
| C12 Legacy cursor | The two retained six-row fixtures | Characterization remains 6/6 and 4/6 if legacy path is preserved; a reviewed corrected capability instead requires 6/6 for both |
| C13 Source fixture | Branching, skipped ancestor, tools, multiple thinking blocks, exact source time, overlapping second export | Archive/projection/mapping accounted independently; belongs to intake implementation, not pilot source scope |
| C14 Dependency/encoding | Import contract entrypoint without model registration; plain DTO round trip including nested dates | No Mongoose/ObjectId/query/Node-side-effect dependency in public contracts; no dropped supported values |

Node 24.16.0 source-build reproduction and applicable type/static/performance checks remain prerequisites for implementation acceptance. The isolated characterization is not a latency measurement. Query-count preservation is necessary but insufficient to establish no performance regression.

## 9. Modules, code fence and remaining work

Proposed contract and Mongo-binding ownership stays in `packages/data-schemas`, with a new isolated export rather than the package's model/implementation-bearing root. Application orchestration remains in `packages/api`; `/api` does composition and CJS compatibility. Browser models remain in `packages/data-provider`. Verify the actual transitive dependency graph and CJS/ESM declaration exports when concrete files are chosen.

Candidate changed consumers remain `BaseClient.js`, `save.ts`, `api/models/index.js`, `messageValidation.js` and explicitly selected ordinary read branches of `routes/messages.js`. Adjacent import, scheduler, trigger, subagent and search writers retain existing methods. This is still a **candidate fence**, not an implementation allowlist. If relationship translation requires modifying shared method results or moving compound orchestration, revisit Slice03 sizing before assignment.

| Decision | Current disposition | Next concrete action / owner |
|---|---|---|
| D01 Read scope | Ordinary reload/server history/ownership/by-ID preferred; query pagination compatibility boundary not frozen | Design owner: mark exact route branches and injection paths after link choice |
| D02 IDs/DTOs/link | Logical identity, plain values and three link intents preferred; receipt versus named compound operation unresolved | Design owner: compare both complete sequences and field-level runtime schemas before signatures |
| D03 Failure | Conservative commit knowledge and legacy facade proposed | Design owner: enumerate caller reactions and determine whether any method instrumentation is necessary |
| D04 Context/patch | Server authority, three cache states and per-field mutation policy proposed | Design owner: finish schema/write/projection census; no generic patch escape hatch |
| D05 Cursor | Reproduced in disposable real Mongo; separate-fix recommendation | Keep legacy behavior explicit; obtain reviewed scope before corrective source work |
| D06 Branch | Required `dev` lineage unresolved | Operator/design owner before source branching; does not block this design |
| D07 Runtime/build | Node 22 installed-dist evidence only | Future implementation author/reviewer: pinned Node 24 and rebuilt package evidence |
| D08 Acceptance | Slice01 attested; Slice02 active; one contributor unchanged | Formal review remains pending; no fabricated reviewer or new handoff |
| D09 Service | SQLite selected; Rust single writer remains architecture proposal | Later arc freezes transport/idempotency/lifecycle; no premature protocol dependency |

The next design pass should settle D02 first because it controls operation boundaries, failure observation and the caller fence. Then complete D03/D04's per-field and per-stage mappings and make D01 exact. This draft is useful preparation, but these consequential choices prevent an honest implementation-ready claim today.
