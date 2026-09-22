# Slice02 — Portable contract design

| Metadata | Value |
|---|---|
| Slice | slice02-portable-contract-design |
| Arc | [Arc01](../arc-plan.md) |
| Status | Active — design preparation; not implementation-ready |
| Workflow | Two contributors: CDC + CC; Expedited Mode |
| Assignment | [cc-prompt-iteration03.md](cc-prompt-iteration03.md), third correction for R2 declarations/projection map; R1/R3 reproduced; pending Operator relay/CC acknowledgement |
| Source baseline | Current CC inspection: `3e3c5410d3863118fdba694fb0cd51baeb7102f9` on `billo-guildhall`; first-pass evidence remains at `ba44443fdb232bbe6d4977e2619774b5a72586ac` |
| Artifact home | `artifacts/` within this slice |
| Depends on | Slice01 attested evidence; unresolved findings retained below |
| Blocks | Slice03 implementation assignment |

## Authority and starting state

On 2026-09-20 the Operator read the Slice01 report, called it a good start, asked whether bubble-up was done, and instructed: “Please continue, regardless!” Slice01's findings were already incorporated into the arc/project plans in `a085652ce`. This instruction authorizes continued contract-design preparation using that evidence. It does not constitute independent reproduction, close Slice01, or authorize a source conversion with unresolved design choices. The prior blanket hold on advancement is superseded for this preparatory work only. Existing acceptance requirements remain open.

## Capability and boundaries

Specify the ordinary message-save/conversation-update/read contract deeply enough to prepare a bounded, reviewable Mongo conversion. Separate present behavior, proposed contract decisions, deliberate future improvements, and unsettled choices. Carry the source-preservation obligations into the design without implementing import or SQLite.

Write only this slice's planning/evidence files and necessary parent-plan, ledger, README and interface-proposal corrections. Inspect source and run bounded synthetic experiments in disposable databases. No application edits, source branch creation, dependency changes, live corpus access, corrective imports, service restarts, or Rust implementation. Do not turn a characterization finding into an incidental fix.

## Inputs and work sequence

1. Read the project/arc plans and ledgers; Slice01's dependency map, B01–B22 behavior matrix, D01–D09 design inputs and retained test baseline; the source instructions and applicable framework guides. Source statements are pinned to the baseline above, not inferred from earlier proposals.
2. Draft operations and context, identity/value/patch rules, named read projections, lifecycle ownership, partial outcomes and compatibility mapping in `artifacts/contract-design.md`. Resolve Mongo relationship translation before freezing signatures. An unresolved alternative stays visibly open.
3. Characterize D05's equal-key cursor risk using the predeclared `artifacts/pagination-protocol.md`. Preserve the harness, all attempt metadata/raw output/results and hashes. This is a controlled property check, not a performance benchmark or independent validation. No existing suite rerun without a new reason.
4. Design discriminating conformance cases and the proposed code fence in the contract document. Account for import losses, adjacent legacy callers, source/dist parity, runtime and branch prerequisites. Determine whether the implementation still fits one slice after remaining choices are resolved.
5. Bubble actionable findings into the parent plans immediately. Keep criteria open until their evidence and review requirements are satisfied. The Operator has now selected CDC + CC. Execute only the bounded evidence prompt issued below; once the design is complete, CDC prepares the source-grounded production implementation assignment using the prompt-authoring guide.

## Verification and exit

Every contract choice must trace to a current caller requirement or a clearly labeled intended change. Check scoped authorization, field-state distinctions, no-upsert and retry/partial-commit behavior explicitly. Demonstrate that the public dependency graph and DTO census can exclude engine details before declaring implementation readiness. Synthetic experiments must fail closed on database target selection and retain unsuccessful attempts. Verify Markdown links, source cleanliness, exact artifact inventory and hashes, and explicit-path commits. Historical self-checks remain attested. New CC work returns to CDC for actual review; a replay of an old harness does not by itself establish integrated conformance or acceptance.

The slice is complete only when all ledger criteria have concrete dispositions, the consequential choices are resolved, the implementation fence and conformance recipe are precise, and applicable review gates are satisfied. A first draft does not close this slice.

