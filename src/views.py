import logging as log
from typing import List, Optional

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from binance import Binance
from models import Account, AvgPrice, NewOrder, Order, Ticker, Trade


# Log Settings
log.basicConfig(
    filename="binance.log",
    format="%(asctime)s %(filename)s:%(lineno)d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)

binance: Binance = Binance()
CONSOLE: Console = Console()

MENU: str = """
# *** BINANCE BOT ***
- a) Account
- b) Balance
- c) Price of coin
- d) Profit Stats
- e) New Order
- f) Open orders
- g) Cancel order
- x) Exit
"""

def print_markdown(text: str) -> None:
    """
    Print a string in Markdown format.
    """
    md: Markdown = Markdown(text)
    CONSOLE.print(md)


def menu() -> None:
    """
    Show program menu.
    """
    print_markdown(MENU)


def account() -> None:
    """
    Show account information.
    """
    account: Account = binance.get_account()
    print("===== PERMISIONS =====")
    print(f"Can trade: {account.can_trade}")
    print(f"Can deposit: {account.can_deposit}")
    print(f"Can wthdraw: {account.can_withdraw}")
    print("===== FEES =====")
    print(f"Maker commission: {account.maker_commission}")
    print(f"Taker commission: {account.taker_commission}")
    print(f"Buyer commission: {account.buyer_commission}")
    print(f"Seller commission: {account.seller_commission}")
    print_markdown("---")


def balance() -> None:
    """
    Show balances.
    """
    account: Account = binance.get_account()
    print("======= BALANCES ========")
    for balance in account.balances:
        if float(balance.free) > 0:
            print(f"{balance.asset}: {balance.free}")
    print_markdown("---")


def order() -> None:
    """
    Place an order and show the details.
    """
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
        assert "Order `type` must be 'LIMIT' or 'MARKET' only"
        print("Error: Order `type` must be 'LIMIT' or 'MARKET'.")
        return None

    # Let's make SURE we want to BUY or SELL
    if side not in ["SELL", "BUY"]:
        assert "Order `side` must be 'BUY' or 'SELL' only"
        print("Error: Order `side` must be 'BUY' or 'SELL'.")
        return None
    order: Order = binance.create_order(
        NewOrder(symbol=symbol, side=side, type_=type_, qty=qty, price=price)
    )
    log.info(f"ORDER DETAILS: {order.dict}")
    print(f'{"--"*15}\nOrder ID: {order.order_id}')
    print(f"Status: {order.status}")
    print(f"Executed Qty: {order.executed_qty}")
    if order.fills:
        for fill in order.fills:
            print(f" * Price: {fill.price}")
            print(f" * Quantity: {fill.qty}")
            print(f' * Fee ({fill.commission_asset}): {fill.commission}')
            print_markdown("---")


def symbol_price(symbol: str) -> None:
    average: AvgPrice = binance.get_avg_price(symbol)
    latest: Ticker = binance.get_latest_price(symbol)
    print(f"{symbol}")
    print(f" * Latest Price: {latest.price}")
    print(f" * Average 5min: {average.price}")
    print_markdown("---")


def _trades(pair: str) -> None:
    trades: List[Trade] = binance.get_trades(pair)
    for trade in trades:
        if trade.is_buyer:
            avg: AvgPrice = binance.get_avg_price(pair)
            roi: float = (float(avg.price) / float(trade.price) - 1) * 100
            print(f"{pair} | {trade.price} | {avg.price} | {round(roi, 2)}")
            break


def profit_stats(pairs: List[str]) -> None:
    print("Pair | Buy Price | Current Price | Profit")
    for pair in pairs:
        _trades(pair)


def cancel_order() -> None:
    open_orders()
    print_markdown("---")
    print("What order you want to cancel?")
    symbol: str = input("Symbol: ").upper()
    order_id: int = int(input("Order id: "))
    order: Order = binance.cancel_open_order(symbol, order_id)
    print_markdown("---")
    print(f"Order ID: {order.order_id}")
    print(f"Symbol  : {order.symbol}")
    print(f"Side    : {order.side}")
    print(f"Price   : {order.price}")
    print(f"Orig Qty: {order.orig_qty}")
    print(f"Exec Qty: {order.executed_qty}")
    print(f"Status  : {order.status}")


def open_orders() -> None:
    orders: List[Order] = binance.get_open_orders()
    for order in orders:
        print_markdown("---")
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
