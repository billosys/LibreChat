# CC intake — Slice02 compatibility evidence

## Identity and acknowledgement

This is the separate CC contributor context for the Operator-issued assignment in `cc-prompt.md`, issued 2026-09-21. A Codex API session identifier is not exposed in this context; the truthful identifier is: `Codex API session, CC evidence packet execution, session identifier unavailable`. I acknowledge the CDC+CC boundary and continue under the assignment without starting another contributor or inventing a thread ID.

The assignment is evidence collection for CDC's remaining DTO decisions. It is not implementation, Slice02 closure, independent acceptance, or a source change. The seven-file output fence is respected below `artifacts/cc-evidence01/`.

## State and authority

| Item | Observed state |
|---|---|
| PLAN | `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`, branch `planning` |
| SOURCE | `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall` |
| pinned source revision | `3e3c5410d3863118fdba694fb0cd51baeb7102f9` |
| source status | clean; no tracked or untracked changes |
| planning prompt transition | `44c77142f97f10082f5628ca76b4d2d1bd6ce4fd`, the commit introducing this prompt |
| prompt SHA-256 | `cdbd9e4922d3d598ee947902a238d211c3c08d18176f973b420aaf40d75e5a99` |
| planning evidence baseline | `6090dbbedf0d122b5b576de3759c741409e84c51` |
| repository Node pin | `24.16.0` (not used for this historical harness replay) |
| replay Node | `/Users/oubiwann/.local/bin/node`, `v22.22.3` |
| TypeScript compiler | `/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js`, `5.9.3`, SHA-256 `3ae902c92cc44dace175c0e69e13a4b0899f6983c6121d76b9ab8dd5795e7675` |

The source remains read-only. No application suite, build, database, dependency installation, migration, restart, export, push, or PR was used.

## Required-reading manifest

The following governing files were read completely in bounded chunks: this prompt; PLAN `AGENTS.md`, `BILLO.md`, `README.md`; the slice `slice-plan.md` and `ledger.md`; SOURCE `AGENTS.md`, `BILLO.md`, and `CLAUDE.md`. The active slice plan still names this prompt and keeps S01–S07 open.

The required project and arc sections were read: project `Goal and boundaries`, `Workflow and authority` including transition and Expedited Mode material, and `Definition of done`; arc `Scope`, `Slice roadmap`, and `Workflow and source boundaries`.

The required framework material was read before execution: engineering-methods prompt-authoring guidance for investigation/intake assignments; engineering-methodology role, Two-Contributor Workflow, and transition guidance; the complete independent-verification guide; and the complete scientific-methods evidence-capture and analysis/threats-to-validity guides. Applied constraints were to retain raw command evidence, distinguish source declarations from witnesses, preserve failed/blocked attempts, and leave acceptance to CDC/independent reproduction.

The sealed historical material was read completely: pass05 `read-contract.md`, `protocol.md`, `experiment.cjs`, `field-matrix.cjs`, `validate.py`, and pass04 `handle.cjs`. Existing manifests were hash-checked from their own parent directories: the slice-root manifest and design-pass02 through design-pass05 manifests all passed without modification. The initial relative-path manifest attempt and the mistaken pass01 subdirectory lookup are retained as unsuccessful preflight history in `execution.log`.

Source inspection covered the complete selected initializers and declarations required by the prompt: `message.ts`, `convo.ts`, `defaults.ts`, `fading.ts`, `types/message.ts`, `types/convo.ts`, `methods/message.ts` including `CLIENT_MESSAGE_SELECT`, and the selected provider schemas/types in `packages/data-provider/src`. Full enclosing functions were read for the claimed ordinary-path witnesses in message routes, agent request/resume/client paths, HITL policy/answers, and provider example generation. Bounded searches covered `api/app/clients`, `api/server/routes/messages.js`, `api/server/controllers/agents`, `packages/api/src/conversations`, `packages/api/src/agents/hitl`, and `packages/data-provider/src`.

## Data-query coverage

`field-matrix.json` was projected over every `records[*].fields[*]` row, including names, source locators, storage definitions, interface types, provider counterparts, default/public/probe reads, and unset rules: 44 message fields plus 73 conversation fields, 117 total. The `exclusions`, `providerOnly`, `interfaceOnly`, and `implicit` populations were also inspected. `result-01.json` was projected over every read case, gate case, preflight case, and negative-control case, retaining names/statuses, full traces and responses, and all provenance fields. The sealed result contains 16 read comparisons, 2 admission gates, 3 preflight cases, and 3 controls.

The new inventory derives its coverage rows from those 117 matrix rows and asserts unique `(record, field)` membership, exactly ten selected roots, and exactly twelve nested exclusion paths. It does not treat those structural assertions as semantic acceptance.

## Contract readback

The assignment requires read-only, bounded evidence. It preserves absent, own-property `undefined`, `null`, empty, and populated states; keeps physical row identifiers private; keeps logical entity references distinct from invocation handles; and does not add serial lookups or early strict-tenant enforcement. `CLIENT_MESSAGE_SELECT` exclusions are nested path exclusions, not permission to discard permitted siblings. `contextMeta` is root-excluded from public reads but remains a server-side field. `tenantId` is not a nested private field. Provider/UI shapes are consumer evidence, not automatic persistence decoders. `Mixed` and `unknown` declarations establish open positions, not JSON-only historical values.

The replay uses storage doubles from the sealed pass05 harness. It compares complete structured behavior to `result-01.json`, records command argv/cwd/timestamps/status/stdout/stderr, and runs the existing validator without changing it. This can reproduce the historical orchestration evidence but cannot establish real-adapter conformance, source-build readiness under the pinned Node version, or independent acceptance. CDC owns unresolved codec/DTO policy, exact composition/file fence, implementation sizing, and the final reviewer decision. All seven ledger rows and Slice01 acceptance remain open.
