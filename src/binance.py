import hashlib
import hmac
from os import environ
import sys
from typing import Callable, Dict, List, Optional
from urllib import parse

import pydantic
import requests
from dotenv import load_dotenv

from models import Account, AvgPrice, NewOrder, Order, Ticker, Trade

load_dotenv()


class Public(object):
    """
    Binance API Endpoints which don't require auth.
    Public endpoints.
    """
    time: str = "/api/v3/time"
    avg_price: str = "/api/v3/avgPrice"
    ticker_24h: str = "/api/v3/ticker/24hr"
    last_price: str = "/api/v3/ticker/price"


class Private(object):
    """
    Binance API Endpoints which require auth.
    Private endpoints, signed requests are nedded.
    """
    account: str = "/api/v3/account"
    order_test: str = "/api/v3/order/test"
    order: str = "/api/v3/order"
    my_trades: str = "/api/v3/myTrades"
    open_orders: str = "/api/v3/openOrders"


class Binance:
    """
    Binance HTTP API v3
    """

    def __init__(self):
        self.base_url: str = "https://api3.binance.com"
        self.api_key: str = environ["API_KEY"]
        self.secret_key: str = environ["SECRET_KEY"]
    
    def _get_url(self, endpoint: str):
        return self.base_url + endpoint

    def _get_public(self, symbol: Optional[str], api_endpoint: str) -> dict:
        params = {"symbol": symbol} if symbol else {}
        response: dict = requests.get(
            url=self._get_url(api_endpoint), params=params
        ).json()
        return response

    def _sign_params(self, params: dict = {}) -> dict:
        response: dict = self._get_public(None, Public.time)
        params["timestamp"] = response["serverTime"]
        signature: str = hmac.new(
            str.encode(self.secret_key),
            str.encode(parse.urlencode(params)),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def get_avg_price(self, symbol: str) -> AvgPrice:
        data: dict = self._get_public(symbol, Public.avg_price)
        try:
            price: AvgPrice = AvgPrice(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(data)
            sys.exit()
        return price

    def get_latest_price(self, symbol: str) -> Ticker:
        data: dict = self._get_public(symbol, Public.last_price)
        try:
            price: Ticker = Ticker(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(data)
            sys.exit()
        return price

    def get_account(self) -> Account:
        response: dict = requests.get(
            url=self._get_url(Private.account),
            params=self._sign_params(),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        try:
            data: Account = Account(**response)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(response)
            sys.exit()
        return data

    def get_trades(self, symbol: str) -> List[Trade]:
        response: dict = requests.get(
            url=self._get_url(Private.my_trades),
            params=self._sign_params({"symbol": symbol}),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        try:
            update: Callable[[dict], Trade] = lambda t: Trade(**t)
            data: List[Trade] = list(map(update, response))
        except Exception as err:
            print(f"*** Error: {err.args}")
            print(response)
            sys.exit()
        return data

    def get_open_orders(self) -> List[Order]:
        response: dict = requests.get(
            url=self._get_url(Private.open_orders),
            params=self._sign_params(),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        try:
            update: Callable[[dict], Order] = lambda x: Order(**x)
            data: List[Order] = list(map(update, response))
        except pydantic.error_wrappers.ValidationError:
            print("*** ValidationError")
        except Exception as err:
            print(f"*** Error: {err.args}")
        finally:
            print(response)
            sys.exit()
        return data

    def cancel_open_order(self, symbol: str, order_id: int) -> Order:
        response: dict = requests.delete(
            url=self._get_url(Private.order),
            params=self._sign_params({"symbol": symbol, "orderId": order_id}),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        return Order(**response)

    def create_order(self, order: NewOrder) -> Order:
        """
        MARKET orders using the `quantity`:
            Using BTCUSDT for example, sending a MARKET order will
            specify how much BTC the user is buying or selling.
        MARKET orders using `quoteOrderQty`:
            Using BTCUSDT for example, sending a MARKET order will
            specify how much USDT the user is going to spend or receive.
        """
        params: dict = {"symbol": order.symbol, "side": order.side}
        # Let's use MARKET orders to BUY...
        # ... And LIMIT orders to SELL
        if order.type_ in ["M", "MARKET"]:
            params["type"] = "MARKET"
            # params["quoteOrderQty"] = order.qty
        elif order.type_ in ["L", "LIMIT"]:
            params["type"] = "LIMIT"
            params["timeInForce"] = "GTC"
            params["price"] = order.price
        params["quantity"] = order.qty
        response: dict = requests.post(
            url=self._get_url(Private.order),
            params=self._sign_params(params),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        try:
            data: Order = Order(**response)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(response)
            sys.exit()
        return data


if __name__ == "__main__":
    print("This is not main!")
