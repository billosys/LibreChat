# Project02 — LibreChat features

| Metadata | Value |
|---|---|
| Project | project02-features |
| Status | Planned — initial sketch; no arc opened |
| Depends on | Source/export format investigation and a scoped design before each feature |
| Blocks | UI import of memories and projects |
| Related | [Project01 portable persistence](../project01-portable-persistence/project-plan.md) |
| Implementation | `features` at `../features` from this planning worktree; see [repository workflow](../repository-workflow.md) |

## Goal

Add practical LibreChat features as small, separable changes that remain easy to maintain alongside upstream. Begin with importing memories and projects through the UI, analogous to conversation import. This project implements application features; Guildhall's broader memory research remains separate.

## Arc roadmap

| Arc | Intended capability | State |
|---|---|---|
| `arc01-import-memory` | Import existing memories through the LibreChat UI, with an understandable result and usable persisted memories | Planned; source formats and target semantics to investigate |
| `arc02-import-projects` | Import projects and available project metadata/relationships, including conversation membership where the source supplies it | Planned; inspect what the Claude export contains and what conversation import omitted |

The Operator reports projects missing after the Claude conversation import. Treat that as the investigation starting point, not proof that all project data is present in the export or recoverable. Define both arcs in detail later; no arc directories, slices or implementation prompts are needed now. The numbering is the proposed order, not an assumed technical dependency between importers.

## Completion and approach

- Both imports are usable from the UI, persist the supported source information and explain rejected or unsupported items.
- Define repeat-import and relationship/identity behavior during each arc's design; protect existing user data and preserve source provenance.
- Branch new feature work from `billo-guildhall` and merge completed, validated work back into it; `features` follows this same rule. Follow [BILLO.md](../BILLO.md), including both required commit trailers. This supersedes treating features as an independent integration line.
- Keep changes focused, use existing extension points and validate against the applicable upstream baseline. Coordinate persistence contracts with Project01 without making the entire Guildhall conversion a prerequisite.

This is a one-contributor planning sketch at the Operator's request. Future implementation/review assignments follow the selected collaboration workflow when each arc is opened. The [ledger](ledger.md) records the initial open completion criteria. No feature implementation is assigned by this sketch.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.1 | 2026-09-20 | Recorded Operator-required Guildhall branch base/merge destination and commit trailers; feature scope and unopened arcs unchanged. |
| v1.0 | 2026-09-20 | Added the Operator's memory-import and project-import feature roadmap, with development isolated on the features worktree. |
