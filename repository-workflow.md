# Repository branches and worktrees

Operator decision, 2026-09-20: keep `main` pristine for upstream synchronization; use separate sibling worktrees for Guildhall integration and standalone LibreChat features. Planning stays on its existing orphan branch.

All paths below are relative to `/Users/oubiwann/lab/billosys/LibreChat/`.

| Branch | Worktree | Purpose |
|---|---|---|
| `main` | `.` | Unmodified upstream release checkout; fast-forward synchronization only; no local feature/planning commits |
| `planning` | `.worktrees/planning` | Canonical plans, decisions, ledgers and evidence for both projects; never merge into application branches |
| `billo-guildhall` | `.worktrees/billo-guildhall` | Project01 persistence interface and Guildhall integration work |
| `features` | `.worktrees/features` | Project02 independently scoped LibreChat features |

## Upstream and integration policy

`origin` remains `git@github.com:billosys/LibreChat.git`. `upstream` is `https://github.com/danny-avila/LibreChat.git`, verified against the repository's package metadata. Local `main` now tracks `upstream/main`. Its ordinary update is `git fetch upstream` followed by `git merge --ff-only upstream/main` from the clean main checkout. A diverged main must be investigated, not reset or merged to conceal divergence.

Both implementation branches start from `upstream/dev`, following the source's branch policy. They intentionally have no tracking branch yet; first publication should explicitly target the corresponding branch on `origin`. No remote branch has been created or pushed by this setup. Upstream contribution PRs still target `dev`; no feature PR should target pristine `main`.

Keep feature commits focused and independently reviewable, avoiding unrelated formatting/refactoring and unnecessary dependencies on Guildhall. Both development branches can incorporate upstream `dev` updates with tests at the resulting commit. When a feature is needed in Guildhall, integrate its reviewed commits explicitly rather than developing the same change twice. Do not automatically merge the two work streams or rewrite published history. Exact merge/rebase sequencing can be chosen when changes exist.

## Verified setup

- Prior `main`: `ba44443fdb232bbe6d4977e2619774b5a72586ac`, with no local commits relative to fetched upstream main and 27 incoming commits.
- `main` fast-forwarded to fetched `upstream/main`: `0cc52cd8c71e8ccbceb8f001ddf8059b10501fce`. No merge or locally authored source commit was created.
- Both new branches/worktrees: `fe79265b2f47937051625719f3ba5080189912c1`, the fetched upstream dev tip. They are independent siblings, not stacked on one another.
- Source branch instructions are unchanged between the original baseline and these worktrees. The earlier missing-dev prerequisite is resolved by using the verified upstream remote; the fork does not need a fabricated dev lineage.

Prior Slice01/Slice02 evidence remains tied to `ba44443fd`, not these newer source tips. The principal inspected save/read source files are unchanged in the bounded comparison, but `package-lock.json` and the Mongo/Meili plugin changed; prior test results are not current-build acceptance. Refresh source/dependency/build evidence in `billo-guildhall` before implementation. Historical artifacts and their checksums remain unchanged. Their old hard-coded checkout checks describe the original experiment environment and must not be treated as current-worktree verification.

The new worktrees contain tracked source only. Local dependency installations and ignored runtime configuration are not copied or linked by this setup. No reinstall, build, database operation or application restart is part of branch creation.
