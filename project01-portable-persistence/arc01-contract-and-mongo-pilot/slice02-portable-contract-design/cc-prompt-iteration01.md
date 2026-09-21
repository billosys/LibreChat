# CC iteration01 — correct Slice02 evidence tooling and nested map

## Assignment and outcome

You are CC in the Operator-selected CDC + CC workflow. Execute this first correction iteration and return the new evidence to the existing CDC design conversation through the Operator. Predecessor: [cc-prompt.md](cc-prompt.md). Reviewed delivery: `99d5ecd794d00cd1c0db7a199633042766af5953`, `artifacts/cc-evidence01`. Review: [cdc-verification.md](cdc-verification.md), findings R1–R3. This prompt supersedes the initial execution assignment, not its preserved contents or the slice's acceptance contract.

The useful results stand: CDC reproduced the exact 16 reads, two gates, three preflight cases, three controls, correct 117 classifications, ten-root membership, twelve exclusion strings, 23 source fingerprints and all 87 historical/CC artifact hashes. Do not repeat older research passes or restart the architecture investigation. Repair the bounded packet's verifier, missing nested detail and inspection evidence. No production implementation, database access, historical corpus inspection or slice closure is assigned.

Paths: `PLAN=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`; `SOURCE=/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`; `SLICE=$PLAN/project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design`; `OUT=$SLICE/artifacts/cc-evidence02`. Planning branch is `planning`; pinned source remains `3e3c5410d3863118fdba694fb0cd51baeb7102f9` on `billo-guildhall`. Resolve and record the commit introducing this iteration prompt and its SHA-256. Verify this is still the active assignment. Record your real context description and acknowledgement in the new intake before dependent execution.

Only these **seven new files** may be created/committed under `OUT`:

```text
intake.md
report.md
nested-fields.json
replay-result.json
execution.log
replay.py
SHA256SUMS
```

Preserve `cc-evidence01`, all CDC review files, all prior artifacts and issued prompts unchanged. Do not update plans/ledgers, change source/dependencies, create source branches, run builds/application suites, touch private exports/live DBs, restart services, push or create PRs. Preserve unrelated working/index files. Findings are evidence for S01/S02/S03/S06/S07; all S01–S07 and Slice01 acceptance remain open. CDC owns final DTO/codec/patch policy, composition fence, D07 and implementation sizing.

## Reading and preflight

**Required-full, in order:** this prompt, predecessor `cc-prompt.md`, current `slice-plan.md`, `ledger.md`, `cdc-verification.md`; the prior CC `intake.md`, `report.md`, `replay.py`, `execution.log`; PLAN `AGENTS.md`, `BILLO.md`, `README.md`; SOURCE `AGENTS.md`, `BILLO.md`, `CLAUDE.md`; pass05 `read-contract.md`, `protocol.md`, `experiment.cjs`, `validate.py` and pass04 `handle.cjs`.

**Required-section:** the initial prompt's project/arc and framework reading sections remain binding. Use their exact named paths/sections: project Goal/boundaries, Definition of done and Workflow/authority with transition/Expedited subsections; arc Scope, Slice roadmap and Workflow/source boundaries; engineering-methods investigation/intake and methodology role/two-contributor/transition sections. The independent-verification and scientific-methods evidence/validity guides listed in that prompt remain required-full. This iteration changes the output home, driver shape and completeness requirements, not the workflow or architecture.

**Required-data:** load the full 117-field projection and all ancillary populations specified by the initial prompt, the ten roots and twelve exclusions from `cc-evidence01/nested-fields.json`, all behavior/provenance records in its replay result, and `artifacts/cdc-review01/result.json` including its four verifier controls. Execute and retain the actual queries and complete selected outputs; partition rather than silently truncate. This is query coverage, not a claim to have semantically read every source file.

