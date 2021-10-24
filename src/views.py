import logging as log
from typing import List, Optional

from binance import Binance
from models import Account, AvgPrice, NewOrder, Order, Ticker, Trade


# Log Settings
log.basicConfig(
    filename="binance.log",
    format="%(asctime)s %(filename)s:%(lineno)d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO
)

b: Binance = Binance()


def menu() -> None:
    print("""
    *** BINANCE BOT ***
      a) Account
      b) Balance
      c) Price of coin
      d) Profit Stats
      e) New Order
      x) Exit
    """)


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
    symbol: str = input(" * Symbol (E.g. BNBUSDT): ").upper()
    side: str = input(" * Buy or Sell?: ").upper()
    type_: str = input(" * Limit or Market?: ").upper()
    qty: float = float(input(" * Quantity: "))
    price: Optional[float]
    if type_ in ["L", "LIMIT"]:
        price = float(input(" * Price: "))
    elif type_ in ["M", "MARKET"]:
        price = None
    else:
        assert "Order ´type´ must be 'LIMIT' or 'MARKET' only"
        print("Error: Order ´type´ must be 'LIMIT' or 'MARKET'.")
        return None

    # Let's make SURE we want to BUY or SELL
    if side not in ["SELL", "BUY"]:
        assert "Order ´side´ must be 'BUY' or 'SELL' only"
        print("Error: Order ´side´ must be 'BUY' or 'SELL'.")
        return None
    order: Order = b.create_order(
        NewOrder(symbol=symbol, side=side, type_=type_, qty=qty, price=price)
    )
    log.info(f"ORDER DETAILS: {order.dict}")
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


def cancel_order() -> None:
    open_orders()
    print("--"*15)
    print("What order you want to cancel?")
    symbol: str = input("Symbol: ").upper()
    order_id: int = input("Order id: ")
    order: Order = b.cancel_open_order(symbol, order_id)
    print("--"*15)
    print(f"Order ID: {order.order_id}")
    print(f"Symbol  : {order.symbol}")
    print(f"Side    : {order.side}")
    print(f"Price   : {order.price}")
    print(f"Orig Qty: {order.orig_qty}")
    print(f"Exec Qty: {order.executed_qty}")
    print(f"Status  : {order.status}")


def open_orders() -> None:
    orders: List[Order] = b.get_open_orders()
    for order in orders:
        print("--"*15)
        print(f"Order ID: {order.order_id}")
        print(f"Symbol  : {order.symbol}")
        print(f"Side    : {order.side}")
        print(f"Price   : {order.price}")
        print(f"Orig Qty: {order.orig_qty}")
        print(f"Exec Qty: {order.executed_qty}")
        print(f"Status  : {order.status}")

if __name__ == "__main__":
    print("This is not main!")
    menu()