'use strict';
/**
 * Time & Config Utilities (utils/time.js)
 * - Parses .env via process.env (dotenv loaded in skill.js)
 * - Validates configuration
 */

function nowStamp(ms) {
  const d = new Date(ms);
  const pad = (n) => String(n).padStart(2, '0');
  return (
    d.getFullYear() +
    pad(d.getMonth() + 1) +
    pad(d.getDate()) +
    '-' +
    pad(d.getHours()) +
    pad(d.getMinutes()) +
    pad(d.getSeconds())
  );
}

function parseWatchlist(raw) {
  if (!raw) return [];
  return raw
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function mustNumber(name, raw, fallback) {
  const v = raw == null || raw === '' ? Number(fallback) : Number(raw);
  if (!Number.isFinite(v)) throw new Error(`Invalid number for ${name}: ${raw}`);
  return v;
}

function mustInt(name, raw, fallback) {
  const v = raw == null || raw === '' ? parseInt(String(fallback), 10) : parseInt(String(raw), 10);
  if (!Number.isFinite(v)) throw new Error(`Invalid int for ${name}: ${raw}`);
  return v;
}

function validateWatchlist(list) {
  if (!Array.isArray(list) || list.length === 0) {
    throw new Error('WATCHLIST is empty. Set WATCHLIST in .env (e.g., WATCHLIST=KRW-BTC,KRW-ETH)');
  }
  for (const m of list) {
    if (typeof m !== 'string' || !m.startsWith('KRW-')) {
      throw new Error(`Invalid WATCHLIST market: ${m}. Expected format like KRW-BTC`);
    }
  }
}

function parseConfig(env) {
  const WATCHLIST = parseWatchlist(env.WATCHLIST);
  validateWatchlist(WATCHLIST);

  return {
    WATCHLIST,
    TARGET_PROFIT: mustNumber('TARGET_PROFIT', env.TARGET_PROFIT, 0.05),
    STOP_LOSS: mustNumber('STOP_LOSS', env.STOP_LOSS, -0.05),
    K_VALUE: mustNumber('K_VALUE', env.K_VALUE, 0.5),
    BUY_COOLDOWN_SEC: mustInt('BUY_COOLDOWN_SEC', env.BUY_COOLDOWN_SEC, 1800),
    MAX_BUYS_PER_RUN: mustInt('MAX_BUYS_PER_RUN', env.MAX_BUYS_PER_RUN, 1),
    LOCK_TTL_SEC: mustInt('LOCK_TTL_SEC', env.LOCK_TTL_SEC, 120),

    // Existing sizing; can be overridden
    BUDGET_KRW: mustInt('BUDGET_KRW', env.BUDGET_KRW, 10000),

    nowStamp,
  };
}

module.exports = { parseConfig, nowStamp, parseWatchlist };
