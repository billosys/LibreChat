# Claude → LibreChat/Mongo reconciliation

Date: 2026-09-20 (America/Chicago); final database comparison at 2026-09-21 02:24:19–02:24:20 UTC. Workflow: one-contributor investigation, self-checked. The Operator explicitly authorized this read-only reconciliation.

## Result

**Mongo matches the current Claude importer's expected stored representation across the entire identified corpus. It does not preserve the complete original Claude data.**

| Measure | Source / expected | Observed in Mongo | Result |
|---|---:|---:|---|
| Conversations | 820 | 820 | All uniquely paired |
| Source messages | 9,838 | 9,731 | 107 explained skips |
| Messages retained by importer rules | 9,731 | 9,731 | All compared |
| Retained messages matching checked fields | 9,731 | 9,731 | No unexplained mismatch |
| Unpaired stored conversations | 0 | 0 | No extra candidate conversations |
| Uncompared stored messages | 0 | 0 | No extra candidate messages |
| Orphan messages | 0 | 0 | Every message refers to a stored conversation |

Every source message is accounted for: **9,731 retained + 107 skipped = 9,838**. “Accounted for” includes known omissions; it does not mean every source record or field was preserved.

The 107 skipped messages yielded neither text nor thinking under the current extraction rules. Of these, 96 had text blocks yielding no text and 11 had no content blocks. **66 skipped messages had file or attachment metadata**: 38 had attachments and 66 had files, with overlapping membership. Describing all skipped messages as empty would be misleading.

## What matched

Conversations matched uniquely by title plus millisecond creation time. All 820 source keys and stored candidates were unambiguous. This was a content comparison used for reconciliation, not recovery of a persisted source-ID mapping.

For all 9,731 retained messages, checks covered extracted text, extracted/concatenated thinking content and resulting content structure, importer-transformed creation timestamp, speaker label, user/assistant flag, submitted-content flag, endpoint, owner/tenant scope, parent link in the imported sequence, unfinished/error flags, and absence of the undeclared `isEdited` field. All matched. Creation time required no monotonicity bump or missing-date fallback in this corpus; three messages used the legacy text fallback.

All stored records had the Anthropic endpoint and one consistent owner/tenant scope. Actual account and tenant identifiers were kept out of the report. The database name was `LibreChat`. The observed conversation model label was uniformly `claude-fable-5-1`; the export supplies no message or conversation model field. This is an import-assigned label, not evidence of which historical model generated each answer.

The conversation documents' embedded `messages` arrays were empty in all 820 records, while all 9,731 message documents had valid conversation references. The current bulk importer does not populate those embedded arrays. This is an observed representation detail, not a missing-message count or a demonstrated UI defect.

## Original-source fidelity differences

| Source data | Observed conversion / omission |
|---|---|
| 8,609 tool-use blocks | Not represented as tool-use blocks in stored messages |
| 8,532 tool-result blocks | Not represented as tool-result blocks in stored messages |
| 2,388 token-budget blocks | Not represented in stored message content |
| Attachments on 287 source messages; files on 583 | No stored message has attachment or file metadata; counts overlap |
| 329 thinking blocks | Concatenated into thinking content on 140 assistant messages; strings match, original block boundaries are not retained |
| Source parent graph | 95 retained parent relationships across 55 conversations differ from the imported linear chains, even after contracting skipped ancestors |
| Source branching | 52 branch points occur in 47 conversations; linearization also affects other multi-root/sequence cases |
| 446 nonempty conversation summaries | No summary field in stored conversation documents |
| Original conversation and message UUIDs | Replaced by new LibreChat IDs; no stored logical ID equals an original source ID in its entity population |
| Original update times | Conversation `updatedAt` reset to creation time (819 source conversations had distinct update times); message `updated_at` not preserved, including 161 retained messages with distinct update times |
| Submillisecond creation-time precision | Lost for 9,719 retained messages at the millisecond storage boundary |

