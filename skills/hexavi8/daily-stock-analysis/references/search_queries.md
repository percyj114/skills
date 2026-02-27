# Search Query Templates (Market-Aware)

Use `<TICKER>`, `<COMPANY>`, `<MARKET>`, `<DATE>` placeholders.
Always capture source URL and publication/update timestamp.

## Source Priority

1. Official / primary:
- Exchange disclosures and filings
- Company investor relations releases
- Regulator filings

2. Tier-1 financial media / data terminals:
- Bloomberg, Reuters, CNBC, WSJ, MarketWatch, Yahoo Finance, TradingView

3. Secondary aggregators:
- Use for discovery only; verify key data in primary/tier-1 sources

## Cross-Verification Rule

For critical values (close, EPS, guidance, major corporate events), verify with at least two independent sources whenever possible.

## A) US Market Queries

1. Filings and disclosures:
- `<TICKER> SEC 8-K 10-Q 10-K latest`
- `<COMPANY> investor relations earnings release <DATE>`

2. Price and technical context:
- `<TICKER> price volume 52-week range`
- `<TICKER> technical analysis RSI MACD moving averages`
- `<TICKER> options implied volatility unusual options activity`

3. Analyst and news flow:
- `<TICKER> analyst rating change price target`
- `<COMPANY> latest news today Reuters Bloomberg`

## B) Hong Kong Market Queries

1. Disclosures and announcements:
- `<TICKER> HKEX announcement`
- `<COMPANY> investor relations results announcement`

2. Price and technical context:
- `<TICKER> HK stock price volume`
- `<TICKER> RSI MACD moving average`

3. Sell-side/news flow:
- `<TICKER> broker target price Hong Kong`
- `<COMPANY> Hong Kong market news`

## C) China A-Share Market Queries

1. Official disclosures:
- `<TICKER> exchange announcement SSE SZSE`
- `<COMPANY> annual report quarterly report`

2. Price and technical context:
- `<TICKER> A-share close volume turnover`
- `<TICKER> technical indicator RSI MACD MA`

3. News and policy context:
- `<COMPANY> regulatory policy industry news`
- `<SECTOR> China policy support demand trend`

## D) Macro and Regime Queries

- `US 10Y yield today`
- `Fed rate expectations today CME FedWatch`
- `DXY index today`
- `USD/CNH today`
- `WTI crude oil price today`
- `<MARKET_INDEX> index trend volatility`

## E) Peer and Relative Queries

- `<COMPANY> peer comparison valuation`
- `<TICKER> vs <PEER_TICKER> margins growth valuation`
- `<SECTOR> ETF fund flow today`

## Data Hygiene Checklist

1. Use latest available session-aligned data.
2. Align date and timezone before comparing values.
3. Distinguish official close vs intraday last trade.
4. Record corporate actions affecting comparability.
5. Annotate unverified/low-confidence items.
