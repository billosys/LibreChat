# Slice01 test baseline

Source: `ba44443fdb232bbe6d4977e2619774b5a72586ac`. Investigation performed 2026-09-20 America/Chicago (2026-09-21 UTC). Evidence is **attested/self-checked**, not independently reproduced acceptance.

## Result and accounting

Four attempts completed successfully: **12 suites, 641 tests passed; 0 failed, 0 skipped/pending, 0 todo, 0 runtime-error suites**. No test attempt was discarded or retried. These are existing tests, not tests of a newly implemented interface.

| Attempt | Workspace | Suites | Passed / total | Exit | Evidence |
|---|---|---:|---:|---:|---|
| 01-data-schemas | packages/data-schemas | 5 | 370 / 370 | 0 | [attempt](runs/01-data-schemas/attempt.json), [log](runs/01-data-schemas/output.log), [Jest JSON](runs/01-data-schemas/jest.json) |
| 02-save-orchestration | packages/api | 1 | 9 / 9 | 0 | [attempt](runs/02-save-orchestration/attempt.json), [log](runs/02-save-orchestration/output.log), [Jest JSON](runs/02-save-orchestration/jest.json) |
| 03-import | api | 3 | 69 / 69 | 0 | [attempt](runs/03-import/attempt.json), [log](runs/03-import/output.log), [Jest JSON](runs/03-import/jest.json) |
| 04-client-read | api | 3 | 193 / 193 | 0 | [attempt](runs/04-client-read/attempt.json), [log](runs/04-client-read/output.log), [Jest JSON](runs/04-client-read/jest.json) |

Per-suite denominators and every assertion's exact name/status are in [assertions.tsv](assertions.tsv). The suites comprise conversation methods (203), message methods (139), traces (10), conversation structure (5), tenant conformance (13), save orchestration (9), importers (55), import timestamps (12), database import (2), BaseClient (155), message routes (34), and routes with real validation middleware (4).

**Seven database-backed suites contain 381 assertions; five mocked-storage suites contain 260.** Database-backed does not mean every assertion exercises a database: seed failure/order tests use doubles, and conversation methods inject mocked message methods. Conversely, the BaseClient and route suites exercise application orchestration but mock storage. No claim of one end-to-end browser → Mongo test follows from combining their counts.

## Runtime and reproducibility

Executed with `/Users/oubiwann/.local/bin/node`, **v22.22.3**, installed workspace dependencies, and cached **MongoDB 8.2.1** at `node_modules/.cache/mongodb-memory-server/mongod-arm64-darwin-8.2.1`. The repository's `.nvmrc` pins **24.16.0**. This is a passing installed-environment baseline, not validation on the pinned release runtime. The available Homebrew Node was 26.9.0 and was not used. No runtime or dependency was installed or upgraded.

Each `attempt.json` retains the exact argv, cwd, explicit nonsecret environment overrides, start/end UTC, source commit, Node version, and exit code. Each attempt invoked the installed Jest executable with `--runInBand --watch=false --coverage=false --runTestsByPath`, explicit files, JSON output, and a `/tmp` cache. Existing package `npm test` scripts enable watch/coverage; they were deliberately not used. No coverage percentage is claimed.

[run-baseline.py](run-baseline.py) preserves the runner; [mongo-guard.cjs](mongo-guard.cjs) preserves the CJS-suite guard. To reproduce, use the recorded argv/environment/cwd, substituting a **fresh output/cache directory** for the captured `/tmp/guildhall-slice01-20260920` paths and the retained guard's absolute location where required. The runner's original `/tmp` paths are intentionally retained as execution provenance; it refuses to overwrite an existing attempt directory. Do not rerun it against an occupied output directory. Install neither dependencies nor a different runtime implicitly; record any reproduction environment differences.

The `packages/api` orchestration tests import the **built** `@librechat/data-schemas` package; CJS consumers import built `@librechat/api` and data-provider too. The data-schemas method suites exercise their source modules. We did not rebuild these artifacts or prove that installed dist bytes correspond exactly to this source commit. [source-fingerprints.json](source-fingerprints.json) and [dist-fingerprints.json](dist-fingerprints.json) identify the inspected/tested inputs. This distinction must survive review; the future implementation must build affected packages and test the resulting exact revision.

## Isolation preflight

- Inspected each selected suite's setup/teardown and workspace Jest setup before execution. `message.spec.ts` creates MongoMemoryServer at 74–102; `conversation.spec.ts` at 49–83 (its error test reconnects to that same server at 3541); `convoStructure.spec.ts` at 21–43; `message.traces.spec.ts` at 33–47; tenant conformance's harness at 27–45; and `save.spec.ts` at 42–63. Every connection derives from its newly created server's URI. Cleanup targets that connection, followed by disconnect/stop.
- `importConversations.database.spec.js:31–57` creates a fresh server, drops only that server's database between cases, and removes its own temporary fixture files. Its two tests use repository fixtures/synthetic data, not the Operator's Claude export. The two importer unit suites mock `~/models` and do not connect.
- The client and message-route suites mock model methods; BaseClient also mocks `~/db/connect`. Supertest opens transient local HTTP listeners. There is no running LibreChat endpoint in their requests.
- CJS `api/test/jestSetup.js` overwrites `MONGO_URI` with `mongodb://127.0.0.1:27017/dummy-uri`. Therefore the runner's sentinel URI is **not** itself a sufficient CJS safeguard. For attempts 03/04, the additional setup wraps Mongoose connection `openUri`: only loopback, explicitly supplied non-default ports above 1023 are allowed. It rejects 27017 in a negative control without connecting. Attempt 03 logged the actual permitted port **56249**. The guard supplements the inspected fresh-server lifecycle; an arbitrary high port alone is not proof of disposability. It does not intercept every possible native Mongo driver call.
- `api/models/index.js` constructs methods, not a connection. The adjacent Keyv Mongo cache uses the existing Mongoose connection rather than opening the default URL. CJS runs explicitly disable Redis/Redis streams and Meili configuration. The first two runs use their inspected native setup and fresh Mongo servers; no additional guard was injected into those runs.
- MongoMemoryServer uses the already cached binary, with runtime downloads disabled. Local socket/process permission was granted for these runs. Outputs and Jest cache went to `/tmp`; no source application file, live configuration, credential, imported corpus, or running service was changed.

## Limits and unrun work

No whole-repository suite, full typecheck, Lighthouse, browser E2E, live Meili/Redis integration, SQLite test, migration, TTL-clock expiry trial, or provider request was run. No application source changed, so implementation-only typecheck/performance gates are not satisfied or substituted by this baseline. Source instructions require those checks when relevant code changes later. Equal-time cursor completeness, full partial-failure/retry integration, Node 24.16.0 reproduction, and dist/source parity remain explicit gaps in the matrix.

Exploratory file lookup misses and a shell `command -a` typo were corrected during discovery; these were not Jest attempts. The four test logs contain no failed-test or warning diagnostics; ordinary fixture `console.log` output remains intact. Prior corpus-reconciliation failures/corrections remain in their original evidence directory and are not counted as these test attempts.
