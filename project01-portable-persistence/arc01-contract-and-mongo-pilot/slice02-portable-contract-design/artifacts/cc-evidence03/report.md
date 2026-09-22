# CC evidence03 report

## Status

Iteration02 evidence is authored and will be sealed only after the replay driver, structural map, raw command records, hashes, and final verify pass are complete. This is a CC proposed-done report, not CDC verification or Operator acceptance.

## R1 — submitted-evidence verification

The driver keeps explicit `--capture`, `--verify`, `--self-test`, and `--packet` modes. Capture refuses an existing `SHA256SUMS`; verify requires the exact sealed packet inventory and never writes to it. Verification preflights the submitted inventory/environment, loads the submitted replay result, compares every behavior/provenance key to the pinned pass05 result with absent/null distinction, runs pass05 into a temporary directory, then compares fresh output to both submitted and pinned results. No differences are allowed and checksums are used only for byte preservation.

The final run records the following separately: valid verification, wrong runtime/head/compiler/source-fingerprint controls through the same verification entry, submitted behavior mutation, submitted provenance mutation, submitted absent/null cases, positive unchanged preservation, negative runner mutation, sealed-destination capture refusal, and sealed-safe self-test. The failing-path runner sentinel must remain at 0 calls; the valid-path sentinel must be exactly 1 call. Positive unchanged preservation is not counted as a rejection.

## R2 — nested contract map

The inventory retains 117 unique coverage rows, 10 roots, and 12 exclusions. Every root has named members, array boundaries, storage/server/provider domains, declared types, declaration contexts, requiredness/default/null evidence, open boundaries, source references, witnesses, and the four operation mappings. The map expands `Agents.ToolCall` including background-task and approval leaves, complete `TFile` and metadata/code-environment members, all attachment variants including numeric expiry and `Partial<TFile>` contexts, independent web/file-search branches, processed web result fields, contextMeta fading tiers, the closed local feedback tag versus minimal stored tag, examples input/output, path markers, workspace selections, and all lineage members.

The exclusion validator canonicalizes array notation and rejects any permitted sibling that is the excluded path or a descendant/ancestor covered by it. Web exclusions are scoped to `web_search`; `file_search` survivors are separately represented. `contextMeta` has an established server disposition but a distinct public exclusion disposition. `subagentThread` public use is recorded as lineage admission, not as a public message-member claim. `completionWakeup`, historical BSON/Mixed values, and DTO/codec/semantic policy remain explicit CDC-owned unresolved decisions.

## R3 — complete matrix and query controls

The corrected queries use `messageSchema` and `convoSchema`, retain complete field projections, assert exact 44/73 field counts and unique identities, and query ancillary data per record with `sourceHead`, `exclusions`, and each record’s provider-only/interface-only/implicit members. Required counts are 10/13 provider-only, 4/3 interface-only, and four implicit keys for each record. The old `conversationSchema` query and old top-level ancillary query are retained as negative historical controls, alongside the evidence02 log search. Each command record includes argv, cwd, exit, stdout, and stderr before dependent validation.

## Evidence limits and disposition

The pass05 harness exercises storage doubles and the available runtime is Node v22.22.3 versus the repository pin v24.16.0. This packet is not a production build, full-suite result, live Mongo result, codec/DTO decision, or semantic acceptance. Source and planning checkouts remain outside the authorized mutation scope. The assigned reviewer is CDC under the Two-Contributor Workflow; the Operator retains acceptance and slice-closure authority.

## Final measured results

The capture completed with exit 0. Structural results were 117 coverage rows, 117 unique keys, 10 selected roots, 12 nested exclusions, and 13 source fingerprints. Root member counts were content 83, files 57, attachments 80, metadata 10, feedback 7, contextMeta 12, userSubmittedMessageFieldPaths 5, examples 9, codeWorkspaces 3, and subagentThread 8. The pass05 replay and validator both exited 0; fresh capture versus the pinned result had `allowedDifferences: []`.

The sealed self-test completed with exit 0. It recorded 15 negative controls and 15 rejections, with two positive checks kept separate. The four actual verification-path preflight controls called their injected runners 0 times in total; the valid-path sentinel called its runner exactly once. Submitted `success:false`, wrong submitted `node`, absent submitted `success`, and null submitted `success` were each rejected through the verification entry. The final packet guard rejected a runner that mutated `report.md` after initial hashes. The positive unchanged packet was accepted with `rejected:false` and `packetUnchanged:true`. The sealed packet hash and log remained unchanged during self-test.

The final read-only verify completed with exit 0. Submitted replay versus pinned, fresh replay versus submitted, and fresh replay versus pinned each reported `allowedDifferences: []`; the pass05 harness exited 0; `packetUnchanged` was true. The preflight observed source head `3e3c5410d3863118fdba694fb0cd51baeb7102f9`, Node `v22.22.3`, and TypeScript compiler `5.9.3` with the pinned compiler digest.

The corrected R3 query returned `messageSchema` with 44 fields and `convoSchema` with 73 unique fields. Ancillary arrays returned 10/13 provider-only and 4/3 interface-only members for message/conversation respectively, with `createdAt`, `updatedAt`, `_id`, and `__v` implicit for each record. The old `conversationSchema` query returned `[]` at exit 0, and the old top-level ancillary query returned null members; both remain labeled negative historical controls. The execution log also preserves evidence02 searches for those earlier failures and the old self-test/sentinel behavior.

Applicability was recorded as: message roots are server-history message-view members and not conversation-result members; examples, codeWorkspaces, and subagentThread are not message-result members and are conversation-view members; public disposition for message roots is survivor except metadata/contextMeta exclusions; subagentThread public disposition is lineage admission; accessProbe is not selected for these roots except subagentThread’s full-lineage object selection. These are source-grounded dispositions in the inventory, not production DTO or semantic acceptance decisions.

Authoring recovery was bounded and preserved in the working execution history: one stale fading declaration line bound and one empty wrong-record jq projection were corrected before the successful capture; the self-test misassignment control was corrected to use a valid but wrong classification. No source, plan, ledger, prior packet, dependency, live database, or infrastructure file was changed.

The final sealed packet manifest is the byte-level identity record for the six payload files; it is not independent acceptance. CDC must inspect the packet and reproduce the controls before any ledger row can close.
