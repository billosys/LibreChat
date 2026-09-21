# CC evidence02 intake

## Assignment and acknowledgement

This is the CC correction iteration `cc-prompt-iteration01.md` for Project01
Arc01 Slice02, “Portable contract design.” I acknowledge the assignment as a
CC/API session operating with the Two-Contributor Workflow (CDC + CC). The
session identifier is not exposed in this API context. This delivery is
proposed-done only; CDC review and Operator acceptance remain open.

The reviewed predecessor delivery is commit `99d5ecd7` (`cc-evidence01`). The
correction responds to the CDC findings recorded in
`artifacts/cdc-review01/cdc-verification.md`: R1 verifier rigor, R2 submitted
inventory richness, and R3 fresh raw query evidence.

## Authority and fence

The planning worktree is `/Users/oubiwann/lab/billosys/LibreChat/.worktrees/planning`
on branch `planning`. The source worktree is
`/Users/oubiwann/lab/billosys/LibreChat/.worktrees/billo-guildhall` on branch
`billo-guildhall`, pinned for this iteration at
`3e3c5410d3863118fdba694fb0cd51baeb7102f9`; source status was clean at
preflight. The introducing prompt is commit
`ff7c50dbfe13eb51477b6aef4d2f203e63469359`, SHA-256
`cd8bdf9db78247d4a15d14ff76106e1e0ce74a45a8b765097bbfeba23bd6904d`.

The packet is limited to the seven files in this directory. Existing
`cc-evidence01`, CDC review artifacts, planning documents, and the pinned
design-pass inputs are preserved and are not rewritten. No source, application,
dependency, build, test-suite, live MongoDB, private export, migration,
restart, push, PR, plan, or ledger change is authorized by this packet.

## Read extents

The iteration prompt was read at lines 1–93 and its predecessor at lines
1–124. Planning state was read from `slice-plan.md` lines 1–110, `ledger.md`
lines 1–13, and `cdc-verification.md` lines 1–61. The packet predecessor was
read from `cc-evidence01/intake.md` lines 1–48, `report.md` lines 1–108,
`replay.py` lines 1–231, and `execution.log` lines 1–85.

Local operating instructions were read from planning `AGENTS.md` lines 1–25,
`BILLO.md` lines 1–52, and `README.md` lines 1–22; source instructions were
read from source `AGENTS.md` lines 1–116, `BILLO.md` lines 1–52, and
`CLAUDE.md` lines 1–376.

The required Project01 and Arc01 plan sections were read: project goal and
boundaries lines 13–21, definition of done lines 35–43, workflow and authority
lines 70–115; Arc01 scope lines 29–33, slice roadmap lines 35–45, and workflow
and source boundaries lines 55–80. The governing framework material was read
from the project-management README lines 1–178, canonical iteration guidance
lines 126–250, top-down iteration guidance lines 134–188, implementation
prompt authoring lines 162–342, methodology roles/workflow lines 75–148 and
303–331, independent verification lines 1–98, evidence capture lines 1–51,
validity lines 1–52, and testing validation gates lines 1–82.

The pinned design-pass inputs were read from `read-contract.md` lines 1–84,
`protocol.md` lines 1–11, `experiment.cjs` lines 1–75, `validate.py` lines
1–48, and the pass04 handle source lines 1–58. Additional source declarations
and enclosing logic were read from the web, agent, file, ownership, schema,
provider, feedback, filter, content, message-method, message-route, and agent
controller/request/resume/response locations recorded by this iteration's
driver in `execution.log`.

The read was completed in bounded chunks; no unresolved truncation is being
treated as a source read.

## Data and contract coverage

The sealed pass05 matrix was queried for all 117 message/conversation fields,
including its `exclusions`, `providerOnly`, `interfaceOnly`, and `implicit`
populations. The predecessor inventory and result were queried for roots,
exclusions, behavior, and provenance. The CDC review result was queried in
full for the four rejected controls. This iteration also records fresh raw
`jq`, `rg`, and `sed` argv, cwd, exit status, stdout, and stderr in
`execution.log`; matrix and result outputs are partitioned rather than
silently truncated.

The submitted inventory retains the original top-level field membership and
117-row denominator while adding ten selected roots, member-level traversal
data, four applicability dimensions, bounded witnesses, twelve explicit
nested exclusions, permitted siblings, source references, and source
fingerprints. It records the required Date-bearing tool-call fields, the
unresolved `resultClaim`/`completionWakeup` shape boundary, TFile optional and
Date/string fields, web-result array boundaries, and the full
`getConvoOwnership` lineage selection.

The historical failed-attempt prose in evidence01 remains retrospective
reporting only. It is not reused as a fresh receipt. CDC still owns DTO shape,
codec/stringification, identifier stripping, legacy rejection, and acceptance
policy decisions.

## Execution boundary

`replay.py` exposes explicit `--capture`, `--verify`, and `--self-test` modes;
without a mode it exits with usage and never captures implicitly. Capture
refuses a sealed destination, validates the immutable submitted inventory,
checks source branch/head/clean status, runtime/compiler and all source
fingerprints, preserves any prior replay bytes before rerunning the pinned
harness, and records exact behavior and provenance equality. Verify validates
the sealed manifest, runs in a fresh temporary replay location, compares all
required keys with no wildcard differences, and checks packet hashes before
and after without writing to the packet. Self-test exercises the required
wrong-runtime, wrong-head, compiler/source digest, classification, denominator,
absent-vs-null, sealed-capture, preflight-sentinel, and packet-hash controls.

The packet stops at this proposed-done evidence boundary. No S01–S07 gate is
claimed closed here.
