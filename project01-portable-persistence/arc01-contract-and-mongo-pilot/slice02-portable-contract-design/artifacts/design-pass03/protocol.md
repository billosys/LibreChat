# Pass 3 — logical reference versus observed-row handoff

Predeclared before execution. One-contributor Slice02 investigation; no application changes.

Question: does the pass-2 WeakMap preserve value-based reference resolution when message storage changes between save and link? Decision: retain or reject the invisible locator optimization; distinguish logical identity from the row observed by a write.

Use the exact `scopeKey`, `refKey`, and `LocatorMemo` declarations extracted from the sealed pass-2 experiment. Pin that file's hash. Run against native Mongo collections in a fresh loopback-only MongoMemoryServer, cached Mongo 8.2.1, downloads disabled. Use the repository's installed Mongo driver, not application dist. Create the same unique `(messageId,user,tenantId)` index as the inspected message schema. No environment files, live application connection, export, or private corpus is loaded. Abort if the generated URI is not 127.0.0.1, has port <=1023 or 27017, or differs from the sole allowed URI. Stop and clean up on any unexpected result; preserve all attempts.

Independent variable: mutation after remembering the observed row. Constants: effective scope, original logical reference values, isolated database, resolution code, lookup filter. Each case uses a new messageId. Resolve the original object and a JSON round-trip copy sequentially after the mutation with no further writes. Record IDs/errors, number of fallback reads, stored rows, and actual conversation append results. Count only reference-resolution reads; fixture inspection queries are excluded from that counter.

Six ordered cases and oracles:

| Case | Expected cached result | Expected copied-reference result | Value equivalence |
|---|---|---|---|
| unchanged | observed row A | A | holds |
| content update | A | A | holds |
| delete only | A | unavailable | fails |
| delete/recreate with same logical key | A | new row B | fails |
| rename logical message ID | A | unavailable | fails |
| move conversation ID | A | unavailable | fails |

For every case, cached resolution must use zero fallback reads and copied resolution one. Append each successful result to a distinct synthetic conversation using the existing `$addToSet` shape; measure whether the referenced physical row exists and whether it still matches the original scoped reference. Deleted/recreated A must be dangling. Renamed/moved A exists but no longer matches the reference. Successful characterization means these observations match, not that the candidate is correct.

Negative controls: reject a live-style URI on port 27017; force `always-lookup` on an unchanged row and verify the zero-extra-read oracle rejects it even though the ID agrees. No timing, probabilistic race rate, performance, full LibreChat conformance, tenant middleware, TTL timing, or schema validation claims. Deterministic intervening mutations witness possible interleavings; they do not measure production frequency. Node 22 remains below the repository's Node 24 pin.

Capture protocol/harness hashes, source head and relevant file hashes, dependency versions, binary hash, command, times, exit, raw output, JSON results and cleanup. Preserve earlier packets unchanged. Do not turn a discovered lifecycle defect into an incidental production fix.
