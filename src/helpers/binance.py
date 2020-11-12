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
    "averagePrice": "/api/v3/avgPrice",
    "ticker24h": "/api/v3/ticker/24hr",
    "ticker": "/api/v3/ticker/price"
}
signed_endpoint = {
    "account": "/api/v3/account",
    "test_order": "/api/v3/order/test",
    "order": "/api/v3/order"
}

# =============================
# GET A SIMPLE SIGNATURE
# =============================
def create_signature():
    secret_key = auth.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    params = {
        "timestamp": server_time
    }
    # Generate Signature
    signature = hmac.new(secret_key.encode('utf-8'), parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()    
    params["signature"] = signature
    return params


# =============================
# GET PARAMS SIGNED
# =============================
def sign_params(params):
    secret_key = auth.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    params['timestamp'] = server_time
    # Generate Signature
    signature = hmac.new(secret_key.encode('utf-8'), parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()    
    res = {
        "signature": signature
    }
    return res


# =============================
# GET ACCOUNT DATA
# =============================
def req_account():
    api_key = auth.get_key('apiKey')
    endpoint = signed_endpoint['account']
    signed_params = create_signature()
    response = requests.get(url + endpoint, params=signed_params, headers={"X-MBX-APIKEY": api_key})
    result = response.json()
    return result


# ==============================
# CREATE AN ORDER  side:BUY/SELL
# ==============================
def order(symbol, side, ordertype, quantity, price):
    api_key = auth.get_key('apiKey')
    endpoint = signed_endpoint['order']
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
    response = requests.post(url + endpoint, params=params, headers={"X-MBX-APIKEY": api_key})
    #result = response.json()
    return response


# =============================
# GET PUBLIC DATA FROM API
# =============================
def req_public(coin, api_url):
    endpoint = public_endpoint[api_url]
    params = {
        "symbol": coin
    }
    response = requests.get(url + endpoint, params=params)
    result = response.json()
    return result


if __name__ == "__main__":
    print('This is not main!')