**Required source sections:** the initial prompt's ten-root initializers/types/projections and needed definitions still govern. For R2, also read complete `SearchResultData`, `ProcessedSource`, `ProcessedOrganic`, `ProcessedTopStory`, `OrganicResult`, `TopStoryResult` in `packages/data-provider/src/types/web.ts`; complete `Agents.ToolCall` in `types/agents.ts`; complete `TFile` in `types/files.ts`; complete `getConvoOwnership` in `packages/data-schemas/src/methods/conversation.ts`. Follow local selected-field definitions to their explicit open or external-SDK boundary; do not survey unrelated actor or SDK internals. Read complete enclosing functions for each claimed producer/consumer witness. Record any inaccessible dependency as unresolved rather than assuming its type.

In `intake.md`, record **actual** loaded file/section/declaration extents, revision, any truncation recovery, and required-data query coverage separately, with concise source-cited readback. Use tool-output IDs when exposed; otherwise record truthful visible ranges. Do not manufacture past receipts. Prior prose-only failed-attempt notes remain reported-only; record that limitation and capture fresh checks accurately. Coherent preflight authorizes execution without another permission exchange.

## R1 — implement a verifier that preserves evidence and rejects drift

Keep the Python-standard-library driver small. Separate authored `nested-fields.json` observations from predicates that validate their coverage. Remove the old behavior of regenerating the submitted inventory during verification.

Provide these entrypoints in `replay.py`:

```text
python3 replay.py --capture --packet /absolute/path/to/cc-evidence02
python3 replay.py --verify --packet /absolute/path/to/cc-evidence02
python3 replay.py --self-test
```

- `--capture` is authoring-only. Refuse before any mutation if `SHA256SUMS` exists in the destination. Read the already-authored inventory; write the new replay result/log only after prerequisite checks. Append raw commands/results and preserve prior failed replay bytes in the log before any retry replacement. Never overwrite the inventory or report. Missing prerequisites produce a nonzero exit and truthful blocked record, not `success:true`.
- `--verify` is read-only for the packet and source, including after sealing. Validate the actual committed/submitted inventory and manifest, run the existing sealed pass05 harness into a fresh temporary directory, compare results and emit its command/result record to stdout. Hash the packet before/after and require equality. Default/no-mode invocation prints usage or acts read-only; it must never capture implicitly.
- Before either mode executes the harness, verify source revision/branch and relevant dirty-state constraints; pinned input hashes from the sealed manifests; actual Node `v22.22.3` and compiler `5.9.3` plus sealed compiler digest; the harness and prior-handle digest; and every source fingerprint claimed by the new inventory. This reproduces the historical harness environment, not the repository's Node 24.16.0 build gate. Do not install missing tools. Preserve unrelated untracked files; if a prerequisite cannot be established, stop the dependent replay and report it.
- Exact equality is required for all behavior fields and, on this host, all provenance fields: `sourceHead`, `node`, `compiler`, `sources`, `experimentSha256`, `priorHandle`. There is no wildcard “allowed difference” list. A relocation/runtime refresh would require a separately named policy, not automatic acceptance. Preserve absent versus present-null keys when comparing JSON; `.get()` equivalence alone does not establish key presence.
- Validate coverage membership/uniqueness and each classification against baseline information, not the authored classification or just its total. Use selected root keys first; conversation `messages` is the physical relationship; other `defaultRead == hidden` fields are hidden; the remainder is the outside-deep-inspection class. Validate all ten root keys, twelve exclusion keys and required record members without treating filled prose as semantic proof. Check source refs against actual files/hashes and line bounds; CDC reviews whether the cited text supports the claim.
- Scope old-manifest checks to a recorded input set (e.g. manifests at the reviewed CC commit), so adding a later review packet does not silently change a historical denominator. Do not hard-code today's global `rglob` total as a forever-valid check.

`--self-test` must exercise the **same predicates/preflight path** used by verification, with temporary fixtures or injected read-only observations. Require a valid control, then rejection of wrong runtime, source head, compiler digest, source-file digest, invalid/misassigned classification, missing/duplicate field, and absent-versus-null provenance/behavior keys. For preflight failures use a runner sentinel to show the harness was not invoked. Test capture rejection against a sealed temporary packet and verify-mode packet hash preservation. Never alter the real source, installed binaries or sealed packets to create controls. Retain outputs/status for the controls and verification in `execution.log` before sealing.

