'use strict';
/**
 * Monitor Once Handler (handlers/monitorOnce.js)
 * Executes a single trading cycle (A-Plan).
 *
 * Requirements:
 * - No loops outside this single run (no setTimeout, no infinite loops)
 * - No fs
 * - JSON-only output handled by skill.js
 * - Strategy logic must remain unchanged (only I/O mapping)
 */

const ExecutionAdapter = require('../adapters/execution');
const PositionsRepo = require('../repo/positionsRepo');
const OrderService = require('../services/orderService');
const RiskManager = require('../domain/riskManager');
const strategies = require('../domain/strategies');
const { createLogBuffer } = require('../utils/log');

const { parseConfig } = require('../utils/time');

function isValidLock(lock, nowMs) {
  if (!lock || typeof lock !== 'object') return false;
  const ts = Number(lock.ts);
  const ttlSec = Number(lock.ttlSec);
  if (!Number.isFinite(ts) || !Number.isFinite(ttlSec)) return false;
  return nowMs < ts + ttlSec * 1000;
}

async function acquireLock(adapter, runId, ttlSec) {
  const lockKey = 'lock:monitor_once';
  const nowMs = Date.now();

  const existing = await adapter.storageGet(lockKey);
  if (isValidLock(existing, nowMs)) return { ok: false, lockKey, existing };

  await adapter.storageSet(lockKey, { runId, ts: nowMs, ttlSec });
  return { ok: true, lockKey };
}

