/**
 * Order Service (orderService.js)
 * High-level trading actions.
 */

class OrderService {
    constructor(adapter) {
        this.adapter = adapter;
    }

    async marketBuy(market, totalKRW) {
        return this.adapter.placeOrder({
            market,
            side: 'bid',
            price: totalKRW.toString(),
            ord_type: 'price'
        });
    }

    async marketSell(market, volume) {
        return this.adapter.placeOrder({
            market,
            side: 'ask',
            volume: volume.toString(),
            ord_type: 'market'
        });
    }

    async getOrder(uuid) {
        return this.adapter.getOrder(uuid);
    }
}

module.exports = OrderService;
