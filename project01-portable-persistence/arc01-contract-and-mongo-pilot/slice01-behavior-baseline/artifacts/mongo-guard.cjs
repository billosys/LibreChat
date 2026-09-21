const mongoose = require('/Users/oubiwann/lab/billosys/LibreChat/node_modules/mongoose');
function validate(uri) {
  const url = new URL(uri);
  if (url.protocol !== 'mongodb:' || url.hostname !== '127.0.0.1' || !url.port || Number(url.port) < 1024 || url.port === '27017') {
    throw new Error('Slice01 guard refused a non-disposable Mongo target');
  }
  return url.port;
}
// Negative control checks the guard without attempting a connection.
let rejected = false;
try { validate('mongodb://127.0.0.1:27017/dummy-uri'); } catch { rejected = true; }
if (!rejected) throw new Error('Slice01 guard negative control failed');
const original = mongoose.Connection.prototype.openUri;
mongoose.Connection.prototype.openUri = function(uri, ...args) {
  const port = validate(uri);
  console.log(`[Slice01 isolation] Mongo connection allowed on loopback port ${port}; default port negative control passed`);
  return original.call(this, uri, ...args);
};
