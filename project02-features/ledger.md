# Project02 composition ledger

Initial criteria only; all remain open and will be refined when the arcs are designed.

| ID | Criterion | Verify | Significance | Origin | Status | Evidence |
|---|---|---|---|---|---|---|
| P01 | Memory import is usable through the UI and preserves supported memory content | Source fixture → import → persisted/reloaded result, with repeat-import and unsupported-item checks defined in Arc01 | correctness-grade | Operator feature request | open | Roadmap only |
| P02 | Project import preserves supported project content and available relationships | Source fixture → import → UI reload, with membership, missing-source and repeat-import checks defined in Arc02 | correctness-grade | Operator feature request | open | Roadmap only |
| P03 | Features compose with LibreChat and remain maintainable against upstream | Focused commits, applicable regression/UI checks and review at the integrated source revision | correctness-grade | Operator upstream-sync preference | open | Separate features branch/worktree created; implementation pending |
