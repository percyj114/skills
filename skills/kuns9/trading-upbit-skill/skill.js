#!/usr/bin/env node
'use strict';

require('dotenv').config();

/**
 * CLI Entrypoint (skill.js)
 * OpenClaw exec-only entry. Outputs exactly ONE JSON line.
 */

const { monitorOnce } = require('./handlers/monitorOnce');
const ExecutionAdapter = require('./adapters/execution');

function writeJson(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  const arg1 = args[1];

  const clawTools = global.tools || (typeof tools !== 'undefined' ? tools : null);

  try {
    if (command === 'help') {
      writeJson({
        ok: true,
        commands: ['monitor_once', 'price', 'holdings', 'assets', 'help'],
        description: 'OpenClaw Upbit Trading Bot (A-Plan)',
      });
      return;
    }

    if (!clawTools) {
      writeJson({
        ok: false,
        runId: null,
        errors: [{ code: 'NO_TOOLS', message: 'OpenClaw Tools not found in environment.' }],
      });
      process.exitCode = 1;
      return;
    }

    const adapter = new ExecutionAdapter(clawTools);

    if (command === 'monitor_once') {
      const result = await monitorOnce({ tools: clawTools });
      writeJson(result);
      process.exitCode = result.ok ? 0 : 1;
      return;
    }

    if (command === 'price') {
      const market = (arg1 || 'KRW-BTC').trim();
      const tickers = await adapter.getTickers([market]);
      const t = Array.isArray(tickers) ? tickers.find(x => x && x.market === market) : null;
      const price = t ? Number(t.trade_price) : NaN;

      if (!Number.isFinite(price)) {
        writeJson({
          ok: false,
          market,
          errors: [{ code: 'NO_PRICE', message: `No price available for ${market}` }],
        });
        process.exitCode = 1;
        return;
      }

      writeJson({ ok: true, market, price, ts: Date.now(), errors: [] });
      process.exitCode = 0;
      return;
    }

    if (command === 'holdings') {
      const accounts = await adapter.getAccounts();
      const list = Array.isArray(accounts) ? accounts : [];

      const holdings = list
        .map(a => {
          const currency = a?.currency;
          const balance = Number(a?.balance || 0);
          const locked = Number(a?.locked || 0);
          const total = balance + locked;
          const unit_currency = a?.unit_currency;
          const avg_buy_price = a?.avg_buy_price != null ? Number(a.avg_buy_price) : null;
          const market = (currency && currency !== 'KRW') ? `KRW-${currency}` : null;
          return { currency, balance, locked, total, avg_buy_price, unit_currency, market };
        })
        .filter(h => h.currency && h.currency !== 'KRW' && Number.isFinite(h.total) && h.total > 0);

      writeJson({ ok: true, ts: Date.now(), holdings, count: holdings.length, errors: [] });
      process.exitCode = 0;
      return;
    }

    if (command === 'assets') {
      const accounts = await adapter.getAccounts();
      const list = Array.isArray(accounts) ? accounts : [];

      let krw = 0;
      const coins = [];
      for (const a of list) {
        const currency = a?.currency;
        const balance = Number(a?.balance || 0);
        const locked = Number(a?.locked || 0);
        const total = balance + locked;
        if (!currency || !Number.isFinite(total) || total <= 0) continue;

        if (currency === 'KRW') {
          krw += total;
          continue;
        }

        coins.push({
          currency,
          total,
          avg_buy_price: a?.avg_buy_price != null ? Number(a.avg_buy_price) : null,
          market: `KRW-${currency}`,
        });
      }

      const markets = coins.map(c => c.market);
      const tickers = markets.length ? await adapter.getTickers(markets) : [];
      const priceMap = {};
      if (Array.isArray(tickers)) {
        for (const t of tickers) {
          if (t?.market) priceMap[t.market] = Number(t.trade_price);
        }
      }

      let coinsValueKrw = 0;
      const priced = [];
      const unpriced = [];

      for (const c of coins) {
        const p = priceMap[c.market];
        if (Number.isFinite(p)) {
          const v = c.total * p;
          coinsValueKrw += v;
          priced.push({ ...c, price: p, valueKrw: v });
        } else {
          unpriced.push({ ...c, reason: 'NO_KRW_MARKET_PRICE' });
        }
      }

      const totalKrw = krw + coinsValueKrw;

      writeJson({
        ok: true,
        ts: Date.now(),
        krw,
        coinsValueKrw,
        totalKrw,
        priced,
        unpriced,
        errors: [],
      });
      process.exitCode = 0;
      return;
    }

    writeJson({
      ok: false,
      errors: [{ code: 'UNKNOWN_COMMAND', message: `Command '${command}' not found.` }],
    });
    process.exitCode = 1;
    return;
  } catch (err) {
    writeJson({
      ok: false,
      runId: null,
      errors: [{ code: 'RUNTIME_ERROR', message: err?.message || String(err) }],
    });
    process.exitCode = 1;
  }
}

main();
