# CC assignment — Slice02 compatibility evidence

## Identity and authority

You are **CC**, a separate contributor context in the Operator-selected **Two-Contributor Workflow (CDC + CC)**. CDC is the existing LibreChat/Guildhall design conversation. The Operator relays this assignment and your report. Record your actual context/session identifier if available, otherwise a truthful session description, in `intake.md`; acknowledge this assignment before dependent work. Do not invent a thread ID or start another contributor.

- Project: `project01-portable-persistence`; Arc: `arc01-contract-and-mongo-pilot`; Slice: `slice02-portable-contract-design`.
- Initial assignment: this slice's `cc-prompt.md`, issued 2026-09-21. No preceding CC prompt. Earlier design passes 1–5 are preserved one-contributor investigation, not CC deliveries.
- Planning root (`PLAN`): `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`, branch `planning`.
- Source root (`SOURCE`): `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall`, branch `billo-guildhall`, revision `3e3c5410d3863118fdba694fb0cd51baeb7102f9`.
- Slice (`SLICE`): `$PLAN/project01-portable-persistence/arc01-contract-and-mongo-pilot/slice02-portable-contract-design`.
- Evidence output (`OUT`): `$SLICE/artifacts/cc-evidence01`.
- Planning evidence baseline: `6090dbbedf0d122b5b576de3759c741409e84c51`; governing transition/open set is the later commit introducing this prompt. Resolve and record that commit with `git log -1 --format=%H -- <this prompt's path>` and its file SHA-256. Recheck that the active assignment in `slice-plan.md` still names this prompt.

**Outcome: an evidence packet for CDC's remaining DTO decisions, not application implementation or Slice02 closure.** Reproduce the latest bounded comparison and inventory the nested shapes named below. The candidate may be wrong: report contradictions, do not tune observations to match its expected results.

All seven Slice02 acceptance rows remain open. This assignment supplies evidence for S01/S02/S03/S07; it does not fully discharge them. S04 cursor reproduction, S05 source-preservation acceptance and S06 implementation/build readiness remain outstanding. Slice01 acceptance is also pending. No new reviewer label upgrades the prior contributor's self-checks to independent acceptance.

## Scope and decision ownership

Binding for this investigation:

- Source is read-only. No adapter implementation, application/fixture changes, new source branches, dependency installation, builds, live Mongo access, private export reads, migrations, server restarts, pushes or PRs. Do not run application suites. The existing pass05 harness uses storage doubles and requires no database.
- Planning writes are limited to the seven new output files listed below. Leave plans, ledgers, this prompt and every existing artifact unchanged. Preserve unrelated staged/unstaged files and editor swap files.
- Keep the ordinary-turn scope from pass05: distinct server/public/probe records; no added serial lookup; no early strict-tenant enforcement at handle creation; physical row IDs private; no incidental cursor fix. Logical entity references remain distinct from the invocation handle that owns an observed write.
- Actual field absence, own-property `undefined`, null, empty values and populated values are different observations. Existing local Date behavior and nested private-field exclusions matter. The UI/provider schema is evidence of consumer expectations, not automatically a lossless persistence decoder.
- No historical-value claim follows merely from a current schema. `Mixed`/`unknown` declarations do not prove JSON-only contents or prove a non-JSON value exists in the corpus. Record what source establishes and what needs later isolated database characterization.

CDC owns the final nested DTO/patch/unknown-value policy, precise composition/file fence and implementation sizing. Recommendations may identify alternatives and their consequences; they are not permission to choose a codec, stringify a BSON value, reject old records, narrow content unions, flatten arrays, or add defaults. Report an unresolved decision with its evidence and affected paths. You may choose private mechanics for extracting/formatting evidence within this scope.

## Required-reading manifest and intake

