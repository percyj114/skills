---
name: Upbit Trading Bot (A-Plan)
description: Cron-driven, single-run automated trading engine for Upbit, optimized for OpenClaw.
version: 3.2.0
author: sgyeo
metadata:
  openclaw:
    runtime: nodejs
    entry: skill.js
    scheduler:
      cron: "*/5 * * * *"
      command: "node skill.js monitor_once"
---

# Upbit Trading Bot (A-Plan)

A high-reliability automated trading SKILL designed for the OpenClaw environment. It operates using a **single-run execution model (A-Plan)**, where each execution performs a full market scan and trade cycle before exiting.

---

# 1. Overview

This SKILL provides:
- **Single-Run Orchestration**: Triggered by cron every 5 minutes.
- **Volatility Breakout Strategy**: Identifies entries based on daily range breakouts.
- **State-Aware Execution**: Manages positions using isolated Storage/KV keys to prevent duplicates.
- **Safety Locks**: Distributed locking prevents overlapping cron runs.
- **Strict JSON Output**: Emits a single line of JSON for seamless logging and monitoring.

This SKILL also includes exec-only **query commands** so OpenClaw can answer user questions:
- Price: `node skill.js price KRW-BTC`
- Holdings: `node skill.js holdings`
- Assets (KRW valuation): `node skill.js assets`

---

# 2. Execution Flow (monitor_once)

When `node skill.js monitor_once` is executed:

1.  **Concurrency Check**: Checks for `lock:monitor_once` in Storage. Exits if a valid lock (TTL active) exists.
2.  **Sell Evaluation**:
    - Loads all `OPEN` positions from Storage.
    - Fetches current prices via OpenClaw `getTickers`.
    - Calculates PnL. If `PnL >= TARGET_PROFIT` or `PnL <= STOP_LOSS`, executes market sell.
3.  **Buy Scanning**:
    - Iterates through the `WATCHLIST`.
    - Fetches daily and hourly candles via OpenClaw `getCandles`.
    - Validates **Volatility Breakout** (Breakout > Target) and **Bullish Filter** (Current > Hour Open).
4.  **Buy Execution**:
    - Performs risk check (Balance vs. Budget).
    - Places market buy order via OpenClaw `placeOrder`.
    - Updates position state to `OPEN`.
5.  **Termination**: Prints execution summary (including diagnostic logs) as a single JSON line and exits.

---

# 3. Storage / KV Schema

| Key | Format | Purpose |
| :--- | :--- | :--- |
| `lock:monitor_once` | `JSON` | Concurrency lock with `runId` and `ts`. |
| `positions:<market>`| `JSON` | Active state (`OPEN`, `FLAT`), entry price, and quantity. |
| `cooldown:<market>` | `JSON` | Timestamp to prevent rapid re-entry after a buy. |
| `active_markets`    | `Array`| List of all markets that have ever been traded. |

---

# 4. Strategy Logic

### Entry Conditions (Both must be TRUE)
1. **Breakout**: `price > (today_open + (yesterday_high - yesterday_low) * K_VALUE)`
2. **Bullish Hour**: `current_price > hour_opening_price`

### Exit Conditions (Either must be TRUE)
1. **Profit Take**: `PnL >= TARGET_PROFIT` (Default: 0.05 / 5%)
2. **Stop Loss**: `PnL <= STOP_LOSS` (Default: -0.05 / -5%)

---

# 5. Environment Variables

Configure the bot using the following environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `WATCHLIST` | `KRW-BTC,KRW-ETH,KRW-SOL` | Comma-separated market symbols. |
| `TARGET_PROFIT` | `0.05` | Profit target ratio. |
| `STOP_LOSS` | `-0.05` | Stop loss ratio. |
| `K_VALUE` | `0.5` | Volatility factor for breakout. |
| `BUDGET_KRW` | `10000` | KRW amount per buy order. |
| `BUY_COOLDOWN_SEC` | `1800` | Prevention time before re-buying same market. |
| `LOCK_TTL_SEC` | `120` | Max duration for a single run lock. |

---

# 6. JSON Output Specification

On completion, the bot outputs a single line:

```json
{
  "ok": true,
  "runId": "run_1707920000000",
  "actions": [
    { "type": "BUY", "market": "KRW-BTC", "result": "SUCCESS" }
  ],
  "errors": [],
  "logs": [
    { "level": "INFO", "message": "Signal: BUY KRW-BTC breakout detected" }
  ],
  "timestamp": "2026-02-14T23:30:00Z"
}
```

---

# 7. Directory Structure

```
skill.js                # CLI Entrypoint & Runner
handlers/
  monitorOnce.js        # Main A-Plan Orchestrator
repo/
  positionsRepo.js      # Storage/KV Abstraction
domain/
  strategies.js         # Strategy Math (Pure)
  riskManager.js        # Balance & Order Validation
adapters/
  execution.js          # OpenClaw Tool Interface
services/
  orderService.js       # Trade Execution logic
utils/
  log.js                # In-memory log buffer (NO stdout)
  time.js               # Time & Config Utilities
```
