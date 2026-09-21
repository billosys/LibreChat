# Skills, prompts, agents, and Claude project import research

## Research record

| Field | Value |
| --- | --- |
| Project | `project02-features` |
| Capability | Skills, prompts, agents, and Claude project/history import |
| Investigated | 2026-09-21 |
| LibreChat source | `/Users/oubiwann/lab/billosys/LibreChat`, `main`, `86c5884c0f6c` |
| Planning checkout | `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning` |
| Evidence | Static source inspection plus official documentation; no live server or user export archive was available |
| Status | Research/design input; not an implementation or acceptance record |

This research follows `memory-import-research.md`. It describes the current upstream-shaped LibreChat checkout, not the proposed DB-agnostic fork. “No CLI” means that the checked-in application does not provide a dedicated command for the operation; authenticated HTTP automation or a new wrapper can still be built.

## Executive findings

| Resource | Current UI support | File/directory link | Programmatic support | Dedicated CLI/import command |
| --- | --- | --- | --- | --- |
| Skills | Upload `.md`, `.zip`, or `.skill`; create/edit/share according to permissions | Deployment directory via `DEPLOYMENT_SKILLS_DIR` and optional GitHub Skill Sync; these are read-only in the UI | Browser API `POST /api/skills/import`; Agent/Skill Management API and skill sync | None found |
| Prompts | Create, edit, group, and share prompt groups | None found | JSON REST CRUD under `/api/prompts` | None found |
| Agents | Build, edit, duplicate, share, and use marketplace/catalog agents | None for agent definitions; agent resource files can be uploaded | Browser API and Agent Management API under `/api/agents/v1/agents` | None found |
| Chat projects | Create projects and move conversations between them | Not relevant | Project CRUD plus conversation assignment under `/api/projects` | None found |
| Claude conversations | Upload `conversations.json` from Settings → Data Controls | Importer reads conversations, not Claude project organization | `POST /api/convos/import` | None found |

The user’s missing Skills menu is not evidence that Skills import is absent. The current UI has an upload action, but the panel and upload action are capability/role gated. Prompts and agent definitions do not have equivalent file-import or directory-link workflows. All three resources can be automated through authenticated APIs, but LibreChat does not ship a resource-import CLI.

The current Claude importer explains the flat result. It recognizes an array whose items contain `chat_messages`, creates one LibreChat conversation per item, and carries over the title, message text, sender, timestamps, and Claude thinking content. It passes an empty metadata object to the conversation builder, so no source project identifier is retained. The project API is a separate feature and is never invoked by the import route. LibreChat therefore does not create projects or assign imported conversations to projects during Claude import.

Project recovery is conditional. If the original Claude export still contains a project identifier/name mapping (in `conversations.json` or another export file), a custom importer can recreate projects and assign conversations. If the archive has no such membership data and only the flat LibreChat rows remain, exact recovery is not possible from those rows; only heuristics or manual curation remain. Claude’s public export article documents that exports include conversation and user data, but does not publish a stable personal-export JSON schema, so the actual archive must be inspected before deciding that organization was lost at the source.

## Skills

### Browser upload

The server accepts a multipart upload at `POST /api/skills/import`. The upload validator permits `.md`, `.zip`, and `.skill` files and applies a default 50 MB limit. The route is guarded by the skill-create permission. The client’s Create Skill menu has “Write skill instructions” and “Upload a skill” actions, with `UploadSkillDialog` handling the upload.

Relevant source:

- `api/server/routes/skills.js` (upload validation and `/import` route)
- `client/src/components/Skills/buttons/CreateSkillMenu.tsx` (UI actions)
- `packages/data-provider/src/data-service.ts` (`importSkill`)
- `packages/data-provider/src/api-endpoints.ts` (`/api/skills/import`)

This explains two common observations:

1. A user without the Skills capability/use permission may not see the Skills panel at all.
2. Seeing Skills does not imply upload is allowed; upload requires create permission.

