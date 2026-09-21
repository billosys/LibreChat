# Operator decisions — normalization and development branches

Recorded 2026-09-20, after Slice02's first design pass. These decisions supplement that pass without rewriting its preserved evidence.

## Practical storage design

The Operator initially allowed denormalization for practical/performance reasons, then clarified that this was barely a recommendation and should not steer the design by itself. Complete normalization is not required, but denormalization is not the chosen direction either. The instruction is to use the existing Guildhall/Lance plans to make lightweight, revisable data-model guesses; deep research and a frozen future schema are unnecessary. The earlier message-link question concerned keeping Mongo's physical IDs out of the portable interface while avoiding another lookup on every save.

Denormalized references, duplicated logical IDs, embedded membership or adapter-owned indexes are valid design candidates. Select them by read/write cost and maintainability, with a clear authoritative value and update/recovery rules. Tenant/owner isolation, retry behavior and relationship correctness still apply. These remain options, not a preference ranking or a requirement for a Mongo migration. The [working identity direction](interface-design.md#working-identity-direction-toward-the-cognitive-data-plane) now guides D02: stable logical references; separate entity/revision/representation identity; explicit provenance and relationships; physical mappings inside each adapter. First explore a named ordinary-turn persistence operation that can reuse the saved Mongo record internally, while preserving the existing sequence and partial outcomes. Denormalization and receipts remain fallback candidates to evaluate against that direction, not goals in themselves.

## Source worktree decision — D06 resolved

The Operator requested `billo-guildhall` for this project's implementation and `features` for independent UI features, with planning retained separately and main kept pristine. See [repository workflow](../repository-workflow.md) for actual paths, upstream references and synchronization policy.

Upstream dev was fetched and both branches start at `fe79265b2f47937051625719f3ba5080189912c1`. Main was fast-forwarded to `0cc52cd8c71e8ccbceb8f001ddf8059b10501fce` and tracks upstream main. No branch was created from the orphan planning history. This resolves D06's missing source lineage; it does not resolve D07's build/runtime validation or the remaining contract choices.

Slice01 and the first Slice02 packet remain historical evidence at `ba44443fd`. Resume source work from the Guildhall worktree, refreshing relevant instructions, dependency/plugin changes and test prerequisites before implementation. The original baseline's saved artifacts and checksums are preserved.

Project02 owns the newly requested UI memory/project imports. Coordinate shared persistence needs, but do not silently fold those features into Project01's ordinary-turn Mongo pilot.
