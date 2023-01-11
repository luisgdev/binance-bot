""" Main function """

import sys
from typing import List, Optional, Tuple

import inquirer

import views
from binance import Binance
from models import Account, AvgPrice, NewOrder, Order, Profit, Trade

binance: Binance = Binance()

OPTIONS: Tuple[str] = (
    "Account",
    "Balance",
    "Price of coin",
    "Profit Stats",
    "New Order",
    "Open orders",
    "Cancel order",
    "Exit",
)


def account_interface() -> None:
    """
    Query and show account information.
    :return: None
    """
    account: Account = binance.get_account()
    views.show_account(account=account)
    main_interface()


def balance_interface() -> None:
    """
    Query and show current balance.
    :return: None
    """
    account: Account = binance.get_account()
    views.show_balance(account=account)
    main_interface()


def _calc_profit(trades: List[Trade]) -> Profit:
    """
    Calc profit.
    :param trades: List of Trade object.
    :return: Profit object.
    """
    for trade in trades:
        total_qty_buy: float = sum(
            float(trade.qty) for trade in trades if trade.is_buyer
        )
        total_qty_sell: float = sum(
            float(trade.qty) for trade in trades if not trade.is_buyer
        )
        total_value_buy: float = sum(
            float(trade.quote_qty) for trade in trades if trade.is_buyer
        )
        total_value_sell: float = sum(
            float(trade.quote_qty) for trade in trades if not trade.is_buyer
        )
    symbol: str = trades[0].symbol
    total_qty: float = total_qty_buy - total_qty_sell
    total_value: float = total_value_buy - total_value_sell
    avg: AvgPrice = binance.get_avg_price(symbol)
    current_value: float = float(avg.price) * total_qty
    return Profit(
        symbol=symbol,
        qty=total_qty,
        buy_value=total_value,
        current_value=current_value,
    )


def profits_interface() -> None:
    """
    CLI interface for coin price.
    :return: None
    """
    question = [
        inquirer.Text(
            name="pairs",
            message="Pairs (E.g. BTCUSDT,ETHUSDT)",
        )
    ]
    answer = inquirer.prompt(question)
    pairs: List[str] = answer["pairs"].replace(" ", "").split(",")
    profits: List[Profit] = []
    for pair in pairs:
        trades: List[Trade] = binance.get_trades(symbol=pair)
        profits.append(_calc_profit(trades))
    views.profit_stats(profits)
    main_interface()


def price_interface():
    """
    CLI interface for coin price.
    :return: None
    """
    question = [
        inquirer.Text(
            name="symbol",
            message="Coin symbol (E.g. BTCUSDT)",
        )
    ]
    answer = inquirer.prompt(question)
    views.symbol_price(symbol=answer["symbol"])
    main_interface()


def place_order_interface() -> None:
    """
    CLI interface for making orders.
    :return: None
    """
    price: Optional[float] = None
    order_type_question = [
        inquirer.List(
            name="type",
            message="Want a fixed price (LIMIT) or market price (MARKET)?",
            choices=["LIMIT", "MARKET"],
        ),
    ]
    questions = [
        inquirer.Text(
            name="symbol",
            message="Coin symbol (E.g. BTCUSDT)",
        ),
        inquirer.List(
            name="side",
            message="Want to buy or sell?",
            choices=["BUY", "SELL"],
        ),
        inquirer.Text(name="qty", message="Quantity"),
    ]
    price_question = inquirer.Text(name="price", message="Order price")
    order_type = inquirer.prompt(order_type_question)["type"]
    if order_type == "LIMIT":
        questions.append(price_question)
    answers = inquirer.prompt(questions)
    new_order = NewOrder(
        symbol=answers["symbol"],
        side=answers["side"],
        type_=order_type,
        qty=answers["qty"],
        price=price if "price" not in answers else answers["price"],
    )
    order: Order = binance.create_order(order=new_order)
    views.place_order(order=order)
    main_interface()


def open_orders_interface() -> None:
    """
    Show a list of open orders.
    :return: None.
    """
    orders: List[Order] = binance.get_open_orders()
    views.open_orders(orders=orders)
    main_interface()


def cancel_order_interface() -> None:
    """
    Cancel an open order.
    :return: None.
    """
    open_orders_interface()
    questions = [
        inquirer.Text(
            name="symbol",
            message="Coin symbol (E.g. BTCUSDT)",
        ),
        inquirer.Text(
            name="order_id",
            message="Order ID",
        ),
    ]
    answers = inquirer.prompt(questions)
    order: Order = binance.cancel_open_order(
        symbol=answers["symbol"].upper(), order_id=int(answers["order_id"])
    )
    views.cancel_order(order=order)
    main_interface()


def main_interface() -> None:
    """
    CLI main.
    :return: None
    """
    actions = (
        account_interface,
        balance_interface,
        price_interface,
        profits_interface,
        place_order_interface,
        open_orders_interface,
        cancel_order_interface,
        sys.exit,
    )
    call_function: dict = dict(zip(OPTIONS, actions))
    views.print_markdown("## Binance bot")
    question = [
        inquirer.List(
            name="choice",
            message="Pick a choice.",
            choices=list(OPTIONS),
        )
    ]
    answer = inquirer.prompt(question)
    call_function[answer["choice"]]()


if __name__ == "__main__":
    main_interface()
