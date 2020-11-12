from helpers import binance

def account():
    data = binance.req_account()
    print('===== PERMISIONS =====')
    print(f'Can trade: {data["canTrade"]}')
    print(f'Can deposit: {data["canDeposit"]}')
    print(f'Can wthdraw: {data["canWithdraw"]}')
    print('===== FEES =====')
    print(f'Maker commission: {data["makerCommission"]}')
    print(f'Taker commission: {data["takerCommission"]}')
    print(f'Buyer commission: {data["buyerCommission"]}')
    print(f'Seller commission: {data["sellerCommission"]}')


def balance():
    data = binance.req_account()
    print('===== BALANCES =====')
    for item in data["balances"]:
        if float(item["free"]) > 0:
            print(f'{item["asset"]} balance: {item["free"]}')


def symbol_price(symbol):
    symbol = f'{symbol}BTC'
    ticker24 = binance.req_public(symbol, 'ticker24h')
    print(f'{symbol} 24hr Ticker')
    print(f'Bid: {ticker24["bidPrice"]}')
    print(f'Ask: {ticker24["askPrice"]}')
    average = binance.req_public(symbol, 'averagePrice')
    print(f'{"--"*10}\n Average (5m): {average["price"]}')


def order(data):
    print(f'Order ID: {data["orderId"]}')
    print(f'Status: {data["status"]}')
    print(f'Executed Qty: {data["executedQty"]}')
    fills = data['fills']
    for item in fills:
        print(f'> Price: {item["price"]}')
        print(f'> Quantity: {item["qty"]}')
        print(f'> Fee ({item["commissionAsset"]}): {item["commission"]}')
        print('--' * 10)