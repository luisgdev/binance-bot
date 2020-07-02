from urllib import parse
import controller
import requests
import hashlib
import json
import hmac


# SETTINGS
url = 'https://api.binance.com'
api = {
    "time": "/api/v3/time",
    "account": "/api/v3/account",
    "averagePrice": "/api/v3/avgPrice",
    "ticker24h": "/api/v3/ticker/24hr"
}


def get_signature():
    secret_key = controller.get_key('secretKey')
    # Get Server Timestamp
    server_time = requests.get(url + api['time']).json()['serverTime']
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


def req_account():
    api_key = controller.get_key('apiKey')
    endpoint = api['account']
    headers = {
        "X-MBX-APIKEY": api_key
    }
    signed_params = get_signature()
    response = requests.get(url + endpoint, params=signed_params, headers=headers)
    result = response.json()
    return result


def req_public(coin, api_url):
    endpoint = api[api_url]
    params = {
        "symbol": coin
    }
    response = requests.get(url+endpoint, params=params)
    result = response.json()
    return result


if __name__ == "__main__":
    print('This is not main!')