async function monitorOnce(context) {
  const runId = `run_${Date.now()}`;
  const log = createLogBuffer();

  let CONFIG;
  try {
    CONFIG = parseConfig(process.env);
  } catch (e) {
    return { ok: false, runId, actions: [], errors: [{ code: 'CONFIG_ERROR', message: e?.message || String(e) }], logs: [] };
  }

  const adapter = new ExecutionAdapter(context.tools);
  const repo = new PositionsRepo(adapter);
  const orderService = new OrderService(adapter);
  const riskManager = new RiskManager(adapter);

  const actions = [];
  const errors = [];

  // STEP 0 — Lock
  const lock = await acquireLock(adapter, runId, CONFIG.LOCK_TTL_SEC);
  if (!lock.ok) {
    return {
      ok: true,
      runId,
      actions: [{ type: 'SKIP', reason: 'LOCK_ACTIVE' }],
      errors: [],
      logs: []
    };
  }

  try {
    // STEP 2 — Load Open Positions (active markets list + filter)
    const activeMarkets = await repo.listActiveMarkets();
    const scanSet = [...new Set([...CONFIG.WATCHLIST, ...activeMarkets])];

    // STEP 3 — Fetch Tickers (batch)
    const priceData = scanSet.length ? await adapter.getTickers(scanSet) : [];
    const priceMap = {};
    if (Array.isArray(priceData)) {
      priceData.forEach(p => {
        if (p && p.market) priceMap[p.market] = Number(p.trade_price);
      });
    } else if (priceData && typeof priceData === 'object') {
      Object.keys(priceData).forEach(m => priceMap[m] = Number(priceData[m].trade_price ?? priceData[m]));
    }

    // STEP 4 — SELL CHECK (for OPEN positions)
    for (const market of activeMarkets) {
      const pos = await repo.load(market);
      if (pos.state !== 'OPEN') continue;

      const currentPrice = priceMap[market];
      if (!Number.isFinite(currentPrice)) {
        errors.push({ code: 'NO_PRICE', market, message: `No price for ${market}` });
        continue;
      }

      const pnl = (currentPrice - pos.entryPrice) / pos.entryPrice;

      if (pnl >= CONFIG.TARGET_PROFIT || pnl <= CONFIG.STOP_LOSS) {
        const reason = pnl >= CONFIG.TARGET_PROFIT ? 'TARGET_HIT' : 'STOPLOSS_HIT';
        log.info(`Signal: SELL ${market}`, { pnl, reason });

        // Transition: OPEN -> EXIT_PENDING
        const t = await repo.transition(market, 'OPEN', 'EXIT_PENDING', { exitReason: reason });
        if (!t.ok) {
          log.warn(`Skip: State mismatch for ${market}`, { currentState: t.reason });
          continue;
        }

        try {
          const sellResult = await orderService.marketSell(market, pos.qty);
          await repo.transition(market, 'EXIT_PENDING', 'FLAT', {
            lastOrder: sellResult?.uuid ?? null,
            exitReason: reason,
          });

          actions.push({
            type: 'SELL',
            market,
            reason,
            pnl,
            result: 'SUCCESS',
          });
        } catch (err) {
          errors.push({ code: 'SELL_FAILED', market, message: err?.message || String(err) });
          await repo.transition(market, 'EXIT_PENDING', 'OPEN', { exitReason: null });
        }
      }
    }

    // STEP 5 — BUY SCAN (WATCHLIST only)
    let buyCount = 0;

    for (const market of CONFIG.WATCHLIST) {
      if (buyCount >= CONFIG.MAX_BUYS_PER_RUN) break;

      const pos = await repo.load(market);
      if (pos.state !== 'FLAT') continue; // Skip quiet

      // Cooldown check
      const cooldown = await adapter.storageGet(`cooldown:${market}`);
      if (cooldown && typeof cooldown.untilTs === 'number' && Date.now() < cooldown.untilTs) continue;

      // Evaluate Breakout
      const dayCandles = await adapter.getCandles({ unit: 'days', market, count: 2 });
      if (!Array.isArray(dayCandles) || dayCandles.length < 2) continue;

      const prevRange = Number(dayCandles[1].high_price) - Number(dayCandles[1].low_price);
      const currentCandle = {
        opening: Number(dayCandles[0].opening_price),
        price: Number(priceMap[market]),
      };

      if (!Number.isFinite(currentCandle.opening) || !Number.isFinite(currentCandle.price) || !Number.isFinite(prevRange)) continue;

      const strategyResult = strategies.volatilityBreakout(currentCandle, prevRange, CONFIG.K_VALUE);

      if (strategyResult.signal === 'BUY') {
        const minuteCandles = await adapter.getCandles({ unit: 'minutes', subUnit: 60, market, count: 1 });
        if (Array.isArray(minuteCandles) && minuteCandles.length > 0 &&
          Number(minuteCandles[0].trade_price) > Number(minuteCandles[0].opening_price)) {

          log.info(`Signal: BUY ${market} breakout detected`);

          const risk = await riskManager.checkBuyFeasibility(market, CONFIG.BUDGET_KRW);
          if (!risk.allow) {
            actions.push({ type: 'BUY_SKIP', market, reason: 'RISK_BLOCK', detail: risk.reason });
            continue;
          }

          const t = await repo.transition(market, 'FLAT', 'ENTRY_PENDING');
          if (!t.ok) continue;

          try {
            const buyResult = await orderService.marketBuy(market, CONFIG.BUDGET_KRW);
            const orderDetail = await adapter.getOrder(buyResult.uuid);

            await repo.transition(market, 'ENTRY_PENDING', 'OPEN', {
              qty: orderDetail.executed_volume,
              entryPrice: orderDetail.avg_buy_price,
              entryTs: Date.now(),
            });

            await adapter.storageSet(`cooldown:${market}`, {
              untilTs: Date.now() + (CONFIG.BUY_COOLDOWN_SEC * 1000),
              reason: 'RECENT_BUY',
            });

            actions.push({ type: 'BUY', market, result: 'SUCCESS' });
            buyCount += 1;
          } catch (err) {
            errors.push({ code: 'BUY_FAILED', market, message: err?.message || String(err) });
            await repo.transition(market, 'ENTRY_PENDING', 'FLAT');
          }
        }
      }
    }

    await adapter.storageSet('last_run:monitor_once', {
      runId,
      ts: Date.now(),
      ok: errors.length === 0,
      actionsCount: actions.length,
      errorsCount: errors.length,
    });

    return { ok: errors.length === 0, runId, actions, errors, logs: log.entries };
  } catch (err) {
    return {
      ok: false,
      runId,
      actions,
      errors: [...errors, { code: 'GLOBAL_ERROR', message: err?.message || String(err) }],
      logs: log.entries
    };
  }
}

module.exports = { monitorOnce };
