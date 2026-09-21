'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const [source, compilerPath, output] = process.argv.slice(2);
const ts = require(compilerPath);
const { beginTurnWrite } = require('./handle.cjs');
const controlledProcess = { env: { TENANT_ISOLATION_STRICT: 'false' } };
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
  vm.runInNewContext(compiled.outputText, { module, exports: module.exports, require: requireFn, Date, Set, process: controlledProcess }, { timeout: 5000 });
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
const tenantSource = read('packages/data-schemas/src/config/tenantContext.ts');
const tenant = compile(tenantSource.text, name => { assert.equal(name, 'async_hooks'); return require('node:async_hooks'); });
const policySource = read('packages/data-schemas/src/tenant/policy.ts');
const policy = compile(policySource.text, name => {
  if (name === '~/config/tenantContext') return tenant;
  if (name === '~/config/winston') return { warn() {} };
  throw new Error(`Unexpected policy dependency: ${name}`);
});
function setStrict(value) { controlledProcess.env.TENANT_ISOLATION_STRICT = String(value); policy.resetTenantStrictCache(); }
function replaceOnce(text, before, after) {
  assert.equal(text.split(before).length, 2, before); return text.replace(before, after);
}
function build(db, candidate, mutation) {
  let helperSource = helper.text;
  if (candidate) helperSource = replaceOnce(helperSource,
    'const appendMessageIds = write.savedMessageId != null ? [write.savedMessageId] : undefined;',
    'const appendMessageIds = undefined;');
  const exports = compile(helperSource, name => {
    if (name === '@librechat/data-schemas') return { logger };
    if (name === 'librechat-data-provider') return provider;
    throw new Error(`Unexpected helper dependency: ${name}`);
  });
  let body = methods;
  if (candidate) {
    body = replaceOnce(body, 'const savedMessage = await db.saveMessage(', 'const turn = db.beginTurnWrite(reqCtx);\n    try {\n    const savedMessage = await turn.saveMessage(');
    body = replaceOnce(body, 'await saveTurnConversation(db, {', 'await saveTurnConversation({ getConvo: db.getConvo, saveConvo: turn.saveConvo }, {');
    body = replaceOnce(body, 'savedMessageId: savedMessage?._id,', '');
    body = replaceOnce(body, 'return { message: savedMessage, conversation };',
      'return { message: savedMessage, conversation };\n    } finally { ' + (mutation === 'omit-release' ? '' : 'turn.release();') + ' }');
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
  let lookups = 0;
  const handles = [];
  const port = candidate ? {
    getConvo: raw.getConvo,
    beginTurnWrite(ctx) { const h = beginTurnWrite(raw, ctx, policy.resolveTenantScope); handles.push(h); return h; },
  } : raw;
  client = build(port, candidate, mutation);
  client.options = { req, endpoint: 'agents', endpointType: 'agents', agent: { id: 'agent_saved' } };
  client.user = 'u1'; client.skipSaveConvo = spec.variant === 'skip'; client.fetchedConvo = spec.variant === 'reset-initialized' ? true : spec.initialized;
  if (spec.variant === 'disposed') client.options = null;
  let active = client;
  if (mutation === 'early-snapshot') { active = build(port, candidate, mutation); Object.assign(active, structuredClone({ options: client.options, user: client.user, skipSaveConvo: client.skipSaveConvo, fetchedConvo: client.fetchedConvo })); }
  let result, error;
  try { result = await active.saveMessageToDatabase({ messageId: 'm1', conversationId: 'c1', text: 'fixture', contextMeta: null }, endpointOptions, spec.variant === 'mismatch' ? 'u2' : 'u1'); }
  catch (caught) { error = caught.message; }
  const publicReference = result?.message?.ref;
  if (result?.message) { result = { ...result, message: { ...result.message } }; delete result.message._id; delete result.message.ref; }
  return { trace, result: canon(result), error: canon(error), cache: canon(active.options?.req ?? req), initialized: canon(active.fetchedConvo), optionsDisposed: client.options === null, referenceLookups: lookups, ...(candidate && { handles: handles.map(h => h.inspectForTest()) }) };
}
function comparable(value) { const { handles, referenceLookups, ...rest } = value; return rest; }
const result = { sourceHead: execFileSync('git',['rev-parse','HEAD'],{cwd:source,encoding:'utf8'}).trim(), node: process.version, compiler: { path: compilerPath, version: ts.version, sha256: hash(compilerPath) }, sources: loaded, experimentSha256: hash(__filename), handleSha256: hash(path.join(__dirname,'handle.cjs')), cases: [], lifecycleCases: [], negativeControls: [], success: false };
const ctx = { userId: 'u1' };
const fields = { messageId: 'm1', conversationId: 'c1', text: 'fixture' };
function fixture(options = {}) {
  const trace = [];
  const raw = {
    async saveMessage(context, input, metadata) {
      trace.push({ method: 'saveMessage', args: canon([context,input,metadata]) });
      if (options.messageGate) await options.messageGate;
      if (options.messageError) throw new Error('message failed');
      if (options.absent) return undefined;
      return { ...input, ...(options.noLocator ? {} : { _id: options.id ?? 'observed-A' }) };
    },
    async saveConvo(context, input, metadata) {
      trace.push({ method: 'saveConvo', args: canon([context,input,metadata]) });
      if (options.conversationGate) await options.conversationGate;
      if (options.conversationError) throw new Error('conversation failed');
      return { conversationId: input.conversationId };
    },
  };
  const h = beginTurnWrite(raw, ctx, policy.resolveTenantScope, options.mutant);
  return { h, trace, raw };
}
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return { promise, resolve }; };
const save = f => f.h.saveMessage(ctx, fields, {});
const link = f => f.h.saveConvo(ctx, { conversationId: 'c1' }, {});
const appended = f => f.trace.filter(t => t.method === 'saveConvo').map(t => t.args[2].appendMessageIds);
async function check(name, fn) {
  const entry = { name, passed: false }; result.lifecycleCases.push(entry);
  await tenant.tenantStorage.run({ tenantId: 't1' }, async () => { setStrict(false); entry.observations = await fn(); });
  entry.passed = true;
}
async function illegal(f, call, pattern = /Invalid turn-write state/) {
  const before=f.trace.length; await assert.rejects(call,pattern); assert.equal(f.trace.length,before);
}
async function overlap(mutant = false) {
  const a = deferred(), b = deferred(); const slot = {};
  const fa=fixture({ id:'A',messageGate:a.promise,...(mutant && {mutant:{sharedSlot:slot}}) });
  const fb=fixture({ id:'B',messageGate:b.promise,...(mutant && {mutant:{sharedSlot:slot}}) });
  const pa=save(fa),pb=save(fb); b.resolve(); await pb; a.resolve(); await pa;
  await link(fb);await link(fa);fa.h.release();fb.h.release();
  return { a:appended(fa),b:appended(fb),states:[fa.h.inspectForTest(),fb.h.inspectForTest()] };
}
(async () => {
 try {
  assert.equal(result.sourceHead,'fe79265b2f47937051625719f3ba5080189912c1');
  for (const spec of cases) {
    const reference=await tenant.tenantStorage.run({tenantId:'t1'},async()=>run(spec,false));
    const candidate=await tenant.tenantStorage.run({tenantId:'t1'},async()=>run(spec,true));
    const released=candidate.handles.every(h=>h.released&&!h.retainsLocator);
    const passed=JSON.stringify(comparable(reference))===JSON.stringify(comparable(candidate))&&candidate.referenceLookups===0&&released;
    result.cases.push({spec,passed,reference,candidate});
    assert(passed,spec.name);
  }
  await check('normal-lifecycle-and-plain-dto',async()=>{const f=fixture();const dto=await save(f);assert(!Object.hasOwn(dto,'_id'));assert(!Object.hasOwn(dto,'ref'));await link(f);assert.deepEqual(appended(f),[['observed-A']]);f.h.release();f.h.release();assert.deepEqual(f.h.inspectForTest(),{state:'released',released:true,retainsLocator:false});return {dto,trace:f.trace,state:f.h.inspectForTest()};});
  await check('conversation-before-message',async()=>{const f=fixture();await illegal(f,()=>link(f));f.h.release();return f.trace;});
  await check('duplicate-message',async()=>{const f=fixture();await save(f);await illegal(f,()=>save(f));f.h.release();return f.trace;});
  await check('concurrent-message',async()=>{const d=deferred(),f=fixture({messageGate:d.promise});const pending=save(f);await illegal(f,()=>save(f));d.resolve();await pending;f.h.release();return f.trace;});
  await check('duplicate-conversation',async()=>{const f=fixture();await save(f);await link(f);await illegal(f,()=>link(f));f.h.release();return f.trace;});
  await check('concurrent-conversation',async()=>{const d=deferred(),f=fixture({conversationGate:d.promise});await save(f);const pending=link(f);await illegal(f,()=>link(f));d.resolve();await pending;f.h.release();return f.trace;});
  await check('release-before-message',async()=>{const f=fixture();f.h.release();await illegal(f,()=>save(f));return f.h.inspectForTest();});
  await check('release-during-message',async()=>{const d=deferred(),f=fixture({messageGate:d.promise});const p=save(f);f.h.release();d.resolve();const dto=await p;assert(dto.messageId);await illegal(f,()=>link(f));assert(!f.h.inspectForTest().retainsLocator);return {trace:f.trace,state:f.h.inspectForTest()};});
  await check('release-during-conversation',async()=>{const d=deferred(),f=fixture({conversationGate:d.promise});await save(f);const p=link(f);f.h.release();d.resolve();await p;await illegal(f,()=>link(f));assert(!f.h.inspectForTest().retainsLocator);return {trace:f.trace,state:f.h.inspectForTest()};});
  await check('message-rejection',async()=>{const f=fixture({messageError:true});await assert.rejects(()=>save(f),/message failed/);await illegal(f,()=>link(f));await illegal(f,()=>save(f));f.h.release();return f.trace;});
  await check('conversation-rejection',async()=>{const f=fixture({conversationError:true});await save(f);await assert.rejects(()=>link(f),/conversation failed/);await illegal(f,()=>link(f));assert(!f.h.inspectForTest().retainsLocator);f.h.release();return f.trace;});
  for (const option of ['absent','noLocator']) await check(option,async()=>{const f=fixture({[option]:true});await save(f);await link(f);assert.equal(appended(f)[0],undefined);f.h.release();return f.trace;});
  await check('other-owner',async()=>{const f=fixture();await save(f);await illegal(f,()=>f.h.saveConvo({userId:'u2'},{},{}),/scope changed/);assert(!f.h.inspectForTest().retainsLocator);return f.trace;});
  for (const [name,from,to] of [['other-tenant','t1','t2'],['scoped-to-system','t1','__SYSTEM__'],['system-to-scoped','__SYSTEM__','t1'],['unscoped-to-scoped',undefined,'t1']]) {
    await check(name,async()=>{const f=await tenant.tenantStorage.run({tenantId:from},async()=>{const x=fixture();await save(x);return x;});await tenant.tenantStorage.run({tenantId:to},async()=>illegal(f,()=>link(f),/scope changed/));return {trace:f.trace,state:f.h.inspectForTest()};});
  }
  await check('strict-missing-scope',async()=>{setStrict(true);let rejected=false;await tenant.tenantStorage.run({},async()=>{assert.throws(()=>fixture(),/without tenant context in strict mode/);rejected=true;});setStrict(false);return {rejected};});
  for (const [name,tenantId] of [['allowed-unscoped',undefined],['allowed-system','__SYSTEM__']]) await check(name,async()=>tenant.tenantStorage.run({tenantId},async()=>{const f=fixture();await save(f);await link(f);assert.deepEqual(appended(f),[['observed-A']]);f.h.release();return f.trace;}));
  await check('strict-enabled-after-begin',async()=>tenant.tenantStorage.run({},async()=>{const f=fixture();await save(f);setStrict(true);await illegal(f,()=>link(f),/without tenant context in strict mode/);setStrict(false);return f.trace;}));
  await check('overlapping-handles-reverse-completion',async()=>{const o=await overlap();assert.deepEqual(o.a,[['A']]);assert.deepEqual(o.b,[['B']]);return o;});
  await check('caller-dto-mutation',async()=>{const f=fixture();const dto=await save(f);dto._id='injected';dto.messageId='changed';await link(f);assert.deepEqual(appended(f),[['observed-A']]);f.h.release();return f.trace;});
  await check('observed-row-after-recreation',async()=>{const f=fixture();await save(f);const currentRow={_id:'replacement-B',...fields};await link(f);assert.deepEqual(appended(f),[['observed-A']]);f.h.release();return {currentRow,trace:f.trace};});
  await check('reject-caller-physical-linkage',async()=>{const f=fixture();await save(f);await illegal(f,()=>f.h.saveConvo(ctx,{}, {appendMessageIds:['forged']}),/Physical linkage is private/);f.h.release();return f.trace;});
  await tenant.tenantStorage.run({tenantId:'t1'},async()=>{
    const f=fixture({mutant:{reResolve:async()=>'replacement-B'}});await save(f);await link(f);f.h.release();result.negativeControls.push({name:'re-resolve-after-recreation',detected:JSON.stringify(appended(f))!==JSON.stringify([['observed-A']]),trace:f.trace});
    const shared=await overlap(true);result.negativeControls.push({name:'shared-locator-slot',detected:JSON.stringify(shared.b)!==JSON.stringify([['B']]),observations:shared});
    const unsafe=fixture({mutant:{unsafeScope:true}});await save(unsafe);await tenant.tenantStorage.run({tenantId:'t2'},async()=>link(unsafe));unsafe.h.release();result.negativeControls.push({name:'bypassed-scope-recheck',detected:unsafe.trace.filter(t=>t.method==='saveConvo').length===1,trace:unsafe.trace});
    const unreleased=await run(cases[0],true,'omit-release');result.negativeControls.push({name:'omitted-release',detected:unreleased.handles.some(h=>!h.released),states:unreleased.handles});
    const reset=cases.find(c=>c.variant==='reset-initialized');const live=await run(reset,false),frozen=await run(reset,false,'early-snapshot');result.negativeControls.push({name:'early-snapshot',detected:JSON.stringify(live.trace)!==JSON.stringify(frozen.trace),live,frozen});
  });
  assert.equal(result.lifecycleCases.length,26);
  assert(result.negativeControls.every(c=>c.detected));
  result.success=true;
 } catch(error){result.error={message:error.message,stack:error.stack};process.exitCode=1;}
 finally {fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');process.stdout.write(JSON.stringify({success:result.success,comparisons:result.cases.length,lifecycleCases:result.lifecycleCases.map(({name,passed})=>({name,passed})),negativeControls:result.negativeControls.map(({name,detected})=>({name,detected})),error:result.error},null,2)+'\n');}
})();
