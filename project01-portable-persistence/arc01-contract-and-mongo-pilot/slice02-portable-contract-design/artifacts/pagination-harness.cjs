'use strict';

const { createRequire } = require('node:module');
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const sourceRoot = process.argv[2];
const output = process.argv[3];
if (!sourceRoot || !output) throw new Error('Usage: node harness.cjs SOURCE_ROOT OUTPUT_JSON');
const req = createRequire(path.join(sourceRoot, 'package.json'));
const binary = path.join(sourceRoot, 'node_modules/.cache/mongodb-memory-server/mongod-arm64-darwin-8.2.1');
process.env.NODE_ENV = 'test';
process.env.LOG_TO_FILE = 'false';
process.env.MEILI_HOST = '';
process.env.MEILI_MASTER_KEY = '';
process.env.MONGOMS_RUNTIME_DOWNLOAD = 'false';
process.env.MONGOMS_SYSTEM_BINARY = binary;
process.env.MONGOMS_VERSION = '8.2.1';
process.env.MONGO_URI = 'mongodb://127.0.0.1:1/blocked';
const mongoose = req('mongoose');
const { MongoMemoryServer } = req('mongodb-memory-server');
const hash = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const result = {
  startedAt: new Date().toISOString(), node: process.version,
  sourceHead: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: sourceRoot, encoding: 'utf8' }).trim(),
  artifacts: [__filename, req.resolve('@librechat/data-schemas'), binary,
    path.join(sourceRoot, 'packages/data-schemas/src/methods/message.ts')]
    .map((file) => ({ file, sha256: hash(file) })),
  versions: { mongoose: req('mongoose/package.json').version,
    memoryServer: req('mongodb-memory-server/package.json').version },
  trials: [], harnessSucceeded: false,
};
let server;
let allowedUri;
const originalOpen = mongoose.Connection.prototype.openUri;
function checkTarget(uri) {
  const parsed = new URL(uri);
  if (uri !== allowedUri || parsed.hostname !== '127.0.0.1' ||
      Number(parsed.port) <= 1023 || parsed.port === '27017') {
    throw new Error('Database target rejected');
  }
}
mongoose.Connection.prototype.openUri = function(uri, ...args) {
  checkTarget(uri);
  result.openedUri = uri;
  return originalOpen.call(this, uri, ...args);
};

(async () => {
  try {
    try { checkTarget('mongodb://127.0.0.1:27017/LibreChat'); }
    catch { result.defaultPortRejected = true; }
    if (!result.defaultPortRejected) throw new Error('Isolation negative control failed');
    server = await MongoMemoryServer.create({
      binary: { systemBinary: binary, version: '8.2.1' },
      instance: { ip: '127.0.0.1', dbName: 'guildhall_synthetic_cursor' },
    });
    allowedUri = server.getUri('guildhall_synthetic_cursor');
    checkTarget(allowedUri);
    const { createModels, createMethods } = req('@librechat/data-schemas');
    createModels(mongoose);
    const { getMessagesByCursor } = createMethods(mongoose);
    await mongoose.connect(allowedUri);
    const Message = mongoose.models.Message;
    for (const kind of ['unique', 'tied']) {
      const conversationId = `synthetic-${kind}`;
      const expected = Array.from({ length: 6 }, (_, i) => `${kind}-${i}`);
      const base = Date.parse('2026-01-01T00:00:00.000Z');
      const docs = expected.map((messageId, i) => ({
        messageId, conversationId, user: 'synthetic-owner',
        createdAt: new Date(base + (kind === 'unique' ? i : Math.max(0, i - 3)) * 1000),
        updatedAt: new Date(base), text: 'synthetic fixture', isCreatedByUser: false,
      }));
      await Message.collection.insertMany(docs);
      const filter = { conversationId, user: 'synthetic-owner' };
      const trial = { kind, expected, storedCount: await Message.collection.countDocuments(filter),
        fixture: docs.map(({ messageId, createdAt }) => ({ messageId, createdAt })), pages: [] };
      result.trials.push(trial);
      let cursor = null;
      const priorCursors = new Set();
      for (let i = 0; i < 10; i++) {
        const page = await getMessagesByCursor(filter, { sortField: 'createdAt', sortOrder: 1, limit: 2, cursor });
        trial.pages.push({ messages: page.messages.map((m) => ({ messageId: m.messageId, createdAt: m.createdAt })), nextCursor: page.nextCursor });
        if (page.nextCursor === null) { trial.termination = 'exhausted'; break; }
        if (priorCursors.has(page.nextCursor)) { trial.termination = 'repeated-cursor'; break; }
        priorCursors.add(page.nextCursor);
        cursor = page.nextCursor;
      }
      trial.termination ??= 'page-limit';
      const ids = trial.pages.flatMap((page) => page.messages.map((m) => m.messageId));
      trial.returnedCount = ids.length;
      trial.missing = expected.filter((id) => !ids.includes(id));
      trial.extra = ids.filter((id) => !expected.includes(id));
      trial.duplicates = ids.filter((id, i) => ids.indexOf(id) !== i);
      trial.completenessPassed = trial.missing.length === 0 && trial.extra.length === 0 &&
        trial.duplicates.length === 0 && trial.termination === 'exhausted';
    }
    const [control, tied] = result.trials;
    if (!control.completenessPassed || control.storedCount !== 6 || tied.storedCount !== 6 ||
        tied.returnedCount !== 4 || tied.missing.length !== 2 || tied.duplicates.length ||
        tied.extra.length || tied.termination !== 'exhausted') throw new Error('Predeclared characterization oracle did not match');
    result.harnessSucceeded = true;
  } catch (error) {
    result.error = { name: error.name, message: error.message, stack: error.stack };
    process.exitCode = 1;
  } finally {
    try { await mongoose.disconnect(); if (server) await server.stop(); result.cleanedUp = true; }
    catch (error) { result.cleanupError = error.message; result.harnessSucceeded = false; process.exitCode = 1; }
    mongoose.Connection.prototype.openUri = originalOpen;
    result.finishedAt = new Date().toISOString();
    fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  }
})();
