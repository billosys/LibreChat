# Billo Systems — LibreChat fork instructions

Read this addendum before choosing a branch, editing files or creating a commit in the Billo Systems fork. It records the Operator's fork policy. It takes precedence over inherited `AGENTS.md` / `CLAUDE.md` instructions about branching and integration for **our fork**; their engineering, testing and module-boundary guidance still applies. Direct Operator instructions govern any exception.

## Development and integration

- Always use **`billo-guildhall`** as the source-development baseline and integration branch. Work there by default, in its dedicated worktree.
- **Never create or amend a commit on `main`.** Keep `main` pristine and aligned with upstream release history. Synchronize a clean main only by fast-forward from `upstream/main`; investigate divergence rather than hiding it with a reset or merge commit.
- Create every new source/feature branch from the current `billo-guildhall` tip, never from `main`, upstream `dev`, or the orphan planning branch. Use a separate worktree for parallel feature work and verify the actual branch/path with `git worktree list` and `git branch --show-current` before editing.
- Work on the assigned feature branch while implementing its scoped feature. **Merge all completed feature-branch work back into `billo-guildhall`**, after the required tests and review/acceptance gates pass. Completion includes that integration and verification of the resulting integration tip. Preserve logical commit history; use a normal merge (fast-forward when possible). Give any newly created merge commit the required footer below.
- The existing `features` branch/worktree follows this same integration policy. It is not a permanently separate release line. Do not merge unfinished or unrelated work just to synchronize branch tips.
- Fork PRs target `billo-guildhall` in `billosys/LibreChat`; set the base explicitly. An intentionally prepared contribution to `danny-avila/LibreChat` still follows upstream's `dev` target. Do not mistake inherited “branch from dev” guidance for our fork policy.
- Bring upstream updates into the Guildhall integration line deliberately and validate the combined result. Preserve upstream commits unchanged; do not add our authorship trailers to inherited upstream history.

## Planning is a separate worktree

The existing orphan **`planning`** branch is the explicit documentation exception to the source-branch rule. Keep project/arc/slice plans, ledgers, research and evidence in `.worktrees/planning`. Never merge that orphan history into source branches. Read its `AGENTS.md`, `README.md`, `repository-workflow.md` and owning plan/ledger before ledgered work.

The usual worktrees beneath the repository root are `.worktrees/billo-guildhall`, `.worktrees/features` and `.worktrees/planning`; verify their current paths rather than assuming the shell is already in the right one. The source copy of this addendum is canonical; the planning branch carries a matching copy for agents starting there. Keep those copies consistent when policy changes.

## Required commit footer

Every commit **we author**, on every branch including `planning` and feature branches, must end with both exact trailers, separated from the commit text by a blank line:

```text
<COMMIT TEXT>

Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

Include both trailers exactly once. Preserve the actual Git author and any other legitimate attribution. Apply the rule to ordinary commits, amendments, squash commits and newly authored merge commits; preserve it across rebases/cherry-picks. For multiline messages, use a message file with `git commit -F` rather than shell interpolation. Inspect the final message, including when a tool generates it:

```sh
git show -s --format=%B HEAD
git show -s --format=%B HEAD | git interpret-trailers --parse
```

Before publication, check **all locally authored commits being published**, not just HEAD. A fast-forward creates no new commit. Inherited upstream commits retain their original messages and authorship. Do not automatically rewrite published history; the Operator's 2026-09-20 request specifically authorized adding these trailers to our existing unpublished history.

## Working discipline

- Inspect the worktree status and staged index. Stage and commit explicit paths; preserve unrelated edits, editor swap files, local settings and ignored files. Do not use broad cleanup/reset/stash operations to make a checkout look clean.
- Keep fork-specific guidance in this addendum, with a small way-finding pointer at the end of `AGENTS.md`, to reduce upstream merge friction. Do not weaken inherited source quality rules.
- Keep feature commits focused and separable. Follow the existing package/module boundaries, injected dependencies, scoped authorization and applicable testing/typechecking/performance requirements. A source build is not a typecheck; a prototype is not integrated conformance.
- Keep private chat exports, local databases, credentials, environment files and runtime data out of commits. Use disposable synthetic fixtures for investigation unless a specific live-data operation is authorized.
- Preserve sealed evidence and its source hashes. If history is deliberately rewritten, retain an old-to-new commit map rather than silently rewriting historical experiment records.
- Report the branch, commit and meaningful validation, including limitations. One contributor's self-checks do not become independent acceptance, and Expedited Mode does not waive scope or review gates.

## Policy record

2026-09-20: the Operator made `billo-guildhall` the source base/integration branch, required completed feature work to merge back, prohibited commits on main, required both co-author trailers on all our branches, and authorized updating our existing unpublished commit messages. This supersedes the earlier policy of two independent source integration lines; the separate orphan planning workflow remains in force.
