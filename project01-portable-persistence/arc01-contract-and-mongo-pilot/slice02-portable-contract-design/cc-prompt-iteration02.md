# CC iteration02 — bind verification to submitted evidence and correct the nested map

## Assignment, authority and fence

Execute this **second correction** as CC in Project01 / Arc01 / Slice02 and return evidence to the existing CDC design conversation through the Operator. Predecessor: [cc-prompt-iteration01.md](cc-prompt-iteration01.md). Reviewed delivery: `5d94ef8d8da18b636279553ed037b906259b2882`, `artifacts/cc-evidence02`. Current findings and reproduced controls: [cdc-verification.md](cdc-verification.md), section “Correction iteration01 review”, and [artifacts/cdc-review02/result.json](artifacts/cdc-review02/result.json). Preserve the initial prompt and both preceding deliveries unchanged. This does not reset refinement accounting.

`PLAN=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`, branch `planning`; `SOURCE=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall`, pinned source `3e3c5410d3863118fdba694fb0cd51baeb7102f9`. `SLICE=$PLAN/project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design`; `OUT=$SLICE/artifacts/cc-evidence03`.

Create/commit **only** these seven new files: `OUT/intake.md`, `OUT/report.md`, `OUT/nested-fields.json`, `OUT/replay-result.json`, `OUT/execution.log`, `OUT/replay.py`, `OUT/SHA256SUMS`. No source edits, builds, application suites, dependency changes, source branches, DB/private-export access, service changes, pushes, PRs, plan/ledger changes or edits to older evidence. Preserve unrelated work/index state. Existing runtime and compiler pins, manifest/source checks, authoring/verification separation and no-fabricated-success rules from iteration01 still govern. Missing prerequisites block dependent work; do not install tools.

CDC retained the actual replay equality, 117 classifications, ten roots, twelve exclusion keys, 22 source fingerprints and the useful Date/file/lineage observations. Do not reopen identity design or repeat the old research passes. S01–S07 and Slice01 acceptance remain open; this is evidence/tooling correction, not production implementation. CDC owns DTO/codec/patch policy, injection fence, D07 and production sizing.

## Required reading and intake

**Required-full:** this prompt; predecessor iteration01; current slice plan/ledger and entire CDC verification; evidence02 intake/report/replay.py; pass05 read-contract.md/protocol.md/experiment.cjs/validate.py; pass04 handle.cjs; PLAN AGENTS.md/BILLO.md/README.md; SOURCE AGENTS.md/BILLO.md/CLAUDE.md. Previously loaded texts may be reused only if their exact revision/content and complete read extent remain available in your current context; otherwise reload. Record truthful extents, prompt-introducing commit/hash, current assignment match, actual CC context and source-cited contract readback before dependent work.

**Required-section:** current project Goal/boundaries, Definition of done, Workflow/authority including complete transition and Expedited sections; arc Scope, Slice roadmap, Workflow/source boundaries. Use the exact framework paths in initial cc-prompt.md for methodology roles/two-contributor/transition, engineering-methods investigation/intake, independent verification, and scientific-methods evidence capture/validity. Required-full guide requirements from iteration01 remain; do not substitute line counts for understanding.

**Required-data:** current committed evidence02 inventory (all coverage rows, root member/applicability/witness records, exclusions and unresolved entries); complete replay behavior/provenance; CDC review02 result; the matrix's 44/73 fields and **per-record** ancillary populations, plus sourceHead/exclusions. Inspect relevant evidence02 log blocks for the incorrect queries and controls; preserve them as historical failures, not successful coverage. Execute corrected queries, partition large outputs and retain all selected data. Complete source sections are those supporting the finite ten-root/type boundary below, with complete enclosing functions for runtime witness claims. No private corpus or unrelated actor/SDK survey.

## R1: verify the submitted result and exercise real control paths

Keep explicit `--capture`, `--verify`, `--self-test`, and `--packet` modes. Capture still refuses a sealed destination before mutation; verify remains read-only. Port the working predicates, not the bug.

