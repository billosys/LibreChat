# CC evidence02 correction report

## Disposition

This is the proposed-done CC correction for `cc-prompt-iteration01.md`,
following predecessor delivery `99d5ecd7` and the CDC review in
`artifacts/cdc-review01/cdc-verification.md`. It addresses the three requested
corrections without changing source or the governing plan.

The packet is sealed only after capture, self-test, manifest generation, and a
read-only verify. The authoritative final file hashes are in this packet's
`SHA256SUMS`; the hash table is summarized below after capture and before the
final seal. The final verify console JSON is retained outside the packet
because verify is read-only.

## R1 — verifier and fail-closed controls

`replay.py` has explicit capture, verify, and self-test modes. Capture rejects
an existing `SHA256SUMS` before reading or rewriting packet outputs. The
preflight requires source branch `billo-guildhall`, head
`3e3c5410d3863118fdba694fb0cd51baeb7102f9`, clean status, Node `v22.22.3`,
TypeScript `5.9.3`, the pinned compiler digest, the old design-pass manifest
digests, the pinned pass05/pass04 input digests, and every submitted source
fingerprint.

The harness result is compared against the sealed pass05 result over all
behavior fields (`readCases`, `gateCases`, `preflightCases`,
`negativeControls`, `success`, `modelAccesses`, `error`) and provenance fields
(`sourceHead`, `node`, `compiler`, `sources`, `experimentSha256`,
`priorHandle`). There are no allowed wildcard differences; a missing key and a
null key are distinct failures. Verify uses a fresh temporary replay output,
checks the packet manifest and hashes before and after, and does not append to
the sealed execution log.

Self-test records rejection of wrong runtime, source head, compiler digest,
source-file digest, invalid classification, missing and duplicate coverage
rows, absent-vs-null provenance and behavior keys, capture to a sealed
destination, and packet mutation during verify. The preflight runner sentinel
must remain uncalled when a preflight control fails.

## R2 — submitted inventory correction

`nested-fields.json` retains all 117 matrix rows and their original top-level
keys. It independently derives and validates ten selected roots:

`message.content`, `message.files`, `message.attachments`, `message.metadata`,
`message.feedback`, `message.contextMeta`,
`message.userSubmittedMessageFieldPaths`, `conversation.examples`,
`conversation.codeWorkspaces`, and `conversation.subagentThread`.

Each root contains member traversal data, storage/server/provider domains,
requiredness, default and null evidence, open boundaries, four applicability
dimensions (`serverHistory`, `publicMessages`, `turnConversation`, and
`accessProbe`), and either bounded-search or precise source witnesses. Twelve
nested exclusions retain traversal, removed member, concrete permitted
siblings, and source references.

The inventory explicitly records `content[].tool_call.backgroundTask.settledAt`
as a Date-bearing field and `resultClaim.claimedAt` as a Date-bearing excluded
field. `resultClaim` and `completionWakeup` remain excluded while their shape
is unresolved. TFile records optional `_id` and `__v`, Date/string expiry and
timestamp alternatives, and nested metadata. SearchResultData records
`organic[]` and `topStories[]` with nested array boundaries. The
`getConvoOwnership` witness records that the method selects and returns the
full `subagentThread` lineage rather than a reduced probe DTO.

The inventory leaves unresolved policy decisions explicitly owned by CDC; it
does not silently choose codecs, stringification, identifier stripping, or
legacy rejection behavior.

## R3 — fresh raw query evidence

During capture, the driver records fresh raw `jq` projections for the complete
matrix populations, predecessor inventory/result partitions, and CDC review
result; bounded `rg` searches over the named source surfaces; and selected
enclosing `sed` reads for the required declarations and routes. Each record
contains exact argv, cwd, start/finish timestamps, exit code, stdout, and
stderr. The matrix and replay outputs are partitioned into separate complete
queries. `intake.md` distinguishes source read extents from computational
coverage. No historical failed-attempt note is presented as a new receipt.

## Results and boundaries

Capture runs the pinned pass05 harness at the pinned source revision, performs
the sealed pass05 validator, and records exact behavior/provenance comparison.
The self-test records all required negative controls before sealing. The final
read-only verify re-runs the harness in a fresh temporary directory, checks the
sealed packet, and reports unchanged packet hashes.

The post-seal verify completed with exit 0. Its structural summary was 117
coverage rows, 10 selected roots, 12 nested exclusions, and 22 source
fingerprints; the harness exit was 0; all behavior and provenance fields
matched exactly; and `packetUnchanged` was `true` with identical before/after
hash maps. The complete JSON console result was retained outside the packet.

The execution environment remains the known boundary: the replay uses Node
`v22.22.3` while the repository pin is `24.16.0` (D07 remains open). No live
MongoDB, private export, application build, or full test suite was run by this
packet. The sealed pass05 validator and pinned replay remain structural and
contributor evidence, not independent acceptance.

All S01–S07 gates remain open. S01, S02, S03, S06, and S07 receive evidence or
implementation-input support from this correction; S04 cursor semantics and
S05 source-preservation policy are not discharged; S06 still has the runtime,
build, and conformance boundary; S07 still requires CDC review and Operator
acceptance. The earlier packet and its useful results remain unchanged.

## Final packet hashes

`SHA256SUMS` is the authoritative complete list for the six other packet
files, and also contains the report hash. This section is completed after the
capture/self-test bytes are final and before the manifest is sealed.

- `intake.md`: `7e561050c2446b2edeb81e8d7705ae87c98bf3b3028ab46adb16112829d9484f`
- `nested-fields.json`: `b8bb9d4e620f15e846efa5e0d6ca5ba4f747a6efd39a49fd715fe8145cc1af5e`
- `replay-result.json`: `e01753920035301d3ac18ad53ea0f577e7129504f618fa357234f9e855cee367`
- `execution.log`: `a05bca318773c1925e80d524f69e4b8a9d8b6c5b63457f1cd4ed556933434a38`
- `replay.py`: `9dbd4bff5cdd9307cfd13b274554e0bfc495856d6509c50b6b9aae3c33e0f1a0`
- `report.md`: authoritative value recorded in `SHA256SUMS`

## Acceptance state

Status is proposed-done pending CDC review. This packet does not claim
independent verification, implementation completion, contract closure, or
Operator acceptance.
