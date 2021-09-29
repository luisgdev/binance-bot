from typing import List, Optional

from binance import Binance
from models import Account, AvgPrice, NewOrder, Order, Ticker, Trade

b: Binance = Binance()


def account() -> None:
    account: Account = b.get_account()
    print("===== PERMISIONS =====")
    print(f"Can trade: {account.can_trade}")
    print(f"Can deposit: {account.can_deposit}")
    print(f"Can wthdraw: {account.can_withdraw}")
    print("===== FEES =====")
    print(f"Maker commission: {account.maker_commission}")
    print(f"Taker commission: {account.taker_commission}")
    print(f"Buyer commission: {account.buyer_commission}")
    print(f'Seller commission: {account.seller_commission}\n{"--"*15}')


def balance() -> None:
    account: Account = b.get_account()
    print("======= BALANCES ========")
    for balance in account.balances:
        if float(balance.free) > 0:
            print(f"{balance.asset}: {balance.free}")
    print("--" * 15)


def order() -> None:
    symbol: str = input("Symbol (E.g. BNBUSDT): ").upper()
    side: str = input("Buy or Sell? (b/s): ")
    qty: float = float(input("Quantity: "))
    price: Optional[float]
    if side in ["s", "S"]:
        side = "sell"
        price = float(input("Price: "))
    elif side in ["b", "B"]:
        side = "buy"
        price = None
    else:
        assert "Order ´side´ must be 'BUY' or 'SELL' only"
        print("Error: Order ´side´ must be 'BUY' or 'SELL'.")
        return None
    order: Order = b.create_order(
        NewOrder(symbol=symbol, side=side, qty=qty, price=price)
    )
    print(f'{"--"*15}\nOrder ID: {order.order_id}')
    print(f"Status: {order.status}")
    print(f"Executed Qty: {order.executed_qty}")
    if order.fills:
        for f in order.fills:
            print(f" * Price: {f.price}")
            print(f" * Quantity: {f.qty}")
            print(f' * Fee ({f.commission_asset}): {f.commission}\n{"--"*15}')


def symbol_price(symbol: str) -> None:
    average: AvgPrice = b.get_avg_price(symbol)
    latest: Ticker = b.get_latest_price(symbol)
    print(f'{"--"*15}\n{symbol}')
    print(f" * Latest Price: {latest.price}")
    print(f' * Average 5min: {average.price}\n{"--"*15}')


def _trades(pair: str) -> None:
    trades: List[Trade] = b.get_trades(pair)
    for t in trades:
        if t.is_buyer:
            avg: AvgPrice = b.get_avg_price(pair)
            roi: float = (float(avg.price) / float(t.price) - 1) * 100
            print(f"{pair} | {t.price} | {avg.price} | {round(roi, 2)}")
            break


def profit_stats(pairs: List[str]) -> None:
    print("Pair | Buy Price | Current Price | Profit")
    for p in pairs:
        _trades(p)


if __name__ == "__main__":
    print("This is not main!")
