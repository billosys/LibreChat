# LibreChat persistence reconnaissance

Inspected 2026-09-20 at source commit `ba44443fdb232bbe6d4977e2619774b5a72586ac`. This is bounded source reconnaissance, not an exhaustive audit or a runtime compatibility result.

## Baseline and authority

The source checkout is `/Users/oubiwann/lab/billosys/LibreChat`, on `main`, with origin `git@github.com:billosys/LibreChat.git`. HEAD subject: `📒 ci: Upload Per-Test Jest Results From Review Workflows (#16110)`. No tracked changes were present at intake. Only `main`, `origin/main`, and `origin/HEAD` appeared in the branch inventory; this does not prove that a remote branch cannot exist outside the local tracking inventory.

Read the root [AGENTS.md](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/AGENTS.md) and [CLAUDE.md](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/CLAUDE.md). They direct database contracts into data-schemas, new backend behavior into packages/api, dependency injection, plain public types, and implementation branching/PRs against `dev`. They also require affected typechecks and tests, plus Lighthouse for specified startup/auth/config/file/message-loading changes. These are implementation obligations; no such source changes were made in this planning pass.

The Operator separately authorized the standard orphan planning branch/worktree. Its initial layout is recorded in the planning root `AGENTS.md`. No source implementation branch was created.

The existing [FerretDB investigation](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/misc/ferretdb/ferretdb-multitenancy-plan.md) is a reference document. Its preference against Mongo and its Docker-oriented setup do not override the current request to retain Mongo first or the native-local preference. Its reported model/index counts and benchmark numbers were not reproduced and are not used as current measurements here.

## Observed integration points