## Assignment history

| Assignment | Date | Predecessor | Reason | Disposition |
|---|---|---|---|---|
| This slice plan v1.0, current conversation | 2026-09-20 | Slice01 evidence packet | Operator explicitly requested continuation after reading the report | Historical one-contributor investigation through pass05; superseded for execution by the initial CC prompt |
| [cc-prompt.md](cc-prompt.md) | 2026-09-21 | One-contributor design passes 1–5; no prior CC prompt | Operator selected CDC + CC; replay pass05 and inventory ten nested roots for CDC decisions | Returned by separate CC context at `99d5ecd794`; CDC reproduced replay/counts and returned R1–R3 for correction |
| [cc-prompt-iteration01.md](cc-prompt-iteration01.md) | 2026-09-21 | [cc-prompt.md](cc-prompt.md), delivery `99d5ecd794` | CDC review R1–R3: verifier/preservation, nested detail and inspection evidence | Returned at `5d94ef8d8`; CDC reproduced partial repairs and returned remaining R1–R3 defects |
| [cc-prompt-iteration02.md](cc-prompt-iteration02.md) | 2026-09-21 | [cc-prompt-iteration01.md](cc-prompt-iteration01.md), delivery `5d94ef8d8` | Actual verifier accepts resealed incorrect submitted results; nested public/view mapping and query coverage need correction | Returned at `0f81e318b`; R1/R3 reproduced, R2 declaration/view/projection defects returned for repair |
| [cc-prompt-iteration03.md](cc-prompt-iteration03.md) | 2026-09-21 | [cc-prompt-iteration02.md](cc-prompt-iteration02.md), delivery `0f81e318b` | R2 source-declaration discrepancies and composed-exclusion predicate; retain R1/R3 fixes | Active third correction; pending Operator relay and acknowledgement |

## Historical initial handoff — 2026-09-21

The Operator selected CDC + CC because the investigation had grown involved. This conversation becomes CDC; a separate CC session receives `cc-prompt.md` through the Operator and records its identity/acknowledgement in the permitted intake file. No CC execution or receipt is claimed at issue time. No CRC is enabled. This supersedes the workflow/assignment statements in historical packets, whose contents remain sealed.

The active assignment produces only `artifacts/cc-evidence01/{intake.md,report.md,nested-fields.json,replay-result.json,execution.log,replay.py,SHA256SUMS}`. CC replays pass05 and inspects ten named nested roots against all 117 fields and twelve nested exclusions. It does not implement DTOs, query live data, update plans/ledgers or close the slice. CDC owns nested codec policy, exact composition/file fence, D07 prerequisites, production prompt authorship and sizing. All seven criteria remain open; future CC refinements preserve the initial prompt and use canonical numbered siblings. Prior exploratory passes and any recorded iteration limits are not reset.

### CDC readiness for the initial evidence assignment

1. **Source-grounded:** current source head/instructions, message/conversation/preset/fading definitions, direct types, public projection and the sealed pass05 harness were inspected. Source remains read-only; source drift blocks same-baseline claims.
2. **Design-complete for investigation:** the prompt binds inspection populations, output schema, preservation rules, replay method and stop conditions. Final DTO/Mixed-value policy remains explicitly CDC-owned; no dependent production work is issued.
3. **Guideline-applied:** engineering-methods' investigation/intake rules require source witnesses and complete declared-data coverage; scientific-methods' evidence/validity guides separate replay from conformance; source CLAUDE's Type Safety/Workspace Boundaries rules require identifying existing types and engine-dependent gaps rather than declaring an opaque catch-all portable. Exact guide paths and applied constraints are in the prompt.
4. **Executable:** existing Node/compiler and sealed harness paths are known; the seven-file output fence fits the canonical artifact home. Missing/runtime-drift inputs have explicit blocker handling; no install or DB dependency is added.
5. **Falsifiable:** exact reference/candidate case comparisons retain wrong-owner, missing-projection and eager-strict-scope controls; coverage keys and nested paths are checked as sets, not trusted totals. Semantic interpretation is reviewed from sources, not inferred from hash/count checks.
6. **Coherent/sized:** prompt, plan and ledger retain all acceptance rows and distinguish historical role text. This is one replay plus ten bounded nested-root investigations, not completion of all DTO/composition work; reading/query scopes are bounded and packet creation stops at the decision inputs. No Slice03 source assignment is implied.

