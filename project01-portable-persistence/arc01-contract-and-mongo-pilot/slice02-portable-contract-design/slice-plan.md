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

## Version History

| Version | Date | Change |
|---|---|---|
| v1.2 | 2026-09-20 | Refined D02 after Operator clarification: future-oriented semantic identity guides the design; denormalization remains optional and physical schema choices remain tentative. |
| v1.1 | 2026-09-20 | Recorded denormalization preference and new source worktree/base, resolving D06 while preserving first-pass artifacts and D07 revalidation. |
| v1.0 | 2026-09-20 | Opened the planned contract-design slice under explicit continuation authority; retained pending Slice01 acceptance and source-work gates. |
