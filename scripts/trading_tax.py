BASE_BROKER_FEE_SELL = 0.0271
TRANSACTION_TAX_SELL = 0.0337
BROKER_FEE_BUY = 0.005

def tax(
    buy_price, sell_price, 
    base_broker_fee_sell=BASE_BROKER_FEE_SELL,
    transaction_tax_sell=TRANSACTION_TAX_SELL,
    broker_fee_buy=BROKER_FEE_BUY,
    apply_fees=True
):
    gross_roi = (sell_price - buy_price) / buy_price
    if not apply_fees:
        return gross_roi
    total_buy = buy_price * (1 + broker_fee_buy)
    total_sell = sell_price * (1 - (base_broker_fee_sell + transaction_tax_sell))
    net_roi = (total_sell - total_buy) / total_buy
    return net_roi
