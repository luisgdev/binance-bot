from helpers import binance
import logging as log
import time
import views


def show_account():
    res = binance.req_account()
    try:
        views.order(res.json())
    except Exception as e:
        print(f'*** ERROR FOUND: {e}')
        print(f'*** RESULT: {res}')


def show_balance():
    views.balance()


def show_symbol(symbol):
    views.symbol_price(symbol)


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


def order_test():
    coin = 'TRX'
    response = test(coin, 'SELL', '1100', '0.00000088')
    if 'orderId' in response:
        # BUY
        buy_price = response['fills'][0]['price']
        print(f'*** EXECUTING ORDER {response["status"]}')
        print(f'BUY price = {buy_price}')
        sell_price = round(float(buy_price) * 1.01, 8)
        # SELL at 1.01
        print(f'SELL at = {sell_price}')
        qty = response['fills'][0]['qty']
        time.sleep(3)
        sell_response = test(coin, 'SELL', qty, sell_price)
        print(f'SELL RESPONSE:\n{sell_response}')
    else:
        print(f'*** ORDER FAILED:\n{response}')


if __name__ == "__main__":
    # Log settings
    log_format = '%(asctime)s - %(message)s'
    log.basicConfig(filename='server.log', format=log_format, level=log.DEBUG)
    # === Start counting elapsed time
    init_time = time.perf_counter()
    # DO THE THING
    #test('SFP', 'BUY', 0.00095340, 0.000032)
    show_balance()
    show_symbol('SFP')
    # === Stop counting elapsed time
    elapsed = round(time.perf_counter() - init_time, 2)
    print(f'*** Elapsed time: {elapsed} s ***\n.')