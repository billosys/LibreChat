'use strict';

// Investigation prototype only. resolveScope is the actual tenant policy in the harness.
function beginTurnWrite(raw, initialContext, resolveScope, options = {}) {
  const key = (ctx) => JSON.stringify([ctx.userId, resolveScope('turn-write')]);
  const initialKey = key(initialContext);
  let state = 'fresh';
  let released = false;
  let locator;
  const discard = () => { locator = undefined; };
  function check(expected, ctx) {
    if (released || state !== expected) throw new Error(`Invalid turn-write state: ${state}`);
    try {
      if (!options.unsafeScope && key(ctx) !== initialKey) throw new Error('Turn-write scope changed');
    } catch (error) {
      released = true; state = 'released'; discard(); throw error;
    }
  }
  return {
    async saveMessage(ctx, fields, metadata) {
      check('fresh', ctx);
      state = 'saving';
      try {
        const row = await raw.saveMessage(ctx, fields, metadata);
        if (!released) {
          locator = row?._id;
          if (options.sharedSlot) options.sharedSlot.locator = locator;
          state = 'saved';
        }
        if (row == null) return row;
        const { _id, ...dto } = row;
        return dto;
      } catch (error) {
        state = released ? 'released' : 'failed'; discard(); throw error;
      }
    },
    async saveConvo(ctx, fields, metadata) {
      check('saved', ctx);
      if (Object.hasOwn(metadata ?? {}, 'appendMessageIds')) throw new Error('Physical linkage is private');
      state = 'linking';
      try {
        // Fault injection only; normal candidate never consults a shared slot or resolver.
        const id = options.sharedSlot ? options.sharedSlot.locator : locator;
        const target = options.reResolve ? await options.reResolve() : id;
        return await raw.saveConvo(ctx, fields, {
          ...metadata,
          ...(target != null ? { appendMessageIds: [target] } : {}),
        });
      } finally {
        state = released ? 'released' : 'settled'; discard();
      }
    },
    release() { released = true; state = 'released'; discard(); },
    inspectForTest() { return { state, released, retainsLocator: locator != null }; },
  };
}

module.exports = { beginTurnWrite };
