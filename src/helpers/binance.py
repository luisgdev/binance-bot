from urllib import parse
from helpers import auth
import requests
import hashlib
import json
import hmac


# SETTINGS
url = 'https://api.binance.com'
public_endpoint = {
    "time": "/api/v3/time",
    "avgprice": "/api/v3/avgPrice",
    "ticker_24h": "/api/v3/ticker/24hr",
    "ticker_price": "/api/v3/ticker/price"
}
signed_endpoint = {
    "account": "/api/v3/account",
    "order_test": "/api/v3/order/test",
    "order": "/api/v3/order",
    "mytrades": "/api/v3/myTrades"
}

#   GENERATE A SIGNATURE
# =============================
def create_signature():
    secret_key = auth.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    # The only param is timestamp
    params = {
        "timestamp": server_time
    }
    # Create Signature
    signature = hmac.new(
        secret_key.encode('utf-8'), 
        parse.urlencode(params).encode('utf-8'), 
        hashlib.sha256).hexdigest()    
    # Add signature to params
    params["signature"] = signature
    return params


#   GET PARAMS SIGNED
# =============================
def sign_params(params):
    secret_key = auth.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    # Add timestamp to params
    params['timestamp'] = server_time
    # Create Signature
    signature = hmac.new(
        secret_key.encode('utf-8'), 
        parse.urlencode(params).encode('utf-8'), 
        hashlib.sha256).hexdigest()
    return {"signature": signature}


#   GET ACCOUNT INFORMATION
# =============================
def get_account():
    api_key = auth.get_key('apiKey')
    signed_params = create_signature()
    response = requests.get(
        url + signed_endpoint['account'], 
        params=signed_params, 
        headers={"X-MBX-APIKEY": api_key})
    result = response.json()
    return result


#   GET TRADES  of a certain pair
# ===============================
def get_trades(coin):
    api_key = auth.get_key('apiKey')
    params = {
        "symbol": coin
    }
    params.update(sign_params(params))
    response = requests.get(
        url + signed_endpoint['mytrades'], 
        params=params, 
        headers={"X-MBX-APIKEY": api_key})
    result = response.json()
    return result


# CREATE AN ORDER  side:BUY/SELL
# ==============================
def order(symbol, side, ordertype, quantity, price):
    api_key = auth.get_key('apiKey')
    params = {
        "symbol": symbol,
        "side": side,
        "type": ordertype
    }
    if side == 'BUY':
        params['quoteOrderQty'] = quantity
    else:
        params['timeInForce'] = 'GTC'
        params['price'] = price
        params['quantity'] = quantity
    params.update(sign_params(params))
    response = requests.post(
        url + signed_endpoint['order'], 
        params=params, 
        headers={"X-MBX-APIKEY": api_key})
    return response


#   GET PUBLIC DATA  no sign nedded
# =================================
def get_public(coin, api_function):
    params = {
        "symbol": coin
    }
    response = requests.get(
        url + public_endpoint[api_function], 
        params=params)
    result = response.json()
    return result


if __name__ == "__main__":
    print('This is not main!')
