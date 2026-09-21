# Planning commit-message migration

The Operator requested both co-author trailers on all our existing commits before first publication. On 2026-09-20 local time, the twelve locally authored commits were found exclusively on orphan `planning`. Live fork inspection showed only `origin/main`; the planning history was unpublished. Source branches had no locally authored commits at that point.

Only commit messages and the necessary parent IDs changed. Every corresponding tree is identical; original author and committer headers (including timestamps) are preserved. There were no signed commits, merge commits or existing trailers in this set. Main and all inherited upstream commits were left unchanged. New commits after this migration include the footer when authored and need no mapping.

Historical experiment output, sealed artifacts and their hashes were not edited to substitute new IDs. When an older plan or evidence file names an old planning commit, resolve it through this table. Application source baseline IDs such as `ba44443fd` and `fe79265b2` are unrelated to this rewrite and remain unchanged.

| Original planning commit | Rewritten planning commit | Subject |
|---|---|---|
| `c90d56654e66d22b69bd6c820274e2c38a7dfedf` | `c3b9ee456c58bddfc212f2a62ff36f8e4c34a044` | docs: establish portable persistence research and planning |
| `82f7d2f5fdd6f697a8942d446428d42b15994f8f` | `4cc62568b6580451079f27f84afec39afc13bc46` | docs: scope Arc01 investigation and Claude-first corpus work |
| `c488193cd65ae1289dfbe4c2dede56b2f04e10a1` | `e984bc8afe381effe21f93ea7066ff4b85ca7c9f` | docs: record initial Claude corpus and local Mongo import |
| `d5e9f537058aad2ba5a4b4a9de6f43575579c719` | `6395ea1c6179910fbe9c22b48485f48fe0a0b61c` | docs: reconcile Claude source corpus with imported Mongo records |
| `e4f43787317d9b9e2a18b184e83b474d6fea6773` | `1e7242a8f35375c518ba9b6201ec0f52ade21488` | docs: open Arc01 and its behavior-baseline investigation |
| `51ca3cff46a9fb653dad8926ae1713e630674133` | `a12664ff845c0b9797d62f7a732dc655c3fb1c7c` | docs: enable expedited workflow and relative prompt reporting |
| `a085652ce8be2b158bb3152786f6d6f08d263f47` | `8b43caed01058e02a332360a228e957fd0f5bfd7` | docs: deliver slice01 persistence behavior baseline |
| `b3b2b7e94eca6dc33f1b6ce19ae1cdece649d6c8` | `4a20b14c421765c5c538221bb7e414cae41e5874` | docs: advance slice02 contract design and cursor characterization |
| `47477869b3eed0e2cd637cde8ef8fab30ee72568` | `a0a6131d63da3d18ec87e8d79c2d103ffe3a2a3c` | docs: define development worktrees and sketch import features |
| `f822a5ada5e645ea9cff9aa85de1095ee0c93738` | `92054d4220040dfaf74259bc1d85d8c7bdc9045b` | docs: guide persistence identity toward the cognitive data plane |
| `190f22920cd0d8a7bf3db7feb4e3aecf01193d97` | `943486bdb472c632864b787fe94ad34dd33f5f0a` | docs: compare logical message references against source orchestration |
| `f29c92f2bdf24fe8c0cc60ec5613180063afd6c8` | `6da2c825efa2be001a0f19c38ecc96aa4d7d47b1` | docs(persistence): reject implicit locator cache after lifecycle checks |

The exact required trailer block is:

```text
Co-authored-by: Codex <noreply@openai.com>
Co-authored-by: Billo AI <ai-engineering@billo.systems>
```

A verified recovery bundle and machine-readable map are retained locally, outside normal branch publication:

```text
/Users/oubiwann/lab/billosys/LibreChat/.git/billo-history-backups/20260921T044907Z/planning-before-trailers.bundle
/Users/oubiwann/lab/billosys/LibreChat/.git/billo-history-backups/20260921T044907Z/commit-map.json
```

The bundle preserves the old planning tip and its reachable objects. No backup branch was created, so an ordinary branch push will not accidentally publish a second uncorrected history. No remote push or force-push was performed. This record does not authorize rewriting future published history.
