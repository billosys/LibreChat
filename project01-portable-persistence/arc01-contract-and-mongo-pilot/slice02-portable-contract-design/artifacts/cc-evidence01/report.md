# CC evidence report — Slice02 compatibility evidence

## Outcome

This packet supplies bounded CC evidence for CDC's remaining DTO and nested-value decisions. The pinned source was unchanged, the sealed pass05 behavior replay matched, all 117 matrix fields were classified exactly once, and all ten requested roots plus all twelve nested public exclusions are recorded. This is proposed-done CC evidence only: S01–S07 remain open, Slice01 acceptance remains pending, and no production or independent acceptance claim is made.

## Identity, scope, and state

This is the separate CC execution context for the assignment issued 2026-09-21. A Codex API session identifier was unavailable; the truthful session description is recorded in `intake.md`. CDC remains the owner of the final codec/DTO/patch policy, composition fence, implementation sizing, and acceptance disposition.

The source is `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall`, revision `3e3c5410d3863118fdba694fb0cd51baeb7102f9`, and was clean before and after the work. Planning is the orphan `planning` branch under `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`. The governing transition is commit `44c77142f97f10082f5628ca76b4d2d1bd6ce4fd`, which introduced the prompt; the prompt SHA-256 is `cdbd9e4922d3d598ee947902a238d211c3c08d18176f973b420aaf40d75e5a99`.

Only the existing historical harness and read-only source inspection were used. No source, application, fixture, plan, ledger, sealed artifact, database, export, dependency, migration, server, branch, push, or PR was changed.

## Replay and validation

The exact required replay was run from PLAN:

```text
/Users/oubiwann/.local/bin/node $SLICE/artifacts/design-pass05/experiment.cjs $SOURCE /Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js $SLICE/artifacts/design-pass04/handle.cjs $OUT/replay-result.json
```

`execution.log` retains the absolute argv, cwd, UTC timestamps, exit status, stdout, and stderr. It also retains the first failed relative-path search and manifest-check attempts before their corrected reruns. The replay exited 0 and reproduced the sealed behavioral fields exactly: 16 read cases, 2 admission gates, 3 preflight cases, 3 negative controls, success, model-access count, and error state. The complete traces and responses were compared, not just the summary counts. Provenance fields were compared separately; no allowed provenance differences occurred.

The three preflight cases were `missing-owner`, `missing-conversation`, and `malformed-conversation`; each passed with zero model accesses. The detected controls were `wrong-owner`, `no-projection`, and `eager-strict-scope`. The existing pass05 validator also exited 0 and reported 117 schema fields, 71 preserved prior-artifact hashes, 87 checked links, 7 open ledger rows, and the evidence class “source-executed read orchestration and preflight with storage doubles; static field matrix, not real-adapter or independent acceptance.”

This is an independent replay in the separate CC context of an existing source-based harness, not an independently designed test, real-Mongo conformance, source-build validation, or integrated adapter acceptance. The replay Node is `v22.22.3`, while the repository pin is `24.16.0`; therefore D07/runtime readiness remains a blocker and this packet makes no same-runtime claim.

## Field coverage and nested inventory

`nested-fields.json` derives its denominator from the sealed matrix: 44 message fields plus 73 conversation fields, 117 total. Every `(record, field)` key occurs once. The resulting classification counts are:

| Classification | Count |
|---|---:|
| selected nested root | 10 |
| other scalar/array field outside this deep inspection | 92 |
| default-hidden specialized field | 14 |
| adapter-private physical relationship | 1 |

The ten roots are message `content`, `files`, `attachments`, `metadata`, `feedback`, `contextMeta`, and `userSubmittedMessageFieldPaths`; and conversation `examples`, `codeWorkspaces`, and `subagentThread`. The one private physical relationship is conversation `messages`, not either message/conversation `files` field. The fourteen default-hidden specialized fields are message `_meiliIndex`, `subagentTranscript`, `subagentActivityProjection`, `subagentTriggerProjection`, and `subagentTask`; and conversation `initial_agent_id`, `subagentThreadLease`, `agentEventBinding`, `agentEventActor`, `agentEventActorCleanup`, `agentEventActorReconciliations`, `agentEventActorEpoch`, `agentEventActorLegacyTurn`, and `agentEventActorSuspension`. They are classified without recursively surveying the event-actor subsystem.

All twelve exclusions from `CLIENT_MESSAGE_SELECT` are present exactly as strings and are mapped in the inventory:

```text
metadata.thoughtSignatures
content.tool_call.backgroundTask.resultClaim
content.tool_call.backgroundTask.completionWakeup
attachments.web_search.knowledgeGraph
attachments.web_search.peopleAlsoAsk
attachments.web_search.relatedSearches
attachments.web_search.shopping
attachments.web_search.places
attachments.web_search.news
attachments.web_search.organic.sitelinks
attachments.web_search.organic.highlights
attachments.web_search.topStories.highlights
```

The nested exclusions remove only the named public paths. A later codec must retain array structure and all permitted sibling data. `contextMeta` is a separate root-level public exclusion with server-side uses; it is not one of the twelve nested paths. The inventory records the exact schema/type/provider/default/public/probe/unset observations and source witnesses for each root, including open positions and unresolved questions.

### Compatibility observations

| Root | Established reuse and witness | Compatibility obstacle / unresolved point |
|---|---|---|
| `message.content` | Storage `Mixed[]` (`schema/message.ts:139-143`), direct `unknown[]` (`types/message.ts:90`), provider `TMessageContentParts[]` (`data-provider/src/schemas.ts:1063-1066`); route and message-method branches handle structured content and tool patches. | Provider discriminants do not establish a lossless decoder for open storage values. Preserve index boundaries and open members; CDC must choose representation. |
| `message.files` | Storage `Mixed[]`, direct `unknown[]`; provider `Partial<TFile>[]` (`types/files.ts:150-221`). | The provider shape is a shallow consumer type, not evidence that all stored members are known or JSON-only. Historical values and null policy remain unknown. |
| `message.attachments` | Storage `Mixed[]`; provider `TAttachment[]` union (`schemas.ts:1039-1061`); route/method branches and the twelve-path projection are witnessed. | Attachment branches and web-search nested values are broader than one closed DTO; permitted siblings and open values must remain lossless. |
| `message.metadata` | Storage `Mixed`, direct `Record<string, unknown>`, provider `z.record(z.unknown())`; projection explicitly excludes `metadata.thoughtSignatures`. | No closed vocabulary or historical value characterization. Do not stringify, narrow, or reject values from this evidence. |
| `message.feedback` | Schema has rating/tag/text (`schema/message.ts:103-121`); provider feedback declarations and validation are in `data-provider/src/feedback.ts:110-145`; route validation starts at `routes/messages.js:693-705`. | Stored `Mixed` tag, expanded server type, and provider minimal tag key do not yet define a portable mapping. |
| `message.contextMeta` | Server schema/type and fading spread (`schema/message.ts:238-246`, `schema/fading.ts:19-34`); server routes and agent client retain/use it (`routes/messages.js:232-241`, `agents/client.js:2249-2320`). | Root is public-excluded and server-retained; server partial optionality and provider validation differ. Null/unset and DTO visibility need CDC policy. |
| `message.userSubmittedMessageFieldPaths` | Closed path/field members (`types/message.ts:68`, `data-provider/src/filters.ts:58-62,184-191`); merge/remap logic is witnessed in `methods/message.ts:304-374,954-975`. | Path markers are typed, but their targets point into open content/attachment values. Index remapping and absent/null behavior need explicit cases. |
| `conversation.examples` | Storage `Mixed[]` (`schema/defaults.ts:30-35,238-239`); provider `tExampleSchema` (`data-provider/src/schemas.ts:867-876`) and generator use (`generate.ts:677-704`). | No ordinary non-test BaseClient writer for the exact field was established in the bounded search; historical values may exceed provider input/output shape. |
| `conversation.codeWorkspaces` | Schema/provider `CodeWorkspaceSelection[]` with required IDs and pattern constraints (`schema/defaults.ts:128-135,327-336`; `schemas.ts:1127-1136`); request/resume/client and HITL policy witnesses distinguish presence/null. | Declarations align, but absent, empty, populated, and null behavior affects agent execution. Adapter conformance is open. |
| `conversation.subagentThread` | Schema/type/provider lineage object (`schema/convo.ts:52-65`; `types/convo.ts:288`; `schemas.ts:1102-1113`); routes/request/resume/responses inspect lineage. | Child identity must remain separate from lease/event-actor private state. Public reads expose only the intended lineage discriminator; null and lifecycle mapping are unresolved. |