1. After packet/manifest/inventory and environment preflight, load **submitted** `packet/replay-result.json` and the pinned baseline. Compare every behavior and provenance key from iteration01 with exact key presence and value equality. Then run the sealed pass05 harness into temporary storage and compare the fresh result with **both submitted and baseline**. Missing, null, false and absent keys must remain distinct. A recalculated checksum only validates bytes; it does not validate a claim.
2. Retain existing positive valid packet/control and negative classifications/membership/key-state tests. Add a valid-but-misassigned classification. Route wrong-runtime/head/compiler-digest/source-fingerprint tests through the same verification entry/preflight path with injected read-only observations and a runner sentinel. The failing path must invoke the sentinel zero times; the valid path must invoke it once. Do not test a separate tuple expression that merely orders a predicate before a sentinel.
3. Copy a valid sealed packet to temporary storage, separately mutate submitted behavior (`success:false`) and provenance (`node` wrong), reseal each copy, and invoke verification. Both must reject. Add absent-versus-null submitted-result cases through that path. These tests must fail against evidence02's verifier. No real source/tool/packet mutation is allowed.
4. For preservation, distinguish a positive unchanged-packet check from a negative mutation check. In a temporary packet only, inject a runner that changes one packet file after the initial hashes are recorded, returns a valid harness result, and require the final preservation guard to reject. Report separate counts for positive checks and negative controls with actual outcomes; do not label an unchanged positive check as a rejected mutant.
5. Self-test on a sealed input must preserve its hashes: emit stdout and use temporary copies. When self-test output needs to enter an unsealed capture log, the authoring caller may append it before sealing. Never append to an already sealed packet, including default `--self-test` use.

Keep all old and new failed attempts visible. Do not replace results with success when a command or predicate fails. The verifier's own structural validation remains distinct from CDC semantic review.

## R2: correct declared shapes, public survivors and named read views

Retain all 117 coverage rows and the ten existing roots. This is the same local-declaration boundary as iteration01, not a new schema design.

**Public exclusions compose.** For each of twelve paths, retain source-declared siblings separately if useful, but `permittedSiblings` must contain only paths that survive the **entire** current projection. Examples: backgroundTask status/settledAt can survive; resultClaim cannot. Organic title/link/snippet and processed content can survive; sitelinks/highlights cannot. Web-search organic/topStories/images/videos/answerBox/references/turn/error can survive, subject to their own nested exclusions; places/news/shopping/relatedSearches cannot. Do not remove whole organic/topStories arrays. Cite `packages/data-schemas/src/methods/message.ts:456–481` and the actual declared members. Add a validator/control that rejects a claimed survivor covered by another exclusion, including canonical array paths; do not interpret `[]` as part of a literal Mongo field name.

**Applicability means the named operation's returned data.** Use pass05 read-contract.md, not “participates somewhere in a turn.” Record materialization/visibility distinctly from incidental admission use:

| Root family | serverHistory | publicMessages | turnConversation | accessProbe |
|---|---|---|---|---|
| Seven message roots | Message-view member, subject to source selection | Preserve according to projection; contextMeta excluded, nested exclusions applied | Not a conversation result member | Not selected |
| examples, codeWorkspaces | Not a message result member | Not a message result member | Conversation-view member, subject to source selection | Not selected |
| subagentThread | Not a message result member | Admission uses lineage; not a public message member | Conversation-view member | Current method selects full lineage object |

Verify this mapping against methods/callers; record a source contradiction rather than silently following an unsupported table. For contextMeta, explicitly say public exclusion; an `established` status is acceptable only if its separate disposition clearly means “established excluded,” not “present.” A type-only witness establishes a declared domain, not runtime production. Do not turn an incomplete search into “no producer exists.”

**Expand closed local declarations to named members.** Avoid slash-separated composite paths that conceal per-member requiredness/domains. Reusable type tables linked from roots may prevent duplication, but expose local members and retain each applicable prefix/array boundary. At minimum repair the demonstrated gaps:

