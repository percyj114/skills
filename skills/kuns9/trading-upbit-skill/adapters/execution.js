/**
 * Execution Adapter (execution.js)
 * High-level wrapper for OpenClaw tools.
 */

class ExecutionAdapter {
    constructor(tools) {
        this.tools = tools;
    }

    // --- Market Data ---

    async getMarkets(filterKRW = true) {
        return this.tools.getMarkets({ filterKRW });
    }

    async getCandles({ unit, market, count = 1, subUnit = 1 }) {
        return this.tools.getCandles({ unit, subUnit, market, count });
    }

    async getTickers(markets) {
        const marketsArray = Array.isArray(markets) ? markets : [markets];
        return this.tools.getTickers({ markets: marketsArray });
    }

    async getOrderbooks(markets) {
        const marketsArray = Array.isArray(markets) ? markets : [markets];
        return this.tools.getOrderbooks({ markets: marketsArray });
    }

    // --- Trading ---

    async placeOrder({ market, side, ord_type, price, volume }) {
        return this.tools.placeOrder({ market, side, ord_type, price, volume });
    }

    async getOrder(uuid) {
        return this.tools.getOrder({ uuid });
    }

    // --- Account / Risk ---

    async getAccounts() {
        return this.tools.getAccounts({});
    }

    async getOrdersChance(market) {
        return this.tools.getOrdersChance({ market });
    }

    // --- Storage ---

    async storageGet(key) {
        const result = await this.tools.storageGet({ key });
        return result?.value ? JSON.parse(result.value) : null;
    }

    async storageSet(key, value) {
        const stringValue = typeof value === 'string' ? value : JSON.stringify(value);
        return this.tools.storageSet({ key, value: stringValue });
    }
}

module.exports = ExecutionAdapter;
