# Read-only Claude reconciliation evidence

Authoritative interpretation: `../../corpus-reconciliation.md`.

`attempt01-summary.json` is the first comparison result with an incorrect persisted `isEdited` expectation. Its full row diagnostics are retained in `attempt01-mismatches.json.gz`. `attempt02-summary.json` is the corrected result. Do not use exit code alone as the verdict: the comparison's `outcome`, coverage counts, mismatch count, and source/collection stability flags are the acceptance evidence.

`topology-exploratory.json` retains the superseded parent analysis before recognizing the observed external-root marker. `topology-final.py`, `topology-final.json`, and `topology-final-locators.json` capture the corrected analysis. The final analysis must be used for topology findings.

Counters are incremented on observed events; an omitted optional counter represents zero occurrences in this script's bounded population. This convention does not apply to absent source data fields. Source locators are zero-based conversation/message array indexes. Hashes in pairings deliberately omit raw source/stored IDs and conversation titles; they document pairing coverage but are not an operational source-ID mapping table.

The scripts use only Mongo read operations, import no application modules, and do not invoke Mongoose model registration. They read the local repository's `.env` solely to resolve Mongo connection configuration, without printing credentials. They compare raw text in memory; saved diagnostics contain no message bodies. The original export and live Mongo data remain outside this evidence directory.

## Reproduction

Use a fresh output directory. The source JSON is fingerprint-pinned. Inspect the intended local Mongo target first; the comparison intentionally fails if multiple endpoint/scope populations are present. It compares the current database, so subsequent imports or edits can legitimately change the result. The paired collection reads detect observed changes but are not a transactionally consistent snapshot.

With Node, Python 3, and the LibreChat checkout's installed `mongodb`/`dotenv` dependencies available:

```bash
test "$(git -C /Users/oubiwann/lab/billosys/LibreChat rev-parse HEAD)" = ba44443fdb232bbe6d4977e2619774b5a72586ac
node --check attempt02.cjs
node attempt02.cjs /tmp/guildhall-reconciliation-reproduction
python3 topology-final.py
```

The Python script currently writes its aggregate/topology outputs to the named `/tmp/guildhall-source-topology-*` paths; it never overwrites the private source export. Connection access may require elevated local execution in a restricted environment. The original sandboxed probe failed with `MongoServerSelectionError`; an authorized elevated retry succeeded. This access failure was not a corpus mismatch.

No test data was written to Mongo. Negative controls perturb an in-memory copy of one stored message and assert that the corresponding comparison fails; the positive control requires the unchanged record to pass first.