## Historical first correction assignment — 2026-09-21

CC returned the seven-file packet at `99d5ecd794d00cd1c0db7a199633042766af5953`, identifying a separate Codex API session without an exposed identifier. The Operator relayed its report. [CDC verification](cdc-verification.md) reproduced all behavior output, the actual classifications and 87 artifact hashes. This accepts those bounded observations for continued design; no ledger row or slice is accepted.

The active [iteration01 prompt](cc-prompt-iteration01.md) corrects R1 (provenance/classification predicates and sealed-packet safety), R2 (concrete nested members, array paths and source witnesses), and R3 (truthful read/query evidence). Its seven-file output home is `artifacts/cc-evidence02/`; the exact filenames remain intake.md, report.md, nested-fields.json, replay-result.json, execution.log, replay.py, SHA256SUMS. CC may not alter evidence01, the review, issued prompts or plans. This is the first CC correction iteration; receipt/execution is pending Operator relay. All seven rows and Slice01 acceptance remain open.

CDC readiness: the review inspected the committed driver/inventory/report and source witnesses, ran the sealed harness in temporary storage and exercised the same verifier predicates with four counterexamples. The prompt supplies concrete CLI modes, preflight/equality/preservation rules, negative-control oracles and the exact ten-root repair method; the required-reading manifest and seven-file fence remain bounded. Domain constraints remain source CLAUDE's Type Safety and Workspace Boundaries, applied as source-backed type reuse and explicit open-value boundaries. The correction does not choose DTO policy or authorize source changes. CDC owns those decisions after the repaired evidence returns; remaining composition/build/sizing work is unchanged.


## Historical second correction assignment — 2026-09-21

The Operator relayed CC's correction at `5d94ef8d8da18b636279553ed037b906259b2882`. [CDC review](cdc-verification.md#correction-iteration01-review--2026-09-21) reproduced read-only verification, the actual submitted replay equality, 117 classifications/ten roots/twelve exclusion keys/22 fingerprints, and all 110 Project01 manifest entries present at that commit. Actual production-path wrong-head preflight rejected before its runner. These results support continued design, not acceptance of a slice or CDC-authored historical harness.

Remaining R1–R3 findings are concrete: the verifier accepts a resealed submitted `success:false` result; self-test/reporting confuses positive preservation with mutation rejection; the nested map lists excluded siblings as permitted and conflates message/conversation/admission views; declared nested members are incomplete; and the logged queries returned an empty conversation population plus null ancillary populations. The [iteration02 prompt](cc-prompt-iteration02.md) supplies fixes and discriminating controls in a new seven-file `artifacts/cc-evidence03` packet. It preserves all older artifacts and prompts. This is the second CC correction; Operator relay/CC acknowledgement is pending. All seven rows and Slice01 acceptance remain open, with unchanged production boundaries.

CDC author readiness: (1) source-grounded in submitted driver/logs, pinned projection, named read contract, tool/file/attachment/web declarations and ownership method; (2) decision-complete for this evidence repair, specifying submitted/baseline/fresh comparisons, seal-safe controls, returned-view semantics and composed exclusions; (3) engineering-methods prompt-authoring and independent-verification rules applied through production-path/resealed-result controls and truthful query receipts; source Type Safety/Workspace Boundaries still require source-backed domain distinctions; (4) executable using existing Python/Node/compiler with the same seven-file output fence and explicit preflight; (5) falsifiable against the reproduced accepted bad result and empty/null queries, plus source-backed survivor counterexamples; (6) coherent with unchanged 27 acceptance rows and CDC ownership of DTO/codec/patch decisions, injection, D07 and sizing. No source implementation is assigned.


## Current third correction assignment — 2026-09-21

