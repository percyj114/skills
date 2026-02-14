#!/usr/bin/env python3
"""
Crypto Regime Report Generator

Fetches data from OKX (daily) and Yahoo Finance (weekly) and generates regime reports
using Supertrend and ADX indicators.
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Config path - can be overridden via REGIME_CONFIG env var
CONFIG_PATH = Path(os.environ.get(
    "REGIME_CONFIG",
    Path(__file__).parent.parent / "references" / "config.json"
))
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

# Yahoo Finance symbol mapping for weekly reports
YAHOO_SYMBOLS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "AVAX": "AVAX-USD",
    "ADA": "ADA-USD",
    "DOT": "DOT-USD",
    "NEAR": "NEAR-USD",
    "ARB": "ARB-USD",
    "OP": "OP-USD",
    "POL": "POL-USD",
    "MATIC": "POL-USD",  # Polygon rebranded
    "UNI": "UNI-USD",
    "AAVE": "AAVE-USD",
    "LINK": "LINK-USD",
    "HYPE": "HYPE-USD",
    "RNDR": "RENDER-USD",
    "RENDER": "RENDER-USD",
    "SUI": "SUI-USD",
    "APT": "APT-USD",
}


def okx_request(endpoint: str) -> dict:
    """Make a request to OKX API using curl (avoids Python urllib blocking)."""
    url = f"https://www.okx.com{endpoint}"
    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise Exception(f"curl failed: {result.stderr}")
    return json.loads(result.stdout)


def fetch_candles(symbol: str, bar: str = "1D", limit: int = 100) -> list:
    """Fetch OHLCV candles from OKX."""
    resp = okx_request(f"/api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}")
    if resp.get("code") != "0":
        raise Exception(f"OKX error: {resp.get('msg')}")
    # OKX returns newest first, reverse for chronological order
    candles = resp["data"][::-1]
    return [{
        "ts": int(c[0]),
        "open": float(c[1]),
        "high": float(c[2]),
        "low": float(c[3]),
        "close": float(c[4]),
        "vol": float(c[5])
    } for c in candles]


def fetch_yahoo_candles(symbol: str, period: str = "2y") -> list:
    """Fetch OHLCV candles from Yahoo Finance using yfinance CLI."""
    yahoo_sym = YAHOO_SYMBOLS.get(symbol, f"{symbol}-USD")
    
    # Use uvx to run yfinance without installing
    code = f'''
import yfinance as yf
import json
ticker = yf.Ticker("{yahoo_sym}")
hist = ticker.history(period="{period}", interval="1wk")
data = []
for idx, row in hist.iterrows():
    if row["Close"] > 0:
        data.append({{
            "ts": int(idx.timestamp() * 1000),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "vol": float(row["Volume"])
        }})
print(json.dumps(data))
'''
    
    result = subprocess.run(
        ["uvx", "--from", "yfinance", "python3", "-c", code],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if result.returncode != 0:
        raise Exception(f"Yahoo Finance error: {result.stderr}")
    
    try:
        candles = json.loads(result.stdout)
        return candles
    except json.JSONDecodeError:
        raise Exception(f"Failed to parse Yahoo Finance response: {result.stdout[:200]}")


def fetch_funding_rate(symbol: str) -> dict:
    """Fetch funding rate from OKX."""
    resp = okx_request(f"/api/v5/public/funding-rate?instId={symbol}")
    if resp.get("code") != "0" or not resp.get("data"):
        return {"rate": None, "next_time": None}
    data = resp["data"][0]
    return {
        "rate": float(data.get("fundingRate", 0)),
        "next_time": int(data.get("nextFundingTime", 0))
    }


def fetch_open_interest(symbol: str) -> float:
    """Fetch open interest from OKX."""
    resp = okx_request(f"/api/v5/public/open-interest?instId={symbol}")
    if resp.get("code") != "0" or not resp.get("data"):
        return 0
    return float(resp["data"][0].get("oiUsd", 0))


def calculate_atr(candles: list, period: int = 10) -> list:
    """Calculate Average True Range using Wilder's smoothing."""
    if len(candles) < period + 1:
        return [None] * len(candles)
    
    trs = []
    for i in range(len(candles)):
        if i == 0:
            trs.append(candles[i]["high"] - candles[i]["low"])
        else:
            h = candles[i]["high"]
            l = candles[i]["low"]
            pc = candles[i - 1]["close"]
            tr = max(h - l, abs(h - pc), abs(l - pc))
            trs.append(tr)
    
    # Wilder's smoothing
    atr = [None] * period
    atr.append(sum(trs[:period]) / period)  # First ATR is simple average
    
    for i in range(period + 1, len(candles)):
        atr.append((atr[-1] * (period - 1) + trs[i]) / period)
    
    return atr


