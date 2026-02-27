# Report Template (Hybrid)

Use `daily` template by default. Use `full_report` template when user explicitly requests comprehensive analysis.

## A) Daily Concise Template (Default)

```markdown
# Daily Stock Analysis - <TICKER> (<EXCHANGE>)

## 1) Execution Metadata
- Run Time: <YYYY-MM-DD HH:mm TZ>
- Market: <US/CN/HK>
- Mode: daily
- Target Session for Prediction: <YYYY-MM-DD>
- Rolling Window Baseline: <7d default or custom>
- Output File: <YYYY-MM-DD-TICKER-analysis.md in workspace root>

## 2) Market Snapshot and Thesis
- Last Price/Close: <VALUE>
- Session Range: <LOW-HIGH>
- Volume/Volatility: <SUMMARY>
- Thesis: <Bullish/Neutral/Bearish + 2-3 sentence rationale>

## 3) Recommendation and Risk Controls
- Recommendation: <Buy/Hold/Sell/Watch>
- Entry Trigger(s): <CONDITIONS>
- Exit/Invalidation Trigger(s): <CONDITIONS>
- Risk Controls: <POSITION/RISK NOTES>

## 4) Next-Trading-Day Close Prediction
- Point Forecast (`pred_close_t1`): <VALUE>
- Optional Forecast Range: <LOW-HIGH>
- Confidence: <High/Medium/Low>
- Key Assumptions:
  1. <ASSUMPTION_1>
  2. <ASSUMPTION_2>

## 5) Prior Forecast Review (if available)
- Previous Forecast (`prev_pred_close_t1`): <VALUE or N/A>
- Actual Close (`prev_actual_close_t1`): <VALUE or N/A>
- AE: <VALUE or N/A>
- APE: <VALUE or N/A>
- Attribution: <WHY HIT/MISS>

## 6) Rolling Accuracy
| Window | Strict (<=1%) | Loose (<=2%) | Direction (opt.) | n |
|---|---:|---:|---:|---:|
| 1d | <...> | <...> | <...> | <...> |
| 3d | <...> | <...> | <...> | <...> |
| 7d | <...> | <...> | <...> | <...> |
| 30d | <...> | <...> | <...> | <...> |
| Custom | <...> | <...> | <...> | <...> |

## 6.1) Forecast Correctness and Improvement Signal
- Latest Forecast Correctness Score (optional): <SCORE_0_TO_100>
- 7d APE Trend: <IMPROVING/STABLE/DEGRADING>
- Strict Hit Rate Change (7d vs previous 7d): <VALUE>
- Improvement Actions for Next Run:
  1. <ACTION_1>
  2. <ACTION_2>

## 7) Next Session Watchlist
1. <EVENT_OR_LEVEL_1>
2. <EVENT_OR_LEVEL_2>
3. <EVENT_OR_LEVEL_3>

## 8) Sources
- <SOURCE_URL_1> (updated/published: <TIMESTAMP>)
- <SOURCE_URL_2> (updated/published: <TIMESTAMP>)
- <SOURCE_URL_3> (updated/published: <TIMESTAMP>)

## 9) Disclaimer
This content is for research and informational purposes only and does not constitute investment advice or a return guarantee. Markets are risky; invest with caution.
```

## B) Comprehensive Template (`full_report` Mode)

```markdown
# Comprehensive Stock Report - <TICKER> (<EXCHANGE>)

## 1) Executive Summary
- Company snapshot
- Core thesis
- Recommendation and conviction
- Key upside/downside drivers
- Output File: <YYYY-MM-DD-TICKER-analysis.md in workspace root>

## 2) Company and Market Overview
- Business model and segment mix
- Industry position and peer context
- Market regime context (rates/FX/commodities/index)

## 3) Fundamental Analysis
- Revenue/earnings/cash flow trends
- Profitability and efficiency metrics
- Balance sheet and leverage profile
- Valuation (historical, peer-relative, scenario-based)

## 4) Technical Analysis
- Trend structure across timeframes
- Support/resistance map
- Indicator readout (MA, RSI, MACD, volume)
- Pattern and momentum interpretation

## 5) Recommendation Framework
- Recommendation: Buy/Hold/Sell/Watch
- Entry/exit criteria
- Invalidation conditions and risk controls

## 6) Next-Trading-Day Prediction
- `pred_close_t1`
- Optional interval and confidence
- Assumption set

## 7) Prior Forecast Review
- `prev_pred_close_t1` vs `prev_actual_close_t1`
- AE/APE and hit status
- Attribution and what to change

## 8) Rolling Forecast Accuracy
- 1d / 3d / 7d / 30d / custom windows
- strict and loose hit rates
- optional direction accuracy
- sample size notes

## 8.1) Continuous Improvement Notes
- Latest correctness score (optional)
- Error pattern summary
- Adjustments for next run

## 9) Catalysts and Risk Calendar
- Positive catalysts with dates
- Negative catalysts/risk events with dates

## 10) Sources and Timestamps
- Primary and secondary sources used

## 11) Disclaimer
This content is for research and informational purposes only and does not constitute investment advice or a return guarantee. Markets are risky; invest with caution.
```
