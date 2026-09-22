# CC iteration03 intake

## Assignment and state

I acknowledge the Operator-relayed third correction as CC in the Project01 / Arc01 / Slice02 Two-Contributor Workflow. This is a separate CC execution context; no exposed session identifier is available, so no identifier is invented. CDC remains the assigned reviewer and owns DTO/codec/patch policy, projection composition, injection, D07 and sizing. No CRC is enabled.

The active prompt is `cc-prompt-iteration03.md`, introduced by planning commit `d31a81ab341225303f0861a3c85396ca5a9ddacf`; its SHA-256 is `9f1aafceeedab3d1070945faf366a91237d41a9e130c584284335aeafd732848`. The current slice plan names this prompt as the third R2 correction and keeps R1/R3 reproduced, all seven acceptance rows open, and Slice03 unopened (`slice-plan.md:1-18,112-116`). The pinned source is `3e3c5410d3863118fdba694fb0cd51baeb7102f9` on `billo-guildhall`; source status was clean at capture. Planning was on branch `planning`; this packet is the only new planning output.

## Required reading record

Complete bounded reads were loaded before capture. The following are the actual file extents; line counts are recorded to make the intake reproducible, not as a substitute for reading:

- Governing planning files: `AGENTS.md` (1–25), `BILLO.md` (1–52), `README.md` (1–22); source `AGENTS.md` (1–116), `BILLO.md` (1–52), `CLAUDE.md` (1–376).
- Current planning sections: `project01-portable-persistence/project-plan.md` (1–177; Goal/boundaries, Definition of done, Workflow/authority and complete transition/Expedited sections); `arc01-contract-and-mongo-pilot/arc-plan.md` (1–102; Scope, Slice roadmap, Workflow/source boundaries); `slice-plan.md` (1–132), `ledger.md` (1–13), and `cdc-verification.md` (1–143).
- Assignment history: initial `cc-prompt.md` (1–124), iteration02 `cc-prompt-iteration02.md` (1–83), and this prompt (1–80). The required methodology/prompt-authoring, project-management, work-verification, engineering-methods, scientific-methods and testing guides were read from their installed skill roots; their constraints are applied here as evidence capture, not as production authorization.
- Prior evidence and sealed harness: `cc-evidence03/intake.md` (1–40), `report.md` (1–41), and `replay.py` (1–623); pass05 `read-contract.md` (1–84), `protocol.md` (1–11), `experiment.cjs` (1–75), `field-matrix.cjs` (1–24), `validate.py` (1–48); pass04 `handle.cjs` (1–58).
- CDC review03: `declarations.cjs` (1–40), `review.py` (1–92), `result.json` (1–2280), and `execution.log` (1–324). Its result hash is `de65a055a5c9d32d503ee67a6285e0fef8706b2e954c2722c79f7261dd80a0ca`.

The prior packet remains byte-for-byte untouched. Its manifest hash is `75b5e048152d12a488e08939a9a1405f9891722abd4642b6a8a81b61e826dc7e`. The pass05 result and matrix hashes used as read-only inputs are `e01753920035301d3ac18ad53ea0f577e7129504f618fa357234f9e855cee367` and `c1e32f81a7a105dc32e2f036ffeb08688c5c362e57e5b038d4ea3cd4e6806ab1`.

## Source-cited contract readback

The slice is still evidence-only. The current plan keeps the ordinary save/update/read contract, source preservation, explicit failure/patch distinctions and named projections in design, while withholding implementation and acceptance. Expedited Mode changes commit/report cadence only; it does not weaken source, runtime, reviewer or Operator gates (`slice-plan.md:29-43`; `arc-plan.md:35-61`).

The extractor in `replay.py` uses the pinned Node executable and TypeScript 5.9.3 compiler only to parse source syntax. It does not evaluate modules, query Mongo, inspect a private export, infer BSON/Mixed values, or turn a provider type into a decoder. Declaration records retain exact declaration/member text, source line, type or initializer expression, optionality, branch label and source digest. Branch labels are separate from literal data paths.

The resulting map distinguishes:

- literal paths from discriminated branches: error members are `content[].text`, `content[].error`, and `content[].initiatedBy`; summary members are element-level `content[].content[]`, `content[].tokenCount`, and `content[].boundary.*`; no `.error.*`, `.summary.*`, or `.variant*` data paths are used;
- optional ancestors from required leaves: `subagentThread?` and `contextMeta?` are separate from their local leaves, while `parentAgentId` is optional and the other seven lineage members are required;
- a shallow use-site wrapper from declaration requiredness: `TMessage.files?: Partial<TFile>[]` makes outer file properties optional at that use site but leaves `TFile.file_id`, `bytes`, `embedded`, `filename`, `filepath`, `object`, `type`, and `usage` locally required;
- message metadata from embedded-file metadata: message `metadata` is `z.record(z.unknown()).optional()` and therefore has no transferred `TFile.metadata.runFile` or `codeEnvRef` members; those remain under `files[].metadata.*` where `TFile` declares them.

The public projection is source-derived from `CLIENT_MESSAGE_SELECT` (`packages/data-schemas/src/methods/message.ts:456-481`): `metadata` is included with nested `metadata.thoughtSignatures` removed; `backgroundTask.status` and `settledAt` survive while `resultClaim` and `completionWakeup` do not; `organic[]` and `topStories[]` survive with their declared nested removals. The map keeps `web_search` and `file_search` separate. `getConvoOwnership` (`packages/data-schemas/src/methods/conversation.ts:2060-2078`) selects the full `user tenantId subagentThread` lineage object, so `subagentThread.accessProbe` is established; public admission use is a separate view.

## Capture result

The raw command/event log is `execution.log`. It preserves three failed authoring attempts (missing workspace declaration request, an overstrict example assertion, and the corrected rerun) before the successful capture. The successful capture recorded clean source, Node `v22.22.3`, compiler `5.9.3` with the pinned digest, fresh matrix queries and the pass05 harness.

Fresh data recorded by the packet:

- 117 unique coverage rows, ten selected roots, twelve nested exclusions, eleven source-file fingerprints, three explicit unresolved policy questions;
- 46 requested local declarations, 226 source-derived member rows, exact closed-set/type/reference comparison against a fresh extraction;
- pass05 replay: 16 read cases, 2 admission gates, 3 preflight cases, 3 detected negative controls; submitted/baseline/fresh results matched exactly;
- corrected matrix: `messageSchema` 44 fields / 10 provider-only / 4 interface-only; `convoSchema` 73 / 13 / 3; each retains the four per-record implicit keys. The wrong record-name and wrong-level ancillary queries are retained as failed controls (statuses 4 and 1).

This intake records proposed-done evidence for CDC review only. It is not independent acceptance, integrated conformance, BSON/Mixed characterization, Node 24/D07 validation, or slice closure.