def calculate_supertrend(candles: list, period: int = 10, multiplier: float = 3.0) -> tuple:
    """
    Calculate Supertrend indicator.
    Returns: (supertrend_values, directions) where direction is 1 for bullish, -1 for bearish
    """
    atr = calculate_atr(candles, period)
    
    supertrend = []
    direction = []
    
    for i in range(len(candles)):
        if atr[i] is None:
            supertrend.append(None)
            direction.append(0)
            continue
        
        hl2 = (candles[i]["high"] + candles[i]["low"]) / 2
        upper_band = hl2 + multiplier * atr[i]
        lower_band = hl2 - multiplier * atr[i]
        
        if i == 0 or supertrend[-1] is None:
            supertrend.append(lower_band)
            direction.append(1)
            continue
        
        # Determine trend based on price position
        prev_st = supertrend[-1]
        prev_dir = direction[-1]
        prev_close = candles[i - 1]["close"]
        
        # Adjust lower band (only can go up)
        if lower_band > prev_st or prev_close < prev_st:
            final_lower = lower_band
        else:
            final_lower = prev_st
        
        # Adjust upper band (only can go down)
        if upper_band < prev_st or prev_close > prev_st:
            final_upper = upper_band
        else:
            final_upper = prev_st
        
        # Determine new direction
        if prev_dir >= 0:  # Was bullish
            if candles[i]["close"] < final_lower:
                new_dir = -1
                new_st = final_upper
            else:
                new_dir = 1
                new_st = final_lower
        else:  # Was bearish
            if candles[i]["close"] > final_upper:
                new_dir = 1
                new_st = final_lower
            else:
                new_dir = -1
                new_st = final_upper
        
        supertrend.append(new_st)
        direction.append(new_dir)
    
    return supertrend, direction


