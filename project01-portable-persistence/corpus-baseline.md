# Initial Claude corpus baseline

Initial record from 2026-09-20; the later [read-only reconciliation](corpus-reconciliation.md) supersedes the pending database checks below. Workflow: one-contributor investigation. Application source remains `ba44443fdb232bbe6d4977e2619774b5a72586ac`, with a clean tracked source checkout at inspection.

## Operator-reported runtime result

The Operator installed and started local MongoDB, ran `npm run reinstall` and `npm run backend`, and imported the extracted Claude JSON through LibreChat. The Operator reports that the import completed quickly and the conversations are viewable at `http://localhost:3080`.

This settles the route: **Claude export → existing LibreChat/Mongo → future SQLite migration → subsequent OpenAI/GPT import**. The successful UI observation is Operator-reported; this investigation has not queried Mongo for imported counts or independently checked the browser. Full import fidelity and the SQLite ledger criteria remain open.

## Source files inspected read-only

- Archive: `/Users/oubiwann/lab/oxur/ixy/workbench/ClaudeDesktopPersonalExport-data-e4d62c87-4fae-414c-94ec-bdd0521b2fd7-1782858190-7d5852f4-batch-0000.zip`
- Extracted input: `/Users/oubiwann/lab/oxur/ixy/workbench/conversations.json`

SHA-256 comparison confirmed that the extracted file exactly matches the archive's sole member named `conversations.json`. No conversation bodies, titles, or private source files were copied into this planning tree.

| Source observation | Value |
|---|---:|
| Archive bytes | 42,105,917 |
| Extracted JSON bytes | 187,982,762 |
| Conversation objects | 820 |
| Message objects | 9,838 |
| Text blocks | 14,416 |
| Tool-use blocks | 8,609 |
| Tool-result blocks | 8,532 |
| Token-budget blocks | 2,388 |
| Thinking blocks | 329 |
| Messages with nonempty attachments | 287 |
| Messages with nonempty files | 583 |

Block counts are not message counts; a message can contain multiple blocks and can have both attachment and file metadata. Nonempty file metadata does not establish that corresponding file bytes are present. Counts cover the actual source JSON, not the imported database.

Source message `created_at` strings range from `2025-08-18T00:33:27.855256Z` to `2026-06-26T05:50:28.204438Z`. These bounds were taken over present string values; they do not prove that this export includes the Operator's final Claude activity. The Operator may obtain a newer export; treat that as another identified source version and design deduplication before importing overlapping history.

Archive SHA-256: `5831743d11f52f9df398cf0d1bcdbbcb4fa616a85211104aed80f07929b917c4`.

Extracted JSON SHA-256: `558271556db71c662d0a8708769cf5d0acd113cf83b49ce9e8b4d985a6392fed`.

Method: stream SHA-256 over both local files and the ZIP member; parse the top-level JSON list; count dictionary messages in each `chat_messages` list; count `content[].type` values, nonempty `attachments`/`files`, and the lexical min/max of string `created_at` values. No database mutation or credential inspection was performed.

## Fidelity finding and next reconciliation

The source mapping in `api/server/utils/import/importers.js:173` and `:202` collects text/thinking, assigns fresh message IDs, creates a linear parent chain, adjusts non-increasing timestamps, and skips messages with no extracted text/thinking. It does not copy tool-use/result/token-budget blocks or attachment/file metadata into the constructed message. This finding is grounded in the mapping code and confirmed source content kinds; actual stored-row reconciliation is still pending.

Keep both the original export and the browsable operational import. Moving the current Mongo rows to SQLite would preserve only what the importer represented; it cannot recover fields that never entered those rows. Arc01 must define source preservation and source-to-LibreChat identity mapping before treating this imported corpus as a complete cognitive record. Re-importing unchanged history with the current fresh-ID behavior is not a deduplication strategy.

Next reconciliation: identify the imported batch and owner read-only; account for conversations and retained/skipped messages; inspect representative structured-content and attachment cases; document transformations separately from losses. A database snapshot/recovery baseline belongs before any corrective import or migration, not before this read-only source inventory.

## Startup log interpretation

The supplied log shows a Mongo connection, HTTP listener, and passing server readiness. Its remaining conditions are separate:

- `librechat.yaml` is absent (`ENOENT`), despite the generic “YAML format is invalid” label. The checked-in example declares version `1.3.16`; configure from the current example when selecting local settings.
- Scheduling refuses writes because the process has not asserted a safe topology. For this single-backend local setup, `SCHEDULES_SINGLE_PROCESS=true` is the documented source switch; restart after changing it. A multi-replica setup instead needs shared stream storage. The source intentionally leaves scheduling unavailable until restart.
- Missing RAG configuration affects the corresponding file/RAG facilities; no such service was provisioned in this investigation.
- Missing `METRICS_SECRET` leaves the metrics endpoint returning 401, as logged.
- Temporary credentials are stored in `.env.temp`. Preserve the current values when configuring permanent credentials; no secret values were read, printed, or modified.

No running service was restarted and no local configuration was changed. These log observations do not constitute backend conformance or performance tests.
