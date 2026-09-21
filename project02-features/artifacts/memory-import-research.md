# Memory-import research

| Field | Value |
|---|---|
| Project | `project02-features` |
| Capability | Arc01 — import existing memories through the LibreChat UI |
| Investigated | 2026-09-21 |
| Source checkout | `/Users/oubiwann/lab/billosys/LibreChat` on `main` |
| Source revision | `ba44443fdb232bbe6d4977e2619774b5a72586ac` |
| Current baseline cross-check | `0cc52cd8c71e8ccbceb8f001ddf8059b10501fce`; import/memory files below were unchanged since the inspected revision |
| Planning checkout | `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning` on `planning` |
| Evidence status | Static source/history inspection; attested research input, not independent runtime acceptance |
| Artifact status | Project-level research/design input; not an implementation prompt, slice close, or acceptance record |

## Question

Does the current LibreChat fork support importing persisted memories in the
same way it supports importing conversations, including support that might
exist in the backend but not be exposed in the UI? The immediate case is a
historic Claude `conversations.json` import whose conversations were imported
successfully but whose memories are not visible.

## Executive conclusion

The current codebase does **not** contain a bulk or file-based memory importer.
It contains a separate memory feature with list/create/update/delete APIs,
agent-memory tooling, and a side-panel UI, but no memory import route, no
memory import client mutation, and no memory file-upload control.

The Claude conversation importer recognizes Claude exports because conversation
items contain `chat_messages`, then imports only those messages into LibreChat
conversations. It does not inspect or persist any memory-like fields that might
also be present in a Claude export.

The existing supported migration path is therefore manual creation in the
Memories panel or an external migration script that submits one memory at a
time to `POST /api/memories`. That endpoint is not a bulk-import contract and
does not define repeat-import, source provenance, or partial-failure behavior.

## Evidence map

### 1. Conversation import is a distinct, exposed feature

The client import component selects one JSON file, wraps it in multipart form
data under `file`, and calls the conversation-upload mutation:

- [ImportConversations.tsx](/Users/oubiwann/lab/billosys/LibreChat/client/src/components/Nav/SettingsTabs/Data/ImportConversations.tsx:45-68)
- The Settings registry exposes that component as `importConversations` under
  the Data section:
  [registry.tsx](/Users/oubiwann/lab/billosys/LibreChat/client/src/components/Nav/Settings/registry.tsx:622-629)
- The backend endpoint is `POST /api/convos/import`; it receives the uploaded
  file and calls `importConversations`:
  [convos.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/routes/convos.js:752-790)

The conversation endpoint is also the only import endpoint represented by the
client data provider:

- [api-endpoints.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/api-endpoints.ts:147-161)
- [data-service.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/data-service.ts:855-863)

### 2. The import dispatcher supports conversation formats, not memories

`getImporter` dispatches among Claude, ChatGPT, Chatbot UI, and LibreChat
conversation formats. Array input is classified as Claude only when the first
conversation has `chat_messages`; otherwise it is treated as ChatGPT when it
has `mapping`. Unsupported shapes throw `Unsupported import type`:

- [importers.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/utils/import/importers.js:86-121)

There is no memory branch, memory file schema, memory importer, or call to the
memory model in this dispatch path.

### 3. Claude import persists messages and conversations only

`importClaudeConvo` loops through `conv.chat_messages`, converts each message
to a LibreChat message, saves the message through the import batch builder,
and finishes each conversation. The imported conversation receives a title,
timestamp, and default Anthropic model. No memory fields are read and no
`createMemory`/`setMemory` operation is invoked:

- [importers.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/utils/import/importers.js:193-284)
- The batch job reads JSON, selects the conversation importer, and deletes the
  temporary uploaded file after processing:
  [importConversations.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/utils/import/importConversations.js:9-47)

Therefore, even if a source export contains additional top-level memory-like
data, the current Claude importer does not preserve it.

### 4. Memories have CRUD support, but no import surface

The memory router currently defines these operations:

- `GET /api/memories` — list the authenticated user's memories
- `POST /api/memories` — create one `{ key, value, agentId? }` record
- `PATCH /api/memories/preferences` — toggle memory use
- `PATCH`/`DELETE /api/memories/:key` — update/delete by key
- `PATCH`/`DELETE /api/memories/id/:id` — update/delete by stored id

The complete route surface is visible in:

- [memories.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/routes/memories.js:132-180)
- [memories.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/routes/memories.js:264-317)
- [memories.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/routes/memories.js:412-434)

The create route accepts JSON with a single key/value pair, applies key/value
validation, content filtering, token counting, and the configured token limit.
It is not a multipart endpoint and accepts no array or import document:

- [memories.js](/Users/oubiwann/lab/billosys/LibreChat/api/server/routes/memories.js:174-260)

The client data provider mirrors this CRUD-only surface. It has
`getMemories`, `createMemory`, update, delete, and preference functions, but no
`importMemories` function:

- [data-service.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/data-service.ts:1553-1602)
- [api-endpoints.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/api-endpoints.ts:572-578)

### 5. The memory UI is separate from conversation import

The Memories side panel is registered as a Brain-icon side-panel entry. It
loads the memory list and offers a plus button that opens a manual create
dialog:

- [useSideNavLinks.ts](/Users/oubiwann/lab/billosys/LibreChat/client/src/hooks/Nav/useSideNavLinks.ts:169-187)
- [MemoryPanel.tsx](/Users/oubiwann/lab/billosys/LibreChat/client/src/components/SidePanel/Memories/MemoryPanel.tsx:149-186)
- [MemoryCreateDialog.tsx](/Users/oubiwann/lab/billosys/LibreChat/client/src/components/SidePanel/Memories/MemoryCreateDialog.tsx:84-98)

The create dialog submits one key/value pair through
`useCreateMemoryMutation`; it has no file input or import parser.

### 6. Permissions can explain a missing Memories panel

The side-panel entry requires both `MEMORIES.USE` and `MEMORIES.READ`:

- [useSideNavLinks.ts](/Users/oubiwann/lab/billosys/LibreChat/client/src/hooks/Nav/useSideNavLinks.ts:69-76)
- [useSideNavLinks.ts](/Users/oubiwann/lab/billosys/LibreChat/client/src/hooks/Nav/useSideNavLinks.ts:179-186)

The default administrator role grants memory permissions, while the default
regular-user role has an empty memory-permission object:

- [roles.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/roles.ts:145-162)
- [roles.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/roles.ts:225-236)

The Settings → Data memory toggle is separately gated by `MEMORIES.OPT_OUT`:

- [registry.tsx](/Users/oubiwann/lab/billosys/LibreChat/client/src/components/Nav/Settings/registry.tsx:593-601)
- [usePersonalizationAccess.ts](/Users/oubiwann/lab/billosys/LibreChat/client/src/hooks/usePersonalizationAccess.ts:1-15)

The interface configuration defaults `memories` to true, but that does not
replace the role/permission checks:

- [config.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/config.ts:2048-2064)
- [config.ts](/Users/oubiwann/lab/billosys/LibreChat/packages/data-provider/src/config.ts:2178-2186)

## Findings

| ID | Finding | Confidence | Consequence |
|---|---|---|---|
| MI-01 | No bulk/file memory importer exists in the current `main` source tree. | High — direct route, client, model, and importer inspection | A Claude JSON upload cannot populate memories through the existing conversation import path. |
| MI-02 | The Claude importer is message/conversation-only. | High — direct control-flow inspection | Any memory-like fields in the Claude export are silently outside this importer's handled scope. |
| MI-03 | Memory persistence is available through single-record CRUD and agent tools. | High — route, data-provider, model, and UI inspection | Manual creation works where the user's role has memory permissions. |
| MI-04 | The Memories panel can be hidden by permissions even though memory configuration defaults on. | High — client gate and role defaults | A regular user may see neither the panel nor the Settings memory control until an administrator grants the relevant permissions. |
| MI-05 | Project02 already names memory import as the planned Arc01 capability, but no arc/slice implementation plan exists yet. | High — planning checkout inspection | This research should inform Arc01 source-format and target-semantics design; it is not implementation evidence. |

## Search and history checks

The source tree was searched for memory/import combinations, memory upload/file
handlers, bulk-memory terminology, and memory import endpoint names while
excluding dependencies, generated client output, logs, and lockfiles. The
current Git refs were also checked for `importMemory`, `ImportMemory`, and
memory-import history. Those checks found memory CRUD, agent-memory behavior,
and unrelated in-memory infrastructure, but no memory importer.

The planning checkout contains the Project02 roadmap and ledger for memory
import. Its references to memory import are future capability planning, not
implemented source behavior.

## Practical migration options today

1. Grant the account the required memory permissions and create records through
   the Memories panel.
2. Build a separate migration utility that reads the source export, applies an
   explicit key/value mapping, and calls `POST /api/memories` once per record.
   The utility must define duplicate handling, repeat-import behavior, rejected
   records, source provenance, and optional `agentId` partitioning.
3. Do not treat direct MongoDB insertion as a supported importer contract. The
   API performs validation, content-policy checks, token counting, limits, and
   tenant/user scoping that a raw database write would need to reproduce.

## Arc01 design questions surfaced

Before implementation, Arc01 should decide and preserve evidence for:

- Which Claude/source memory formats are actually available, and whether the
  source contains memories separately from conversations.
- The target representation: allowed key grammar, value limits, summaries,
  token counts, agent partitions, and source IDs/provenance.
- Whether the UI accepts one source file, an export bundle, or a normalized
  intermediate format.
- Duplicate and repeat-import semantics, including rename/update behavior.
- Partial success behavior and how unsupported/malformed records are reported.
- Permission and tenant behavior for bulk import.
- Whether imported memories should be created through the existing CRUD
  service or through a dedicated validated batch service.

## Scope and evidence limits

- This was a static source and Git-history investigation against the clean
  `main` checkout at the inspected revision recorded above; the current
  fast-forwarded `main` baseline was then checked for changes to the
  import/memory files, and only an unrelated config file differed. No source
  files were changed.
- No live LibreChat server, browser session, database, or actual Claude export
  was used in this pass.
- The conclusion that the importer ignores extra source fields is based on its
  current control flow. It does not assert that every Claude export contains
  memories or that Claude's source format is stable.
- No tests were run because the request was to record research, not to modify
  or validate implementation behavior.
- This artifact is supporting research for Project02/Arc01. It must not be
  cited as independent acceptance of a future memory-import implementation.