These are findings about structured representation. The comparison does not claim that every omitted tool string is absent from all ordinary text: textual duplication can exist. File metadata counts do not prove that the archive contains corresponding file bytes. Recoverability and availability of those bytes were not investigated.

## Method and evidence

The original JSON fingerprint was asserted before the database read and checked again afterward: `558271556db71c662d0a8708769cf5d0acd113cf83b49ce9e8b4d985a6392fed`. Application source remained `ba44443fdb232bbe6d4977e2619774b5a72586ac`.

The comparison script independently constructed the importer's expected text/thinking and timestamp representation from the pinned source JSON, without calling application imports, model registration, or application write methods. It read the local connection URI without printing credentials and refused a nonlocal URI. Raw conversation bodies were compared in memory, not copied into planning evidence.

The database had only the one endpoint/scope population; no guess was needed about selecting between multiple users or batches. Pairing used title and creation time, then every stored message was checked in timestamp order. Counts, pairing uniqueness, record coverage, ownership, and parent links were checked in addition to content equality.

Both collections were read twice in each comparison. Their full-document digests matched between reads, and the same digests held across the two comparison attempts. This detects observed changes across reads; it is not a transactional point-in-time snapshot and cannot rule out changes that reverted between reads. Observed data commands were `find` and `getMore`; the probe used read-only `aggregate`. There were no application-data write commands, service restarts, or configuration changes.

The final comparator had a passing positive control and 12 deliberately altered field cases that each triggered the relevant mismatch. A separate Python source analysis independently reproduced the skip predicate, inspected parent topology, contracted skipped ancestors, and independently confirmed the submillisecond precision count.

Evidence is under [research-inventory/claude-reconciliation-20260920/](research-inventory/claude-reconciliation-20260920/): executable scripts, both comparison summaries, the final zero-mismatch result, skipped source-array locators, hashed conversation pairings, topology counts/locators, and compressed first-attempt mismatch diagnostics. Source-array locators are zero-based; no titles, message text, credentials, or raw account identifiers are committed. `SHA256SUMS` fingerprints the retained evidence files.

## Attempts and interpretation corrections

1. The initial sandboxed Mongo probe failed with `MongoServerSelectionError`. The authorized elevated read-only probe succeeded and found 820 conversations and 9,731 messages. This was an access/runtime attempt, not a failed import.
2. Comparison attempt 01 reported 9,731 mismatches, all for `isEdited`. The builder sets `isEdited: false`, but the message schema does not declare it and no stored document contains it. The first oracle incorrectly treated a builder-only field as persisted data. Its output and script are retained; it is not hidden as a green result. Its exit code indicated script completion, not comparison success; the JSON outcome was `requires_investigation`.
3. Comparison attempt 02 corrected only that stored-field expectation and added a positive comparator control. All 9,731 messages then passed every checked field, with 12 negative controls passing. Counts and collection digests were unchanged.
4. Exploratory source-topology analysis initially treated Claude's common external-root marker (`00000000-0000-4000-8000-000000000000`) as an unresolved parent. The refined analysis explicitly normalizes that observed marker. The initial figures are retained as superseded diagnostics; the final topology result is **95 changed retained relationships in 55 conversations**, with no unresolved parents after normalization. This is a documented source-format interpretation, not a change to Mongo records.

## Consequence for Arc01

We have a usable baseline of current LibreChat import behavior, with no unexplained missing conversation or retained-message record in this run. Database migration can test preservation of that representation.

Guildhall's richer data requirements need a second obligation: preserve the original source alongside its operational view, with stable source identities, original graph relationships, content blocks, and metadata. SQLite migration alone cannot reconstruct fields omitted before they reached Mongo. Keep the existing browsable import unchanged while designing that source-preserving intake and mapping. A fresh overlapping Claude export also requires explicit deduplication; current fresh-ID imports are not idempotent.

This result does not accept the future SQLite migration, validate every LibreChat feature, prove attachment-byte recovery, or independently verify this contributor's work. Project ledger rows remain open. No corrective import was attempted.
