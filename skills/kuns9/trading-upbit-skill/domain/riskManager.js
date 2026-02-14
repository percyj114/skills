/**
 * Risk Manager (riskManager.js)
 */

class RiskManager {
    constructor(adapter) {
        this.adapter = adapter;
    }

    async checkBuyFeasibility(market, budgetKRW) {
        const chance = await this.adapter.getOrdersChance(market);
        const krwBalance = parseFloat(chance.bid_account.balance);
        const minTotal = parseFloat(chance.market.bid.min_total);

        if (krwBalance < budgetKRW) {
            return { allow: false, reason: 'INSUFFICIENT_BALANCE', detail: `${krwBalance} < ${budgetKRW}` };
        }
        if (budgetKRW < minTotal) {
            return { allow: false, reason: 'UNDER_MIN_TOTAL', detail: `${budgetKRW} < ${minTotal}` };
        }

        return { allow: true };
    }

    async checkSellFeasibility(market) {
        const accounts = await this.adapter.getAccounts();
        const currency = market.split('-')[1];
        const asset = accounts.find(a => a.currency === currency);

        if (!asset || parseFloat(asset.balance) <= 0) {
            return { allow: false, reason: 'NO_ASSET_TO_SELL' };
        }
        return { allow: true, volume: asset.balance };
    }
}

module.exports = RiskManager;
