---
name: asrai
description: Crypto market analysis using Asrai API. Covers technical analysis, screeners, sentiment, forecasting, smart money, Elliott Wave, cashflow, DEX data, and AI-powered insights. Requires asrai-mcp installed and PRIVATE_KEY env var set. Each API call costs $0.001 USDC from your own wallet on Base mainnet via x402.
license: MIT
---

# Asrai — Crypto Analysis via x402

## Prerequisites

This skill requires **asrai-mcp** to be installed:
```bash
pip install asrai-mcp
```

And a `~/.env` file with your wallet key:
```
PRIVATE_KEY=0x<your_private_key>
```

Each API call costs **$0.001 USDC** from your wallet on Base mainnet ($0.002 for `ask_ai`). `indicator_guide` is FREE.

## Payment transparency

- Always inform the user of the cost before making calls if they ask.
- The `ASRAI_MAX_SPEND` env var sets a per-session cap (default $2.00).
- Payments are signed by the user's own wallet — never a shared key.

## MCP tools available

| Tool | What it does | Cost |
|---|---|---|
| `market_overview` | Trending, gainers/losers, RSI, top/bottom | $0.004 (4 calls) |
| `technical_analysis(symbol, timeframe)` | Signal, ALSAT, SuperALSAT, PSAR, MACD-DEMA, AlphaTrend, TD | $0.007 (7 calls) |
| `sentiment` | CBBI, CMC sentiment, CMC AI | $0.003 (3 calls) |
| `forecast(symbol)` | AI price forecast | $0.001 |
| `screener(type)` | Find coins by criteria | $0.001 |
| `smart_money(symbol, timeframe)` | SMC, order blocks, FVGs, support/resistance | $0.002 (2 calls) |
| `elliott_wave(symbol, timeframe)` | Elliott Wave analysis | $0.001 |
| `ichimoku(symbol, timeframe)` | Ichimoku cloud | $0.001 |
| `cashflow(mode, symbol)` | Capital flow | $0.001 |
| `coin_info(symbol)` | Stats, info, price, tags | $0.004 (4 calls) |
| `dexscreener(contract)` | DEX data | $0.001 |
| `chain_tokens(chain, max_mcap)` | Low-cap tokens on chain | $0.001 |
| `portfolio` | Portfolio analysis | $0.001 |
| `channel_summary` | Latest narratives | $0.001 |
| `ask_ai(question)` | AI analyst answer | $0.002 |
| `indicator_guide(name)` | Guide for Asrai custom indicators (ALSAT, SuperALSAT, PMax, AlphaTrend, MavilimW etc.) | FREE |

## indicator_guide usage

Call only when you encounter an unfamiliar indicator name in tool output. Standard indicators (RSI, MACD, Ichimoku, BB, Elliott Wave) are well-known — skip them.

- `indicator_guide()` or `indicator_guide("list")` → compact 1-line summary of all custom indicators
- `indicator_guide("ALSAT")` → full details for that indicator
- `indicator_guide("all")` → full guide for everything (avoid unless necessary)

## Output rules

- Think like both a trader AND a long-term investor. Default to investor mode (macro thesis, cycle position, accumulation zones). Switch to trader mode only when user asks for entry/when to buy.
- Keep responses 200-400 words — thorough but easy to read.
- Use emojis to structure sections: 📊 market context, 🎯 target/entry, ⚠️ risk, 📈📉 direction, 💡 insight.
- Never list raw indicator values — synthesize into plain language verdict.
- Never address the user by name in responses.

## Default analysis pattern

1. **Set regime** — BTC/ETH trend + market mood (CBBI)
2. **Find signals** — ALSAT/SuperALSAT cycle position, PMax trend, momentum
3. **Translate to action** — clear verdict: accumulate / wait / avoid + price zones

## References

- Full endpoint catalog: `skills/asrai/references/endpoints.md`
