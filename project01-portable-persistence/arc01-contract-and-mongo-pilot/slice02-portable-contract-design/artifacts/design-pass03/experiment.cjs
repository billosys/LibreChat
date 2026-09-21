'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const [source, dependencyRoot, prior, output] = process.argv.slice(2);
assert(source && dependencyRoot && prior && output);
const req = createRequire(path.join(dependencyRoot, 'package.json'));
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const binary = path.join(dependencyRoot, 'node_modules/.cache/mongodb-memory-server/mongod-arm64-darwin-8.2.1');
process.env.MONGOMS_RUNTIME_DOWNLOAD = 'false';
process.env.MONGOMS_SYSTEM_BINARY = binary;
process.env.MONGOMS_VERSION = '8.2.1';
const { MongoMemoryServer } = req('mongodb-memory-server');
const { MongoClient } = req('mongodb');
const text = fs.readFileSync(prior, 'utf8');
const start = text.indexOf('const scopeKey =');
const end = text.indexOf('const cases = [];', start);
assert(start > 0 && end > start);
const memoSource = text.slice(start, end);
const LocatorMemo = vm.runInNewContext(`${memoSource}\nLocatorMemo`, {}, { timeout: 1000 });
const result = {
  startedAt: new Date().toISOString(), node: process.version,
  sourceHead: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: source, encoding: 'utf8' }).trim(),
  sourceFiles: ['packages/data-schemas/src/methods/message.ts', 'packages/data-schemas/src/methods/conversation.ts', 'packages/data-schemas/src/schema/message.ts'].map(p => ({ path: p, sha256: hash(path.join(source, p)) })),
  experimentSha256: hash(__filename), prior: { path: prior, sha256: hash(prior), extractedSource: memoSource },
  binary: { path: binary, sha256: hash(binary) },
  versions: { mongodb: req('mongodb/package.json').version, memoryServer: req('mongodb-memory-server/package.json').version },
  cases: [], negativeControls: [], success: false,
};
let server, client, allowedUri;
function checkTarget(uri) {
  const u = new URL(uri);
  if (uri !== allowedUri || u.hostname !== '127.0.0.1' || Number(u.port) <= 1023 || u.port === '27017') throw new Error('Database target rejected');
}
(async () => {
  try {
    let rejected = false;
    try { checkTarget('mongodb://127.0.0.1:27017/LibreChat'); } catch { rejected = true; }
    assert(rejected);
    result.negativeControls.push({ name: 'default-port', detected: rejected });
    server = await MongoMemoryServer.create({ binary: { systemBinary: binary, version: '8.2.1' }, instance: { ip: '127.0.0.1', dbName: 'guildhall_synthetic_lifecycle' } });
    allowedUri = server.getUri('guildhall_synthetic_lifecycle');
    checkTarget(allowedUri);
    result.openedUri = allowedUri;
    client = new MongoClient(allowedUri);
    await client.connect();
    const db = client.db('guildhall_synthetic_lifecycle');
    result.mongoVersion = (await db.admin().serverInfo()).version;
    const messages = db.collection('messages');
    const conversations = db.collection('conversations');
    await messages.createIndex({ messageId: 1, user: 1, tenantId: 1 }, { unique: true });
    const ctx = { userId: 'synthetic-owner', tenantMode: 'tenant', tenantId: 'synthetic-tenant' };
    for (const kind of ['unchanged', 'content-update', 'delete', 'recreate', 'rename', 'move']) {
      const filter = { messageId: crypto.randomUUID(), user: ctx.userId, tenantId: ctx.tenantId };
      const conversationId = crypto.randomUUID();
      const inserted = await messages.insertOne({ ...filter, conversationId, text: 'synthetic' });
      const observed = await messages.findOne({ _id: inserted.insertedId });
      const memo = new LocatorMemo();
      const ref = memo.remember(observed, ctx);
      if (kind === 'content-update') await messages.updateOne(filter, { $set: { text: 'changed' } });
      if (kind === 'delete' || kind === 'recreate') await messages.deleteOne(filter);
      if (kind === 'recreate') await messages.insertOne({ ...filter, conversationId, text: 'new incarnation' });
      if (kind === 'rename') await messages.updateOne(filter, { $set: { messageId: crypto.randomUUID() } });
      if (kind === 'move') await messages.updateOne(filter, { $set: { conversationId: crypto.randomUUID() } });
      const trace = [];
      let reads = 0;
      const lookup = async (r, c) => {
        reads++;
        const query = { messageId: r.messageId, conversationId: r.conversationId, user: c.userId, tenantId: c.tenantId };
        const row = await messages.findOne(query);
        trace.push({ query, row });
        return row;
      };
      async function resolve(r, mode) {
        const before = reads;
        try { return { id: String(await memo.resolve(r, ctx, lookup, mode)), reads: reads - before }; }
        catch (error) { return { error: error.message, reads: reads - before }; }
      }
      const hot = await resolve(ref);
      const cold = await resolve(JSON.parse(JSON.stringify(ref)));
      const same = hot.id === cold.id && hot.error === cold.error;
      const expectedSame = kind === 'unchanged' || kind === 'content-update';
      const entry = { kind, observed, reference: ref, hot, cold, same, expectedSame, trace, links: [] };
      result.cases.push(entry);
      assert.equal(hot.id, String(observed._id));
      assert.equal(hot.reads, 0); assert.equal(cold.reads, 1); assert.equal(same, expectedSame);
      if (kind === 'recreate') { assert(cold.id); assert.notEqual(cold.id, hot.id); }
      if (['delete', 'rename', 'move'].includes(kind)) assert.equal(cold.error, 'Message reference unavailable');
      for (const [label, resolution] of [['hot', hot], ['cold', cold]]) {
        if (!resolution.id) continue;
        const { ObjectId } = req('mongodb');
        const locator = new ObjectId(resolution.id);
        await conversations.updateOne({ name: `${kind}-${label}` }, { $addToSet: { messages: { $each: [locator] } } }, { upsert: true });
        const conversation = await conversations.findOne({ name: `${kind}-${label}` });
        const linkedRow = await messages.findOne({ _id: conversation.messages[0] });
        const matchesReference = linkedRow !== null && linkedRow.messageId === ref.messageId && linkedRow.conversationId === ref.conversationId && linkedRow.user === ctx.userId && linkedRow.tenantId === ctx.tenantId;
        entry.links.push({ label, conversation, linkedRow, physicalRowExists: linkedRow !== null, matchesReference });
        assert.equal(linkedRow !== null, !(label === 'hot' && ['delete', 'recreate'].includes(kind)));
        assert.equal(matchesReference, label === 'cold' || expectedSame);
      }
      if (kind === 'unchanged') {
        const forced = await resolve(ref, 'always-lookup');
        const detected = forced.reads !== 0;
        assert.equal(forced.id, hot.id); assert(detected);
        result.negativeControls.push({ name: 'always-lookup', forced, detected });
      }
      entry.passed = true;
    }
    result.success = true;
  } catch (error) {
    result.error = { message: error.message, stack: error.stack }; process.exitCode = 1;
  } finally {
    try { if (client) await client.close(); if (server) await server.stop(); result.cleanedUp = true; }
    catch (error) { result.cleanupError = error.message; result.success = false; process.exitCode = 1; }
    result.finishedAt = new Date().toISOString();
    fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  }
})();
