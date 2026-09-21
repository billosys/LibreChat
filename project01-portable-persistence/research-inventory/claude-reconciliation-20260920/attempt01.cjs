/* Read-only reconciliation. Does not import the application or register models. */
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const { createHash } = require('node:crypto');
const { execFileSync } = require('node:child_process');
const assert = require('node:assert/strict');
const repo = '/Users/oubiwann/lab/billosys/LibreChat';
const sourcePath = '/Users/oubiwann/lab/oxur/ixy/workbench/conversations.json';
const outputDir = process.argv[2];
assert(outputDir, 'Supply a local evidence output directory');
const req = createRequire(path.join(repo, 'package.json'));
const { MongoClient } = req('mongodb');
const dotenv = req('dotenv');
const NO_PARENT = '00000000-0000-0000-0000-000000000000';
const sha = (value) => createHash('sha256').update(value).digest('hex');
function canonical(value) {
  if (value instanceof Date) return value.toISOString();
  if (value && typeof value.toHexString === 'function') return value.toHexString();
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  }
  return value;
}
const encoded = (value) => JSON.stringify(canonical(value));
const equal = (a, b) => encoded(a) === encoded(b);
const fingerprint = (value) => sha(encoded(value));
const present = (o, key) => Object.hasOwn(o, key);
const increment = (o, key, n = 1) => { o[key] = (o[key] || 0) + n; };
const counts = {};
const sourceBytes = fs.readFileSync(sourcePath);
const sourceHash = sha(sourceBytes);
assert.equal(sourceHash, '558271556db71c662d0a8708769cf5d0acd113cf83b49ce9e8b4d985a6392fed', 'Source baseline changed');
const source = JSON.parse(sourceBytes);
assert(Array.isArray(source));
const omissions = { contentBlocks: {}, skippedContentBlocks: {}, retainedContentBlocks: {}, skippedReasons: {} };
const skippedLocators = [];
const sourceMessageIds = new Set();
const sourceConversationIds = new Set();
const sourceShape = { conversationFields: {}, messageFields: {}, senderValues: {} };
const projection = source.map((conversation, ci) => {
  assert(Array.isArray(conversation.chat_messages), `Invalid messages at conversation ${ci}`);
  for (const key of Object.keys(conversation)) increment(sourceShape.conversationFields, key);
  sourceConversationIds.add(conversation.uuid);
  const created = new Date(conversation.created_at);
  assert(Number.isFinite(created.getTime()), `Missing/invalid conversation date at ${ci}`);
  const messages = [];
  let lastMs = null;
  for (const [mi, message] of conversation.chat_messages.entries()) {
    increment(counts, 'sourceMessages');
    sourceMessageIds.add(message.uuid);
    for (const key of Object.keys(message)) increment(sourceShape.messageFields, key);
    increment(sourceShape.senderValues, message.sender);
    assert(message.content === undefined || Array.isArray(message.content), `Invalid content at ${ci}/${mi}`);
    let text = '';
    let thinking = '';
    for (const part of message.content || []) {
      increment(omissions.contentBlocks, part.type);
      if (part.type === 'text' && part.text) { assert.equal(typeof part.text, 'string'); text += part.text; }
      if (part.type === 'thinking' && part.thinking) { assert.equal(typeof part.thinking, 'string'); thinking += part.thinking; }
    }
    if (!text && message.text) { assert.equal(typeof message.text, 'string'); text = message.text; increment(counts, 'textFallbacks'); }
    const skipped = !text && !thinking;
    for (const part of message.content || []) increment(skipped ? omissions.skippedContentBlocks : omissions.retainedContentBlocks, part.type);
    const hasAttachments = Array.isArray(message.attachments) && message.attachments.length > 0;
    const hasFiles = Array.isArray(message.files) && message.files.length > 0;
    if (hasAttachments) increment(counts, 'sourceMessagesWithAttachments');
    if (hasFiles) increment(counts, 'sourceMessagesWithFiles');
    if (skipped) {
      increment(counts, 'predictedSkippedMessages');
      if (hasAttachments) increment(counts, 'skippedMessagesWithAttachments');
      if (hasFiles) increment(counts, 'skippedMessagesWithFiles');
      const types = [...new Set((message.content || []).map((p) => p.type))].sort().join('+') || 'no_content_blocks';
      increment(omissions.skippedReasons, types);
      skippedLocators.push({ sourceConversationIndex: ci, sourceMessageIndex: mi, contentTypes: types, hasAttachments, hasFiles });
      continue;
    }
    const human = message.sender === 'human';
    const sourceTime = message.created_at || conversation.created_at;
    const date = new Date(sourceTime);
    let ms = date.getTime();
    assert(Number.isFinite(ms), `Invalid retained message date at ${ci}/${mi}`);
    if (!message.created_at) increment(counts, 'messageDateFallbacks');
    if (/\.\d{3}[1-9]\d*Z$|\.\d{4}[1-9]\d*Z$|\.\d{5}[1-9]\d*Z$/.test(sourceTime)) increment(counts, 'retainedMessageSubmillisecondPrecisionLost');
    if (lastMs !== null && ms <= lastMs) { ms = lastMs + 1; increment(counts, 'messageTimestampBumps'); }
    lastMs = ms;
    if (thinking) increment(counts, human ? 'humanThinkingMessages' : 'assistantThinkingMessages');
    messages.push({
      sourceMessageIndex: mi,
      text, sender: human ? 'user' : 'Claude', isCreatedByUser: human,
      createdAt: new Date(ms),
      content: thinking && !human ? [{ type: 'think', think: thinking }, { type: 'text', text }] : undefined,
      hasAttachments, hasFiles,
    });
  }
  return { sourceIndex: ci, title: conversation.name || 'Imported Claude Chat', createdAt: created, messages };
});
counts.sourceConversations = projection.length;
counts.expectedRetainedMessages = projection.reduce((n, c) => n + c.messages.length, 0);

