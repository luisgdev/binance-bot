import binhelper
import time


def show_account():
    data = binhelper.req_account()
    print('===== PERMISIONS =====')
    print(f'Can trade: {data["canTrade"]}')
    print(f'Can deposit: {data["canDeposit"]}')
    print(f'Can wthdraw: {data["canWithdraw"]}')
    print('===== FEES =====')
    print(f'Maker commission: {data["makerCommission"]}')
    print(f'Taker commission: {data["takerCommission"]}')
    print(f'Buyer commission: {data["buyerCommission"]}')
    print(f'Seller commission: {data["sellerCommission"]}')
    print('===== BALANCES =====')
    for item in data["balances"]:
        if float(item["free"]) > 0:
            print(f'{item["asset"]} balance: {item["free"]}')


def test2():
    data = binhelper.req_account()
    print(data)


def test():
    print('==== TEST ====')
    #print(show_account())
    #print(f'Average price (5m): {binhelper.req_public('BNBBTC', 'averagePrice')})
    ticker24 = binhelper.req_public('BNBBTC', 'ticker24h')
    print(f'Bid: {ticker24["bidPrice"]}')
    print(f'Ask: {ticker24["askPrice"]}')
    res = binhelper.order('BNBBTC', 'BUY', 'LIMIT', 0.1, float(ticker24['askPrice']))
    try:
        print(res.json())
    except Exception as e:
        print(res)
    #print(binhelper.req_public('BNBBTC', 'ticker'))


if __name__ == "__main__":
    # Start counting elapsed time
    init_time = time.perf_counter()
    # DO THE THING
    test()
    # Stop counting elapsed time
    elapsed = round(time.perf_counter() - init_time, 2)
    print(f'*** Elapsed time: {elapsed} s ***\n.')