Paths below are local on this host. `K` means `/Users/oubiwann/.codex/skills`. Follow governing instructions; references to historical artifacts are evidence, not additional assignments. Read required text in complete bounded chunks, recovering any truncation. Record source state, read extents and data-query coverage separately in `intake.md`, with a short source-cited contract readback covering scope, preservation, failure handling and review limits. Acknowledgement is not a new permission gate: continue once preflight is coherent.

Read in this order:

1. **Required-full:** this prompt; `$PLAN/AGENTS.md`, `$PLAN/BILLO.md`, `$PLAN/README.md`; `$SLICE/slice-plan.md` and `$SLICE/ledger.md`; `$SOURCE/AGENTS.md`, `$SOURCE/BILLO.md`, `$SOURCE/CLAUDE.md`. These define assignment, scope, fork policy and engineering constraints. Source-specific implementation rules do not authorize application edits in this evidence assignment.
2. **Required-section:** `$PLAN/project01-portable-persistence/project-plan.md`, complete `Goal and boundaries`, `Workflow and authority` (including all nested transition/Expedited sections), and `Definition of done`; `$SLICE/../arc-plan.md`, complete `Scope`, `Slice roadmap`, `Workflow and source boundaries`. These retain architecture and acceptance ownership without requiring all historical narrative.
3. **Required-section:** `$K/engineering-methods/guides/07-implementation-prompt-authoring.md`, `Investigation and semantic evidence assignments` and `Required reading and CC intake`; `$K/collaboration-framework/knowledge/engineering-methods/guides/01-engineering-methodology.md`, `Roles and Shared Invariants`, `Two-Contributor Workflow`, and `Workflow Selection and Transitions`. **Required-full:** `$K/work-verification/guides/05-independent-verification.md` and `$K/scientific-methods/guides/06-evidence-capture.md` plus `08-analysis-and-threats-to-validity.md` in that same directory.
4. **Required-full:** `$SLICE/artifacts/design-pass05/read-contract.md`, `protocol.md`, `experiment.cjs`, `field-matrix.cjs`, `validate.py`; `$SLICE/artifacts/design-pass04/handle.cjs`. The pass05 scope-capture correction governs over the sealed pass04 prototype's earlier enforcement recommendation. Statements in old artifacts that no CC is assigned are historical; the current transition governs roles.
5. **Required-data:** pass05 `field-matrix.json`: inspect all `records[*].fields[*]` names, source locators, `storageDefinition`, `interfaceType`, `provider`, `defaultRead`, `publicRead`, `portableServerRead`, `endpointUnsetRule`; all `exclusions`; all `providerOnly`, `interfaceOnly`, and `implicit` entries. Partition output by record/field as needed, retaining complete population coverage. Baseline denominator is 44 message + 73 conversation fields; derive counts, do not copy them as evidence. Read pass05 `result-01.json` completely by projecting every read/gate/preflight/control case's name, expected status where present, passed/detected, traces and responses, plus all provenance fields; record query commands and counts. Hash-check all existing slice/arc manifests without changing them.
6. **Required-section, source inspection:** complete `messageSchema` and `convoSchema` initializers in `packages/data-schemas/src/schema/message.ts` and `convo.ts`; complete `conversationPreset` declaration/initializer in `schema/defaults.ts`; complete `schema/fading.ts`; `IMessage` in `types/message.ts`; `IConversation`, `IAgentEventActorContextMeta` and definitions they use for the selected fields in `types/convo.ts`; `CLIENT_MESSAGE_SELECT` in `methods/message.ts`. Resolve selected-field provider/type references from their source definitions, reading each complete declaration, and cite every dependency followed. Only follow field/type/projection dependencies of the ten roots below, not the whole event-actor subsystem. Stop expansion at declared open/Mixed positions and external SDK boundaries; record their exact named type/import and unresolved contract instead of recursively surveying the SDK.
7. **Conditional:** if inspecting a claimed existing producer/consumer witness, read the full enclosing function and necessary helper definitions before making that claim. Start with the relevant type/schema imports and repository `rg` searches; retain matches and explain the bounded search surface. If source drift, missing dependencies or an unresolved type prevents a claim, record the gap instead of inventing the declaration. Repository Markdown reached as governing instructions must be read before applicable work.

