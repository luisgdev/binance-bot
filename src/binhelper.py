from urllib import parse
import controller
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
def get_signature():
    secret_key = controller.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    # Generate Sign
    params = {
        "timestamp": server_time
    }
    signature = hmac.new(secret_key.encode('utf-8'), parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()    
    total_params = {
        "timestamp": server_time,
        "signature": signature
    }
    return total_params

# =============================
# GET ACCOUNT DATA
# =============================
def req_account():
    api_key = controller.get_key('apiKey')
    endpoint = signed_endpoint['account']
    headers = {
        "X-MBX-APIKEY": api_key
    }
    signed_params = get_signature()
    response = requests.get(url + endpoint, params=signed_params, headers=headers)
    result = response.json()
    return result


# =============================
# GET A SIGNATURE WITH PARAMS
# =============================
def signed_req(params):
    secret_key = controller.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    # Generate Sign
    params['timestamp'] = server_time
    print(f'PARAMS: {params}')
    signature = hmac.new(secret_key.encode('utf-8'), parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()    
    total_params = {
        "signature": signature
    }
    return total_params


# =============================
# CREATE AN ORDER
# =============================
def order(symbol, side, ordertype, quantity, price):
    server_time = requests.get(url + public_endpoint['time']).json()['serverTime']
    api_key = controller.get_key('apiKey')
    endpoint = signed_endpoint['order']
    headers = {
        "X-MBX-APIKEY": api_key
    }
    payload = {
        "symbol": symbol,
        "side": side,
        "type": ordertype,
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price
    }
    signed_params = signed_req(payload)
    payload.update(signed_params)
    print(f'SIGNED: {payload}')
    response = requests.post(url + endpoint, params=payload, headers=headers)
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
