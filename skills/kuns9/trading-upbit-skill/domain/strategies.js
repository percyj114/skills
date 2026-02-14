/**
 * Strategy Logic (strategies.js)
 */

/**
 * 변동성 돌파 전략 (Volatility Breakout)
 */
function volatilityBreakout(current, range, k = 0.5) {
    const target = current.opening + (range * k);
    if (current.price > target) {
        return { signal: 'BUY', target };
    }
    return { signal: 'HOLD', target };
}

module.exports = {
    volatilityBreakout
};
