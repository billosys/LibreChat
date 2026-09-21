const fs = require('node:fs');
const { createRequire } = require('node:module');
const { createHash } = require('node:crypto');
const req = createRequire('/Users/oubiwann/lab/billosys/LibreChat/package.json');
const { MongoClient } = req('mongodb');
const dotenv = req('dotenv');
const envPath = '/Users/oubiwann/lab/billosys/LibreChat/.env';
const parsed = fs.existsSync(envPath) ? dotenv.parse(fs.readFileSync(envPath)) : {};
const uri = process.env.MONGO_URI || parsed.MONGO_URI;
if (!uri || !/^mongodb:\/\/(?:[^@/]+@)?(?:127\.0\.0\.1|localhost|\[::1\])(?::\d+)?\//.test(uri)) {
  throw new Error('Expected an explicit local Mongo URI; refusing to guess or connect remotely.');
}
const client = new MongoClient(uri, { serverSelectionTimeoutMS: 4000, maxPoolSize: 1, appName: 'guildhall-readonly-reconciliation', monitorCommands: true });
const commands = {};
client.on('commandStarted', ({ commandName }) => { commands[commandName] = (commands[commandName] || 0) + 1; });
const alias = (value) => createHash('sha256').update(JSON.stringify(value)).digest('hex').slice(0, 16);
(async () => {
  try {
    await client.connect();
    const db = client.db();
    const report = { database: db.databaseName, at: new Date().toISOString(), collections: {} };
    for (const name of ['conversations', 'messages']) {
      const rows = await db.collection(name).aggregate([
        { $group: { _id: { user: '$user', tenantId: '$tenantId', endpoint: '$endpoint' }, count: { $sum: 1 } } },
      ], { maxTimeMS: 15000 }).toArray();
      report.collections[name] = rows.map((r) => ({ scopeAlias: alias([r._id.user, r._id.tenantId]), endpoint: r._id.endpoint, count: r.count }));
    }
    report.commands = commands;
    console.log(JSON.stringify(report, null, 2));
  } finally { await client.close(); }
})().catch((error) => { console.error(JSON.stringify({ errorType: error.name, code: error.code || null })); process.exitCode = 1; });
