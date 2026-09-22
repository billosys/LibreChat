# CC evidence03 intake

## Assignment and source state

This is the CC execution record for `cc-prompt-iteration02.md`, “bind verification to submitted evidence and correct the nested map.” The executing context acknowledges the assignment as evidence-only work: it may inspect the pinned source and sealed design packet, author the seven files in this packet, and run the named controls. It may not modify application source, dependencies, plans, ledgers, prior evidence, the live database, or infrastructure. No CC session identifier was supplied by the relay; this file records the actual prompt and source identities instead of inventing one.

- Planning checkout: `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`, branch `planning`, planning HEAD at intake `a0c16f4031ca050e226b501db72387d1177fa45e`.
- Source checkout: `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall`, pinned clean source `3e3c5410d3863118fdba694fb0cd51baeb7102f9`.
- Reviewed prior delivery: `cc-evidence02` commit `5d94ef8d8da18b636279553ed037b906259b2882`.
- Current assignment commit: planning commit `a0c16f4031ca050e226b501db72387d1177fa45e`.
- Current prompt: `project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design/cc-prompt-iteration02.md`, full read 1–83, SHA-256 `c0b4f94e2954dde39f9265c465f4dea9a46934fb7f24ebabac56f365102a4d51`.
- Output home: `artifacts/cc-evidence03/`. The intended sealed packet has exactly `intake.md`, `report.md`, `nested-fields.json`, `replay-result.json`, `execution.log`, `replay.py`, and `SHA256SUMS`.

## Required reading loaded

The active assignment, predecessor, and governing planning files were loaded before authoring:

- Required-full: `cc-prompt-iteration02.md` 1–83; `cc-prompt-iteration01.md` 1–93; initial `cc-prompt.md` 1–124; `slice-plan.md` 1–121; `ledger.md` 1–13; `cdc-verification.md` 1–101.
- Required-section: project plan goal/boundaries 13–21, definition of done 35–43, workflow/authority and Expedited Mode 70–122; arc plan scope 29–33, roadmap 35–45, workflow/source boundaries 55–80.
- Required-section: planning `AGENTS.md` 1–25, `BILLO.md` 1–52, `README.md` 1–22; source `AGENTS.md` 1–116, `BILLO.md` 1–52, and `CLAUDE.md` 1–376.
- Required-section: project-management README 1–178; canonical planning worktree 126–250; top-down planning/iteration 134–188; implementation-prompt authoring investigation/intake/oracle/assembly guidance 162–342; engineering methodology roles/shared invariants 75–148 and two-contributor/transition material 303–331; independent verification 1–98; scientific evidence capture 1–51; validity 1–52; testing validation gates 1–82.

Iteration02 required-data and witness material was loaded as follows:

- Required-data: sealed pass05 `field-matrix.json` with both complete record projections; all 117 coverage rows, 10 selected roots, 12 nested exclusions, and unresolved decision ownership from the prior inventory; complete pass05 replay behavior/provenance; prior packet manifests and CDC review outputs.
- Required-section: pass05 `read-contract.md` 1–84, `protocol.md` 1–11, `experiment.cjs` 1–75, `field-matrix.cjs` full, `validate.py` 1–48, and pass04 `handle.cjs` 1–58. Pinned hashes are checked by `replay.py`.
- Required-section: source declarations and enclosing consumers: `types/agents.ts` 81–135; `types/files.ts` 150–221; `types/web.ts` 19–58 and 403–420; `types/content.ts` 1–220 and 244–315; `schemas.ts` 867–876, 1039–1061, 1102–1113, and 1127–1136; `codeEnvRef.ts` 68–77; `feedback.ts` 1–145; fading, message, conversation, defaults, and schema sections recorded in `replay.py`; message/conversation methods and route/controller ranges recorded there as complete bounded reads.
- Required-data: evidence02 execution history was inspected for the incorrect `conversationSchema` query, top-level ancillary query, self-test labeling, resealed submitted-result behavior, and sentinel ordering. Those are retained as historical failures; the corrected controls are separate.

## Contract readback

The packet must prove only evidence behavior. Capture is allowed to populate an unsealed destination and must refuse a sealed one. Verification is read-only: after packet/manifest, inventory, and environment preflight it compares the submitted `replay-result.json` to the pinned pass05 result, runs the sealed pass05 harness in a temporary output, and compares fresh output to both submitted and pinned values with presence-aware exact equality. Wrong runtime/head/compiler/source observations must fail before the injected runner; a valid injected runner must be called exactly once. Positive unchanged preservation and negative runner mutation are separate controls. Self-test output may be logged only before sealing and must not append to a sealed packet.

The nested map preserves the 117-row census while expanding ten named roots. Arrays are path notation, not Mongo field names. The twelve exclusions list only actual survivors after the entire projection; a validator rejects a claimed survivor covered by an exclusion. Applicability is an operation-level mapping: message roots are message-view members, conversation roots are not message result members, and `subagentThread` public admission is lineage-based. Provider declarations are type witnesses only; historical BSON/Mixed behavior, DTO/codec policy, and semantic acceptance remain CDC-owned.

R3 must query `convoSchema`, not the old `conversationSchema`, and must retain complete 44/73 projections plus per-record ancillary arrays: 10/13 provider-only, 4/3 interface-only, and four implicit keys per record. The old wrong-name and wrong-level controls remain visible and are not relabeled as current success.

## Boundaries and gates

The run uses the repository’s pinned evidence harness with storage doubles; the available Node is v22.22.3 while the source repository pins Node 24.16.0. No build, full suite, live database, migration, restart, push, or PR is authorized or claimed. This is proposed-done CC evidence pending CDC review and Operator acceptance. All Slice02 ledger rows remain open, and this packet does not close the slice or advance Slice03.
