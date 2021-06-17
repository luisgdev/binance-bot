from helpers import binance
import logging as log
import time
import views


def show_account():
    res = binance.get_account()
    try:
        views.order(res.json())
    except Exception as e:
        print(f'*** ERROR FOUND: {e}')
        print(f'*** RESULT: {res}')


def test(coin, side, qty, price):
    symbol = f'{coin}BTC'
    print(f'===== {side} {symbol} =====')
    views.symbol_price(coin)
    # Settings
    if side == 'BUY':
        order_type = 'MARKET'
        # When buying quantity is in btc
        quantity = qty
    else:
        order_type = 'LIMIT'
        # When buying quantity is in assets
        quantity = qty
    # PLACE ORDER
    res = binance.order(symbol, side, order_type, quantity, price)
    try:
        views.order(res.json())
        return res.json()
    except Exception as e:
        print(f'*** ERROR: {res}\n{e}')
        return res


if __name__ == "__main__":
    # Log settings
    log_format = '%(asctime)s - %(message)s'
    log.basicConfig(filename='server.log', format=log_format, level=log.DEBUG)
    init_time = time.perf_counter()
    # --------------------------------
    # Menu Interface
    command = ''
    while command != 'x':
        print(f'{"--"*15}\n*** BINANCE BOT ***\n{"--"*15}')
        menu = ' a) Account Balance\n b) Price of a coin\n c) Profit Stats\n x) Exit'
        command = input(f'{menu}\n > ').lower()
        if command == 'a':
            views.balance()
        elif command == 'b':
            coin = input('> Coin symbol: ').upper()
            views.symbol_price(coin)
        elif command == 'c':
            pairs = input('Enter pairs p1,p2,pn: ').upper()
            views.profit_stats(pairs.replace(' ', '').split(','))
        command = input('> Any key to continue: ').lower()
    # --------------------------------
    elapsed = round(time.perf_counter() - init_time, 2)
    print(f'*** Elapsed time: {elapsed} s ***\n.')