function messageDifferences(expected, stored, parentId, scope) {
  const checks = {
    text: stored.text === expected.text,
    content: equal(stored.content, expected.content),
    createdAt: stored.createdAt instanceof Date && stored.createdAt.getTime() === expected.createdAt.getTime(),
    sender: stored.sender === expected.sender,
    isCreatedByUser: stored.isCreatedByUser === expected.isCreatedByUser,
    isUserSubmitted: stored.isUserSubmitted === true,
    parentMessageId: stored.parentMessageId === parentId,
    endpoint: stored.endpoint === 'anthropic',
    scope: equal([stored.user, stored.tenantId], scope),
    unfinished: stored.unfinished === false,
    isEdited: stored.isEdited === false,
    error: stored.error === false,
  };
  return Object.entries(checks).filter(([, result]) => !result).map(([name]) => name);
}

const environment = fs.existsSync(path.join(repo, '.env')) ? dotenv.parse(fs.readFileSync(path.join(repo, '.env'))) : {};
const uri = process.env.MONGO_URI || environment.MONGO_URI;
assert(uri && /^mongodb:\/\/(?:[^@/]+@)?(?:127\.0\.0\.1|localhost|\[::1\])(?::\d+)?\//.test(uri), 'Refusing nonlocal/unspecified database');
const client = new MongoClient(uri, { maxPoolSize: 1, serverSelectionTimeoutMS: 4000, appName: 'guildhall-readonly-reconciliation', monitorCommands: true });
const commands = {};
client.on('commandStarted', ({ commandName }) => { increment(commands, commandName); });
async function readRows(db, name) {
  return db.collection(name).find({}, { maxTimeMS: 30000 }).sort({ _id: 1 }).toArray();
}
(async () => {
  try {
    await client.connect();
    const db = client.db();
    const began = new Date().toISOString();
    const conversations = await readRows(db, 'conversations');
    const messages = await readRows(db, 'messages');
    const initialDigest = { conversations: fingerprint(conversations), messages: fingerprint(messages) };
    counts.storedConversations = conversations.length;
    counts.storedMessages = messages.length;
    const scopes = new Set([...conversations, ...messages].map((row) => encoded([row.user, row.tenantId])));
    assert.equal(scopes.size, 1, 'Multiple scopes: explicit owner selection required');
    assert([...conversations, ...messages].every((row) => row.endpoint === 'anthropic'), 'Non-Anthropic rows: establish batch selection first');
    const scope = JSON.parse([...scopes][0]);
    const scopeAlias = fingerprint(scope).slice(0, 16);
    const key = (row) => encoded([row.title, row.createdAt]);
    const indexedConversations = new Map();
    for (const c of conversations) {
      const k = key(c);
      if (!indexedConversations.has(k)) indexedConversations.set(k, []);
      indexedConversations.get(k).push(c);
    }
    const sourceKeys = new Map();
    for (const c of projection) incrementKey(sourceKeys, key(c));
    function incrementKey(map, k) { map.set(k, (map.get(k) || 0) + 1); }
    const byConversation = new Map();
    for (const m of messages) {
      if (!byConversation.has(m.conversationId)) byConversation.set(m.conversationId, []);
      byConversation.get(m.conversationId).push(m);
    }
    for (const rows of byConversation.values()) rows.sort((a, b) => a.createdAt - b.createdAt || String(a._id).localeCompare(String(b._id)));
    const mismatches = [];
    const matchedConversationIds = new Set();
    const matchedMessageIds = new Set();
    const matchedStoredObjectIds = new Set();
    const pairings = [];
    const fieldsFailed = {};
    const modelCounts = {};
    const storageShape = { conversationFields: {}, messageFields: {} };
    let negativeControls = null;
    for (const c of conversations) {
      increment(modelCounts, c.model === undefined ? '<absent>' : String(c.model));
      for (const field of Object.keys(c)) increment(storageShape.conversationFields, field);
      if (sourceConversationIds.has(c.conversationId)) increment(counts, 'storedConversationIdsEqualSourceIds');
    }
    for (const m of messages) {
      for (const field of Object.keys(m)) increment(storageShape.messageFields, field);
      if (sourceMessageIds.has(m.messageId)) increment(counts, 'storedMessageIdsEqualSourceIds');
      if (Array.isArray(m.attachments) && m.attachments.length) increment(counts, 'storedMessagesWithAttachments');
      if (Array.isArray(m.files) && m.files.length) increment(counts, 'storedMessagesWithFiles');
      for (const part of m.content || []) increment(counts, `storedContentType:${part.type}`);
    }
    for (const expected of projection) {
      const candidates = indexedConversations.get(key(expected)) || [];
      if (candidates.length !== 1 || sourceKeys.get(key(expected)) !== 1) {
        mismatches.push({ sourceConversationIndex: expected.sourceIndex, kind: 'conversation_pairing', candidateCount: candidates.length, sourceKeyCount: sourceKeys.get(key(expected)) });
        continue;
      }
      const stored = candidates[0];
      assert(!matchedConversationIds.has(stored.conversationId), 'Duplicate selected conversation identity');
      matchedConversationIds.add(stored.conversationId);
      increment(counts, 'pairedConversations');
      const rows = byConversation.get(stored.conversationId) || [];
      if (rows.length !== expected.messages.length) mismatches.push({ sourceConversationIndex: expected.sourceIndex, kind: 'message_count', expected: expected.messages.length, actual: rows.length });
      if (!equal(stored.updatedAt, expected.createdAt)) mismatches.push({ sourceConversationIndex: expected.sourceIndex, kind: 'conversation_updatedAt' });
      if (!equal([stored.user, stored.tenantId], scope)) mismatches.push({ sourceConversationIndex: expected.sourceIndex, kind: 'conversation_scope' });
      if (Array.isArray(stored.messages) && stored.messages.length === 0) increment(counts, 'conversationEmbeddedMessageListEmpty');
      pairings.push({ sourceConversationIndex: expected.sourceIndex, sourceConversationIdHash: fingerprint(source[expected.sourceIndex].uuid), storedConversationIdHash: fingerprint(stored.conversationId), messageCount: rows.length });
      for (const [i, e] of expected.messages.entries()) {
        const actual = rows[i];
        if (!actual) continue;
        const parentId = i === 0 ? NO_PARENT : rows[i - 1].messageId;
        const failed = messageDifferences(e, actual, parentId, scope);
        increment(counts, 'comparedMessages');
        if (failed.length) {
          mismatches.push({ sourceConversationIndex: expected.sourceIndex, sourceMessageIndex: e.sourceMessageIndex, kind: 'message_fields', failed });
          for (const f of failed) increment(fieldsFailed, f);
        } else increment(counts, 'matchingMessages');
        if (matchedMessageIds.has(actual.messageId)) increment(counts, 'duplicateStoredMessageIds');
        matchedMessageIds.add(actual.messageId);
        matchedStoredObjectIds.add(String(actual._id));
        if (!negativeControls) {
          const mutations = {
            text: { text: `${actual.text}X` },
            content: { content: [{ type: 'text', text: 'counterexample' }] },
            createdAt: { createdAt: new Date(actual.createdAt.getTime() + 1) },
            sender: { sender: 'counterexample' },
            isCreatedByUser: { isCreatedByUser: !actual.isCreatedByUser },
            isUserSubmitted: { isUserSubmitted: false },
            parentMessageId: { parentMessageId: 'counterexample' },
            endpoint: { endpoint: 'counterexample' },
            scope: { user: 'counterexample' },
            unfinished: { unfinished: true }, isEdited: { isEdited: true }, error: { error: true },
          };
          negativeControls = Object.fromEntries(Object.entries(mutations).map(([field, patch]) => [field, messageDifferences(e, { ...actual, ...patch }, parentId, scope).includes(field)]));
          assert(Object.values(negativeControls).every(Boolean), 'Comparator negative control failed');
        }
      }
    }
    counts.unpairedStoredConversations = conversations.filter((c) => !matchedConversationIds.has(c.conversationId)).length;
    counts.uncomparedStoredMessages = messages.filter((m) => !matchedStoredObjectIds.has(String(m._id))).length;
    counts.sourceMessagesAccountedFor = (counts.comparedMessages || 0) + (counts.predictedSkippedMessages || 0);
    counts.storedOrphanMessages = messages.filter((m) => !conversations.some((c) => c.conversationId === m.conversationId)).length;
    const finalConversations = await readRows(db, 'conversations');
    const finalMessages = await readRows(db, 'messages');
    const finalDigest = { conversations: fingerprint(finalConversations), messages: fingerprint(finalMessages) };
    const stable = equal(initialDigest, finalDigest);
    const sourceStable = sha(fs.readFileSync(sourcePath)) === sourceHash;
    const report = {
      protocol: 'Claude-to-current-importer projection comparison; no claim of raw-source losslessness',
      sourcePath, sourceSha256: sourceHash,
      sourceCommit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: repo, encoding: 'utf8' }).trim(),
      database: db.databaseName, scopeAlias, began, ended: new Date().toISOString(),
      sourceUnchangedDuringRun: sourceStable, repeatedCollectionReadsIdentical: stable,
      initialDigest, finalDigest, counts, omissions, sourceShape, storageShape,
      conversationModels: modelCounts, mismatchCount: mismatches.length, fieldsFailed,
      negativeControls, commands,
      outcome: stable && sourceStable && mismatches.length === 0 && counts.unpairedStoredConversations === 0 && counts.uncomparedStoredMessages === 0 && counts.sourceMessagesAccountedFor === counts.sourceMessages ? 'matches_current_import_projection' : 'requires_investigation',
    };
    fs.mkdirSync(outputDir, { recursive: true });
    for (const [name, value] of Object.entries({ 'summary.json': report, 'mismatches.json': mismatches, 'skipped-source-locators.json': skippedLocators, 'conversation-pairings.json': pairings })) {
      fs.writeFileSync(path.join(outputDir, name), `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
    }
    console.log(JSON.stringify(report, null, 2));
    if (!stable || !sourceStable) process.exitCode = 2;
  } finally { await client.close(); }
})().catch((error) => {
  console.error(JSON.stringify({ errorType: error.name, code: error.code || null, assertion: error.code === 'ERR_ASSERTION' ? error.message : undefined }));
  process.exitCode = 1;
});
