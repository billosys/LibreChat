# CC iteration03 — repair R2 from declarations, without inventing payload structure

## Assignment and preserved progress

Execute the **third correction** for Project01 / Arc01 / Slice02 as CC and return the packet to the existing CDC design conversation through the Operator. Predecessor: [cc-prompt-iteration02.md](cc-prompt-iteration02.md). Reviewed delivery: `0f81e318bdd78619b5092c188c5149ae5178de35`, `artifacts/cc-evidence03`. Governing review: [cdc-verification.md](cdc-verification.md), “Correction iteration02 review”. The actual discriminating result is in [artifacts/cdc-review03/result.json](artifacts/cdc-review03/result.json), with complete command output in its execution.log.

**R1 and R3 corrections are reproduced and leave the active defect list.** Preserve submitted/baseline/fresh comparisons, sealed-safe verification/self-test, runtime/source preflight, and correct matrix queries. Regression-run them after the repair, but do not redesign them or reopen the earlier identity/route research. R2 remains: declared fields/types/presence/paths, two view mappings and the composed-exclusion validator. All S01–S07 remain open; no production or slice closure is assigned. CDC owns DTO/codec/patch policy, injection, D07 and sizing.

`PLAN=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`, branch `planning`; `SOURCE=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall`, pinned source `3e3c5410d3863118fdba694fb0cd51baeb7102f9`; `SLICE=$PLAN/project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design`; `OUT=$SLICE/artifacts/cc-evidence04`.

Create/commit only these seven new files: `OUT/intake.md`, `OUT/report.md`, `OUT/nested-fields.json`, `OUT/replay-result.json`, `OUT/execution.log`, `OUT/replay.py`, `OUT/SHA256SUMS`. Preserve every prior packet, review and issued prompt byte-for-byte. No source/dependency edits, database/private-export access, application builds/suites, service changes, new source branches, plan/ledger edits, pushes or PRs. Preserve unrelated working/index changes, including Project02. Existing evidence pins remain Node v22.22.3, TypeScript 5.9.3 and its sealed digest; this is not the Node 24.16.0 build gate. No installs. A missing prerequisite blocks dependent execution.

## Intake and reading

Verify this assignment against current slice-plan.md; record the actual context, source state and this prompt's introducing commit/hash. Required-full: this prompt, iteration02, current slice plan/ledger and complete CDC verification; evidence03 intake/report/replay.py; PLAN AGENTS.md/BILLO.md/README.md; SOURCE AGENTS.md/BILLO.md/CLAUDE.md; pass05 read-contract.md/protocol.md/experiment.cjs/field-matrix.cjs/validate.py; pass04 handle.cjs; CDC review03 declarations.cjs and review.py. Apply the initial prompt's methodology/workflow, independent-verification and evidence-capture/validity readings; complete required project/arc Goal, DoD, Scope, roadmap, workflow/authority/transition/Expedited sections still govern. Reuse already loaded text only when exact revision/content and full relevant extents remain in context; otherwise reload. Record actual coverage, not reconstructed receipts.

Required-data: all 117 coverage records, all ten root maps, all twelve exclusions, source fingerprints and unresolved entries in evidence03; its complete replay behavior/provenance; CDC review03 results and source-declaration command output; complete 44/73 matrix records with the per-record ancillary populations. Partition projections to avoid truncation. Read every local source declaration used for a member or domain claim completely, plus exact source method/projection used for view claims. Read complete enclosing functions for runtime producer/consumer claims; otherwise state type-only or bounded-search evidence. The ten-root scope and open/external boundary from iteration02 still apply; no historical-value survey or unrelated subsystem research.

Before authoring the corrected map, provide a concise source-cited readback distinguishing literal member paths from discriminated branches, optional ancestors from required leaves, shallow Partial wrappers from nested requiredness, and message metadata from TFile metadata. This is an execution preflight, not a new permission exchange.

## R2 repair method

The evidence03 map cannot be repaired by adding more names or boilerplate. Reconcile **all current member rows**, removing unsupported declaration claims and correcting their paths/types/presence. Keep the ten-root and 117-field scope; there is **no target nested-member count**. Count actual source-derived rows after reconciliation.

