---
name: daily-stock-analysis
description: Daily stock analysis and forecasting skill for multi-market equities, with explicit predictive pricing, next-run postmortem review, and continuous-improvement feedback loop. Use when users ask for next-trading-day close predictions, recommendation decisions (Buy/Hold/Sell/Watch), forecast correctness scoring, rolling accuracy statistics (1d/3d/7d/30d/custom), and iterative improvement of future analysis quality.
---

# Daily Stock Analysis

Perform market-aware, evidence-based daily stock analysis with prediction, next-run review, rolling accuracy tracking, and a structured self-evolution mechanism that updates future assumptions from observed forecast errors.

## Core Capability Focus

This skill is optimized around three linked capabilities:

1. `price_prediction`

- Predict next-trading-day closing price (`pred_close_t1`) with confidence and assumptions.

2. `postmortem_review`

- Re-evaluate previous forecast against actual close and explain miss/hit attribution.

3. `continuous_improvement`

- Convert review findings into explicit, reusable improvements for the next run: assumption updates, factor-weight adjustments, event-risk handling, and confidence calibration.

## Self-Evolution Loop

Treat each run as labeled feedback for the next run, not just a one-off report.

### Trigger Conditions

Start/refresh self-evolution when any of these occurs:

- Material forecast miss (`AE`/`APE` above recent baseline)
- Wrong direction call (bullish vs bearish miss)
- User correction that changes thesis, assumptions, or catalyst interpretation
- Data-quality conflict or tool failure that degraded analysis confidence

### Learning Record (Per Run)

Create a concise learning record with:

- `observation`: what was wrong or unstable
- `root_cause`: why the miss happened
- `action`: what to change next run
- `scope`: where it applies (`ticker-specific` or `cross-ticker`)
- `expiry`: when to stop applying this rule (if regime-dependent)

Write this into current report via `improvement_actions` (and optional `learning_note`).

### Application Priority (Next Run)

Apply prior learnings before generating new prediction:

1. Data quality and event handling fixes
2. Factor-weight and horizon adjustments
3. Confidence calibration updates
4. Recommendation threshold tuning

If multiple learnings conflict, prefer the most recent learning with better observed follow-up accuracy.

### Validation and Rollback

After applying a learning:

- Track whether rolling metrics improve over next valid samples.
- If no improvement after multiple samples, downgrade or remove that learning.
- Keep only learnings that change decisions or improve calibration.

## Operation Modes

1. `daily` (default)

- Generate a concise daily report.
- Include recommendation, next-trading-day close prediction, prior-day review (if available), and rolling accuracy metrics.

2. `full_report` (optional)

- Generate a comprehensive investment report.
- Expand fundamental, technical, valuation, catalysts, and risk sections.

## Trigger Guidance

Activate this skill when the user asks for:

- Daily stock analysis (for example: "Analyze AAPL for tomorrow")
- Daily recurring review (for example: "Analyze Tencent every morning and review yesterday's forecast")
- Trading recommendation with rationale (Buy/Hold/Sell/Watch)
- Next-day closing price prediction
- Forecast quality review and error tracking
- Rolling prediction accuracy for 1/3/7/30 days or a custom window
- A full stock report (for example: "Give me a full report for TSLA")

## Input Defaults

If the user does not specify values, apply these defaults:

- Mode: `daily`
- Run time: local morning run, target 10:00
- Window: last 7 valid forecast samples
- Language: follow user language for response content (skill docs remain English)
- Recommendation labels: Buy / Hold / Sell / Watch
- Report file output: write one markdown report to workspace root on every run

If ticker is missing, infer from company name and confirm ticker + exchange before analysis.

## Default Report Persistence

Persist every run as a markdown file in workspace root so future runs can reuse history for review and accuracy computation.

- Default filename format: `YYYY-MM-DD-<TICKER>-analysis.md`
- Example: `2026-02-24-AAPL-analysis.md`
- Include at minimum: prediction fields, prior-review fields, rolling metrics, and improvement actions

## Reference Files

Read references as needed:

- `references/workflow.md`: end-to-end execution sequence and edge handling
- `references/search_queries.md`: market-aware web search playbook
- `references/metrics.md`: error and accuracy definitions
- `references/report_template.md`: output templates (`daily` and `full_report`)
- `references/fundamental-analysis.md`: business and financial framework
- `references/technical-analysis.md`: technical framework and indicators
- `references/financial-metrics.md`: metric definitions and formulas

## Core Execution Rules

1. Verify all time-sensitive market data from current, authoritative sources.
2. Prefer primary sources first (exchange filings, company IR, official releases), then tier-1 media.
3. Cross-check key numbers with at least two independent sources when possible.
4. Use market calendar and timezone correctly for US/CN/HK trading sessions.
5. Before new analysis, first load and review previous analysis markdown files (if available) from workspace root.
6. Clearly separate facts, assumptions, and inferences.
7. If data is missing or conflicting, state uncertainty and reduce confidence.
8. Always include legal disclaimer at the end.

## Standardized Output Contract

Each run must provide:

1. `recommendation`

- One of: Buy / Hold / Sell / Watch
- Include trigger conditions and risk controls.

2. `prediction`

- `pred_close_t1`: point estimate for next trading day close
- Optional interval `[pred_low_t1, pred_high_t1]`
- Confidence level: High / Medium / Low
- Key assumptions list

3. `review`

- Compare previous forecast vs actual close:
  - `prev_pred_close_t1`
  - `prev_actual_close_t1`
  - `AE`, `APE`
- Explain primary forecast miss/hit drivers

4. `accuracy`

- Rolling strict and loose hit rates for 1d/3d/7d/30d (as data permits)
- Optional custom window if user requests
- Optional direction accuracy

5. `improvement_actions`

- 1-3 concrete adjustments for the next run based on forecast review
- Example: reduce weight on short-term momentum during event-heavy sessions
- Optional `learning_note`: one concise self-evolution record from this run
- Optional `learning_scope`: `ticker-specific` or `cross-ticker`
- Optional `learning_expiry`: condition/date after which learning should be retired

## Scheduling Guidance

When user asks for daily automation at 10:00:

- Use weekday schedule (Mon-Fri) in user's local timezone.
- Keep schedule in automation config, not in analysis prompt text.
- The analysis prompt should describe only the task behavior.

## Compliance Disclaimer (Required)

Append this (or equivalent meaning) in every report:

"This content is for research and informational purposes only and does not constitute investment advice or a return guarantee. Markets are risky; invest with caution."