- `Agents.ToolCall` (`types/agents.ts:81–135`): all named local members and backgroundTask/resultClaim/approval leaves, including Date distinctions; keep args' record open, completionWakeup unresolved unless a precise declaration is found. Preserve other local content-union branches from `TMessageContentParts` and their named local definitions, stopping at explicit open/external SDK boundaries rather than replacing them with an invented JSON shape.
- `TFile` (`types/files.ts:150–221`): named properties and metadata members; distinguish outer `Partial<TFile>` from nested requiredness; follow local referenced declarations to their open/external boundary. Embedded IDs and Date/string values remain observations, not permission to strip/stringify them.
- `TAttachmentMetadata` / all three `TAttachment` variants (`schemas.ts:1039–1061`): include numeric `expiresAt` in its branch, workspaceChange/memory/ui_resources/file_search as well as web_search, and their closed local member definitions/open boundaries. The file-search branch must not inherit web-search exclusions by analogy.
- `SearchResultData`, ProcessedSource, ProcessedOrganic, ProcessedTopStory and Highlight (`types/web.ts`): list named fields, including optional turn/error/references and inherited local fields; identify additional arrays correctly. Local nested declarations retain their actual domains; excluded and allowed siblings remain distinct.
- contextMeta fading/fadingTiers: member rows for v/budgetTokens/masked and tier agentId with correct server/provider requiredness. Retain feedback's storage/provider tag mismatch and expand its local closed tag shape. Keep examples' input/output members, path markers, workspace selections and lineage individually addressable.

This completes declared-shape evidence only. Historical BSON/Mixed contents, codecs and policy remain explicitly unresolved/CDC-owned. Do not invent consumer evidence or flatten disagreements. Add every newly cited source to fingerprints; validate source-ref line bounds and actual support. Full enclosing symbols are required for runtime witness claims; otherwise label the excerpt/type/search evidence accurately.

## R3: make query coverage executable and truthful

Use `messageSchema` and **`convoSchema`**, not `conversationSchema`. Select `providerOnly`, `interfaceOnly`, `implicit` from **each `records[]` object**. For example:

```jq
{sourceHead, exclusions,
 records: [.records[] | {name, providerOnly, interfaceOnly, implicit}]}
```

Capture complete field projections per record. Assert exact identities, uniqueness, 44/73 field counts and equality to baseline membership; ancillary checks require the keys and their actual arrays/objects, not synthesized nulls. Expected provider-only counts are 10/13, interface-only 4/3, with four implicit keys per record. Required jq queries require exit **0**, plus shape/content predicates; an empty successful selection is a failure. Bounded rg searches may legitimately return 1 for no matches, but record that distinction. Log argv/cwd/exit/stdout/stderr immediately, before raising or executing dependent steps. Add negative controls for the old wrong record name and wrong-level ancillary projection, and retain their outputs.

Correct new intake/report claims to the actual query results and loaded text extents. Preserve old failures as failures; do not retroactively claim the old logs covered the conversation/ancillary populations. Use the slice-root `cdc-verification.md` path. Report that resultClaim has a known local declaration, distinct from uncertain historical values and completionWakeup's unresolved declaration. Do not manufacture earlier raw receipts.

## Finish and return

Run capture, all affected controls, structural inventory/source/hash checks and `git diff --check`. Report actual counts and failures; do not target a cosmetic total of fourteen. Preserve the existing source/runtime limitations and all open rows. Freeze logs before hashing the other six files into SHA256SUMS, then run `--verify --packet "$OUT"` and sealed-safe `--self-test --packet "$OUT"` with output retained outside the packet; require unchanged packet hashes. Record final verification evidence through the execution environment without appending to the seal.

Inspect staged state and commit only the seven named OUT files on `planning` with `git commit --only -F <message-file> -- <seven explicit paths>`. Both exact trailers are required:

```text
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

Return the commit, exact report/manifest paths, dispositions R1–R3, failed/passed checks and limitations to CDC through the Operator. Status is proposed-done pending CDC review and Operator acceptance. Do not close any ledger row or begin Slice03.
