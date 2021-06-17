from helpers import binance


def account():
    data = binance.get_account()
    print('===== PERMISIONS =====')
    print(f'Can trade: {data["canTrade"]}')
    print(f'Can deposit: {data["canDeposit"]}')
    print(f'Can wthdraw: {data["canWithdraw"]}')
    print('===== FEES =====')
    print(f'Maker commission: {data["makerCommission"]}')
    print(f'Taker commission: {data["takerCommission"]}')
    print(f'Buyer commission: {data["buyerCommission"]}')
    print(f'Seller commission: {data["sellerCommission"]}\n{"--"*15}')


def balance():
    data = binance.get_account()
    print('======= BALANCES ========')
    for item in data["balances"]:
        if float(item["free"]) > 0:
            print(f'{item["asset"]} balance: {item["free"]}')
    print('--' * 15)


def symbol_price(symbol):
    symbol = f'{symbol}'
    ticker24 = binance.get_public(symbol, 'ticker_24h')
    average = binance.get_public(symbol, 'avgprice')
    print(f'{"--"*15}\n{symbol}')
    print(f' * 24hr Bid: {ticker24["bidPrice"]}')
    print(f' * 24hr Ask: {ticker24["askPrice"]}')
    print(f' * 5min Avg: {average["price"]}\n{"--"*15}')


def order(data):
    print(f'{"--"*15}\nOrder ID: {data["orderId"]}')
    print(f'Status: {data["status"]}')
    print(f'Executed Qty: {data["executedQty"]}')
    fills = data['fills']
    for item in fills:
        print(f' * Price: {item["price"]}')
        print(f' * Quantity: {item["qty"]}')
        print(f' * Fee ({item["commissionAsset"]}): {item["commission"]}\n{"--"*15}')


def trades(coin):
    trades_list = binance.get_trades(coin)
    for item in trades_list:
        if item['isBuyer']:
            price = item["price"]
            average = binance.get_public(coin, 'avgprice')["price"]
            change = round( (float(average)/float(price) - 1)*100 ,2)
            print(f'{coin} | {price} | {average} | {change}')
            break


def profit_stats(pairs):
    print('Pair | Buy Price | Current Price | Profit')
    for item in pairs:
        trades(item)


if __name__ == "__main__":
    print('This is not main!')    