The Operator relayed CC iteration02 at `0f81e318bdd78619b5092c188c5149ae5178de35`. [CDC review](cdc-verification.md#correction-iteration02-review--2026-09-21) reproduced R1 submitted/baseline/fresh verification, fifteen rejected controls with 0/1 failing/valid runner calls, sealed preservation, actual submitted replay equality, and R3 exact complete field/ancillary queries. All 119 Project01 manifest entries at that commit passed. R1/R3 are resolved for this bounded evidence correction, not slice acceptance or integrated conformance.

R2 remains materially wrong: metadata is marked wholly public-excluded, lineage is marked absent from the access probe, some fields/paths are invented, requiredness and Partial/union contexts are conflated, and 257 of 274 member rows have placeholder types. The predicate checks only each exclusion's own sibling list against that exclusion, accepting a sibling excluded elsewhere. [Iteration03](cc-prompt-iteration03.md) changes the repair method to literal source-declaration extraction plus explicit use-site/branch interpretation and whole-projection validation. Output is the same seven-file shape under `artifacts/cc-evidence04`. This is the third correction, pending Operator relay/acknowledgement; prior evidence/prompts remain frozen. All seven rows, Slice01 acceptance and production gates remain open.

CDC author readiness: source statements were checked against pinned TypeScript/Zod declarations, the exact projection and ownership method; a syntax-only extractor reproduced eleven declarations and shows the false path-marker/example/summary/lineage claims. The prompt specifies declaration graph/use-site separation, explicit optional-ancestor/shallow-Partial rules, exact closed-member validation, false-path removal and composed exclusions with retained-container obligations. These apply engineering-methods' source-grounded prompt/oracle guidance and source Type Safety/Workspace Boundaries without selecting a DTO codec. The existing Node/compiler and seven-file fence make the method executable; supplied mutants distinguish the rejected evidence03 claims, while replay/query mechanisms remain regression requirements. Scope is still the same ten roots and 117 top-level fields; there is no nested-member target or production assignment. CDC retains DTO/patch decisions, injection, D07 and sizing.

## Subsequent Operator decisions

See [Operator decisions](../../operator-decisions.md): practical denormalization is permitted, and source work now belongs in the new Guildhall worktree. The Operator then clarified that denormalization is merely an option. Follow the [working identity direction](../../interface-design.md#working-identity-direction-toward-the-cognitive-data-plane), making lightweight guesses about future Lance/cognitive-data models. Start D02 with a named turn operation that keeps physical linkage internal; validate sequence, policy ownership and read counts before freezing that choice. Preserve logical entity identity across future revisions/representations without implementing those future stores now. D06's missing-dev blocker is resolved by the verified upstream dev base. The preserved first-pass contract/report still describe the decisions and source state at their creation; these later decisions supersede their D06-open status without changing those evidence files. Revalidate relevant upstream changes before implementation; no feature import is added to this pilot.

## Historical design result — pass 2 (preference superseded below)

The [logical-reference comparison](artifacts/design-pass02/decision.md) found a smaller working candidate than the compound command: preserve the two-stage application sequence and let the Mongo binding privately reuse the locator associated with a returned logical-reference object. All 28 source-based orchestration cases matched, eight memo/fallback cases passed, and three negative controls were detected. Stores were mocked; this is not database conformance or an implementation assignment. A naive detached early snapshot changes a mid-await cleanup case.

This result supersedes the earlier instruction to investigate the compound operation first. Next resolve cached-locator lifetime/invalidation under concurrent delete/recreate, then finish field-level DTO/projection and error/patch mapping. The public reference must remain meaningful without the optimization. Artifacts for this pass have their own manifest under `artifacts/design-pass02/`; the first-pass files and checksum list remain frozen historical evidence. No slice acceptance status changes.

## Historical design result — pass 3

The [real-Mongo lifecycle packet](artifacts/design-pass03/decision.md) rejects the pass-2 invisible hint/fallback contract. Original and copied references agree in two controls but differ after deletion, recreation, rename and conversation move. All six characterization oracles and both negative controls behaved as predeclared; this is evidence of a defect in the candidate, not six cache-correctness passes.

The working replacement is a per-invocation turn-write handle retaining the observed row privately, separate from value-based logical references. Its proposed lifecycle, release, scope and failure rules are in the decision. Next compare that candidate against the prior 28 orchestration scenarios plus lifecycle/overlap cases, then complete field-level DTO and failure mapping. No source conversion or contributor prompt is issued; all seven acceptance rows remain open. The prior packets stay sealed.

## Historical design result — pass 4

The [handle comparison](artifacts/design-pass04/decision.md) matched 28 source-based orchestration cases, passed 26 lifecycle/scope checks and detected five mutants. It uses actual tenant policy/AsyncLocalStorage with mocked stores. Per-invocation observed-write ownership is the working direction; do not reopen identity alternatives without new evidence.

The [field/patch/outcome mapping](artifacts/design-pass04/contract-mapping.md) and reproducible census cover 44 message and 73 conversation schema fields. Next reconcile provider types, named read projections and actual ordinary callers; define concrete DTOs and settle strict-scope versus invalid-input validation ordering. Source build/runtime and integrated adapter checks remain required. No source change, CC prompt or acceptance claim follows; all seven rows stay open.

## Current design result — pass 5

The [read contract and field matrix](artifacts/design-pass05/read-contract.md) select the ordinary full reload, by-ID, server history and shared ownership-probe paths. The combined query/search/pagination route remains legacy. Sixteen source-based read comparisons, two controlled admission-gating checks and three early-validation cases passed; three mutants were detected. The handle now captures non-enforcing scope so actual legacy methods retain strict-mode validation order; this supersedes the pass-4 begin-time strict check.

The matrix accounts for all 117 declared schema fields and nested public exclusions. Next finish concrete nested DTO/patch types and historical Mixed-value policy, then the composition/injection file fence and pinned-runtime/source-build prerequisites. This narrows remaining work rather than reopening the handoff alternatives. All acceptance rows remain open and no implementation prompt is issued.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.10 | 2026-09-21 | Reproduced iteration02 R1/R3 fixes; issued iteration03 for source-declaration, applicability and composed-projection defects in R2; all scope and acceptance gates retained. |
| v1.9 | 2026-09-21 | Reviewed CC iteration01; retained reproduced evidence and issued iteration02 for submitted-result verification, semantic-map errors and missing query populations; scope and gates unchanged. |
| v1.8 | 2026-09-21 | Reviewed initial CC evidence: replay and classifications reproduced; issued first correction for R1–R3 without changing slice scope or acceptance. |
| v1.7 | 2026-09-21 | Activated Operator-selected CDC + CC; issued the initial bounded replay/nested-field evidence prompt with explicit ownership, output fence, intake and readiness record. |
| v1.6 | 2026-09-21 | Fixed the read/caller boundary using source comparison; corrected handle scope-capture order and completed the top-level provider/projection matrix. |
| v1.5 | 2026-09-20 | Supported per-invocation handoff with 28 comparison/26 lifecycle cases and five mutants; added AST field inventory and patch/error mapping without claiming complete DTO or real-method conformance. |
| v1.4 | 2026-09-20 | Real-Mongo lifecycle characterization superseded pass 2's private-hint preference; separated logical reference meaning from observed-write ownership and specified the next candidate's validation obligations. |
| v1.3 | 2026-09-20 | Added source-based logical-reference prototype evidence: 28 matched scenarios, eight memo cases, three detected negative controls; preferred the staged-write/private-hint candidate over an early compound snapshot, with lifetime and real-DB validation still open. |
| v1.2 | 2026-09-20 | Refined D02 after Operator clarification: future-oriented semantic identity guides the design; denormalization remains optional and physical schema choices remain tentative. |
| v1.1 | 2026-09-20 | Recorded denormalization preference and new source worktree/base, resolving D06 while preserving first-pass artifacts and D07 revalidation. |
| v1.0 | 2026-09-20 | Opened the planned contract-design slice under explicit continuation authority; retained pending Slice01 acceptance and source-work gates. |