Reference-only: earlier Slice01 and Slice02 packets not explicitly listed above. They remain authoritative evidence at their pinned revisions, but this assignment does not replay all of them or claim to accept their results.

## Execution method

### 1. Establish and preserve the baseline

Record exact branches, heads, tracked/untracked status, tool paths/versions and relevant dirty state. Stop dependent replay if the source head differs from the pinned revision or relevant tracked source is dirty; do not reset it. Unrelated user files are not authorization to clean up. Verify the existing manifests and source fingerprints before execution. A mismatch is an evidence finding and a blocker to claiming reproduction.

Use the already-installed Node `/Users/oubiwann/.local/bin/node` (record actual version; pass05 used 22.22.3) and compiler `/Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js` (pass05 used 5.9.3). The repository pin is Node 24.16.0; this historical-harness reproduction does not satisfy D07. If the tools differ, retain that observation and stop a same-environment reproduction claim; do not install or switch runtimes as an incidental fix.

### 2. Replay pass05 from sealed bytes

Read/verify the harness before running. From the planning root, run the following with absolute paths substituted, writing only the new result under `OUT`:

```text
/Users/oubiwann/.local/bin/node $SLICE/artifacts/design-pass05/experiment.cjs $SOURCE /Users/oubiwann/lab/billosys/LibreChat/node_modules/typescript/lib/typescript.js $SLICE/artifacts/design-pass04/handle.cjs $OUT/replay-result.json
```

Retain command argv, cwd, timestamps, exit status, stdout/stderr in `execution.log`, including unsuccessful attempts. A successful result should reproduce the 16 reference/candidate read comparisons and exact per-case statuses, two admission gates, three preflight outcomes with zero model accesses, and three detected controls. Compare every structured case to sealed `result-01.json`, not just the summary counts. Paths/provenance may differ because the harness now runs at its sealed path; enumerate allowed provenance differences individually, never omit behavior fields wholesale.

Also run the existing pass05 validator from `PLAN`, recording the result. It checks the historical packet and inventory; it does **not** validate your new nested-field interpretation or constitute integrated adapter testing. Do not modify the validator to accept a mismatch. Inspect its assertions and explain that coverage boundary.

### 3. Produce a bounded nested-field inventory

Use the full 117-field input population as a coverage denominator. Classify each field exactly once as one of: selected nested root; other scalar/array field outside this deep inspection; default-hidden specialized field; adapter-private physical relationship. Preserve record namespace: message `files` and conversation `files` are distinct.

Deeply inspect exactly these **ten roots**, plus their nested type/projection dependencies:

| Record | Roots | Why selected |
|---|---|---|
| Message | `content`, `files`, `attachments`, `metadata`, `feedback`, `contextMeta`, `userSubmittedMessageFieldPaths` | Mixed arrays/objects, nested public exclusions, structured feedback/provenance and server-only context |
| Conversation | `examples`, `codeWorkspaces`, `subagentThread` | Mixed preset payloads, structured workspace references, access/lineage shape |

For each root, record: schema locator and declared shape/default/requiredness; direct TypeScript shape; provider counterpart or absence; nested named members/discriminants; array boundaries; leaf value domains; explicit open/Mixed positions; implicit subdocument `_id` possibility where source establishes it; server/public/probe applicability; every applicable nested exclusion; field-state and unset implications. Cite revision, file, symbol and line span for each substantive observation. Expand imported schema spreads such as fading definitions. Do not treat a schema metadata `_id: false` entry as a stored boolean member.