The bounded name searches were broad rather than exhaustive: `content` 1165, `files` 412, `attachments` 210, `metadata` 413, `feedback` 57, `contextMeta` 88, `userSubmittedMessageFieldPaths` 36, `examples` 21, `codeWorkspaces` 35, and `subagentThread` 15 matches. The report relies on the inspected enclosing functions and records “not established” where a direct ordinary producer/consumer was not proven.

## Decision inputs for CDC

| Unresolved policy | Affected fields | Available evidence | Options and consequences | Next discriminating check |
|---|---|---|---|---|
| Representation for open content/tool values | `content`, nested exclusions | Mixed/unknown storage, provider union, route/method patch witnesses | Preserve an opaque lossless value; map known variants with an explicit open remainder; or narrow/reject. The latter two risk legacy loss. | Characterize representative historical values and define round-trip/state cases before choosing a codec. |
| File and attachment value shape | `files`, `attachments` | Mixed storage versus `Partial<TFile>`/`TAttachment` consumers | Use a storage DTO, a tagged lossless envelope, or a validated consumer projection. Consumer projection can discard fields. | Inspect permitted historical values and compare round-trip plus absent/null/empty/populated cases. |
| Metadata and feedback mapping | `metadata`, `feedback` | Record/Mixed declarations, feedback provider/server mismatch, public exclusions | Preserve unknown values; define a tagged known/unknown form; or adopt provider minimal forms. Narrowing/stringifying can lose BSON or legacy data. | Run isolated corpus characterization and enumerate server/provider write/read paths. |
| Context/provenance policy | `contextMeta`, `userSubmittedMessageFieldPaths` | Server retention/merge logic, public root exclusion, typed path markers | Keep server-only fields internal; expose a versioned DTO; or split provenance from content. Each affects patch/unset semantics and index remapping. | Write discriminating conformance cases for null/unset, path remap, and public projection. |
| Conversation nested contracts | `examples`, `codeWorkspaces`, `subagentThread` | Provider schema and agent witnesses; examples producer gap; lineage discriminator | Reuse named types where shapes are closed; retain open examples; keep private lifecycle fields out of lineage. Over-validation risks old records. | Characterize examples and execute absent/empty/populated/null cases through ordinary callers without adding reads. |

These are alternatives and consequences, not decisions. No codec, BSON stringification, flattening, default insertion, legacy rejection, or universal future Guildhall model is selected here.

## S01–S07 contribution and remaining work

- **S01 — open.** The replay reinforces the ordinary ownership, projection, route/history/probe ordering and early-validation evidence. Exact composition and unchanged-caller fence remain CDC work.
- **S02 — open.** The 117-row inventory and ten-root observations expose type reuse and engine-type boundaries. Concrete DTOs, relationship translation, and query-count conformance remain unresolved.
- **S03 — open.** The packet explicitly preserves absent/undefined/null/empty/populated distinctions and nested unset implications. Complete value, error, and partial-commit mapping is not supplied.
- **S04 — open.** This assignment does not reproduce the cursor characterization; the independent cursor reproduction remains pending.
- **S05 — open.** Source preservation was checked for this packet only. Migration/source-loss obligations and their later owners remain open.
- **S06 — open.** The packet identifies runtime drift and unresolved DTO choices. No implementation fence, source-build proof, or integrated conformance is ready.
- **S07 — open.** The packet is explicit, hashable, and returned to CDC; no reviewer label upgrades prior attested work and no acceptance is claimed.

## Bubble-up recommendation

Keep the existing three-slice roadmap unchanged until CDC and the Operator disposition these choices. At the next sizing checkpoint, split the remaining work if the open-value codec/DTO contract, composition/file fence, source-preservation mapping, and runtime/build/conformance gates cannot be reviewed as one bounded implementation slice. A likely safe decomposition is contract/DTO policy followed by adapter composition/conformance, but that is a planning recommendation, not a new assignment.

## Evidence paths and blockers

The raw replay result is `replay-result.json`; the full command history and failed attempts are in `execution.log`; the source-backed inventory is `nested-fields.json`; and the standard-library replay/validation driver is `replay.py`. The packet's final six-file hashes are sealed in `SHA256SUMS`.

Blockers and limitations are intentional: the repository Node pin is not the installed replay Node, no live Mongo or historical corpus was accessed, no source build or application suite was authorized, examples lack an established ordinary writer in the bounded search, and open/Mixed value semantics remain CDC-owned. These prevent claims of D07 readiness, real-adapter conformance, and Slice02 acceptance.
