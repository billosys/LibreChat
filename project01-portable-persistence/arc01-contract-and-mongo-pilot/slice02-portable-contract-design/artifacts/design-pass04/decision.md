# Turn-write handle comparison and contract mapping

**Working decision:** use per-invocation ownership for the observed message-to-conversation handoff. The prototype preserves all 28 selected orchestration cases, passes 26 lifecycle/scope cases and detects all five deliberately broken variants. The result supports this boundary; it does not establish full adapter conformance or finish Slice02.

The [protocol](protocol.md), [prototype](handle.cjs), [experiment](experiment.cjs), [attempt](attempt-01.json), [raw summary](output-01.log) and [full traces](result-01.json) are retained. One execution attempt, exit 0; no skipped cases. Source is `fe79265b2f47937051625719f3ba5080189912c1`; seven source files and the TypeScript compiler are hashed in the result. Node 22.22.3 / TypeScript 5.9.3. No application source, installed application dist, database or private corpus was used.

## Evidence and its meaning

| Check | Result | Meaning |
|---|---|---|
| Source-based orchestration | 28/28 match | Same selected legacy call ordering/arguments, normalized returned values/errors and request/client state; every created candidate handle released |
| Lifecycle, scope and overlap | 26/26 | Invalid/repeated/overlapping stage calls rejected without another store call; release blocks future stages; independent handles retain separate locators |
| Negative controls | 5/5 detected | Re-resolving to a replacement row, sharing a locator slot, bypassing scope checks, omitting release and early client snapshot each violate an oracle |
| Source inventory | 44 message / 73 conversation fields | AST-declared top-level schema fields, with conversationPreset expanded; evidence for field mapping, not complete runtime DTOs |

The comparison reuses the prior 28 fixture definitions and reference path. Candidate transformations remove the physical-ID argument from `saveTurnConversation`, create a handle immediately before message persistence, route conversation persistence through that handle and release in `finally`. Application rules are still extracted from actual source. There is no eager capture of later `skipSaveConvo`, `fetchedConvo`, endpoint options or request cache. The only normalized output difference is returned message `_id`; the candidate adds no ref or receipt field.

The prototype retains the observed locator, not a whole public reference object or a global map. Its ordinary path has no resolver and introduces no extra mocked legacy reads. The pass-3 real-Mongo counterexamples explain why it must not substitute a current logical lookup. Here the recreation test is a deterministic double, not another Mongo run.

## Scope and lifetime contract

The experiment transpiles the actual `tenantContext.ts` and `tenant/policy.ts`, uses Node AsyncLocalStorage, and calls the real `resolveTenantScope`. Only strict-mode environment and logging are controlled doubles. Owner identity comes from the existing trusted write context; this check is not a replacement for authentication, ACLs, query scoping or payload sanitization.

```text
fresh --saveMessage--> saving --returned--> saved --saveConvo--> linking --settled--> settled
                          |                                            |
                       rejection                                    rejection
                          v                                            v
                        failed                                      settled

release from any state -> released; subsequent dispatches rejected
scope mismatch/policy rejection before dispatch -> released
```

`settled` describes completion of the call, not successful persistence. Release is idempotent. A write already dispatched may complete and return its normal result after release; it may not repopulate the retained locator or enable another stage. A message failure forbids the conversation stage. A conversation failure is terminal for that handle; callers do not silently retry it. New workflow invocations obtain independent handles. Tests use explicit deferred promises, not timing sleeps.

Cross-owner and changed tenant modes fail before the next handle write. Tests include other tenant, scoped/system transitions, unscoped-to-scoped, strict missing scope, allowed non-strict unscoped/system, and strict policy becoming active after begin. Underlying reads/writes still need their normal policy; the handle does not grant authority. In particular, the application's pre-conversation read is outside the handle and still requires the normal scoped method.

The mock result omits only top-level `_id`. **It is not a finished DTO sanitizer.** Nested Mixed values, hidden fields, timestamps, implicit Document fields and projection-specific outputs still need explicit treatment. `inspectForTest` and fault-injection switches exist only for this experiment and must not be exported by a production interface.

The proposed local methods retain context arguments for comparison and reject changed owner/scope. Final type names and signatures can become narrower once the field contract is complete. Seed remains a separate unchanged application path; no seed execution or complete request lifecycle proof occurred here. This local interface does not define a future Rust service session protocol.

An integrated comparison must also resolve validation ordering: begin-time strict-scope rejection can precede the legacy message method's missing-owner/invalid-conversation-ID checks. The mocked store comparison does not prove identical outcomes for combinations of invalid input and absent strict scope. Treat that as an explicit compatibility decision, not an automatically accepted hardening change.

## Field and result mapping progressed

The [field census](field-census.json) is generated by [field-census.cjs](field-census.cjs) directly from five hashed source files. It records definition text, source line, default/select/required declarations, interface members, preset overrides and mismatches. See [contract mapping](contract-mapping.md) for concrete implications and current outcome/patch rules.

Two mismatches matter immediately: the runtime conversation schema has `thinkingLevel`, absent from `IConversation`; `plugin` and `plugins` appear in `IMessage` but have no active top-level message schema declaration. Do not resolve these by silently dropping existing data or blindly treating an interface as the persisted schema. `isShared` is explicitly request-derived, and timestamp fields are supplied by schema options. These are reconciliation inputs, not yet classified upstream defects.

## Disposition and next work

D02 handoff direction is now supported by the bounded comparison and lifecycle tests; the invisible cache remains rejected. D03/D04 have a concrete compatibility mapping in this packet. Next reconcile the named server-history/public-message projections and actual callers against the census, define concrete engine-neutral DTO types, and resolve the remaining build/runtime and implementation fence before issuing a contributor prompt. Do not spend another pass exploring identity alternatives without a new counterexample.

The type/consumer work must retain hidden coordination fields outside ordinary public projections and avoid leaking `Document`/ObjectId or accepting arbitrary engine operators. Mongo's real methods still require integrated tests for provenance, retention, project statistics, no-upsert, partial failure and tenant isolation. All seven Slice02 acceptance rows remain open; no independent review or workflow transition is claimed.
