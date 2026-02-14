'use strict';
/**
 * Position Repository (repo/positionsRepo.js)
 * Manages position state using per-market Storage/KV keys.
 *
 * State machine:
 *   FLAT -> ENTRY_PENDING -> OPEN -> EXIT_PENDING -> FLAT
 *
 * Safety:
 * - transition() enforces expected fromState to prevent duplicate orders.
 */

class PositionsRepo {
  constructor(adapter) {
    this.adapter = adapter;
  }

  _getKey(market) {
    return `positions:${market}`;
  }

  async load(market) {
    const data = await this.adapter.storageGet(this._getKey(market));
    return data || { market, state: 'FLAT' };
  }

  async save(market, data) {
    await this.adapter.storageSet(this._getKey(market), data);
  }

  async listActiveMarkets() {
    const list = (await this.adapter.storageGet('active_markets')) || [];
    return Array.isArray(list) ? list : [];
  }

  async trackMarket(market) {
    const list = await this.listActiveMarkets();
    if (!list.includes(market)) {
      list.push(market);
      await this.adapter.storageSet('active_markets', list);
    }
  }

  /**
   * Transition only if current state matches fromState.
   * Returns {ok:boolean, pos?:object, reason?:string}
   */
  async transition(market, fromState, toState, extra = {}) {
    const pos = await this.load(market);

    if (pos.state !== fromState) {
      return { ok: false, reason: `STATE_MISMATCH:${pos.state}!=${fromState}` };
    }

    const next = {
      ...pos,
      ...extra,
      market,
      state: toState,
      lastActionTs: Date.now(),
    };

    await this.save(market, next);

    // Track any market that ever becomes non-FLAT (indexing)
    if (toState !== 'FLAT') {
      await this.trackMarket(market);
    } else {
      // Optional: keep it in active_markets; harmless and avoids needing delete.
      await this.trackMarket(market);
    }

    return { ok: true, pos: next };
  }

  /**
   * Ensure a FLAT position exists for market (idempotent).
   */
  async ensureFlat(market) {
    const pos = await this.load(market);
    if (pos.state === 'FLAT') return pos;
    const next = { market, state: 'FLAT', lastActionTs: Date.now() };
    await this.save(market, next);
    await this.trackMarket(market);
    return next;
  }
}

module.exports = PositionsRepo;
