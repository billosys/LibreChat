# Ordinary-turn read contract and conversion boundary

Working design from current source `3e3c5410d3863118fdba694fb0cd51baeb7102f9` (the preceding source change adds only Billo guidance). This supersedes the unfrozen read-route choice in the [first contract draft](../contract-design.md). It does not authorize application edits or claim completed DTO codecs.

## Named operations

| Operation | Inputs | Result and exact compatibility obligation |
|---|---|---|
| `readConversationForTurn` | Trusted owner context, conversation ID | Default-selected server conversation or null. Preserve fields/key presence used by retention, endpoint options and unset calculation. No new expiration filter or request-cache mutation in the adapter. |
| `readServerHistory` | Trusted owner context, conversation ID | Complete default-selected message array, existing createdAt-ascending order; no pagination, parent walk or summary truncation in storage. |
| `probeConversationAccess` | Trusted owner context, conversation ID | Owner, tenant identity and child-thread discriminator, or null. Delegate current owner/tenant/active-expiration filter; it is not a complete conversation and cannot populate the retention cache. |
| `readPublicMessages` | Trusted owner context, conversation ID; optional message ID | Array with the current public projection. Full reload returns all messages; by-ID stays an array, including an empty array. No generic filters, projection strings or arbitrary sort settings in this port. |

Context is supplied by server composition. Logical IDs remain opaque for reads; do not reuse new-write UUID validation to reject historical reads. The ordinary probe does not introduce an explicit tenant argument where current callers rely on ambient tenant policy. A future explicit service scope must preserve scoped/unscoped/system distinctions, not reinterpret missing tenant as system access.

The probe's legacy query selects `user tenantId subagentThread`; an implicit Mongo `_id` may also exist. The portable result omits the physical ID. Its child discriminator may be represented by explicit child status for admission only, but do not use that reduced record where lineage/navigation is required.

## Selected and retained caller paths

| Path | Pilot disposition | Preservation requirement |
|---|---|---|
| BaseClient ordinary `saveMessageToDatabase` and `loadHistory` | Convert | Preserve live post-await decisions and full server rows before the application parent/summary walk. |
| Conversation helper retention lookup and ordinary save; seed helper | Convert through injected operations | Preserve unread/known-null/known-undefined cache states, seed's empty-link intent and seed ordering. |
| `GET /api/messages/:conversationId` | Convert | Start scoped message read alongside admission when `shouldFetchMessages`; response remains admission-gated; wrap early rejection immediately. |
| `GET /api/messages/:conversationId/:messageId` | Convert | Middleware validates first, then scoped projected read. Preserve current array response and `200 []` for an empty result; do not introduce a single-record/404 change. |
| `messageValidation.js` dependency wiring | Convert the ownership-probe dependency | The factory is shared by reads and mutations. Preserve all method-specific policy, status/body mappings and job checks; mutation writers remain legacy. |
| `GET /api/messages/` query/search/pagination route | Retain legacy, all branches together | Single-message query, cursor pagination, Meili search and result hydration stay behind existing methods in this pilot. The known equal-time cursor defect remains separately scoped. |
| Message POST/PUT/artifact/branch/feedback routes | Retain legacy writes | Their sanitizers and mutation policy are not silently replaced by the read DTO. |
| Shared-link, subagent and event-actor specialized reads/writes | Retain legacy | Distinct projections, leases and admission semantics remain owned by their existing paths. |

This satisfies a bounded ordinary saved-and-reloaded turn; it does not make LibreChat Mongo-free. Arc02 still owns the remaining persistence families. The shared middleware dependency is a deliberate wider wiring effect, not authority to change mutation semantics.

Agent history needs special care: `AgentClient.onHistoryLoaded` captures the complete rows fetched by BaseClient before summary narrowing. `prepareRetainedAnswers` reuses those rows and only queries its own `RETAINED_ANSWER_ROW_FIELDS` when no stored rows were supplied and the branch is incomplete. Preserve that reuse. Its warm-event-actor fallback is an explicitly retained legacy path, not evidence that ordinary history may be truncated. See `api/server/controllers/agents/client.js:2271,2308–2320` and `packages/api/src/agents/hitl/answers.ts:377–454`.

## Admission and scheduling obligations

The actual middleware at `packages/api/src/middleware/messageValidation.ts` retains:

- `new` sentinel: 200 with an empty sent array, no ownership/message query.
- Conflicting supplied conversation IDs: 400 and no message query.
- Missing/expired or public child-thread conversation: 404. Foreign owner: 403 if such a record is returned by the dependency.
- Active-job exception only for GET/HEAD without a message ID; correct owner and tenant compatibility are required. Running jobs qualify; requires-action jobs qualify only while the pending action is live.
- Job lookup failure fails admission closed. Legacy jobs without tenant metadata remain readable by their owner under the existing policy.
- Public message reads do not themselves authorize response delivery. An early successful result cannot bypass admission; an early read error must not replace a later admission denial or become unhandled.

The [experiment](experiment.cjs) executes the actual middleware and full-reload callback. All 16 reference/candidate cases match, with explicit expected HTTP statuses. Two promise-controlled cases verify admission wins over early message success/failure. Wrong-owner and omitted-projection mutants are detected. Stores are doubles; projection enforcement, expiry, indexes and actual tenant middleware are not database-tested here. The by-ID active-job exclusion is exercised through the middleware predicate in the reload harness; the by-ID route itself is source-inspected, not executed in this packet.

