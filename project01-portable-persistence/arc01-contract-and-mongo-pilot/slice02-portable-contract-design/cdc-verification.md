# CDC verification — Slice02 CC evidence

Current disposition: see [Correction iteration03 review](#correction-iteration03-review--2026-09-22). Earlier reviews below remain historical evidence.

## Initial review — verdict and scope

**2026-09-21: partial evidence reproduced; initial CC assignment returned for correction. Slice02 remains open.** This is an actual CDC review of CC commit `99d5ecd794d00cd1c0db7a199633042766af5953`, assigned by [cc-prompt.md](cc-prompt.md) at planning commit `44c77142f97f10082f5628ca76b4d2d1bd6ce4fd`. CDC is the existing LibreChat/Guildhall design conversation; CC identifies itself in [intake.md](artifacts/cc-evidence01/intake.md) as a separate Codex API session with no exposed session ID. The Operator relayed its report. No CRC is assigned.

Source remained clean at `3e3c5410d3863118fdba694fb0cd51baeb7102f9` on `billo-guildhall`. The seven-file CC packet and initial prompt are preserved unchanged. Review artifacts live in [artifacts/cdc-review01](artifacts/cdc-review01/result.json); the [review script](artifacts/cdc-review01/review.py) loads the committed CC verifier without calling its writing `main`, runs the sealed harness into a temporary directory and applies separate structural checks. The script pins manifest membership to the reviewed commit so future packets do not change this review's denominator.

## Reproduced evidence

- All structured replay output equals CC's result, including 16 read cases, two admission gates, three preflight cases and three detected negative controls. No database or application build ran.
- All 117 `(record, field)` keys are present exactly once, and their actual classifications agree with the baseline schema/default-selection information. Ten selected roots and twelve nested exclusion strings match the requested sets.
- All 23 inventory source fingerprints match the unchanged source. All 87 artifact hashes present at the reviewed commit pass, including the six CC manifest entries. The CC commit changes exactly its seven allowed files and has both required trailers.
- The report correctly leaves S01–S07 and Slice01 acceptance open and distinguishes Node 22 replay from the repository's Node 24.16.0/source-build requirement.

This confirms CC's actual run and structural observations. The underlying comparison harness was authored by this CDC context during one-contributor investigation; rerunning it does not independently validate its design or establish integrated Mongo conformance. No historical gate is accepted by relabeling the author.

## Findings requiring correction

### R1 — verifier accepts undeclared drift and rewrites sealed evidence

`artifacts/cc-evidence01/replay.py:193–199` compares behavior but labels every provenance difference “allowed”; the caller does not reject those differences. The review supplied a wrong Node version, wrong source head and wrong compiler digest separately to this predicate. All three were accepted. The driver does check the real source head later; these controls concern its result-comparison predicate, not a claim that the entire driver accepts an actually changed checkout. Runtime equality is not enforced before replay.

`validate_inventory` at lines 179–190 verifies key sets and totals but accepts an invalid classification label. The actual delivered labels are correct under CDC's separate check; the failure is that the verifier does not establish its own classification claim.

`main` at lines 202–226 regenerates `nested-fields.json`, overwrites `replay-result.json` and appends to `execution.log` in the fixed sealed packet, with no read-only mode or seal guard. It validates generated inventory rather than the artifact submitted for review and performs source checks after replay. A reviewer must not run that entrypoint against the committed packet. CDC did not do so.

Required correction: an explicit, fail-closed provenance and preflight contract; validation of the submitted inventory with independently derived classifications; a read-only verification mode using temporary outputs; and a guarded authoring mode that refuses a sealed destination. Keep new controls in the next packet, never repair the sealed one.

### R2 — named roots are present, but the requested nested map is incomplete

The ten root records mostly contain prose summaries. All twelve exclusion records at `replay.py:173` carry the same generic preservation text, without the requested explicit array/member path and permitted siblings. The root `applicability` text is likewise generic rather than specifying each server/public/probe boundary. The `files` witness names “BaseClient and formatMessages” without a file/symbol/span, although the prompt required precise witnesses or a bounded `not established` finding.

Concrete omissions affecting the next design decision:

- `packages/data-provider/src/types/agents.ts`, `Agents.ToolCall.backgroundTask`, lines 103–117 declares `settledAt: Date` and `resultClaim.claimedAt: Date`. This is a declared non-JSON leaf, not evidence of any historical corpus value. The public projection removes `resultClaim` but not `settledAt`.
- `packages/data-provider/src/types/files.ts`, `TFile`, lines 150–221 includes optional `_id`/`__v`, `expiresAt?: string | Date`, nested metadata, and Date/string timestamps. Those are concrete engine-metadata/temporal compatibility questions; a bare pointer to `Partial<TFile>` leaves them implicit.
- `packages/data-provider/src/types/web.ts`, `SearchResultData`, lines 43–58 declares both `organic[]` and `topStories[]`. The exclusion path `attachments.web_search.organic.highlights` crosses both `attachments[]` and `organic[]`; retaining only the former array boundary would be wrong. This source is not in CC's source-fingerprint list.
- `packages/data-schemas/src/methods/conversation.ts`, `getConvoOwnership`, selects `user tenantId subagentThread`; its returned `subagentThread` is the selected lineage object, used as a discriminator. A reduced boolean/discriminator-only DTO is a proposed contract option, not the current method's return shape. Qualify the report/inventory wording accordingly.

Required correction: complete the original ten-root bounded map, naming members/leaf domains, open boundaries, projection applicability and exact witnessed array traversal. Do not silently choose a decoder, strip nested IDs, or declare stored historical types from this source evidence. No broad caller census or live corpus investigation is requested.

### R3 — intake and raw-inspection coverage are asserted without the required detail

`intake.md` asserts complete bounded reads but records no actual per-document read extents, selected declaration extents, truncation recovery, or identifiable query outputs. `execution.log` contains the replay and validator commands, then retrospective prose about failed searches/manifests; it does not retain the required structured-data query commands/results or the bounded witness searches behind the match counts. This does not prove that CC failed to read them, but the submitted packet does not support the stronger retained-evidence claim.

Required correction: perform fresh, bounded reads/queries for the affected inventory, record real commands/status/results and actual loaded extents, and distinguish old reported-only attempts from newly captured evidence. Do not fabricate historical stdout, timestamps or receipts. Existing replay output is reusable; repeating application suites or older investigation passes is unnecessary.

## Ledger walk and bubble-up

| Row | Review disposition |
|---|---|
| S01 | Open. The scoped reload/probe harness is reproduced; actual composition wiring and complete caller preservation remain pending. |
| S02 | Open. Membership/classification counts reproduced; R2 blocks treating the nested inventory as complete DTO decision input. |
| S03 | Open. R2 leaves important concrete value/presence/projection distinctions insufficiently mapped; full failure/patch contracts remain CDC-owned. |
| S04 | Open, unreviewed here. Cursor characterization/reproduction has its existing owner and separate scope. |
| S05 | Open, unreviewed here. Preserved repository artifacts do not discharge original-source/corpus fidelity obligations. |
| S06 | Open. No production assignment, source-build proof or integrated adapter conformance; R1 must be corrected for a dependable evidence driver. |
| S07 | Open. Commit scope/trailers/hashes verified; R1/R3 require evidence-tooling and intake corrections before accepting this bounded packet. |

The parent plans now record returned-for-correction rather than pending relay. Existing architecture, three-slice roadmap, scope and acceptance criteria remain unchanged. The next assignment is [cc-prompt-iteration01.md](cc-prompt-iteration01.md), limited to R1–R3 and a new seven-file `artifacts/cc-evidence02` packet. This is the first CC correction iteration; earlier exploratory passes are not erased or renamed. CDC retains DTO policy, composition/file fence, D07 prerequisites and the later sizing decision. Once the corrected evidence is sufficient, use it to make those decisions rather than open another general research loop.

## Correction iteration01 review — 2026-09-21

**Verdict: partial corrections reproduced; return R1–R3 for iteration02.** Reviewed commit `5d94ef8d8da18b636279553ed037b906259b2882`, assigned by [cc-prompt-iteration01.md](cc-prompt-iteration01.md) at `ff7c50dbfe13eb51477b6aef4d2f203e63469359`. The Operator relayed the report from the separate CC context. The preceding review remains historical; this section is the current disposition. No S01–S07 row or Slice01 acceptance is closed.

### Reproduced and retained

[Review results](artifacts/cdc-review02/result.json), [commands/output](artifacts/cdc-review02/execution.log), and the [review script](artifacts/cdc-review02/review.py) preserve the checks. CDC ran the actual submitted `--verify` against the original sealed packet: exit 0, unchanged seven-file hashes, 117 correct classifications, ten roots, twelve exclusion keys and 22 matching source fingerprints. CDC separately compared the **actual submitted** replay JSON to the pass05 baseline: equal, including all 16 reads, two gates, three preflight cases and three original controls. This confirms these observations, not integrated conformance or the design of the CDC-authored historical harness.

All **110 manifest entries under Project01 at the reviewed commit** matched. This explicitly scoped denominator includes Slice01 and Slice02; it is not a claim that the prior 87-entry review gained only six files. Source remained clean at `3e3c5410d3863118fdba694fb0cd51baeb7102f9`. The CC delivery contains its seven allowed files and required commit trailers. No database, private export, source build, dependency installation or application suite was used.

CDC ran self-test on a disposable packet copy because it appends to the supplied log. It returned 14 control entries marked `rejected:true`; thirteen are negative-control entries and the last is an unchanged-packet **positive** check. The original packet was untouched. CDC also injected an incorrect source-head observation into the actual `verify_packet` path; it rejected before invoking the injected harness (zero calls). Thus the production preflight ordering works for that control, although CC's tuple-expression sentinel does not test it.

### R1 continuation — submitted replay is not verified; controls overstate coverage

`cc-evidence02/replay.py:374–399` validates the manifest/inventory and compares a fresh run only to the older pass05 result. It never loads the submitted `replay-result.json`. CDC copied the packet, changed its submitted `success` from true to false, recomputed the copied manifest, and ran the actual CLI verifier. **Exit 0: the incorrect submitted result was accepted.** The unchanged actual delivery is correct, but the reusable verifier cannot establish that fact. Compare submitted, baseline and fresh results with the same key-preserving predicates; add resealed submitted-result mutants through the actual verify path.

Self-test at lines 410–462 checks preflight and then calls a sentinel in a tuple expression, rather than invoking the verification path with an injected runner. Its final positive preservation check is recorded as a rejection. The report claims rejection of mutation during verify, but the injected runner never mutates the copy. These are control/reporting defects, not evidence that all preflight guards are broken. Separate positive and negative outcomes; test actual preflight ordering and a real temporary-packet mutation. A default self-test against an already sealed packet must not append to that packet; emit results to stdout or use temporary storage.

### R2 continuation — inaccurate projection survivors and read-view mapping

The improved Date, embedded file identity and full-lineage observations are useful. The semantic map is still not safe input for public DTO design:

- `nestedExclusions[].permittedSiblings` lists other **excluded** paths as permitted: `resultClaim` beside `completionWakeup`; `organic[].sitelinks[]` beside organic highlights; and places/news/shopping/relatedSearches under multiple web-search exclusions. Source `packages/data-schemas/src/methods/message.ts:456–481` excludes these together. Compute public survivors against the complete exclusion set; distinguish source-declared siblings from surviving siblings. Never drop whole arrays to remove a nested member.
- Applicability confuses “used somewhere in a turn” with the named `readConversationForTurn` result. All seven message roots are marked established for `turnConversation`; conversation roots are marked established for `serverHistory`, although that read returns messages. `subagentThread` affects public admission but is not a public message property. `contextMeta` is excluded from public output. The named-operation definitions are in pass05 `read-contract.md`; explicitly describe presence, exclusion, admission-only use or non-applicability, rather than labeling them all established.
- Closed local members remain omitted or collapsed into parent references. For example, `TFile.metadata` is a parent-only row despite its named fields at `types/files.ts:199–217`; content has no member rows for the known `backgroundTask.version/taskId/toolName/status/cancelled` or resultClaim's kind/claimId/generationId; contextMeta fading leaves occur in prose, without member-level domains/default/null evidence. `TAttachment`'s numeric-expiry variant and metadata's file_search/memory/ui_resources/workspaceChange branches are absent from member rows. These are declared-shape gaps under iteration01, not a request to infer historical Mixed values.

CDC reviewed these concrete contradictions, not every possible nested source value. Complete the already-scoped local declaration inventory with reusable type records if helpful, retaining explicit external/open boundaries and domain mismatches. A type declaration alone does not establish a runtime producer; witness excerpts must cover the claimed enclosing symbol or state their narrower evidence strength.

### R3 continuation — logged queries omit required populations

`fresh_query` at lines 301–353 selects `conversationSchema`, but the matrix's actual record name is `convoSchema`. Its logged output is `[]` (execution.log lines 167–174, repeated later). The ancillary query requests top-level providerOnly/interfaceOnly/implicit; those properties belong to each `records[]` entry and the log returns nulls (lines 139–146). CDC reproduced both mistakes. Correct data contains 44 message and 73 conversation fields, provider-only counts 10/13, interface-only counts 4/3, and four implicit keys per record. The full census validator is separate and still passes; query coverage cannot be inferred from it.

Retain corrected complete outputs and assert expected record identities, exact field membership/counts and required ancillary keys. Fail a required jq query on every nonzero exit, and fail a successful-but-empty/wrong-shaped projection. Preserve raw failure records before stopping. Update the intake/report from actual loaded extents and outputs; do not reinterpret the old empty/null outputs as complete reads. The old review path written as `artifacts/cdc-review01/cdc-verification.md` is also incorrect; the review lives at the slice root.

### Return and design ownership

[Iteration02](cc-prompt-iteration02.md) is the second CC correction, pending Operator relay and CC acknowledgement. It repairs the existing evidence assignment in a new seven-file `cc-evidence03` packet and preserves all older packets/prompts. R1–R3 remain partially resolved until the above checks pass. All 27 project/arc/slice acceptance rows remain open. Concrete DTO/codec/patch policy, injection scope, D07 source-build readiness and production sizing remain CDC-owned; none is delegated implicitly by this correction.

## Correction iteration02 review — 2026-09-21

**Verdict: R1 and R3 corrections reproduced; R2 returned for a declaration-grounded repair.** Reviewed CC commit `0f81e318bdd78619b5092c188c5149ae5178de35`, assigned by [cc-prompt-iteration02.md](cc-prompt-iteration02.md), currently introduced in planning history at `a0c16f4031ca050e226b501db72387d1177fa45e`. Its prompt bytes equal those at the previously recorded `fa5515be9`; historical review identities remain preserved. The Operator relayed CC's return to the existing CDC context. No acceptance row or slice closes.

### Reproduced checks and disposition

[Results](artifacts/cdc-review03/result.json), [raw commands/output](artifacts/cdc-review03/execution.log), [review driver](artifacts/cdc-review03/review.py), and [syntax-only declaration extractor](artifacts/cdc-review03/declarations.cjs) record this pass. CDC verified the seven packet files against the reviewed commit, its allowed commit scope and both trailers, and all **119 Project01 manifest entries at that commit**. Source stayed clean at `3e3c5410d3863118fdba694fb0cd51baeb7102f9`; original packet hashes were unchanged throughout. No database, private corpus, build, package install or application suite ran.

- **R1 resolved for the assigned evidence correction:** actual sealed CLI verification and self-test passed. All fifteen negative controls rejected; failing preflight runner calls totaled zero and the valid sentinel ran once. The submitted replay equals the pinned baseline; submitted-to-baseline, fresh-to-submitted and fresh-to-baseline comparisons pass. Separate CDC CLI tests with resealed `success:false` and wrong `node` results both reject. Final packet mutation rejects and sealed self-test leaves the original packet untouched. These establish the repaired paths, not arbitrary-input formal correctness or integrated Mongo conformance.
- **R3 corrected data coverage reproduced:** independent complete projections match the pinned matrix exactly: 44/73 unique fields, 10/13 provider-only names, 4/3 interface-only names and four implicit keys per record. The committed corrected queries/logs use the right record names and per-record ancillary fields. Reading receipts remain CC-attested; source-reference support is reviewed separately under R2. The old empty/null query outputs remain historical failures.
- **R2 only partially repaired:** message versus conversation applicability is mostly corrected, and the actual sibling lists no longer name directly excluded leaves. Containers such as organic/topStories legitimately survive with nested removals; the review explicitly separates those partial containers from excluded leaves. Nevertheless, the map's types, paths, presence claims and two view dispositions remain unreliable.

### R2a — wrong applicability and incomplete composed-exclusion predicate

`metadata.publicMessages` says `public exclusion`; source `CLIENT_MESSAGE_SELECT` excludes **metadata.thoughtSignatures**, not the whole metadata object. `subagentThread.accessProbe` says `not selected`, contradicting `getConvoOwnership`'s `user tenantId subagentThread` projection at `methods/conversation.ts:2060–2078`. The report claims full-lineage selection while the actual inventory says the opposite; the latter is the artifact to repair.

`replay.py:239–253` compares each permitted sibling only with its owning exclusion. CDC replaced a completionWakeup sibling with `content[].tool_call.backgroundTask.resultClaim`; the validator **accepted** it, although another exclusion removes resultClaim. The existing self-test covers only a sibling equal to its own exclusion. Validate against the whole exclusion set. Ancestor containers need explicit nested-removal obligations, not blanket rejection: retaining organic[] while removing each element's highlights/sitelinks is correct.

### R2b — unsupported fields, invented path segments and erased type information

The inventory contains **274 members; 257** use `declaredType: "declared local type; see sourceRefs"`. Domains often name a resource instead of a value type; repeated broad source refs do not support each row. Examples below were checked directly and against a syntax-only extraction of eleven pinned declarations. That extraction is evidence of literal source syntax, not a portable DTO generator or full type resolver.

| Submitted claim | Source-backed correction |
|---|---|
| `userSubmittedMessageFieldPaths[].source` and `.operation` are declared members | `filters.ts:184–191` declares a strict object with only `path` and `field`; both are required within each element. The validator itself incorrectly requires `.source`. |
| `examples[].input/output.role` and `.files` are declared fields | `schemas.ts:867–874` declares input/output objects containing required content strings. Storage remains Mixed; this does not prove historical values lack other fields. |
| `content[].error.text` and `content[].summary.boundary.contentIndex` | Error and summary are discriminated branches of a content element, not nested `error`/`summary` wrapper objects. The element has `.text`/`.error` in the error branch and `.boundary.contentIndex` in the summary branch (`types/content.ts:195–220,244–315`). |
| Message `metadata.codeEnvRef`, runFile and related fields cite `TFile` | `TFile.metadata` describes embedded file metadata, not the open message metadata record. Names may exist in historical records, but this citation does not establish their declaration or producer at the message root. |
| settledAt is optional with a placeholder type | `Agents.ToolCall.backgroundTask.settledAt` is `Date`, required when the optional backgroundTask object exists (`types/agents.ts:103–117`). The Date distinction explicitly requested in earlier prompts is lost in the member row. |
| `subagentThread.parentAgentId` is required | `subagentThreadLineageSchema` declares it optional (`schemas.ts:1102–1113`). |
| `files[].file_id` is required as a root file member | `TFile.file_id` is required in TFile; `TMessage.files` is `Partial<TFile>[]`. Those declaration and application contexts must remain separate; Partial is shallow. |
| `attachments[].variant2.expiresAt` is an optional data path | `variant2` is an analytical branch label, not a property. The numeric expiry is required within that attachment union branch (`schemas.ts:1054–1061`). Other fabricated variant path segments have the same problem. |
| Processed fields are placed at `attachments[].web_search.content/highlights` | ProcessedSource is intersected into organic/topStories elements, not SearchResultData itself (`types/web.ts:25–58`). Preserve the actual array and member positions. |

The current validator's minimum member count and hand-authored required-path sets force some incorrect rows, including `.source`, the summary wrapper and message metadata.codeEnvRef. A row count is not a declaration-completeness oracle. Correct those predicates together with the data; do not add invented rows to satisfy them.

### Focused return and next design work

[Iteration03](cc-prompt-iteration03.md) is the **third CC correction**, pending Operator relay/acknowledgement. R1/R3 mechanisms and reproduced observations are retained; R2 must be rebuilt from literal declarations and checked member-by-member, with branch labels separate from data paths and explicit wrapper/presence semantics. Source-based exact-membership controls replace padding the map to a target count. Preserve all previous packets and reports, including these failures.

This is a change in evidence method within the same ten-root assignment, not new application scope. All S01–S07, Slice01 acceptance and the 27 Project01/Arc01/Slice02 criteria remain open. CDC continues to own DTO/codec/patch decisions, injection scope, D07/runtime/build readiness and production sizing. The map cannot yet support those decisions as a complete, validated field contract.

## Correction iteration03 review — 2026-09-22

**Verdict: actual replay and R3 queries reproduced; R1 regressed and R2 remains incomplete. Return for a fourth correction.** Reviewed CC commit `76d15b5d33668e3c50ddd3db7b98a8e6c12a814c`, assigned by [iteration03](cc-prompt-iteration03.md) at `d31a81ab341225303f0861a3c85396ca5a9ddacf`. The Operator relayed the separate CC context's report. This is CDC review under the existing two-contributor workflow; no CRC, source implementation or slice closure is implied.

[Review results](artifacts/cdc-review04/result.json), [raw commands/output](artifacts/cdc-review04/execution.log) and the [reproduction script](artifacts/cdc-review04/review.py) retain the evidence. The script retrieves the exact recipe bytes from the reviewed Git commit, verifies the original seven files against those committed bytes, executes the actual CLI, and confines mutations to temporary packet copies. Its injected preflight and runner tests are identified separately from unmodified CLI runs. Reproduce into a fresh output directory; the script refuses to overwrite a sealed review.

### Retained progress and limits

- The actual submitted result equals the pinned pass05 baseline. The unmodified CLI `--verify` succeeds; fresh/submitted/baseline comparisons match for 16 reads, two gates, three preflight cases and three original controls. A separate resealed `success:false` CLI mutant correctly rejects.
- The sealed self-test succeeds and reports two positives plus eleven rejected controls. Original packet hashes remain unchanged. These are actual outcomes; their semantic strength is qualified below.
- R3's fresh complete matrix projection and all five committed capture-query outputs agree: 44/73 fields, 10/13 provider-only, 4/3 interface-only and four implicit keys per record. This remains resolved for the query-coverage correction. Reading receipts remain attested.
- All **129 Project01 manifest entries present at the reviewed commit** pass; all eleven supplied source fingerprints match. Source is clean at `3e3c5410d3863118fdba694fb0cd51baeb7102f9`. The commit has exactly seven allowed files and both trailers.
- Literal declaration extraction is a substantial improvement: 46 records and 226 generated member rows replace the earlier placeholder types. Path-marker keys, example content fields, Date leaves, parentAgentId optionality, metadata's nested exclusion and the full ownership-probe selection have concrete repairs. However, the generator and validator share interpretation logic; their equality is not an independent completeness or semantic oracle.

No database/private export, application build, dependency install or application suite ran. Node22/storage-double limits remain; D07/Node24, integrated Mongo conformance, historical BSON populations and all acceptance gates remain open. CDC cannot independently accept its own old harness merely by replaying it.

### R1 regression — verification bypasses preflight and loses preservation checks

`cc-evidence04/replay.py:798–814,918–924` invokes validate_packet from both verification modes without calling `preflight`. That function is called only by capture. The optional `observed` argument checks two manually supplied values; the ordinary CLI supplies none. CDC injected a failing environment guard into the **actual main/verify path** and counted calls: guard **0**, runner **1**, accepted. This proves the guard is bypassed; it is not a claim that the real checkout/runtime was changed during review. Equality against baseline may catch some drift later, but does not preserve fail-before-execution behavior or the complete pinned-input checks.

There is also no end-of-verification packet hash comparison. CDC's disposable runner changed report.md and returned the otherwise matching baseline; validate_packet accepted. The original packet was never changed. Evidence03 had both the production environment path and final hash comparison; iteration03 expressly required preserving them.

Coverage also regressed (`build_coverage`, lines 451–479). Its selected set uses `convo` while the normalized record is `conversation`; the hidden-field and conversation.messages rules were dropped. The result has **7 selected / 110 other**, versus the source-matrix classification **10 selected / 14 hidden / 1 physical relationship / 92 other**. All 117 identities remain present, but eighteen classifications are wrong. Comparing against the same new builder accepts the mistakes.

### R2 — declaration extraction still lacks correct application closure

The root map (`build_roots`, lines 482–560) is manually assembled from selected extracted declarations, without a complete resolvable application graph:

- TAttachment's third `Partial<Pick<TFile,'filename'|'filepath'>> & Pick<TFile,'conversationId'> & TAttachmentMetadata` branch has no member applications. Numeric expiresAt is labeled generically `attachment-union`, detached from the selected numeric-expiry fields. The report claims a `partial-filename-filepath-pick` branch that is absent from the submitted map. Source: schemas.ts:1054–1061.
- Computed keys become literal paths such as `attachments[].[Tools.web_search]`, not `attachments[].web_search`. SearchResultData/ProcessedSource declarations exist in the table, but no explicit graph applies them under the web/file search use sites. The root calls local SearchResultData an open boundary. Reusable local declarations are allowed; unresolved local application edges are not the same as a declared external/open value.
- Summary `Array<{type; text}>` elements are not traversed; FileContext/FileSources enum declarations and local WorkspaceChange/MemoryArtifact/UIResource definitions are missing. Other captured content/file declarations are not consistently linked at their use sites. CodeEnvRefBase is expanded, but CodeEnvRef union/record applications remain a prose boundary. Source witnesses in result.json show the relevant declarations and exact revisions. These are existing selected-root dependencies, not additional subsystem research.
- `contextMeta.publicMessages` again says included, although CLIENT_MESSAGE_SELECT excludes the entire root. The generic applicability function treats it like other message members. The actual new metadata and full-lineage corrections are retained.
- The validator compares selected member fields but omits application-context/wrapper semantics except one file_id prose check, ignores supplied source fingerprints, and silently collapses duplicate member keys. The actual supplied fingerprints are correct; the defect is acceptance of forged submitted fingerprints.

### R2 — projection obligations remain bypassable

`validate_projection`, lines 646–665, loops only over supplied partialContainers; removing the list skips the obligations. It accepts a subset of actual nested exclusions (`expected <= actual`), so organic with only sitelinks removed passes despite omitted highlights. Strings containing ` except ` skip survivor validation completely. Every survivor must instead establish the exact applicable removal set against the full exclusion set; metadata also needs its thoughtSignatures obligation. Source root exclusions must separately inform root applicability.

CDC ran the actual committed CLI on nine disposable, resealed packet variants. Eight incorrect inventories were **accepted**:

1. Remove all retained-container obligations.
2. Omit organic.highlights from required removals.
3. Claim excluded resultClaim survives with a freeform `except nothing` suffix.
4. Change filename's Partial application to required.
5. Replace file_id's declared use-site wrapper with TFile[].
6. Supply a false source fingerprint.
7. Duplicate a strict path-marker member.
8. Assert contextMeta is fully public.

The ninth control, submitted success:false, rejects correctly. The production-path preflight and mid-verification packet-mutation checks above are separate injected tests, not included in this nine-CLI denominator.

Two of CC's eleven nominal semantic controls reject at missing `sourceRefs` (KeyError), before testing the intended invented path. The file_id control changes local TFile requiredness rather than testing incorrect effective Partial behavior. Self-test catches arbitrary Exception, so a crash can count as a successful semantic rejection. Use well-shaped single-defect mutations, explicit evidence errors and actual runner-call assertions. Keep positive checks separate.

### Disposition, ledger walk and next assignment

| Row | Current disposition |
|---|---|
| S01 | Open; reproduced read behavior is retained, composition/caller policy remains CDC-owned. |
| S02 | Open; concrete declaration repairs are useful, but classifications/application closure are not reliable enough for final DTO decisions. |
| S03 | Open; presence/Partial/branch/projection distinctions still need correction; patch/codec policy remains separate. |
| S04 | Open; cursor evidence and independent-verification requirement are unchanged and outside this packet review. |
| S05 | Open; repository preservation does not discharge original-corpus fidelity obligations. |
| S06 | Open; no production fence/build/conformance acceptance; R1 verifier guards must be restored. |
| S07 | Open; scope/manifest/commit checks reproduced; R1/R2 prevent accepting the packet as complete. |

[Iteration04](cc-prompt-iteration04.md) is the fourth correction, awaiting Operator relay and CC acknowledgement. It restores evidence03's verified guards/classification rules, preserves R3, separates syntax from application semantics, supplies worked source-to-application examples, and makes all accepted counterexamples regression requirements. A representative internal validation pass precedes expansion across the unchanged ten roots. No full typechecker, general-purpose schema system or application implementation is assigned.

The recurrence is now recorded as a method/sizing concern: replacing previously verified infrastructure introduced regressions while same-generator equality hid incomplete interpretations. This warrants a bounded corrective method, not an automatic framework edit or a reset of history. The Operator asked to leave framework guidance unchanged; no skill/framework files were edited. Prior exploratory passes and the three completed CC corrections remain in history; the five-correction cap is unchanged. All 27 project/arc/slice rows and Slice01 acceptance remain open. CDC owns remaining DTO/codec/patch policy, injection, D07 and eventual implementation sizing.