Use the available TypeScript compiler to extract literal declarations without evaluating application modules. The reviewed `artifacts/cdc-review03/declarations.cjs` demonstrates a working syntax-only route with the installed compiler; pass05 field-matrix.cjs already extracts source initializer text. The review extractor returns syntax and source locations, not full type resolution or persisted paths. CC must preserve declaration ownership and structural parent/branch edges when adapting this approach. Keep any added helper code inside replay.py (for example, a JavaScript string invoked with the pinned Node/compiler), and emitted declaration records inside nested-fields.json/log so the seven-file fence stays intact.

Concrete implementation route:

1. Parse each bounded source with `ts.createSourceFile`; locate the exact named type/interface/variable by namespace and symbol, rejecting missing/ambiguous matches. Capture actual declaration/member text, file digest and line span. Type members use their literal type text and question token; Zod members use the initializer expression, retaining `.optional()`, `.nullable()`, defaults and `.strict()` verbatim. Do not execute Zod or the app to get this data.
2. Keep the declaration graph separate from its use sites. Represent unions, intersections, named local references, arrays, records, `Pick` and shallow `Partial` explicitly. Follow local named definitions needed by the ten roots to their declared open/external boundary. Do not call an available local type “external” merely to avoid reading it. Unknown external definitions remain named unresolved boundaries; do not invent their fields.
3. Derive a member's actual data path from that graph and its use site. A union branch discriminator or analytical branch ID belongs in `declarationContext`/a separate branch field, never an invented path segment such as `.variant2`, `.summary` or `.error`. Reusable local declaration tables may avoid repeating every type under every prefix. Each root/member must reference the declaration and application context that establish it.
4. Record actual value domains separately: storage Mixed/unknown is not a closed provider type; provider Date is not a transport string; a type-only optional field is not a stored default. `declaredType` must contain real type/initializer text or a precise declaration reference resolvable to that text, not “declared local type; see sourceRefs”. Keep default/null evidence separately; unknown evidence remains unknown. State whether requiredness is local to the member, conditional on optional ancestors, and affected by a use-site wrapper. Structured requiredness records are permitted; carry validators and report forward consistently.
5. Validate submitted declaration records against fresh source extraction and exact member sets at closed local declarations, not against lists copied from the submitted inventory. Preserve open records as open; do not require an arbitrary minimum of three members. Remove all false required-path assertions inherited from evidence03. Validators must reject nonexistent members, wrong paths/types/requiredness and missing required local members within the declared inspection boundary. Semantic/path/application interpretations still require CDC review; syntax extraction alone is not acceptance.

### Concrete source corrections and oracles

These are minimum regression examples, not permission to leave the other member rows unexamined:

| Surface | Required correction and discriminating check |
|---|---|
| Path markers | `filters.ts:184–191` is a strict two-member object: required path and field. No declared source/operation. Exact key-set check rejects their addition and removal of either actual member. Add this source to fingerprints. |
| Examples | `schemas.ts:867–874` declares input/output, each with required content:string. Remove role/files declaration claims. Mixed storage remains broader; do not infer historical absence. |
| Content branches | Error branch has element-level text/error/initiatedBy, not an error object. SummaryContentPart has element-level content/tokenCount/etc and optional boundary with required messageId/contentIndex; no summary wrapper. Keep branch identity separate from data paths. Read types/content.ts:195–315 and referenced local branches. |
| Tool lifecycle | backgroundTask is optional, but settledAt:Date and version/taskId/toolName/status are required inside it; cancelled is optional. resultClaim is optional with required kind/claimId/claimedAt:Date and optional generationId. Approval has required actionId/allowed_decisions and optional description. Preserve the public exclusions separately. |
| Message metadata | Its declared domain is an open record/Mixed value; TFile.metadata does not declare message metadata.codeEnvRef/runFile/etc. Do not transfer fields between similarly named objects. A genuine producer observation requires an exact source witness and remains distinct from a declared key. |
| File use sites | TFile.file_id is required in TFile, but TMessage.files uses Partial<TFile>[]; outer properties become optional at that use site while nested object requiredness is unchanged. Inspect actual FileContext/FileSources, RunFileProvenance and CodeEnvRef/CodeEnvRefBase declarations rather than marking local definitions open by default. |
| Attachment variants | Use actual attachments[].expiresAt with a separate union-branch record: numeric expiry is required in its numeric branch. Pick preserves selected-field requiredness and Partial changes only its selected outer fields. Do not fabricate variant1/2/3 data properties or metadata fields in branches that do not contain them. |
| Search results | ProcessedSource content/attribution/references/highlights/processed occur under organic[] and topStories[] intersections, not SearchResultData's root. Read References and Highlight to establish array versus record structure. Preserve web_search versus file_search differences without borrowing projection exclusions. |
| Lineage | parentAgentId is optional; the other seven named lineage fields are required in the local schema. Root optionality is separate. |
| Workspace selections | Root codeWorkspaces is optional; each supplied entry requires environmentId/workspaceId. Do not mark the whole root required because the entries have required fields. |