## Field matrix and DTO rules

[field-matrix.json](field-matrix.json), generated by [field-matrix.cjs](field-matrix.cjs), joins all **44 message and 73 conversation schema fields** with direct interface types, provider Zod declarations, default selection, public projection and endpoint-unset rules. Every row has its source location and original definition. Implicit timestamps and Mongo metadata are accounted separately. This is the source-of-record mapping for the next DTO edit; it is not a claim that declared schemas describe every historical row.

The message projection has **24 exclusions**, including **12 nested exclusions**. Together with five default-hidden schema fields it leaves **29 explicitly declared top-level message fields** eligible for public reads, plus timestamp fields. `tenantId` is not currently excluded; do not silently remove it as part of compatibility work. `metadata` excludes thought signatures; content excludes background result claims/completion wakeups; attachments exclude selected web-search detail paths. Removing only top-level private keys is insufficient. Preserve array structure and permitted sibling properties when translating nested exclusions.

Use distinct DTOs for public messages, server history, turn conversation state, access probes and observed write outcomes. The public type is not `TMessage` wholesale, and the server type is not `IMessage extends Document`. Do not run persisted rows through the UI Zod schema as a generic decoder: it has defaults and fields used by optimistic/rendered state, and cannot preserve all server fields or original absence.

Resolved mismatches:

- `thinkingLevel` exists in the runtime preset and provider conversation schema. Preserve it in turn conversation state/options; the missing direct `IConversation` member is not a reason to drop it.
- `plugin`/`plugins` exist in the direct message interface but not the active schema or provider message shape. Do not invent new persistence fields for them. Any legacy-record compatibility requires read/migration evidence, not a TypeScript-interface inference.
- `createdAt`/`updatedAt` are schema-generated timestamps. Keep existing Date behavior at the initial local compatibility boundary and existing HTTP serialization; the future service codec is separately specified. This supersedes treating the first draft's RFC3339 transport preference as a required local representation now.
- `isShared`, optimistic tree/depth/queue metadata and other provider-only fields are not automatically stored attributes. The matrix lists them explicitly rather than silently merging UI and storage types.
- `_id`, `__v`, and conversation `messages` physical links stay adapter-private. The conversation helper's excluded-key set contains all three, so they are not needed to compute its unset-key intent. Keep any other required key presence, including nullable and undefined values; nested payloads still need deliberate codecs.

Default `select:false` is not a universal write-response sanitizer. Observed write outcomes must map explicitly to their server DTO; public HTTP mapping is a separate operation. Preserve current endpoint/provider payloads and provenance; do not flatten content or manufacture defaults.

## Validation-order decision

Pass 4's begin-time `resolveTenantScope` is **superseded**. The actual message method first rejects a missing owner and returns undefined for a missing/malformed conversation ID, before any model access. Under strict mode without tenant context, eager handle construction replaced those outcomes with a tenant error. Three source-executed preflight cases reproduce that mismatch, with zero model accesses.

For the Mongo compatibility handle, capture scope using non-enforcing `currentTenantScope`; compare scope/owner before each dispatch to prevent a handle crossing contexts. Let the existing methods/plugins perform strict enforcement at their existing query/write boundaries. This preserves early-return and error ordering and also preserves `saveConvo`'s own caught-error return behavior. Do not duplicate the UUID/auth validators in a second generic preflight layer.

This does not allow unscoped strict-mode queries: the binding still invokes the existing scoped methods, and their plugin uses `resolveTenantScope('Query')`, `resolveTenantScope('Save')`, etc. A changed-scope handle remains invalid use with its own explicit failure. Real method/plugin tests must prove this before implementation acceptance; this experiment only proves the early paths and does not establish strict query enforcement through an integrated adapter.

## Source and packaging boundary

Portable types and operation contracts belong under a new isolated data-schemas persistence entrypoint; Mongo binding imports the legacy methods through injected dependencies. Inspect both ESM/CJS outputs and declarations. Current data-schemas exports only root and capabilities, and `tsdown.config.mjs` lists two entries; adding a source barrel alone would not expose a usable subpath.

Application admission, parent walks, request cache and live client state stay in packages/api. The CJS route/client files remain wiring. Compose the adapter once with the methods created in `api/models/index.js`; converted logic must receive the port rather than importing a singleton internally. Existing legacy method exports remain for classified unconverted paths. Constructor/composition injection and declaration output still need the exact file-level assignment, not an implementer-selected fallback.

Implementation groups now have a fixed behavioral boundary: (1) contract/export and Mongo binding, (2) turn/seed/history orchestration and composition, (3) the two ordinary read routes and shared probe wiring, (4) conformance and source-build verification. This is a sizing input, not a frozen source allowlist or authorization to start Slice03.

## Remaining work, without reopening settled choices

The read-route choice and validation-order direction are now explicit. Remaining D02/D04 work is the concrete nested DTO/patch types and lossless compatibility policy for Mixed/historical values; the top-level census alone cannot settle those. Finish the injection/file fence and code/package declaration checks. D07 still requires Node 24.16.0 and rebuilt source validation: the available inspected executables were Node 22.22.3 and Homebrew Node 26.9.0, neither the pin. No dependency install or application build was performed. The one-contributor workflow and all existing acceptance gates remain in force.