def calculate_adx(candles: list, period: int = 14) -> list:
    """Calculate ADX (Average Directional Index) using Wilder's method."""
    if len(candles) < period * 2:
        return [None] * len(candles)
    
    # Calculate +DM and -DM
    plus_dm = [0]
    minus_dm = [0]
    
    for i in range(1, len(candles)):
        up_move = candles[i]["high"] - candles[i-1]["high"]
        down_move = candles[i-1]["low"] - candles[i]["low"]
        
        if up_move > down_move and up_move > 0:
            plus_dm.append(up_move)
        else:
            plus_dm.append(0)
        
        if down_move > up_move and down_move > 0:
            minus_dm.append(down_move)
        else:
            minus_dm.append(0)
    
    # Calculate TR
    trs = [candles[0]["high"] - candles[0]["low"]]
    for i in range(1, len(candles)):
        h = candles[i]["high"]
        l = candles[i]["low"]
        pc = candles[i-1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    
    # Wilder's smoothing function
    def wilder_smooth(values, period):
        smoothed = []
        for i in range(len(values)):
            if i < period - 1:
                smoothed.append(None)
            elif i == period - 1:
                smoothed.append(sum(values[:period]))
            else:
                smoothed.append(smoothed[-1] - smoothed[-1] / period + values[i])
        return smoothed
    
    smoothed_tr = wilder_smooth(trs, period)
    smoothed_plus_dm = wilder_smooth(plus_dm, period)
    smoothed_minus_dm = wilder_smooth(minus_dm, period)
    
    # Calculate DI and DX
    plus_di = []
    minus_di = []
    dx = []
    
    for i in range(len(candles)):
        if smoothed_tr[i] is None or smoothed_tr[i] == 0:
            plus_di.append(None)
            minus_di.append(None)
            dx.append(None)
        else:
            pdi = 100 * smoothed_plus_dm[i] / smoothed_tr[i]
            mdi = 100 * smoothed_minus_dm[i] / smoothed_tr[i]
            plus_di.append(pdi)
            minus_di.append(mdi)
            
            di_sum = pdi + mdi
            if di_sum == 0:
                dx.append(0)
            else:
                dx.append(100 * abs(pdi - mdi) / di_sum)
    
    # Smooth DX to get ADX
    adx = [None] * len(candles)
    
    # Find first valid DX index
    first_valid = None
    for i in range(len(dx)):
        if dx[i] is not None:
            first_valid = i
            break
    
    if first_valid is None:
        return adx
    
    # First ADX is average of first 'period' DX values
    valid_dx = [d for d in dx if d is not None]
    if len(valid_dx) < period:
        return adx
    
    adx[first_valid + period - 1] = sum(valid_dx[:period]) / period
    
    # Subsequent ADX values use Wilder's smoothing
    dx_idx = period
    for i in range(first_valid + period, len(candles)):
        if dx[i] is not None:
            adx[i] = (adx[i-1] * (period - 1) + dx[i]) / period
            dx_idx += 1
    
    return adx


def get_regime(direction: int, adx_value: float, thresholds: dict) -> str:
    """Determine regime classification."""
    if adx_value is None:
        return "Unknown"
    
    strong = thresholds["strong_threshold"]
    weak = thresholds["weak_threshold"]
    
    if direction > 0:  # Bullish Supertrend
        if adx_value >= strong:
            return "Strong Bull"
        elif adx_value >= weak:
            return "Weak Bull"
        else:
            return "Ranging"
    else:  # Bearish Supertrend
        if adx_value >= strong:
            return "Strong Bear"
        elif adx_value >= weak:
            return "Weak Bear"
        else:
            return "Ranging"


def analyze_asset(asset: dict) -> dict:
    """Analyze a single asset."""
    symbol = asset["okx"]
    
    try:
        # Fetch candles
        candles = fetch_candles(symbol, limit=CONFIG["report"]["candle_count"])
        if len(candles) < 30:
            return {"error": "Not enough data", "symbol": asset["symbol"]}
        
        # Calculate indicators
        st, direction = calculate_supertrend(
            candles,
            CONFIG["indicators"]["supertrend"]["period"],
            CONFIG["indicators"]["supertrend"]["multiplier"]
        )
        adx = calculate_adx(candles, CONFIG["indicators"]["adx"]["period"])
        
        # Current values
        current_price = candles[-1]["close"]
        current_st = st[-1]
        current_dir = direction[-1]
        current_adx = adx[-1]
        
        if current_st is None or current_adx is None:
            return {"error": "Indicator calculation failed", "symbol": asset["symbol"]}
        
        # Price change
        prev_close = candles[-2]["close"]
        price_change = ((current_price - prev_close) / prev_close) * 100
        
        # Regime
        regime = get_regime(current_dir, current_adx, CONFIG["indicators"]["adx"])
        
        # Funding rate
        funding = fetch_funding_rate(symbol)
        funding_rate = funding["rate"]
        
        # Open interest
        oi = fetch_open_interest(symbol)
        
        return {
            "symbol": asset["symbol"],
            "name": asset["name"],
            "price": current_price,
            "change_24h": price_change,
            "supertrend": current_st,
            "direction": "bullish" if current_dir > 0 else "bearish",
            "adx": current_adx,
            "regime": regime,
            "funding_rate": funding_rate * 100 if funding_rate else None,
            "open_interest": oi / 1e9 if oi else None  # In billions
        }
    except Exception as e:
        return {"error": str(e), "symbol": asset["symbol"]}


def format_report(results: list, report_type: str = "regime") -> str:
    """Format results as a Telegram-ready report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M PST")
    
    lines = [f"📊 *Crypto Regime Report*", f"_{now}_", ""]
    
    # Sort by regime priority
    regime_order = {"Strong Bull": 0, "Weak Bull": 1, "Ranging": 2, "Weak Bear": 3, "Strong Bear": 4, "Unknown": 5}
    sorted_results = sorted(results, key=lambda x: regime_order.get(x.get("regime", "Unknown"), 5))
    
    for r in sorted_results:
        if "error" in r:
            lines.append(f"❌ *{r['symbol']}*: {r['error']}")
            continue
        
        # Emoji for regime
        regime_emoji = {
            "Strong Bull": "🟢",
            "Weak Bull": "🟡",
            "Ranging": "⚪",
            "Weak Bear": "🟠",
            "Strong Bear": "🔴"
        }.get(r["regime"], "❓")
        
        # Price formatting
        if r["price"] >= 1000:
            price_str = f"${r['price']:,.0f}"
        elif r["price"] >= 1:
            price_str = f"${r['price']:,.2f}"
        else:
            price_str = f"${r['price']:,.4f}"
        
        # Change emoji
        change_emoji = "📈" if r["change_24h"] > 0 else "📉" if r["change_24h"] < 0 else "➡️"
        
        lines.append(f"{regime_emoji} *{r['symbol']}* {price_str} {change_emoji} {r['change_24h']:+.1f}%")
        lines.append(f"   _{r['regime']}_ | ADX: {r['adx']:.1f} | {r['direction'].capitalize()}")
        
        if r["funding_rate"] is not None:
            funding_emoji = "🔥" if abs(r["funding_rate"]) > 0.01 else ""
            lines.append(f"   Funding: {r['funding_rate']:+.4f}% {funding_emoji}")
        
        lines.append("")
    
    # Summary
    bull_count = sum(1 for r in sorted_results if "Bull" in r.get("regime", ""))
    bear_count = sum(1 for r in sorted_results if "Bear" in r.get("regime", ""))
    range_count = sum(1 for r in sorted_results if r.get("regime") == "Ranging")
    
    lines.append(f"📈 Bulls: {bull_count} | 📉 Bears: {bear_count} | ⚪ Range: {range_count}")
    
    return "\n".join(lines)


def fetch_weekly_candles(symbol: str, limit: int = 52) -> list:
    """Fetch weekly OHLCV candles from Yahoo Finance (more historical data).
    Falls back to OKX for assets not on Yahoo Finance.
    """
    # Try Yahoo Finance first (more history)
    yahoo_sym = YAHOO_SYMBOLS.get(symbol, f"{symbol}-USD")
    
    # Known Yahoo Finance gaps - use OKX for these
    YAHOO_GAPS = {"POL", "MATIC", "UNI", "HYPE", "SUI", "APT", "ARB"}
    
    if symbol not in YAHOO_GAPS:
        try:
            return fetch_yahoo_candles(symbol, period="2y")
        except Exception:
            pass  # Fall through to OKX
    
    # Fallback to OKX weekly candles
    okx_sym = f"{symbol}-USDT-SWAP"
    return fetch_candles(okx_sym, bar="1W", limit=100)


def analyze_asset_weekly(asset: dict) -> dict:
    """Analyze a single asset on weekly timeframe using Yahoo Finance."""
    # Use asset symbol for Yahoo Finance, OKX symbol for funding/OI
    symbol = asset["symbol"]
    okx_symbol = asset["okx"]
    
    try:
        # Fetch weekly candles (Yahoo Finance with OKX fallback)
        candles = fetch_weekly_candles(symbol, limit=100)
        if len(candles) < 30:
            return {"error": "Not enough data", "symbol": asset["symbol"]}
        
        # Calculate indicators
        st, direction = calculate_supertrend(
            candles,
            CONFIG["indicators"]["supertrend"]["period"],
            CONFIG["indicators"]["supertrend"]["multiplier"]
        )
        adx = calculate_adx(candles, CONFIG["indicators"]["adx"]["period"])
        
        # Current values
        current_price = candles[-1]["close"]
        current_st = st[-1]
        current_dir = direction[-1]
        current_adx = adx[-1]
        
        if current_st is None or current_adx is None:
            return {"error": "Indicator calculation failed", "symbol": asset["symbol"]}
        
        # Weekly price change
        prev_close = candles[-2]["close"]
        price_change = ((current_price - prev_close) / prev_close) * 100
        
        # Regime
        regime = get_regime(current_dir, current_adx, CONFIG["indicators"]["adx"])
        
        # Funding rate (from OKX)
        funding = fetch_funding_rate(okx_symbol)
        funding_rate = funding["rate"]
        
        # Open interest (from OKX)
        oi = fetch_open_interest(okx_symbol)
        
        # Check for regime change from last week
        prev_dir = direction[-2] if len(direction) > 1 else 0
        regime_change = None
        if prev_dir != current_dir and prev_dir != 0:
            regime_change = "bullish" if current_dir > 0 else "bearish"
        
        return {
            "symbol": asset["symbol"],
            "name": asset["name"],
            "price": current_price,
            "change_wtd": price_change,
            "supertrend": current_st,
            "direction": "bullish" if current_dir > 0 else "bearish",
            "adx": current_adx,
            "regime": regime,
            "funding_rate": funding_rate * 100 if funding_rate else None,
            "open_interest": oi / 1e9 if oi else None,
            "regime_change": regime_change
        }
    except Exception as e:
        return {"error": str(e), "symbol": asset["symbol"]}


def format_weekly_report(results: list) -> str:
    """Format results as a weekly Telegram-ready report."""
    now = datetime.now().strftime("%Y-%m-%d")
    
    lines = [f"📊 *Weekly Crypto Regime Report*", f"_Friday {now}_", ""]
    
    # Sort by regime priority
    regime_order = {"Strong Bull": 0, "Weak Bull": 1, "Ranging": 2, "Weak Bear": 3, "Strong Bear": 4, "Unknown": 5}
    sorted_results = sorted(results, key=lambda x: regime_order.get(x.get("regime", "Unknown"), 5))
    
    # Regime changes first
    changes = [r for r in sorted_results if r.get("regime_change")]
    if changes:
        lines.append("🔄 *Regime Changes This Week*")
        for r in changes:
            change_emoji = "🟢" if r["regime_change"] == "bullish" else "🔴"
            lines.append(f"{change_emoji} *{r['symbol']}* flipped to {r['regime_change']}")
        lines.append("")
    
    lines.append("*Weekly Regime Status*")
    
    for r in sorted_results:
        if "error" in r:
            continue
        
        # Emoji for regime
        regime_emoji = {
            "Strong Bull": "🟢",
            "Weak Bull": "🟡",
            "Ranging": "⚪",
            "Weak Bear": "🟠",
            "Strong Bear": "🔴"
        }.get(r["regime"], "❓")
        
        # Price formatting
        if r["price"] >= 1000:
            price_str = f"${r['price']:,.0f}"
        elif r["price"] >= 1:
            price_str = f"${r['price']:,.2f}"
        else:
            price_str = f"${r['price']:,.4f}"
        
        # Weekly change emoji
        change_emoji = "📈" if r["change_wtd"] > 0 else "📉" if r["change_wtd"] < 0 else "➡️"
        
        lines.append(f"{regime_emoji} *{r['symbol']}* {price_str} {change_emoji} {r['change_wtd']:+.1f}% (wk)")
        lines.append(f"   _{r['regime']}_ | ADX: {r['adx']:.1f} | {r['direction'].capitalize()}")
        
        if r["funding_rate"] is not None:
            funding_emoji = "🔥" if abs(r["funding_rate"]) > 0.01 else ""
            lines.append(f"   Funding: {r['funding_rate']:+.4f}% {funding_emoji}")
        
        lines.append("")
    
    # Summary
    bull_count = sum(1 for r in sorted_results if "Bull" in r.get("regime", ""))
    bear_count = sum(1 for r in sorted_results if "Bear" in r.get("regime", ""))
    range_count = sum(1 for r in sorted_results if r.get("regime") == "Ranging")
    
    lines.append(f"📈 Bulls: {bull_count} | 📉 Bears: {bear_count} | ⚪ Range: {range_count}")
    
    return "\n".join(lines)


def main(timeframe: str = "daily"):
    """Main entry point."""
    if timeframe == "weekly":
        print("Fetching weekly market data...", file=sys.stderr)
        
        results = []
        for asset in CONFIG["watchlist"]:
            print(f"  Analyzing {asset['symbol']} (weekly)...", file=sys.stderr)
            result = analyze_asset_weekly(asset)
            results.append(result)
        
        print("\n" + "="*50 + "\n", file=sys.stderr)
        report = format_weekly_report(results)
        print(report)
    else:
        print("Fetching market data...", file=sys.stderr)
        
        results = []
        for asset in CONFIG["watchlist"]:
            print(f"  Analyzing {asset['symbol']}...", file=sys.stderr)
            result = analyze_asset(asset)
            results.append(result)
        
        print("\n" + "="*50 + "\n", file=sys.stderr)
        report = format_report(results)
        print(report)
    
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate crypto regime reports")
    parser.add_argument("--weekly", action="store_true", help="Generate weekly report instead of daily")
    parser.add_argument("--config", type=str, help="Path to custom config.json file")
    args = parser.parse_args()
    
    # Override config if provided
    if args.config:
        CONFIG_PATH_OVERRIDE = Path(args.config)
        with open(CONFIG_PATH_OVERRIDE) as f:
            CONFIG_OVERRIDE = json.load(f)
        # Replace global CONFIG
        globals()["CONFIG"] = CONFIG_OVERRIDE
        globals()["CONFIG_PATH"] = CONFIG_PATH_OVERRIDE
    
    main(timeframe="weekly" if args.weekly else "daily")
