import views

if __name__ == "__main__":
    # Menu Interface
    command = ""
    while command != "x":
        print(f'{"--"*15}\n*** BINANCE BOT ***\n{"--"*15}')
        menu = " a) Account\n b) Balance\n c) Price of coin\n"
        menu += " d) Profit Stats\n e) New Order\n x) Exit"
        command = input(f"{menu}\n > ").lower()
        if command in ["a", "A"]:
            views.account()
        elif command == "b":
            views.balance()
        elif command == "c":
            coin = input("> Pair (E.g. BTCUSDT): ").upper()
            views.symbol_price(coin)
        elif command == "d":
            pairs = input("Pairs (E.g. CAKEBNB,BNBBTC): ").upper()
            views.profit_stats(pairs.replace(" ", "").split(","))
        elif command in ["e", "E"]:
            print("Creating New Order.")
            views.order()
        command = input("> Any key to continue: ").lower()
