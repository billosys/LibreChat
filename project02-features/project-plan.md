# Project02 — LibreChat features

| Metadata | Value |
|---|---|
| Project | project02-features |
| Status | Planned — expanded feature roadmap; no arc opened |
| Depends on | Source/export format investigation and a scoped design before each feature |
| Blocks | Resource import, project context, local libraries and CLI workflows |
| Related | [Project01 portable persistence](../project01-portable-persistence/project-plan.md) |
| Implementation | `features` at `../features` from this planning worktree; see [repository workflow](../repository-workflow.md) |

## Goal

Add practical LibreChat features as small, separable changes that remain easy to maintain alongside upstream. Begin with importing memories and projects through the UI, then support prompt and agent imports, richer project context, local resource libraries and command-line automation. Project import covers Claude and ChatGPT/OpenAI exports, including an explicit assessment of whether each supplied export contains enough metadata to reconstruct conversation organization in LibreChat’s Projects sidebar. This project implements application features; Guildhall's broader memory research remains separate.

## Arc roadmap

| Arc | Intended capability | State |
|---|---|---|
| `arc01-import-memory` | Import existing memories through the LibreChat UI, with an understandable result and usable persisted memories | Planned; source formats and target semantics to investigate |
| `arc02-import-projects` | Inspect Claude and ChatGPT/OpenAI exports for sufficient project/membership metadata; populate LibreChat’s Projects sidebar and place imported conversations under their source projects where supported, explaining incomplete or unrecoverable mappings | Planned; source-format investigation and reconstruction policy required |
| `arc03-import-prompts` | Import prompt files/bundles into prompt groups with preview, validation, provenance and repeat-import behavior | Planned; define supported formats and group/version mapping |
| `arc04-import-agents` | Import agent definitions and resolve supported skill/resource dependencies, reporting missing dependencies and unsupported settings | Planned; define package contract and dependency/permission handling |
| `arc05-project-instructions-and-knowledge` | Give projects usable instructions and knowledge resources, with explicit conversation inheritance and access behavior | Planned; further design needed for precedence, retrieval and resource boundaries |
| `arc06-local-resource-libraries` | Connect local prompt and agent libraries with explicit refresh, change previews and conflict reporting; reuse existing skill source facilities where applicable | Planned; further design needed; start with one-way source-managed resources |
| `arc07-resource-management-cli` | Inspect, validate and import supported resources from the terminal using the same application services as the UI | Planned; further design needed; reuse resource contracts and expose machine-readable outcomes |

The Operator reports projects missing after the Claude conversation import. Treat that as the investigation starting point, not proof that a particular export contains recoverable project data. On 2026-09-21 the Operator requested broader feature planning from the two research artifacts and explicitly chose to expand existing Arc02 for both Claude and GPT exports. No separate project08 or duplicate project-import arc is created.

Define arcs in detail when they approach execution; no arc directories, slices or implementation prompts are opened by this roadmap. Numbering is organizational, not a universal execution dependency. Arcs01–04 establish their concrete import contracts; Arc06 and Arc07 reuse those contracts and existing supported skill APIs. Arc05 supplies the application behavior for richer project instructions/knowledge, distinct from Arc02's organization and metadata mapping; Arc02 does not require that richer context capability to deliver project membership import. Arc03 and Arc04 are the clearest next import additions; Arc05–Arc07 require more design before implementation assignment.

## Research inputs and shared boundaries

- [Memory-import research](artifacts/memory-import-research.md) informs Arc01, including memory visibility/permissions, validation, token limits and the absence of an import workflow at its inspected baseline.
- [Skills, prompts, agents and project-import research](artifacts/skills-prompts-agents-project-import-research.md) informs Arcs02–07. It records existing skill upload/deployment/sync paths, prompt/agent APIs without equivalent package-import workflows, and a project model lacking usable instructions/knowledge resources at its inspected baseline.
- These are static research inputs, not implementation or runtime acceptance. Revalidate the relevant findings against the assigned Guildhall source baseline when opening each arc.
- Reuse supported skill import/source facilities; this roadmap does not add a duplicate skills importer. Permission-gated visibility is a prerequisite/UX concern, not proof that a feature is absent.
- Preview, validation, source provenance, repeat-import behavior, scoped authorization and partial-failure reporting are shared import requirements. Extract common machinery from concrete importer needs rather than making a general import platform a prerequisite.
- Keep source/archive analysis in the owning import arc. Broader archival persistence and storage-neutral contracts remain coordinated with Project01. CLI and local-library operations must use application services rather than bypass validation through direct database writes.

