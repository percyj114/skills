# Workflow

Use this sequence for every run. Treat it as the execution contract.

## 1. Resolve Instrument Context

1. Resolve ticker, exchange, market (US/CN/HK), and quote currency.
2. Resolve user timezone and market timezone.
3. Resolve trading calendar:
- Determine current trading day vs non-trading day.
- Identify the next valid trading day (`t+1`).

## 2. Review Historical Analysis Files First (Required)

Before collecting new data, load existing markdown reports in workspace root for the same ticker.

1. Find recent files matching:
- `YYYY-MM-DD-<TICKER>-analysis.md`

2. Prioritize review order:
- Most recent file first
- Then rolling history (default last 7 valid files, or user-specified window)

3. Extract from history:
- prior prediction values
- prior actual values (if recorded)
- prior AE/APE, strict/loose hit status
- prior `improvement_actions`

4. Summarize what to carry forward:
- recurring miss patterns
- assumptions that failed repeatedly
- adjustments that improved accuracy

If no historical file exists, mark review bootstrap state and continue.

## 3. Collect Data (Multi-Source)

Collect and timestamp these data groups:

1. Market data:
- Last price or close, open/high/low, volume, volatility, gap behavior.

2. News and event data:
- Company disclosures, filings, earnings guidance, major headlines, regulatory events.

3. Fundamental and valuation data:
- Growth, margins, leverage, cash flow, valuation multiples.

4. Technical data:
- Trend state, moving averages, RSI, MACD, support/resistance, volume confirmation.

5. Macro and regime data:
- Rates, FX, commodities, index trend/risk regime relevant to the ticker.

## 4. Build Daily Thesis and Recommendation

1. Produce directional thesis (bullish / neutral / bearish).
2. List top drivers (3-5) and major risks (2-4).
3. Output recommendation: Buy / Hold / Sell / Watch.
4. Attach conditional triggers:
- Entry conditions
- Exit/invalidation conditions
- Risk controls (position sizing/stop logic at high level)

## 5. Predict Next Trading Day Close

Output:

- `pred_close_t1` (required point estimate)
- Optional interval `[pred_low_t1, pred_high_t1]`
- Confidence level (High/Medium/Low)
- Assumptions that must hold

## 6. Review Prior Forecast on Next Run

If prior forecast exists and actual close is available:

- Load `prev_pred_close_t1` and `prev_actual_close_t1`
- Compute `AE` and `APE`
- Explain miss/hit attribution (news shock, liquidity shift, macro surprise, technical failure)

If actual close is unavailable:

- Mark review as pending
- Do not fabricate result

## 7. Compute Forecast Correctness and Rolling Accuracy

Use definitions in `metrics.md` and compute as data permits:

- 1-day, 3-day, 7-day, 30-day windows
- Optional custom window requested by user
- Strict hit rate, loose hit rate, optional direction accuracy

If sample count is insufficient, show:

- available `n`
- which windows are partial or unavailable

## 8. Apply Improvement Loop

Convert review findings into next-run improvements:

1. Identify recurring miss patterns:
- Event-driven misses
- Regime-change misses
- Trend-following or mean-reversion bias errors

2. Update analysis emphasis for next run:
- Increase/decrease weight for technical vs fundamental vs macro signals
- Tighten or loosen confidence level assignment
- Update trigger sensitivity for recommendation decisions

3. Record explicit improvement actions in output (`improvement_actions`).

## 9. Render Report

Choose template in `report_template.md`:

- Default: concise daily template (`daily` mode)
- Optional: comprehensive template (`full_report` mode)

Report must include:

- Execution metadata
- Market snapshot + thesis
- Recommendation + conditions + risk controls
- Next-day prediction
- Prior-day review (or pending state)
- Rolling metrics table
- Improvement actions for next run
- Watchlist for next session
- Source list with timestamps
- Legal disclaimer

## 10. Persist Report to Workspace Root (Required)

After rendering, save exactly one markdown report file to workspace root for historical traceability.

- Filename format: `YYYY-MM-DD-<TICKER>-analysis.md`
- The `<DATE>` must reflect run date in user-local timezone.
- Overwrite same-day same-ticker file only if rerun is intentional; otherwise keep one canonical file per ticker per day.

This persisted file is the default source for:

- prior-day forecast review
- rolling correctness and accuracy computations
- continuous-improvement comparisons across runs

## Edge Cases and Handling Rules

1. Non-trading day/holiday:
- Use last valid session data for context.
- Predict next valid trading session close.

2. Missing close at runtime:
- Mark prediction review pending until official close is available.

3. Corporate actions (split/dividend):
- Use adjusted series when comparing historical forecast accuracy.
- Flag major actions in report notes.

4. Conflicting sources:
- Prefer official filings/exchange prints.
- If conflict remains, show both values and confidence downgrade.

5. First run (no prior forecast):
- Skip review section with explicit "not available on first run" note.

6. Missing historical files in workspace root:
- Mark review/rolling metrics as limited by available history.
- Continue with current-day analysis and prediction.