An acceptable Date member, for example, identifies `content[].tool_call.backgroundTask.settledAt`, its `Agents.ToolCall` branch, actual `Date` provider type, required leaf beneath optional backgroundTask, and storage/server open boundaries. It cites the settledAt declaration and parent/use-site definitions. The same source text cannot prove a historical BSON population or decide its future codec.

### Read views and the full exclusion set

Keep the corrected message-versus-conversation separation. Repair these exact rows:

- `metadata.publicMessages`: included with nested thoughtSignatures exclusion, **not whole-root excluded**. Source: `CLIENT_MESSAGE_SELECT`, methods/message.ts:456–481.
- `subagentThread.accessProbe`: selected full lineage object. Cite complete `getConvoOwnership`, methods/conversation.ts:2060–2078, and add its fingerprint. Its public use remains admission-only, not a public message member.

Validate every permitted path against **all twelve** nested exclusions after canonicalizing array notation. Equality or descent beneath any excluded path must reject. A retained ancestor container is allowed only with explicit applicable nested removals; the validator checks the obligation list against the full set. Thus organic[] can survive with sitelinks/highlights removed, while resultClaim cannot be named as a survivor of completionWakeup. Preserve other array contents and siblings. Do not apply web_search exclusions to file_search.

Controls must reject the CDC counterexample (resultClaim claimed as a completionWakeup survivor), an exact/descendant excluded path, and a container falsely labeled fully preserved. A positive control must accept organic[] with its correct nested removals. Keep existing R1 controls and classify positive checks separately.

## Verification, seal and return

Run capture with source-backed declaration validation, exact matrix queries, the unchanged sealed harness and the repaired projection controls. Add source-derived negative controls for the table above, including invented path-marker keys, invented summary wrapper, wrong parentAgentId optionality, Date-to-string mutation, and required TMessage.files.file_id despite Partial. Tests must reject the corresponding evidence03 claims and accept the correct declaration/use-site cases. Do not hard-code the old member count or manufacture members to make tests pass.

Keep raw argv/cwd/status/stdout/stderr and failed attempts. Report R1/R3 as retained/reproduced and R2 against each concrete correction; include actual new source/member/control counts. Fresh semantic extraction and source refs must be inspectable. Hash/count checks and self-tests do not establish CDC semantic acceptance. Preserve historical limits: storage doubles, Node 22 replay versus Node 24 source-build readiness, unknown historical Mixed/BSON values.

Finish logs, seal the other six files in SHA256SUMS, then run final `--verify --packet "$OUT"` and `--self-test --packet "$OUT"` against the sealed packet, retaining output outside it and requiring unchanged hashes. Run `git diff --check`, verify prior packet/source preservation and inspect the exact seven-file inventory. No extra approval exchange is needed for this assigned evidence work.

Inspect the index; commit only the seven named OUT paths on planning using `git commit --only -F <message-file> -- <seven explicit paths>`, preserving unrelated staged work. Required final trailers:

```text
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

Return the commit, report/manifest paths, reproduced checks, failed/blocked attempts and remaining limitations to CDC through the Operator. Status remains proposed-done pending CDC review and Operator acceptance. This is the third correction; do not reset the iteration budget or open Slice03.