## Arc02 — imported-conversation organization in the Projects sidebar

The explicit user-facing outcome is the **Projects sidebar**: create the supported source project entries and associate imported conversations with the correct projects so the organization remains visible after reload. This arc does not recreate a Claude/GPT knowledge workspace or apply project instructions; those are separate Arc05 concerns. Unresolved membership must remain visibly accounted for rather than silently assigning a guessed project.

Inspect the supplied files or export bundle before creating projects or assigning conversations. Do not assume that either provider guarantees project metadata in every export version.

1. Inventory source project identifiers/names, conversation identifiers and explicit membership links, retaining source-file locators and provenance. Only source information needed to reconstruct the sidebar organization is required for this capability.
2. Preview reconstruction sufficiency per relationship and across the import: reconstructable, partial, absent, ambiguous/conflicting or malformed. Account for every conversation in the import set, distinguishing explicit absence of project membership from unknown membership.
3. Reconstruct supported projects and memberships using a deterministic mapping from provider/source identities to destination identities. Names and conversation titles are not unique identity keys. Define repeat-import, existing-project collisions, partial failure and safe retry behavior before implementation.
4. If metadata is insufficient, explain the missing information and offer explicit choices such as conversation-only import, deferring affected records or supplying a manual mapping. Any heuristic/manual grouping must be labeled and confirmed; it cannot be reported as recovered source organization.
5. Report actual created project entries, linked conversations, skipped records, conflicts and unresolved memberships. Verify that the Projects sidebar shows the imported projects and their correct conversation membership after reload. Preserve existing data and ordinary ownership/tenant rules. Validate both provider families with version-identified synthetic fixtures covering complete, partial, missing, conflicting and malformed metadata, plus repeat import and interrupted/retried operations.

Successful support includes an honest insufficiency result for an export that lacks the necessary metadata. It does not promise reconstruction from information absent in the supplied source.

## Completion and approach

- Memory, project, prompt and agent imports are usable from the UI, preserve supported source information and explain rejected or unsupported items. Arc02 assesses reconstruction sufficiency for both provider families before writes.
- Project context has explicit inheritance/access behavior; local libraries support inspectable refresh/conflict handling; CLI workflows share application semantics and provide machine-readable results. Each capability requires its own scoped design and validation before acceptance.
- Define repeat-import and relationship/identity behavior during each arc's design; protect existing user data and preserve source provenance.
- Branch new feature work from `billo-guildhall` and merge completed, validated work back into it; `features` follows this same rule. Follow [BILLO.md](../BILLO.md), including both required commit trailers. This supersedes treating features as an independent integration line.
- Keep changes focused, use existing extension points and validate against the applicable upstream baseline. Coordinate persistence contracts with Project01 without making the entire Guildhall conversion a prerequisite.

This remains a one-contributor planning roadmap at the Operator's request. Future implementation/review assignments follow the selected collaboration workflow when each arc is opened. The [ledger](ledger.md) records the initial open completion criteria. No feature implementation is assigned by this sketch.

## Version History

| Version | Date | Change |
|---|---|---|
| v1.2 | 2026-09-21 | Added Arcs03–07 from the recorded research and expanded Arc02, at the Operator's direction, to Claude/GPT Projects-sidebar reconstruction with metadata-sufficiency checks; all arcs remain unopened. |
| v1.1 | 2026-09-20 | Recorded Operator-required Guildhall branch base/merge destination and commit trailers; feature scope and unopened arcs unchanged. |
| v1.0 | 2026-09-20 | Added the Operator's memory-import and project-import feature roadmap, with development isolated on the features worktree. |
