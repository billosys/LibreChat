# Slice02 — Portable contract design

| Metadata | Value |
|---|---|
| Slice | slice02-portable-contract-design |
| Arc | [Arc01](../arc-plan.md) |
| Status | Active — design preparation; not implementation-ready |
| Workflow | One contributor; Expedited Mode |
| Assignment | This plan, owned by the current conversation; no CC/CRC handoff |
| Source baseline | First-pass evidence: `ba44443fdb232bbe6d4977e2619774b5a72586ac`; next source work: `billo-guildhall` from `fe79265b2f47937051625719f3ba5080189912c1`, requiring revalidation |
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
5. Bubble actionable findings into the parent plans immediately. Keep criteria open until their evidence and review requirements are satisfied. Once the design is complete, prepare the actual workflow transition and source-grounded implementation assignment using the prompt-authoring guide; do not issue a speculative prompt now.

## Verification and exit

Every contract choice must trace to a current caller requirement or a clearly labeled intended change. Check scoped authorization, field-state distinctions, no-upsert and retry/partial-commit behavior explicitly. Demonstrate that the public dependency graph and DTO census can exclude engine details before declaring implementation readiness. Synthetic experiments must fail closed on database target selection and retain unsuccessful attempts. Verify Markdown links, source cleanliness, exact artifact inventory and hashes, and explicit-path commits. These are self-checks, not independent acceptance.

The slice is complete only when all ledger criteria have concrete dispositions, the consequential choices are resolved, the implementation fence and conformance recipe are precise, and applicable review gates are satisfied. A first draft does not close this slice.

## Assignment history

| Assignment | Date | Predecessor | Reason | Disposition |
|---|---|---|---|---|
| This slice plan v1.0, current conversation | 2026-09-20 | Slice01 evidence packet | Operator explicitly requested continuation after reading the report | Active design preparation; no implementation prompt |

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
| v1.6 | 2026-09-21 | Fixed the read/caller boundary using source comparison; corrected handle scope-capture order and completed the top-level provider/projection matrix. |
| v1.5 | 2026-09-20 | Supported per-invocation handoff with 28 comparison/26 lifecycle cases and five mutants; added AST field inventory and patch/error mapping without claiming complete DTO or real-method conformance. |
| v1.4 | 2026-09-20 | Real-Mongo lifecycle characterization superseded pass 2's private-hint preference; separated logical reference meaning from observed-write ownership and specified the next candidate's validation obligations. |
| v1.3 | 2026-09-20 | Added source-based logical-reference prototype evidence: 28 matched scenarios, eight memo cases, three detected negative controls; preferred the staged-write/private-hint candidate over an early compound snapshot, with lifetime and real-DB validation still open. |
| v1.2 | 2026-09-20 | Refined D02 after Operator clarification: future-oriented semantic identity guides the design; denormalization remains optional and physical schema choices remain tentative. |
| v1.1 | 2026-09-20 | Recorded denormalization preference and new source worktree/base, resolving D06 while preserving first-pass artifacts and D07 revalidation. |
| v1.0 | 2026-09-20 | Opened the planned contract-design slice under explicit continuation authority; retained pending Slice01 acceptance and source-work gates. |
