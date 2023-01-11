""" Views """

import logging as log
from typing import List, Tuple

from rich.console import Console
from rich.markdown import Markdown

from binance import Binance
from models import Account, AvgPrice, Order, Profit, Ticker

# Log Settings
log.basicConfig(
    filename="binance.log",
    format="%(asctime)s %(filename)s:%(lineno)d - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)

binance: Binance = Binance()
CONSOLE: Console = Console()


def print_markdown(text: str) -> None:
    """
    Print a string in Markdown format.
    :return: None
    """
    md_text: Markdown = Markdown(text)
    CONSOLE.print(md_text)


def show_account(account: Account) -> None:
    """
    Show account information.
    :param account: Account object.
    :return: None
    """
    print_markdown("**Account info:**")
    lines: Tuple[str] = (
        "PERMISIONS",
        f"Can trade: {account.can_trade}",
        f"Can deposit: {account.can_deposit}",
        f"Can wthdraw: {account.can_withdraw}",
        "FEES",
        f"Maker commission: {account.maker_commission}",
        f"Taker commission: {account.taker_commission}",
        f"Buyer commission: {account.buyer_commission}",
        f"Seller commission: {account.seller_commission}",
        "---",
    )
    for line in lines:
        print_markdown(line)


def show_balance(account: Account) -> None:
    """
    Show balances.
    :param account: Account object.
    :return: None
    """
    print_markdown("**Current balance:**")
    for balance in account.balances:
        if float(balance.free) > 0:
            print(f"{balance.asset}: {balance.free}")
    print_markdown("---")


def place_order(order: Order) -> None:
    """
    Place an order and show the details.
    :param order: Order object.
    :return: None
    """
    log.info("ORDER DETAILS: %s", order.dict)
    print(f'{"--"*15}\nOrder ID: {order.order_id}')
    print(f"Status: {order.status}")
    print(f"Executed Qty: {order.executed_qty}")
    if order.fills:
        for fill in order.fills:
            print(f" * Price: {fill.price}")
            print(f" * Quantity: {fill.qty}")
            print(f" * Fee ({fill.commission_asset}): {fill.commission}")
            print_markdown("---")


def symbol_price(symbol: str) -> None:
    """
    Show the average and 5min price of a symbol.
    :param symbol: String with the symbol.
    :return: None
    """
    average: AvgPrice = binance.get_avg_price(symbol)
    latest: Ticker = binance.get_latest_price(symbol)
    print(f" * Latest Price: {latest.price}")
    print(f" * Average 5min: {average.price}")
    print_markdown("---")


def profit_stats(profits: List[Profit]) -> None:
    """
    List profit stats.
    :param pairs: List of Profit object.
    :return: None
    """
    if profits:
        print("Symbol | Buy Qty | Buy value | Current Price | Profit")
        for item in profits:
            item: Profit
            change: float = item.buy_value / item.current_value
            line: str = "\t".join(
                [
                    item.symbol,
                    str(round(item.qty, 8)),
                    str(round(item.buy_value, 2)),
                    str(round(item.current_value, 2)),
                    str(round(float(1 - change) * 100, 2)),
                ]
            )
            print(line)
    else:
        print("No trades found!")


def cancel_order(order: Order) -> None:
    """
    Cancel an order.
    :param order: Order object.
    :return: None
    """
    print_markdown("---")
    print(f"Order ID: {order.order_id}")
    print(f"Symbol  : {order.symbol}")
    print(f"Side    : {order.side}")
    print(f"Price   : {order.price}")
    print(f"Orig Qty: {order.orig_qty}")
    print(f"Exec Qty: {order.executed_qty}")
    print(f"Status  : {order.status}")


def open_orders(orders: List[Order]) -> None:
    """
    List open orders.
    :param: List of Order object.
    :return: None
    """
    if orders:
        for order in orders:
            print_markdown("---")
            print(f"Order ID: {order.order_id}")
            print(f"Symbol  : {order.symbol}")
            print(f"Side    : {order.side}")
            print(f"Price   : {order.price}")
            print(f"Orig Qty: {order.orig_qty}")
            print(f"Exec Qty: {order.executed_qty}")
            print(f"Status  : {order.status}")
    else:
        print("There are no open orders!")


if __name__ == "__main__":
    pass
