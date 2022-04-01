"""
MAIN INTERFACE
"""

import sys

import views

if __name__ == "__main__":
    command = ""
    while command != "x":
        print(
            """
    *** BINANCE BOT ***
    a) Account
    b) Balance
    c) Price of coin
    d) Profit Stats
    e) New Order
    f) Open orders
    g) Cancel order
    x) Exit """
        )
        command = input(" > ").lower()
        if command == "a":
            views.account()
        elif command == "b":
            views.balance()
        elif command == "c":
            coin = input("> Pair (E.g. BTCUSDT): ").upper()
            views.symbol_price(coin)
        elif command == "d":
            pairs = input("Pairs (E.g. CAKEBNB,BNBBTC): ").upper()
            views.profit_stats(pairs.replace(" ", "").split(","))
        elif command == "e":
            print("Creating New Order..")
            views.order()
        elif command == "f":
            print("Fetching open Orders..")
            views.open_orders()
        elif command == "g":
            print("Fetching open Orders..")
            views.cancel_order()
        elif command == "x":
            sys.exit()
        else:
            command = input("> Any key to continue: ").lower()
