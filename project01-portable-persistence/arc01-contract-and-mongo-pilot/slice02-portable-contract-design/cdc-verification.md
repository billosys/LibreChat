# CDC verification — Slice02 initial CC evidence

## Verdict and scope

**2026-09-21: partial evidence reproduced; initial CC assignment returned for correction. Slice02 remains open.** This is an actual CDC review of CC commit `99d5ecd794d00cd1c0db7a199633042766af5953`, assigned by [cc-prompt.md](cc-prompt.md) at planning commit `44c77142f97f10082f5628ca76b4d2d1bd6ce4fd`. CDC is the existing LibreChat/Guildhall design conversation; CC identifies itself in [intake.md](artifacts/cc-evidence01/intake.md) as a separate Codex API session with no exposed session ID. The Operator relayed its report. No CRC is assigned.

Source remained clean at `3e3c5410d3863118fdba694fb0cd51baeb7102f9` on `billo-guildhall`. The seven-file CC packet and initial prompt are preserved unchanged. Review artifacts live in [artifacts/cdc-review01](artifacts/cdc-review01/result.json); the [review script](artifacts/cdc-review01/review.py) loads the committed CC verifier without calling its writing `main`, runs the sealed harness into a temporary directory and applies separate structural checks. The script pins manifest membership to the reviewed commit so future packets do not change this review's denominator.

## Reproduced evidence

- All structured replay output equals CC's result, including 16 read cases, two admission gates, three preflight cases and three detected negative controls. No database or application build ran.
- All 117 `(record, field)` keys are present exactly once, and their actual classifications agree with the baseline schema/default-selection information. Ten selected roots and twelve nested exclusion strings match the requested sets.
- All 23 inventory source fingerprints match the unchanged source. All 87 artifact hashes present at the reviewed commit pass, including the six CC manifest entries. The CC commit changes exactly its seven allowed files and has both required trailers.
- The report correctly leaves S01–S07 and Slice01 acceptance open and distinguishes Node 22 replay from the repository's Node 24.16.0/source-build requirement.

This confirms CC's actual run and structural observations. The underlying comparison harness was authored by this CDC context during one-contributor investigation; rerunning it does not independently validate its design or establish integrated Mongo conformance. No historical gate is accepted by relabeling the author.

## Findings requiring correction

### R1 — verifier accepts undeclared drift and rewrites sealed evidence

`artifacts/cc-evidence01/replay.py:193–199` compares behavior but labels every provenance difference “allowed”; the caller does not reject those differences. The review supplied a wrong Node version, wrong source head and wrong compiler digest separately to this predicate. All three were accepted. The driver does check the real source head later; these controls concern its result-comparison predicate, not a claim that the entire driver accepts an actually changed checkout. Runtime equality is not enforced before replay.

`validate_inventory` at lines 179–190 verifies key sets and totals but accepts an invalid classification label. The actual delivered labels are correct under CDC's separate check; the failure is that the verifier does not establish its own classification claim.

`main` at lines 202–226 regenerates `nested-fields.json`, overwrites `replay-result.json` and appends to `execution.log` in the fixed sealed packet, with no read-only mode or seal guard. It validates generated inventory rather than the artifact submitted for review and performs source checks after replay. A reviewer must not run that entrypoint against the committed packet. CDC did not do so.

Required correction: an explicit, fail-closed provenance and preflight contract; validation of the submitted inventory with independently derived classifications; a read-only verification mode using temporary outputs; and a guarded authoring mode that refuses a sealed destination. Keep new controls in the next packet, never repair the sealed one.

### R2 — named roots are present, but the requested nested map is incomplete

The ten root records mostly contain prose summaries. All twelve exclusion records at `replay.py:173` carry the same generic preservation text, without the requested explicit array/member path and permitted siblings. The root `applicability` text is likewise generic rather than specifying each server/public/probe boundary. The `files` witness names “BaseClient and formatMessages” without a file/symbol/span, although the prompt required precise witnesses or a bounded `not established` finding.

