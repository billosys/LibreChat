# Repository branches and worktrees

Operator decision, 2026-09-20: [BILLO.md](BILLO.md) is the current fork policy. Always use `billo-guildhall` as the source baseline/integration branch; create new feature branches from it and merge completed, validated feature work back into it. Never commit on `main`. Planning stays on its existing orphan branch as the explicit documentation exception.

All paths below are relative to `/Users/oubiwann/lab/billosys/LibreChat/`.

| Branch | Worktree | Purpose |
|---|---|---|
| `main` | `.` | Unmodified upstream release checkout; fast-forward synchronization only; no local feature/planning commits |
| `planning` | `.worktrees/planning` | Canonical plans, decisions, ledgers and evidence for both projects; never merge into application branches |
| `billo-guildhall` | `.worktrees/billo-guildhall` | Project01 persistence interface and Guildhall integration work |
| `features` | `.worktrees/features` | Project02 scoped feature work; completed work merges into `billo-guildhall` |

## Upstream and integration policy

`origin` is `git@github.com:billosys/LibreChat.git`; current `upstream` transport is `git@github.com:danny-avila/LibreChat.git` (the setup originally used HTTPS). Local `main` tracks `upstream/main`. Its ordinary update is `git fetch upstream` followed by `git merge --ff-only upstream/main` from the clean main checkout. Investigate divergence; never create a local main commit to conceal it.

Create new source branches/worktrees from `billo-guildhall`, and merge all completed feature work back after its required validation/review gates. Fork PRs explicitly target `billo-guildhall`; intentional upstream contribution PRs still target upstream `dev`. Keep commits separable and verify integration at the resulting tip. Do not merge unfinished work or rewrite published history without specific authorization.

**Superseded policy:** both source branches were initially independent siblings created from upstream dev, with integration chosen case by case. The Operator's later instruction replaces that ongoing policy with Guildhall as the common base and required destination. The initial source lineage below remains accurate historical evidence. The clean `features` branch was fast-forwarded to the source policy commit `3e3c5410d3863118fdba694fb0cd51baeb7102f9`; both source worktrees now carry the same addendum.

Every locally authored commit, including planning and merge commits, uses both exact co-author trailers from BILLO.md. The Operator authorized a one-time message-only rewrite of our 12 unpublished planning commits; [the migration map](commit-message-migration.md) preserves the original IDs. Inherited upstream history is unchanged. No branch has been pushed by this work; live `origin` inspection showed only `main` at `ba44443fdb232bbe6d4977e2619774b5a72586ac` before the rewrite.

## Verified setup

- Prior `main`: `ba44443fdb232bbe6d4977e2619774b5a72586ac`, with no local commits relative to fetched upstream main and 27 incoming commits.
- `main` fast-forwarded to fetched `upstream/main`: `0cc52cd8c71e8ccbceb8f001ddf8059b10501fce`. No merge or locally authored source commit was created.
- Both new branches/worktrees: `fe79265b2f47937051625719f3ba5080189912c1`, the fetched upstream dev tip. They are independent siblings, not stacked on one another.
- At initial setup, source branch instructions were unchanged between the original baseline and these worktrees; the later Billo addendum now overrides fork branch policy. The earlier missing-dev prerequisite is resolved by using the verified upstream remote; the fork does not need a fabricated dev lineage.

Prior Slice01/Slice02 evidence remains tied to `ba44443fd`, not these newer source tips. The principal inspected save/read source files are unchanged in the bounded comparison, but `package-lock.json` and the Mongo/Meili plugin changed; prior test results are not current-build acceptance. Refresh source/dependency/build evidence in `billo-guildhall` before implementation. Historical artifacts and their checksums remain unchanged. Their old hard-coded checkout checks describe the original experiment environment and must not be treated as current-worktree verification.

The new worktrees contain tracked source only. Local dependency installations and ignored runtime configuration are not copied or linked by this setup. No reinstall, build, database operation or application restart is part of branch creation.

## Version history

| Date | Change |
|---|---|
| 2026-09-20 | Operator made Guildhall the source base/merge target, required co-author trailers and authorized rewriting unpublished local messages; preserved the orphan planning exception and upstream main. |
| 2026-09-20 | Initial pristine-main and sibling-worktree setup; independent source-line policy is now superseded above. |