For every open/Mixed position, distinguish a declaration from a witnessed producer/consumer expectation. Search the selected ordinary-path surface (`api/app/clients`, `api/server/routes/messages.js`, `api/server/controllers/agents`, `packages/api/src/conversations`, `packages/api/src/agents/hitl`, `packages/data-provider/src`) for direct uses; inspect a concrete witness where found, otherwise record search scope and `not established`. This is a bounded witness inventory, not a claim to enumerate every caller in LibreChat. Follow directly imported selected-field type definitions when needed; report broader gaps for CDC.

Account explicitly for all twelve nested public exclusions in `CLIENT_MESSAGE_SELECT`. Record the array/member path and permitted sibling data that a later codec must preserve. `contextMeta` is excluded at the root for public reads but used on server paths; `tenantId` is not a nested private field to drop. Provider/UI-only fields do not become persistence fields merely because they have richer types. Classify hidden event-actor structures without recursively inventorying them.

In `nested-fields.json`, use a top-level object with `sourceHead`, `sources` (path/hash), `coverage` (one row per record/field with classification), `roots` (ten root records with the observations above), `nestedExclusions` (twelve mapped entries), and `unresolved` (question, evidence, affected root, owner=CDC). Keep missing evidence explicit. Opaque/open values may remain unresolved; no JSON codec/type narrowing is being accepted here.

### 4. Return the decision inputs

Write `report.md` with:

- Assignment identity/context, exact source and planning states, commands/results and evidence paths.
- Replay matches/differences and negative controls, distinguishing independent replay of an existing harness from an independently designed test or real-Mongo conformance.
- The nested compatibility obstacles and source-backed type reuse opportunities. Explain whether each is established by a schema, declared type, actual source use, inference, or remains unknown.
- A small decision table for CDC: unresolved policy, affected fields, available evidence, options/consequences, and next discriminating check. Do not design a universal future Guildhall data model.
- A row walk of S01–S07 explaining this assignment's contribution and what remains open. Do not mark rows done or write slice close/verification files.
- Bubble-up recommendations, especially whether the remaining DTO/composition/conformance work needs re-slicing. The existing three-slice roadmap is unchanged until CDC/Operator disposition.

Stop when the replay is accounted for, all 117 fields are classified, the ten roots and twelve nested exclusions have source-backed records or explicit blockers, and the return packet is validated. Do not continue into another unassigned research pass.

## Output, checks and commit contract

Create only these seven files under `artifacts/cc-evidence01/`:

```text
intake.md
report.md
nested-fields.json
replay-result.json
execution.log
replay.py
SHA256SUMS
```

`replay.py` is a small Python-standard-library driver for the exact replay, logged commands, structured-case comparison, inventory membership/uniqueness/count checks, source hashes and sealed-artifact preservation. Keep observations in JSON separate from validation expectations. It must report failed/blocked commands truthfully and preserve all attempts (append logs; retain each failed result in the log before a retry replaces the result path). Do not write new JavaScript/TypeScript harnesses or copy/alter sealed ones. If a prerequisite blocks replay, the result file records that blocker instead of a fabricated pass. Structural validation checks coverage/identity, not the semantic correctness of authored field interpretations.

Before committing: inspect the diff and staged index; verify exact output inventory; parse JSON; verify coverage keys equal all baseline `(record, field)` keys with no duplicates; require the ten selected roots and exact twelve nested exclusion strings; recheck relevant source/old-artifact hashes and unchanged source status; run `git diff --check`. Seal all six other output files in `SHA256SUMS` after logs are final. Re-running a checker must not rewrite a sealed packet silently; use temporary output for reviewer reproduction.

Commit only those seven explicitly named paths on `planning` using `git commit --only -F <message-file> -- <seven paths>`; preserve others' index entries. The message must end with exactly:

```text
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

Return the commit, project-relative `arc01-contract-and-mongo-pilot/slice02-portable-contract-design/artifacts/cc-evidence01/report.md` path, results and blockers to the Operator for CDC review. CDC will inspect and reproduce your new work; production readiness and slice acceptance remain separate decisions.