The official [Skills documentation](https://www.librechat.ai/docs/features/skills) describes the same upload formats and permission behavior.

### Directory and GitHub sources

LibreChat can initialize deployment skills from a filesystem directory. `DEPLOYMENT_SKILLS_DIR` defaults to `skill`; relative paths are resolved from the project root. Deployment skills are read-only in the application UI. The same docs show a GitHub Skill Sync configuration with repository sources, paths, a ref, an interval, and an optional token. Synced skills are also read-only from the UI.

Relevant source/config:

- `packages/api/src/skills/deployment.ts` (`DEPLOYMENT_SKILLS_DIR` and startup load)
- `packages/api/src/skills/sync` and `api/server/services/Skills/sync.js` (GitHub sync)
- `packages/data-provider/src/config.ts` (skill-sync configuration)
- `librechat.example.yaml` (configuration surface)

This is a genuine “point LibreChat at a skill source” path, but it is deployment/synchronization, not a general-purpose writable import directory. The sync documentation is at [Skill Sync configuration](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/skill_sync).

### API automation

The browser route is sufficient for an authenticated automation script. LibreChat also documents a machine-oriented Agent/Skill Management API. The management documentation is in `docs/skills-management-api.md`; the public overview is in [Agent Management API](https://www.librechat.ai/docs/features/agents_api). There is no checked-in command such as `librechat import skills`; the root `package.json` scripts cover server, user-admin, migration, build, and test operations but no resource importer.

## Prompts

Prompts are stored as prompt groups and prompt records. The UI supports manual creation and sharing through the prompt dialog and permission model. The server exposes JSON endpoints to create a group with an initial prompt, add prompts to a group, update groups/prompts, list, and delete.

Relevant source:

- `api/server/routes/prompts.js` (`POST /api/prompts`, group prompt routes, update/list/delete)
- `client/src/components/Prompts/buttons/CreatePromptButton.tsx` (manual-create UI)
- `packages/data-provider/src/data-service.ts` (prompt CRUD)
- `packages/data-provider/src/api-endpoints.ts` (prompt endpoints)

There is no multipart prompt-import endpoint, prompt directory setting, filesystem watcher, or prompt bundle import/export route in the checked-in code. The `prompts: use/create/share/public` configuration controls permissions; it does not configure a prompt source directory. The `config/translations/prompts` tree contains internal translation-generation prompts, not a user prompt-library import mechanism.

Consequently, prompts are linkable through LibreChat’s own groups and sharing ACLs, and they are scriptable through authenticated JSON REST calls, but they are not importable from a directory and have no dedicated CLI.

## Agents

The browser API supports agent creation, listing, reading, updating, duplication, version/revert, deletion, and avatar/resource-file operations. The management API exposes the same machine-oriented lifecycle under `/api/agents/v1/agents`, plus attached-file management. An attached file is an agent resource; it is not an agent-definition package or a link to an agent directory.

Relevant source:

- `api/server/routes/agents/v1.js` (browser agent lifecycle)
- `api/server/routes/agents/management.js` (management API and file routes)
- `packages/data-provider/src/data-service.ts` (agent CRUD/duplicate calls)
- `docs/skills-management-api.md` and the [Agent Management API docs](https://www.librechat.ai/docs/features/agents_api)

The current UI has an Agent Builder and duplicate/edit flows, and marketplace/catalog discovery can expose agents already available to the instance. I found no route named import/export for agent definitions, no agent-directory configuration, and no root CLI command. An automation tool can still POST a JSON agent definition and upload its files through the management API, subject to authentication and permissions.

## Claude conversation and project import

### What LibreChat currently imports

LibreChat’s importer dispatches Claude only when the uploaded JSON is an array whose first item has a `chat_messages` array. `importClaudeConvo` then:

- starts one LibreChat conversation per Claude item;
- converts each Claude message into a LibreChat message with generated IDs;
- preserves message text, user/assistant sender, timestamps, Anthropic endpoint, and thinking content;
- uses `conv.name` as the title; and
- calls `finishConversation(..., {}, defaultModel)` with an empty source-conversation object.

`finishConversation` copies fields from that source object into the stored conversation. Since the Claude path passes `{}`, no `chatProjectId` or other source grouping metadata can reach the stored record.

Relevant source:

- `api/server/utils/import/importers.js` (`getImporter` and `importClaudeConvo`)
- `api/server/utils/import/importBatchBuilder.js` (`finishConversation`)
- `api/server/routes/convos.js` (`POST /api/convos/import`)

The official [LibreChat conversation import guide](https://github.com/LibreChat-AI/librechat.ai/blob/main/content/docs/features/import_convos.mdx) documents ChatGPT, Claude, and ChatbotUI conversation import and tells users to select Claude’s `conversations.json`. It does not document project recreation or project membership mapping.

### What LibreChat projects currently contain

The current `ChatProject` schema contains a name, description, owner, timestamps, tenant, and derived conversation statistics. It does not contain Claude project instructions, knowledge files, source project IDs, or an import provenance field. Project handlers expose:

```text
POST /api/projects
PUT  /api/projects/conversations/:conversationId
GET/PATCH/DELETE /api/projects/:projectId
```

The create body is `{ name, description }`; the assignment body is `{ projectId }` (or `null` to remove membership). Relevant source:

- `packages/data-schemas/src/schema/chatProject.ts`
- `packages/data-schemas/src/types/chatProject.ts`
- `packages/api/src/projects/handlers.ts`
- `api/server/routes/projects.js`
- `packages/data-provider/src/data-service.ts` (project CRUD and assignment)

This means a custom migration can create a LibreChat project after import and assign each imported conversation, but the stock Claude import flow does not do so. It also means a Claude project’s instructions/files require an explicit mapping decision: LibreChat’s current project model is primarily a name/description plus conversation membership, not a full Claude-project knowledge workspace.

### Is the lost organization recoverable?

Use this decision tree before rerunning or deleting anything:

1. **The original Claude export ZIP is available.** Preserve a copy and inspect every file, not only `conversations.json`. Check each conversation object for fields such as `project_uuid`, `projectId`, `project_id`, or an embedded project object, and look for a separate project metadata/membership file. If a stable conversation-to-project mapping exists, exact membership is recoverable with a custom importer even though LibreChat currently ignores it.
2. **The ZIP contains conversations but no project membership or project metadata.** Exact organization is not recoverable from that export alone. Title/content/date heuristics can propose groups, but they cannot prove the original project boundaries.
3. **Only the flat LibreChat import remains.** The stock importer generated new conversation IDs and did not persist source project metadata, so the source grouping cannot be reconstructed exactly from LibreChat’s imported records.

The public [Claude export article](https://support.claude.com/en/articles/9450526-export-your-claude-data) confirms that exports include conversation and user data and are requested from Settings → Privacy, but it does not define a guaranteed JSON schema for personal exports. Claude’s [project documentation](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) confirms that projects, project instructions/knowledge, and project membership are first-class product concepts. Neither source proves that every personal export version includes a project-membership field, so archive inspection is required.

A quick, read-only first pass against a preserved ZIP is:

```sh
unzip -l claude-export.zip
unzip -p claude-export.zip conversations.json | jq 'type, (.[0] | keys)'
unzip -p claude-export.zip conversations.json \
  | jq -r '.[] | [.uuid, .project_uuid, .projectId, .project_id] | @tsv' \
  | head -20
```

Field names vary by export generation; a missing result is evidence only for that archive, not a universal statement about Claude exports.

## Implications for the fork

The import surfaces are not symmetrical. Skills already have three source modes (upload, deployment directory, GitHub sync), while prompts, agents, and projects are database/API resources with no source-package contract. A DB-agnostic fork should avoid treating each current route as the long-term contract. A shared intermediate import model would make future adapters possible:

```text
source system + source resource ID
resource kind (skill | prompt | agent | project | conversation)
display metadata and content
relationships (project membership, prompt group, agent resources)
source timestamps and provenance
attachments/files
```

For Claude migration specifically, the next implementation slice should be a read-only archive analyzer before changing the importer. It should produce a manifest of files, top-level JSON keys, candidate project identifiers, conversation IDs, and unmapped records. The importer can then create a deterministic source-ID map, create LibreChat projects, import conversations, and assign memberships through the project API. It should report missing project metadata rather than silently flattening it. Instructions, knowledge files, and other Claude project resources need a separate mapping policy because they have no direct fields in the current LibreChat `ChatProject` schema.

## Evidence limits and follow-up

- This is static inspection of the checked-in source and official documentation; no LibreChat instance was started and no real Claude archive was supplied.
- The “no CLI” conclusion is based on the root package scripts and repository routes searched here. A third-party wrapper or locally maintained script may exist outside this checkout.
- The decisive next evidence is the user’s original Claude export archive. Preserve it before any re-export, and run the read-only inventory before importing again.
- No implementation, tests, or database migration were performed in this research pass.