| Evidence at pinned source | Observation | Design implication (inference) |
|---|---|---|
| [api/models/index.js:6](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/api/models/index.js#L6) | Constructs `createMethods(mongoose, deps)` and exports methods plus seeding | A useful composition seam already exists |
| [api/db/index.js:9](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/api/db/index.js#L9) | Registers models before loading index synchronization; source explains ordering dependence | Factory substitution must include startup ordering |
| [api/db/connect.js:43](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/api/db/connect.js#L43) | Mongo connection entrypoint, with URI requirement and cached connection state | Selecting another backend must remove this startup requirement on that path |
| [api/server/index.js:196](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/api/server/index.js#L196) | Connects DB, starts reconciliation/index work, and later seeds under system context | A model-only migration is insufficient |
| [methods/index.ts:291](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/methods/index.ts#L291) | Aggregate factory connects conversation methods to message methods and queued/trigger workflows | Migrate dependency-connected operations rather than arbitrary collections |
| [methods/message.ts:791](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/methods/message.ts#L791) | Public methods include Mongo query filters, selections, and engine-specific result shapes | Existing signatures need translation; a factory is not yet a portable contract |
| [methods/message.ts:848](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/methods/message.ts#L848) | Save path validates identity, derives retention from context, treats null context metadata as clearing, and merges provenance | Generic JSON replacement would risk changing semantics |
| [methods/conversation.ts:280](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/methods/conversation.ts#L280) | `appendMessageIds` uses `Types.ObjectId[]` | Relationship references need a private storage translation |
| [methods/conversation.ts:2187](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/methods/conversation.ts#L2187) | Save uses append IDs when supplied; otherwise reads message IDs; protects selected insertion metadata | Preserve semantics and the existing avoided-read optimization |
| [conversations/save.ts:6](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/api/src/conversations/save.ts#L6) | Injected conversation store derives its types from those Mongo-oriented methods | Consumer isolation must include transitive type exposure |
| [BaseClient.js:1332](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/api/app/clients/BaseClient.js#L1332) | Ordinary save path saves a message then updates conversation state using saved `_id` | Candidate first application conversion; partial failure needs characterization |
| [schema/message.ts:310](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/schema/message.ts#L310) | TTL, scoped unique identity, and ordering indexes | Schema effects must become contract/adapter obligations |
| [models/message.ts](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/models/message.ts) | Applies tenant isolation and conditional Meili integration | Raw writes that bypass plugins can lose behavior |
| [tenant/policy.ts:14](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/tenant/policy.ts#L14) | Scoped/system/unscoped policy; strict mode opt-in; Mongo-shaped update inputs | Preserve policy and tests, but do not export operator-shaped updates as the new API |
| [tenant/conformance.ts](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/tenant/conformance.ts) | Existing engine harness and common tenant conformance suite | Extend an existing portable test seam; do not mistake tenant coverage for all-domain coverage |
| [utils/transactions.ts](https://github.com/billosys/LibreChat/blob/ba44443fdb232bbe6d4977e2619774b5a72586ac/packages/data-schemas/src/utils/transactions.ts) | Probes actual Mongo transaction support and retries after materializing a probe collection | Avoid assuming all supported Mongo deployments provide identical transaction capabilities |

## Reproducible lexical inventory

A read-only lookup agent enumerated tracked blobs at the pinned commit; CDC inspected the script, representative matches, and key source paths. This is delegated reconnaissance, not independent acceptance of a change.

Scope: `api/`, `packages/api/src/`, `packages/data-schemas/src/`, `packages/data-provider/src/`, `client/src/`. Selected 2,820 code files with extensions `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`, `.mts`, `.cts`. Excluded dependency/build/generated/test directories and test/spec/Jest filename patterns as encoded in the retained script.

| Root | Files importing/requiring mongoose | Files importing/requiring mongodb | Distinct union |
|---|---:|---:|---:|
| api | 23 | 1 | 24 |
| packages/api/src | 62 | 3 | 64 |
| packages/data-schemas/src | 182 | 4 | 183 |
| packages/data-provider/src | 0 | 0 | 0 |
| client/src | 0 | 0 | 0 |
| Total | 267 | 8 | 271 |

Counts include static `import type`; they are not all runtime dependencies. The line-based regular expression is:

```text
\b(?:from\s+|require\s*\(\s*|import\s+)["'](mongoose|mongodb)["']
```

Separate inline `import('mongoose')` references occur in 3 api files, 8 packages/api files, and 95 data-schemas files. Inline `import('mongodb')` occurs in 4 data-schemas files. These populations overlap; do not add them to the table. `api/typedefs.js` is an example of JSDoc-only references.

Raw lookup outputs are preserved under [research-inventory/](research-inventory/): `inventory.py`, `static_or_require.txt`, `inline_import_reference.txt`, and `factories.txt`. The script pins both commit and source checkout path and writes its output into `/tmp/guildhall-librechat-inventory`; ensure that output directory exists before rerunning:

```bash
mkdir -p /tmp/guildhall-librechat-inventory
python3 research-inventory/inventory.py
```

Run from this project directory. The retained script uses `git ls-tree` and `git show` against the stated baseline, not the current working files. Factory declaration listings were captured separately with `rg` in the clean source checkout:

```bash
rg -n '^export function create.*(Model|Methods)\(' \
  packages/data-schemas/src/models packages/data-schemas/src/methods \
  -g '*.ts' -g '!*.spec.ts' -g '!*.test.ts'
```

The registered model map contains 47 entries. The declaration scan finds 45 domain method factories plus aggregate `createMethods`; `createMCPAuthorizationFenceRetryStorage` is an additional storage factory outside that naming pattern. Representative bypass surfaces include `packages/api/src/cache/keyvMongo.ts`, `packages/api/src/agents/checkpoints/saver.ts`, and `packages/api/src/conversations/import.ts`. These are follow-up inventory targets, not fully analyzed subsystems.

Limitations: lexical matching excludes transitive imports, computed identifiers, package subpaths, and multiline syntax split across lines. Zero direct frontend matches does not prove that every shared type is storage-neutral. No exhaustive caller graph or semantic method census has been completed. The large message/conversation modules were read in relevant bounded sections, not exhaustively audited.

## Existing tests to build on

Real Mongo setup was observed in the following test sources. None was executed in this planning pass, and setup does not imply every individual test case is unmocked.

| Purpose | Source test paths |
|---|---|
| Ordinary conversations/messages | `packages/data-schemas/src/methods/conversation.spec.ts`, `convoStructure.spec.ts`, `message.spec.ts`, `message.traces.spec.ts` |
| Conversation save orchestration | `packages/api/src/conversations/save.spec.ts` |
| Deletion, access, import | `api/server/routes/__tests__/messages-delete.spec.js`, `api/server/middleware/validate/convoAccess.spec.js`, `api/server/utils/import/importConversations.database.spec.js` |
| Portable tenant reference | `packages/data-schemas/src/tenant/conformance.mongoose.spec.ts` |
| Tenant plugin, probes, bulk writes, index migration | `packages/data-schemas/src/models/plugins/tenantIsolation.spec.ts`, `packages/data-schemas/src/tenant/probe.spec.ts`, `packages/data-schemas/src/utils/tenantBulkWrite.spec.ts`, `packages/data-schemas/src/migrations/tenantIndexes.spec.ts` |

The first slice needs discriminating tests for its exact contract, not a new suite that merely repeats implementation structure. Extend existing real-database cases where they already express the behavior; introduce a shared adapter harness where it can enforce the same domain outcome for two implementations.

## What this pass establishes

It establishes a source-grounded starting seam, concrete examples of engine leakage and hidden persistence semantics, an explicit research scope, and a proposed backend direction. It does not establish runtime compatibility, performance, migration safety, complete boundary coverage, or readiness to issue an implementation prompt. Those remain open in the project ledger.

## Follow-up: initial Claude corpus, 2026-09-20

The Operator requested historical Claude data as the first dataset, fully brought into SQLite before an OpenAI/GPT import. A bounded inspection of the existing importer found these concrete behaviors at the same source baseline:

- `api/server/utils/import/importers.js:173`: `extractClaudeContent` collects text and thinking blocks, with a text fallback. This function does not preserve arbitrary content blocks.
- `api/server/utils/import/importers.js:202`: `importClaudeConvo` assigns fresh UUIDs, links each retained message to the previous one, skips messages with no extracted text/thinking, and advances non-increasing timestamps by one millisecond. It assigns a configured/default model. Therefore source identity, topology, time, and model provenance require explicit mapping if fidelity is the goal; do not mistake these transformed fields for preserved source metadata.
- `api/server/utils/import/importConversations.js`: the import job reads a JSON file and unlinks the passed path in `finally`. Preserve the original export and pass a disposable working copy to any rehearsal using this job.
- `packages/api/src/conversations/import.ts:1`: import batches use BSON/ObjectId types and Mongo document-size checks. The write orchestrator begins at line 83 and uses staged saves with cleanup after errors. Import has its own persistence and failure contract; routing ordinary message saves does not migrate this path automatically.

These observations do not establish which fields or content kinds exist in the Operator's export; no private export has been inspected. They establish questions to resolve before a real import and before declaring the portable interface sufficient. No import or runtime test was executed in this follow-up.