## R2 — complete the already-scoped nested map

Keep the same ten roots and complete 117-field denominator. Do not replace the inventory with a broad future schema or require the private corpus. Retain the original JSON top-level keys and improve each root's data:

- `members`: source-backed path/member rows with array boundaries, declared storage/server/provider domains, required/optional/default/null evidence, and explicit open/Mixed/SDK boundaries. Closed local nested declarations must expose their named fields, not just link a parent type. A declaration proves a type claim, not the historical value population.
- `applicability`: explicit `serverHistory`, `publicMessages`, `turnConversation`, `accessProbe` dispositions with source refs or `not applicable`/`not established` and reason. A single generic sentence for every root is insufficient.
- `witnesses`: full repository-relative path, enclosing symbol, line span and observation, or a precise bounded-search record establishing that no witness was found. `BaseClient and formatMessages` without a locator is not a witness. Identify producer/consumer/type-only evidence separately.
- `nestedExclusions`: for each exact projection string, record the traversal with array positions (for example `attachments[].web_search.organic[].highlights`), the removed member, and concrete permitted siblings with source refs. Record a type/shape gap explicitly if it cannot be established; do not invent it. Mixed historical values remain uncharacterized.

Mandatory source-backed details that the earlier packet missed:

1. `content[].tool_call.backgroundTask.settledAt` is declared Date; `resultClaim.claimedAt` is also Date, but `resultClaim` is publicly excluded. Keep that difference explicit, including the separate `completionWakeup` exclusion whose source shape must be traced or marked unresolved.
2. `TFile` includes optional `_id`/`__v`, Date/string expiry and timestamps, and nested metadata. These require an explicit future policy decision for embedded file/attachment values. **Do not strip or stringify them now.** Top-level message physical-ID privacy does not itself resolve embedded payload semantics.
3. `SearchResultData.organic[]` and `topStories[]` add array boundaries beneath `attachments[]`. Inspect permitted siblings, not only the twelve excluded strings. Add every newly used source to the fingerprint list.
4. `getConvoOwnership` currently selects the lineage object in `subagentThread`; it is used as a child discriminator. Distinguish that actual shape from a possible future reduced probe DTO and from public HTTP response data.

The original declared-field/property and source-preservation obligations remain. Do not infer requiredness or a JSON vocabulary from repeated names. For source/provider mismatches, record both declarations and exact consequence/question rather than quietly picking one. CDC will settle policy from the corrected inventory; no additional codec experiment or live-value survey is assigned.

## R3 — capture truthful, inspectable reading and query evidence

Retain fresh required-data query argv/code, cwd, exits and complete projected results in `execution.log`, plus the bounded witness-search commands/results and selected enclosing-function read ranges. Keep text reading coverage in `intake.md` distinct from computational coverage. Partition large outputs and recover truncation before marking a read complete. Do not claim the old failed attempts have raw evidence when only a retrospective description survives; carry that limitation visibly into the new report. Do not copy private data or secrets.

## Return, seal and commit

`report.md` identifies this iteration and the reviewed delivery; dispositions R1–R3 with concrete evidence; reports checks including failed/blocked attempts; walks S01–S07 as still open; and identifies unresolved **CDC-owned decisions**. Preserve useful findings from evidence01 and explain corrections. No new architectural recommendation is needed unless a source contradiction materially changes the boundary.

Run capture and controls. Inspect the exact seven-file inventory and JSON; check old artifact/source preservation and `git diff --check`. Finish logs before computing `SHA256SUMS` for the other six files. Run read-only verification again after sealing, retaining its console output through the execution environment without appending to the sealed log. Report the final verification result and packet hashes; if it fails, retain the attempt and repair only the new unissued packet with explicit resealing history, never evidence01.

Commit the seven individually named new paths on `planning` using `git commit --only -F <message-file> -- <seven paths>`; inspect the index first and preserve unrelated staged work. Every commit ends with exactly these trailers:

```text
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

Return the commit and project-relative `arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/cc-evidence02/report.md` to the Operator for CDC review. Stop after this correction packet. No ledger closure, next slice or further autonomous research pass follows.
