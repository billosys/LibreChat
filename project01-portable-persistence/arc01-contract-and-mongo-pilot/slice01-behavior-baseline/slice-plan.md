# Slice01 — Pilot behavior baseline

| Metadata | Value |
|---|---|
| Slice | slice01-behavior-baseline |
| Arc | [Arc01](../arc-plan.md) |
| Status | Open — investigation assignment active; baseline execution pending |
| Workflow | One contributor, explicitly selected by the Operator |
| Execution mode | Expedited Mode under the project policy; current one-contributor assignment unchanged |
| Assignment | This slice plan; no separate CC assignment in the current workflow |
| Source baseline | `ba44443fdb232bbe6d4977e2619774b5a72586ac` |
| Artifact home | `artifacts/` inside this slice |
| Blocks | Slice02 concrete contract design |

## Goal

Produce an evidence-backed specification of the current ordinary message-save/conversation-update/read path and the import requirements that constrain its future interface. Run the relevant existing Mongo-backed tests in disposable databases and expose coverage gaps. The output is a behavior baseline and bounded design questions, not an application change.

## Scope and fences

Trace `BaseClient.saveMessageToDatabase`, `saveTurnConversation`/seed behavior, and the data-schemas operations they invoke. Enumerate direct callers of the candidate store methods and classify ordinary turns, import/bulk paths, and background/subagent writers. Read adjacent paths only to resolve shared preconditions, mutation semantics, or lifecycle effects. Do not treat a whole-repo import count as a complete caller map.

Carry forward the completed Claude reconciliation, including source IDs, original parents, structured content, skipped messages, summaries, update times, and timestamp precision. Identify how these constrain the eventual contract without designing the entire Guildhall memory system or implementing a replacement importer.

Writes are limited to this slice's plan/ledger/artifacts and necessary parent-plan status or finding updates on `planning`. Source inspection and existing test execution are allowed. No application code edits, dependency upgrades, source-branch creation, database migration, live corpus writes, credential changes, or service restarts are part of this slice. Incidental test reports/caches must be directed into `artifacts/` or a recorded disposable directory where configuration allows; inspect any source-checkout changes before cleanup and preserve unrelated work.

## Required inputs

- [Project plan](../../project-plan.md), [arc plan](../arc-plan.md), and [slice ledger](ledger.md).
- [Interface proposal](../../interface-design.md), [research](../../research.md), and [corpus reconciliation](../../corpus-reconciliation.md).
- Current source `AGENTS.md`/`CLAUDE.md` and the collaboration framework's planning, testing, and evidence guidance applicable to the actual work.
- Relevant complete functions and their dependencies in `api/app/clients/BaseClient.js`, `packages/api/src/conversations/save.ts`, `packages/data-schemas/src/methods/message.ts`, `methods/conversation.ts`, `tenant/policy.ts`, and registration/model plugins. Record the inspected symbols/line extents; these large files are not claimed fully audited merely because selected functions were read.
- Import mapping and bulk-writer paths identified in the existing reconciliation. Check how their contracts differ from ordinary saves.
- Each selected test's configuration, setup, teardown, and connection route before running it. The [opening baseline](artifacts/opening-baseline.md) lists discovered test/config paths.

## Work sequence and expected artifacts

1. **Confirm intake and test isolation.** Record source commit, clean/unrelated-change status, runtime prerequisites, test configuration, and database connection targets. Resolve any setup that can reach the running Mongo corpus before execution. Produce `artifacts/test-baseline.md` with commands, output locations, and disposition of every attempt.
2. **Build the bounded dependency map.** Produce `artifacts/dependency-map.md`: entrypoint → orchestration → domain method → storage operation/plugin/side effect, with owner/tenant context and adjacent caller classification. Include read/reload and the boundary between message save and conversation update.
3. **Define the observed behavior matrix.** Produce `artifacts/behavior-matrix.md`: trigger, source evidence, current outcome, existing test, result/coverage gap, and contract implication. Cover create/update/no-op/upsert, omission/null/clear, logical/storage IDs, cached absent versus unread state, provenance, retention, invalid input, duplicate IDs, ordering, and partial failure. Import-specific rows distinguish source truth from operational representation.
4. **Run and account for the existing baseline.** Execute the selected focused suites after their isolation is established. Preserve command, cwd, environment overrides excluding secret values, exit status, suite/test denominators, failures, skipped/unrun cases, and raw logs. Compare results with the behavior matrix. A failed pre-existing test is evidence, not permission to fix source in this slice.
5. **Synthesize the next design boundary.** Produce `artifacts/design-inputs.md` with exact pilot operations/callers, proposed code fence, source-preservation constraints, unresolved decisions with owners, and the tests that would reject an incorrect adapter. State whether the pilot still fits one implementation slice. Record the implementation `dev` baseline decision as resolved or explicitly still open; it need not block the read-only baseline.

These artifacts are created as their work is performed, not as empty placeholders at opening. Prior project-level evidence remains in its original home and is linked rather than copied into invented historical slice outputs.

## Test selection and evidence rules

Start with the save orchestration and tenant conformance suites, then select message/conversation tests needed by the mapped path and import tests that constrain it. Read each test's actual setup first. Use existing installed tooling and explicit test paths; package `npm test` scripts currently enable watch/coverage, so select a deliberate non-watch invocation after checking the configs. Do not start a whole-repository suite by accident.

Map each behavior row to an executed existing assertion or a named coverage gap. Extend the run only when an uncovered dependency or result warrants it. Passing counts alone do not prove the future interface; new conformance cases belong to the later implementation assignment. Preserve environmental failures and any elevated retry as separate attempts.

## Exit and handoff

Every slice ledger row must have concrete evidence and an honest disposition. Deliver the map, matrix, baseline results, and design inputs with source and command provenance. A blocked test remains blocked; it cannot be relabeled as passed because corpus reconciliation succeeded. If a required result cannot be obtained, keep the relevant row open or request an explicit disposition rather than silently dropping it.

Current evidence is self-checked, not independent acceptance. Existing project/arc review gates remain pending. Do not manufacture `cc-prompt.md`, `cdc-verification.md`, or `crc-verification.md` for imaginary contributors. Before a later multi-contributor implementation handoff, record the workflow transition and actual contexts, apply the implementation-prompt authoring readiness guide, and issue the canonical assignment then.

## Assignment history

| Assignment | Date | Predecessor | Reason | Disposition |
|---|---|---|---|---|
| This slice plan, v1.0; current conversation | 2026-09-20 | None | Operator requested opening Arc01 after source/import reconciliation | Active investigation; no CC prompt issued |

## Version History

| Version | Date | Change |
|---|---|---|
| v1.1 | 2026-09-20 | Applied Operator-requested Expedited Mode and inherited prompt-path reporting; no new contributor assignment or acceptance claim. |
| v1.0 | 2026-09-20 | Opened the bounded behavior-baseline investigation under one-contributor workflow. |
