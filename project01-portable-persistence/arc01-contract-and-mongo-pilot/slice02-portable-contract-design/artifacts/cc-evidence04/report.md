# CC iteration03 report — source declarations and composed projections

## Disposition

Iteration03 rebuilt R2 within the same ten-root / 117-field fence. R1 and R3 were retained and freshly reproduced. The packet is proposed-done pending CDC review and Operator acceptance; no ledger row, slice, arc or implementation gate is closed.

## Evidence and limits

The packet contains exactly seven files: `intake.md`, `report.md`, `nested-fields.json`, `replay-result.json`, `execution.log`, `replay.py`, and `SHA256SUMS`. The driver records argv, cwd, status, stdout and stderr for each command, including failed attempts. It runs the sealed pass05 storage-double harness and a syntax-only TypeScript extractor. It does not change source, install dependencies, run application suites, access Mongo/private exports, or claim corpus values from `Mixed`/`unknown` declarations.

Source state was `3e3c5410d3863118fdba694fb0cd51baeb7102f9`, clean, with Node `v22.22.3` and TypeScript `5.9.3`. The repository's Node 24.16.0/D07 and source-build requirements remain unverified. The earlier `cc-evidence03` packet and all prompts/reviews were preserved unchanged.

## R1 — submitted-result and sealed-path verification

The pass05 result was replayed from its sealed bytes. The new `replay-result.json` equals the pinned pass05 result and the successful capture compared submitted, baseline and fresh values across all behavior/provenance keys: 16 read cases, 2 gates, 3 preflight cases and 3 negative controls. The new verifier loads the submitted result, validates fresh source declarations and compares fresh harness output to both submitted and baseline. Sealed verification is read-only. Self-test runs against temporary copies and has a positive unchanged-packet check; its negative controls are reported separately below.

The older R1 defects are not silently reclassified: evidence03's resealed-result acceptance and tuple-expression control remain historical review findings. The new driver exercises the actual verification path with wrong-head, wrong-result and mutation controls. Hashes and self-tests are structural evidence only; they are not CDC acceptance.

## R2 — declaration-grounded corrections

`nested-fields.json` contains 46 requested declaration records and 226 member rows generated from fresh source syntax. Every submitted declaration identity, source span, exact declaration text, literal/member set, type or initializer, branch label and source reference is compared with a fresh extraction. No cosmetic minimum member count is used.

The concrete repairs are:

- `userSubmittedMessageFieldPaths[]` is the strict `path`/`field` pair from `filters.ts:184-189`; `source` and `operation` are rejected.
- `examples[].input.content` and `examples[].output.content` are required strings from `schemas.ts:867-874`; role/files are rejected while storage breadth remains unresolved.
- content branches use element-level paths. Error and summary paths have no fabricated wrappers; the summary content elements and boundary fields are represented literally.
- `Agents.ToolCall` preserves optional `backgroundTask` with required version/taskId/toolName/status/settledAt `Date`, optional cancelled/resultClaim, and the exact nested claim/approval members. `Date` is not mutated to a transport string.
- `TMessage.files?: Partial<TFile>[]` records the shallow use-site wrapper separately from the local TFile declaration. `TFile.metadata` is expanded only beneath file records; message metadata remains an open record.
- attachment branch IDs (`tfile-intersection`, `numeric-expiry-pick`, `partial-filename-filepath-pick`) are metadata, not path segments. The numeric `expiresAt` branch is required and numeric; `Pick` and `Partial` effects remain distinct.
- processed search fields are attached to `organic[]`/`topStories[]` element declarations through `ProcessedSource`; `References`, `Highlight`, `MediaReference` and `UsedReferences` remain explicit local declarations. `web_search` exclusions are not copied to `file_search`.
- lineage keeps optional `parentAgentId`, required siblings, optional root semantics and the full `getConvoOwnership` access-probe mapping. `codeWorkspaces` keeps an optional root and required `environmentId`/`workspaceId` entries.

The projection map stores source literals and canonical array paths. Its validator rejects an exact or descendant excluded survivor, the evidence03 `resultClaim` cross-exclusion counterexample, and a container falsely described as fully preserved. It accepts `organic[]` with `sitelinks` and `highlights` removed while preserving siblings. `metadata.publicMessages` is included with a nested exclusion, not excluded as a whole.

## R3 — replay/query coverage

The corrected queries use `messageSchema` and `convoSchema`, retain complete field-name arrays, and retain provider-only, interface-only and implicit populations at the record level. Successful-but-empty or wrong-shaped results fail the driver. The old wrong-name and wrong-level queries are logged as negative controls rather than presented as coverage.

## Self-test controls

The sealed self-test passed with `inputPreserved: true`, 2 positive checks and 11 negative controls. The positives were the unchanged sealed packet and acceptance of `organic[]` with its declared nested removals. All 11 negative controls rejected: wrong source head; resealed `success:false`; wrong node provenance; invented path-marker key; invented summary wrapper; wrong lineage optionality; Date-to-string mutation; required `files[].file_id`; the cross-exclusion `resultClaim` survivor; an exact excluded path; and a falsely fully preserved `organic[]` container. The actual rejection reasons are retained in the self-test output and the driver logic; no control result is inferred from a hash alone.

## CDC decision inputs and open policy

| Open policy | Affected paths | Evidence | Consequence / next check |
|---|---|---|---|
| Codec and field-state policy | content, files, attachments, metadata, contextMeta | source declarations and 117-field matrix distinguish optional, nullability, defaults and shallow wrappers | CDC must choose absent/undefined/null/empty/populated handling and test it against the real adapter boundary |
| Open/Mixed and BSON preservation | message metadata, provider tool/search branches, examples | `z.record(z.unknown())`, named external boundaries and provider types; no corpus access | characterize representative values in an isolated authorized fixture before narrowing or stringifying |
| Projection composition | metadata, backgroundTask, organic/topStories, web/file search | exact `CLIENT_MESSAGE_SELECT` literals plus composed exclusion controls | CDC must freeze public DTO/projection policy and retain siblings while removing only named leaves |
| Implementation fence and runtime | all ten roots | storage doubles, Node 22, pinned source head; no build or application suite | resolve D07/source-build and precise file fence before Slice03 assignment |

## S01–S07 contribution

| Row | This packet contributes | Remaining open work |
|---|---|---|
| S01 | source-grounded ordinary read replay and projection evidence | complete portable contract and integrated conformance |
| S02 | exact declaration graph, 117-field coverage and ten-root nested map | CDC review and DTO/codec decisions |
| S03 | optional/null/default/branch/Partial distinctions and open boundaries | patch/failure/unknown-value policy and tests |
| S04 | none beyond preserved prior evidence | cursor characterization owner remains separate |
| S05 | preserves source/projection fingerprints and explicit provenance limits | original-source/corpus fidelity remains separate |
| S06 | no implementation or build claim; preserves Node22-vs-Node24 limitation | implementation-ready fence, source build and integrated adapter checks |
| S07 | seven-file packet, raw failed attempts, manifest and explicit-path commit | CDC/Operator review and acceptance |

Recommendation: keep Slice02 open for CDC's DTO/composition decision and D07 review. Do not open Slice03 from this packet alone. The evidence supports a focused implementation prompt later, but it does not choose a decoder, flatten unions, narrow Mixed values, or close the arc.
