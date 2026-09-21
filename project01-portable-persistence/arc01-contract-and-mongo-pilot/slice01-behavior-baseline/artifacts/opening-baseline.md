# Slice01 opening baseline

Date: 2026-09-20. This records intake observations only; no application test suite was run while opening the arc.

## Repository state

Source checkout: `/Users/oubiwann/lab/billosys/LibreChat`.

```text
git rev-parse HEAD
ba44443fdb232bbe6d4977e2619774b5a72586ac

git status --short
(no output)

git worktree list
/Users/oubiwann/lab/billosys/LibreChat                      ba44443fd [main]
/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning  d5e9f5370 [planning]
```

The explicit read-only remote query succeeded:

```text
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10' git ls-remote origin refs/heads/dev refs/heads/main
ba44443fdb232bbe6d4977e2619774b5a72586ac refs/heads/main
```

No `refs/heads/dev` was returned. This confirms its absence from the queried fork remote at intake, beyond the earlier local tracking-ref inventory. No fetch, branch creation, remote mutation, or push occurred. The source instructions' `dev` policy therefore needs an explicit implementation-baseline resolution before code branching; current investigation is not blocked.

## Test tooling discovered

| Workspace | Configuration | Package test script |
|---|---|---|
| packages/data-schemas | `jest.config.mjs` | `jest --coverage --watch` |
| packages/api | `jest.config.mjs`, `jest.setup.cjs` | Jest with coverage/watch and integration/helper/manual exclusions |
| api | `jest.config.js` | Invocation and setup still to inspect for any selected import suite |

The data-schemas config calls `jest.globalSetup.mjs`, which prewarms a `mongodb-memory-server` binary; download failure there is warned and retried by individual suites. It does not establish that the binary is currently available. The API setup file supplies a `File` polyfill when needed; it is not itself a database-isolation guarantee.

The inspected setup in `packages/api/src/conversations/save.spec.ts` creates `MongoMemoryServer`, connects to that instance's URI, and disconnects/stops it at teardown. Its per-test collection deletes are appropriate only on that disposable connection. The tenant harness in `packages/data-schemas/src/tenant/conformance.mongoose.spec.ts` likewise starts its own memory server. Read complete setup/dependency paths before execution; these opening observations do not claim every selected test is isolated or unmocked.

Candidate existing suites, subject to Slice01 coverage selection:

- `packages/api/src/conversations/save.spec.ts`
- `packages/data-schemas/src/tenant/conformance.mongoose.spec.ts`
- `packages/data-schemas/src/methods/message.spec.ts`
- `packages/data-schemas/src/methods/message.traces.spec.ts`
- `packages/data-schemas/src/methods/conversation.spec.ts`
- `packages/data-schemas/src/methods/convoStructure.spec.ts`
- `api/server/utils/import/importers.spec.js`
- `api/server/utils/import/importers-timestamp.spec.js`
- `api/server/utils/import/importConversations.database.spec.js`

The initial lookup for `packages/data-schemas/jest.config.js` returned file-not-found. File enumeration identified the actual `.mjs` path, which was then read. This was a discovery correction, not a failed test. No test command has yet been selected or executed for this slice.

## Prior corpus evidence

Use the [existing reconciliation](../../../corpus-reconciliation.md) and its retained evidence in place. All 820 conversations and 9,731 retained messages matched the current import representation; 107 skips and material source losses were accounted for. Do not rerun the reconciliation merely to populate this new slice: rerun only if the source or live corpus changes or a specific finding requires it.
