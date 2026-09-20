# LibreChat → Guildhall: practical persistence work

The immediate goal is a portable application persistence boundary: first backed by existing MongoDB behavior, then exercised by one genuinely different backend.

Start with [Project01](project01-portable-persistence/project-plan.md). Its design package contains:

- [Source reconnaissance](project01-portable-persistence/research.md): what the current code actually does, and the limits of this first inspection.
- [Interface proposal](project01-portable-persistence/interface-design.md): domain contracts, compatibility obligations, and a first conversion candidate.
- [Backend decision proposal](project01-portable-persistence/backend-decision.md): SQLite, hosted by a local Rust service.
- [Project ledger](project01-portable-persistence/ledger.md): the still-open composition criteria.

Status: **initial research and draft design prepared; no application implementation or runtime validation performed**. SQLite and the staged service architecture are CDC recommendations for Operator review, not recorded Operator decisions.

Source baseline: `ba44443fdb232bbe6d4977e2619774b5a72586ac`, source branch `main`, inspected 2026-09-20. Origin: `git@github.com:billosys/LibreChat.git`. The source checkout had no tracked changes at intake. The planning branch is deliberately orphaned; its commit IDs do not identify an application build.

The next planning action is to settle the proposal's deployment assumptions and boundary, then detail Arc01 against a refreshed source baseline. No CC prompt is ready yet: its first slice must resolve the pilot's complete call graph, failure behavior, concrete DTOs, and executable acceptance tests.
