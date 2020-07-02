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


def test():
    print('==== TEST ====')
    print(binhelper.req_public('ONGBTC', 'averagePrice'))
    print(binhelper.req_public('ONGBTC', 'ticker24h'))


if __name__ == "__main__":
    # Start counting elapsed time
    init_time = time.perf_counter()
    # DO THE THING
    test()
    # Stop counting elapsed time
    elapsed = round(time.perf_counter() - init_time, 2)
    print(f'*** Elapsed time: {elapsed} s ***\n.')