'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const [source, compilerPath, output] = process.argv.slice(2);
const ts = require(compilerPath);
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const loaded = [];
function read(name) {
  const file = path.join(source, name);
  const text = fs.readFileSync(file, 'utf8');
  loaded.push({ path: name, sha256: hash(file) });
  return { text, ast: ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true) };
}
function declaration(input, name) {
  for (const node of input.ast.statements) {
    if (node.name?.text === name) return node.getText(input.ast);
    if (ts.isVariableStatement(node) && node.declarationList.declarations.some((d) => d.name.getText(input.ast) === name)) return node.getText(input.ast);
  }
  throw new Error(`Declaration not found: ${name}`);
}
function compile(text, requireFn) {
  const compiled = ts.transpileModule(text, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 }, reportDiagnostics: true });
  assert.equal(compiled.diagnostics.length, 0);
  const module = { exports: {} };
  vm.runInNewContext(compiled.outputText, { module, exports: module.exports, require: requireFn, Date, Set }, { timeout: 5000 });
  return module.exports;
}
const providerConfig = read('packages/data-provider/src/config.ts');
const providerSchema = read('packages/data-provider/src/schemas.ts');
const providerParsers = read('packages/data-provider/src/parsers.ts');
const provider = compile([declaration(providerConfig, 'excludedKeys'), declaration(providerSchema, 'EModelEndpoint'), declaration(providerSchema, 'isAgentsEndpoint'), declaration(providerParsers, 'isEphemeralAgentId')].join('\n'), () => { throw new Error('Unexpected provider dependency'); });
const helper = read('packages/api/src/conversations/save.ts');
const clientSource = read('api/app/clients/BaseClient.js');
const clazz = clientSource.ast.statements.find((n) => ts.isClassDeclaration(n) && n.name.text === 'BaseClient');
assert(clazz);
const methods = ['saveMessageToDatabase', 'getTurnConversationFields'].map((name) => {
  const node = clazz.members.find((member) => member.name?.getText(clientSource.ast) === name);
  assert(node, name); return node.getText(clientSource.ast);
}).join('\n');
const logger = { error() {} };
function build(db, candidate) {
  const helperSource = candidate ? helper.text.replaceAll('savedMessageId', 'savedMessageRef').replaceAll('appendMessageIds', 'appendMessageRefs') : helper.text;
  const exports = compile(helperSource, (name) => {
    if (name === '@librechat/data-schemas') return { logger };
    if (name === 'librechat-data-provider') return provider;
    throw new Error(`Unexpected helper dependency: ${name}`);
  });
  let body = methods;
  if (candidate) {
    assert.equal(body.split('savedMessageId: savedMessage?._id').length, 2);
    body = body.replace('savedMessageId: savedMessage?._id', 'savedMessageRef: savedMessage?.ref');
  }
  const C = vm.runInNewContext(`(class Probe { ${body} })`, { db, logger, ...exports }, { timeout: 5000 });
  return new C();
}
function canon(value) {
  if (value === undefined) return { $undefined: true };
  if (value === null || typeof value !== 'object') return value;
  if (Object.prototype.toString.call(value) === '[object Date]') return { $date: value.toISOString() };
  if (Array.isArray(value)) return Array.from(value, canon);
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canon(value[key])]));
}
const scopeKey = (ctx) => JSON.stringify([ctx.tenantMode, ctx.tenantId ?? null, ctx.userId]);
const refKey = (ref) => JSON.stringify([ref.kind, ref.messageId, ref.conversationId]);
class LocatorMemo {
  #entries = new WeakMap();
  remember(record, ctx) {
    if (!record?._id) return undefined;
    const ref = { kind: 'message', messageId: record.messageId, conversationId: record.conversationId };
    this.#entries.set(ref, { scope: scopeKey(ctx), logical: refKey(ref), locator: record._id });
    return ref;
  }
  async resolve(ref, ctx, lookup, mode = 'normal') {
    const cached = this.#entries.get(ref);
    if (mode !== 'always-lookup' && cached && cached.logical === refKey(ref) && (mode === 'unsafe-scope' || cached.scope === scopeKey(ctx))) return cached.locator;
    const row = await lookup(ref, ctx);
    if (!row) throw new Error('Message reference unavailable');
    return row._id;
  }
}
const cases = [];
for (const cache of ['unread', 'null', 'present']) for (const retention of [false, true]) for (const initialized of [false, true]) cases.push({ name: `${cache}/retention=${retention}/initialized=${initialized}`, cache, retention, initialized });
for (const variant of ['disposed','mismatch','skip','missing-result','missing-id','read-failure','message-failure','conversation-failure','conversation-error-object','no-upsert','endpoint-override','bound-retention','dispose-during-write','reset-initialized','populate-cache','change-endpoint-options']) cases.push({ name: variant, cache: 'unread', retention: false, initialized: false, variant });
async function run(spec, candidate, mutation = 'normal') {
  const trace = [];
  const existing = { conversationId: 'c1', endpoint: 'openAI', temperature: 0.7, isTemporary: true, expiredAt: new Date('2030-01-01T00:00:00Z') };
  const req = { user: { id: 'u1' }, body: { isTemporary: false, addedConvo: false }, config: { interfaceConfig: spec.retention ? { retentionMode: 'all', generalChatRetention: 30 } : {} }, conversationCreatedAt: '2026-01-01T00:00:00Z' };
  if (spec.cache !== 'unread') req.resolvedConversation = spec.cache === 'null' ? null : structuredClone(existing);
  if (spec.variant === 'no-upsert') req._agentEventBindingParentConversationId = 'parent';
  if (spec.variant === 'bound-retention') req._agentEventBindingRetention = { isTemporary: false, expiredAt: new Date('2031-01-01T00:00:00Z') };
  const endpointOptions = { agent_id: 'agent_saved', model: 'model-1' };
  if (spec.variant === 'endpoint-override') endpointOptions.conversationId = 'c2';
  let client;
  const raw = {
    async getConvo(...args) { trace.push({ method: 'getConvo', args: canon(args) }); if (spec.variant === 'read-failure') throw new Error('read failed'); return structuredClone(existing); },
    async saveMessage(...args) {
      trace.push({ method: 'saveMessage', args: canon(args) });
      if (spec.variant === 'message-failure') throw new Error('message failed');
      if (spec.variant === 'dispose-during-write') client.options = null;
      if (spec.variant === 'reset-initialized') client.fetchedConvo = null;
      if (spec.variant === 'populate-cache') req.resolvedConversation = structuredClone(existing);
      if (spec.variant === 'change-endpoint-options') endpointOptions.model = 'model-2';
      if (spec.variant === 'missing-result') return undefined;
      return { ...args[1], ...(spec.variant !== 'missing-id' && { _id: 'mongo-private-1' }) };
    },
    async saveConvo(...args) { trace.push({ method: 'saveConvo', args: canon(args) }); if (spec.variant === 'conversation-failure') throw new Error('conversation failed'); if (spec.variant === 'conversation-error-object') return { message: 'Error saving conversation' }; if (spec.variant === 'no-upsert') return null; return { conversationId: args[1].conversationId, title: 'saved' }; },
  };
  const memo = new LocatorMemo();
  let lookups = 0;
  const bindingScope = (ctx) => ({ userId: ctx.userId, tenantMode: 'tenant', tenantId: 't1' });
  const port = candidate ? {
    getConvo: raw.getConvo,
    async saveMessage(...args) { const saved = await raw.saveMessage(...args); if (!saved) return saved; const { _id, ...dto } = saved; const ref = memo.remember(saved, bindingScope(args[0])); return { ...dto, ...(ref && { ref }) }; },
    async saveConvo(ctx, fields, metadata) {
      const { appendMessageRefs, ...rest } = metadata;
      if (Object.hasOwn(metadata, 'appendMessageRefs')) {
        rest.appendMessageIds = await Promise.all(appendMessageRefs.map((ref) => memo.resolve(ref, bindingScope(ctx), async () => { lookups++; return { _id: 'mongo-private-1' }; }, mutation)));
      }
      return raw.saveConvo(ctx, fields, rest);
    },
  } : raw;
  client = build(port, candidate);
  client.options = { req, endpoint: 'agents', endpointType: 'agents', agent: { id: 'agent_saved' } };
  client.user = 'u1'; client.skipSaveConvo = spec.variant === 'skip'; client.fetchedConvo = spec.variant === 'reset-initialized' ? true : spec.initialized;
  if (spec.variant === 'disposed') client.options = null;
  let active = client;
  if (mutation === 'early-snapshot') { active = build(port, candidate); Object.assign(active, structuredClone({ options: client.options, user: client.user, skipSaveConvo: client.skipSaveConvo, fetchedConvo: client.fetchedConvo })); }
  let result, error;
  try { result = await active.saveMessageToDatabase({ messageId: 'm1', conversationId: 'c1', text: 'fixture', contextMeta: null }, endpointOptions, spec.variant === 'mismatch' ? 'u2' : 'u1'); }
  catch (caught) { error = caught.message; }
  const publicReference = result?.message?.ref;
  if (result?.message) { result = { ...result, message: { ...result.message } }; delete result.message._id; delete result.message.ref; }
  return { trace, result: canon(result), error: canon(error), cache: canon(active.options?.req ?? req), initialized: canon(active.fetchedConvo), optionsDisposed: client.options === null, referenceLookups: lookups, ...(candidate && { publicReference: canon(publicReference) }) };
}
function comparable(value) { const { publicReference, referenceLookups, ...rest } = value; return rest; }
const result = { sourceHead: execFileSync('git',['rev-parse','HEAD'],{cwd:source,encoding:'utf8'}).trim(), node: process.version, compiler: { path: compilerPath, version: ts.version, sha256: hash(compilerPath) }, sources: loaded, experimentSha256: hash(__filename), cases: [], memoCases: [], negativeControls: [], success: false };
(async () => {
 try {
  assert.equal(result.sourceHead,'fe79265b2f47937051625719f3ba5080189912c1');
  for (const spec of cases) {
    const reference = await run(spec, false); const candidate = await run(spec, true);
    const passed = JSON.stringify(comparable(reference)) === JSON.stringify(comparable(candidate)) && candidate.referenceLookups === 0;
    result.cases.push({ spec, passed, reference, candidate });
  }
  const ctx = { userId:'u1', tenantMode:'tenant', tenantId:'t1' };
  const memo = new LocatorMemo(); const row = {_id:'private-A',messageId:'m1',conversationId:'c1'}; const ref = memo.remember(row,ctx);
  async function memoCheck(name, instance, reference, context, expectedLookup, expectedLocator, missing=false) {
    let count=0,actual,error;
    try { actual=await instance.resolve(reference,context,async()=>{count++;return missing?null:{_id:'scoped-B'};}); } catch(e){error=e.message;}
    const passed=count===expectedLookup && (missing?error==='Message reference unavailable':actual===expectedLocator);
    result.memoCases.push({name,lookups:count,actual,error,passed});
  }
  await memoCheck('same-object',memo,ref,ctx,0,'private-A');
  await memoCheck('copied-reference',memo,structuredClone(ref),ctx,1,'scoped-B');
  await memoCheck('different-binding',new LocatorMemo(),ref,ctx,1,'scoped-B');
  await memoCheck('different-tenant',memo,ref,{...ctx,tenantId:'t2'},1,'scoped-B');
  await memoCheck('different-owner',memo,ref,{...ctx,userId:'u2'},1,'scoped-B');
  const changed=memo.remember(row,ctx);changed.messageId='m2';
  await memoCheck('mutated-reference',memo,changed,ctx,1,'scoped-B');
  await memoCheck('missing-row',memo,structuredClone(ref),ctx,1,undefined,true);
  result.memoCases.push({name:'plain-reference-shape',passed:JSON.stringify(ref)===JSON.stringify({kind:'message',messageId:'m1',conversationId:'c1'})});
  const normal=await run(cases[0],true);const extra=await run(cases[0],true,'always-lookup');
  result.negativeControls.push({name:'always-lookup-regression',detected:extra.referenceLookups>normal.referenceLookups,normal:normal.referenceLookups,mutant:extra.referenceLookups});
  const leaked=await memo.resolve(ref,{...ctx,tenantId:'t2'},async()=>({_id:'scoped-B'}),'unsafe-scope');
  result.negativeControls.push({name:'unchecked-scope-reuse',detected:leaked==='private-A',unsafeLocator:leaked,requiredScopedLocator:'scoped-B'});
  const reset=cases.find((c)=>c.variant==='reset-initialized');const live=await run(reset,false);const frozen=await run(reset,false,'early-snapshot');
  result.negativeControls.push({name:'early-snapshot-timing',detected:JSON.stringify(live.trace)!==JSON.stringify(frozen.trace),live,frozen});
  result.success=result.cases.every((c)=>c.passed)&&result.memoCases.every((c)=>c.passed)&&result.negativeControls.every((c)=>c.detected);
  if(!result.success)process.exitCode=1;
 } catch(error){result.error={message:error.message,stack:error.stack};process.exitCode=1;}
 finally {fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');process.stdout.write(JSON.stringify({success:result.success,comparisons:result.cases.length,comparisonFailures:result.cases.filter(c=>!c.passed).map(c=>c.spec.name),memoCases:result.memoCases,negativeControls:result.negativeControls.map(({name,detected})=>({name,detected})),error:result.error},null,2)+'\n');}
})();