Concrete omissions affecting the next design decision:

- `packages/data-provider/src/types/agents.ts`, `Agents.ToolCall.backgroundTask`, lines 103–117 declares `settledAt: Date` and `resultClaim.claimedAt: Date`. This is a declared non-JSON leaf, not evidence of any historical corpus value. The public projection removes `resultClaim` but not `settledAt`.
- `packages/data-provider/src/types/files.ts`, `TFile`, lines 150–221 includes optional `_id`/`__v`, `expiresAt?: string | Date`, nested metadata, and Date/string timestamps. Those are concrete engine-metadata/temporal compatibility questions; a bare pointer to `Partial<TFile>` leaves them implicit.
- `packages/data-provider/src/types/web.ts`, `SearchResultData`, lines 43–58 declares both `organic[]` and `topStories[]`. The exclusion path `attachments.web_search.organic.highlights` crosses both `attachments[]` and `organic[]`; retaining only the former array boundary would be wrong. This source is not in CC's source-fingerprint list.
- `packages/data-schemas/src/methods/conversation.ts`, `getConvoOwnership`, selects `user tenantId subagentThread`; its returned `subagentThread` is the selected lineage object, used as a discriminator. A reduced boolean/discriminator-only DTO is a proposed contract option, not the current method's return shape. Qualify the report/inventory wording accordingly.

Required correction: complete the original ten-root bounded map, naming members/leaf domains, open boundaries, projection applicability and exact witnessed array traversal. Do not silently choose a decoder, strip nested IDs, or declare stored historical types from this source evidence. No broad caller census or live corpus investigation is requested.

### R3 — intake and raw-inspection coverage are asserted without the required detail

`intake.md` asserts complete bounded reads but records no actual per-document read extents, selected declaration extents, truncation recovery, or identifiable query outputs. `execution.log` contains the replay and validator commands, then retrospective prose about failed searches/manifests; it does not retain the required structured-data query commands/results or the bounded witness searches behind the match counts. This does not prove that CC failed to read them, but the submitted packet does not support the stronger retained-evidence claim.

Required correction: perform fresh, bounded reads/queries for the affected inventory, record real commands/status/results and actual loaded extents, and distinguish old reported-only attempts from newly captured evidence. Do not fabricate historical stdout, timestamps or receipts. Existing replay output is reusable; repeating application suites or older investigation passes is unnecessary.

## Ledger walk and bubble-up

| Row | Review disposition |
|---|---|
| S01 | Open. The scoped reload/probe harness is reproduced; actual composition wiring and complete caller preservation remain pending. |
| S02 | Open. Membership/classification counts reproduced; R2 blocks treating the nested inventory as complete DTO decision input. |
| S03 | Open. R2 leaves important concrete value/presence/projection distinctions insufficiently mapped; full failure/patch contracts remain CDC-owned. |
| S04 | Open, unreviewed here. Cursor characterization/reproduction has its existing owner and separate scope. |
| S05 | Open, unreviewed here. Preserved repository artifacts do not discharge original-source/corpus fidelity obligations. |
| S06 | Open. No production assignment, source-build proof or integrated adapter conformance; R1 must be corrected for a dependable evidence driver. |
| S07 | Open. Commit scope/trailers/hashes verified; R1/R3 require evidence-tooling and intake corrections before accepting this bounded packet. |

The parent plans now record returned-for-correction rather than pending relay. Existing architecture, three-slice roadmap, scope and acceptance criteria remain unchanged. The next assignment is [cc-prompt-iteration01.md](cc-prompt-iteration01.md), limited to R1–R3 and a new seven-file `artifacts/cc-evidence02` packet. This is the first CC correction iteration; earlier exploratory passes are not erased or renamed. CDC retains DTO policy, composition/file fence, D07 prerequisites and the later sizing decision. Once the corrected evidence is sufficient, use it to make those decisions rather than open another general research loop.
