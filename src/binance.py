import hashlib
import hmac
from os import environ
import sys
from typing import Callable, Dict, List, Optional
from urllib import parse
import pydantic

import requests
from dotenv import load_dotenv
from requests.models import Response

from models import Account, AvgPrice, NewOrder, Order, Ticker, Trade

load_dotenv()

# Public and Private endpoints
public: Dict[str, str] = {
    "time": "/api/v3/time",
    "avg_price": "/api/v3/avgPrice",
    "ticker_24h": "/api/v3/ticker/24hr",
    "last_price": "/api/v3/ticker/price",
}
private: Dict[str, str] = {
    "account": "/api/v3/account",
    "order_test": "/api/v3/order/test",
    "order": "/api/v3/order",
    "my_trades": "/api/v3/myTrades",
    "open_orders": "/api/v3/openOrders",
}


class Binance:
    """
    Binance HTTP API v3
    """

    def __init__(self):
        self.url: str = "https://api.binance.com"
        self.api_key: str = environ["API_KEY"]
        self.secret_key: str = environ["SECRET_KEY"]

    def _get_public(self, symbol: Optional[str], api_function: str) -> dict:
        params = {"symbol": symbol} if symbol else {}
        response: dict = requests.get(
            url=self.url + public[api_function], params=params
        ).json()
        return response

    def _sign_params(self, params: dict = {}) -> dict:
        response: dict = self._get_public(None, "time")
        params["timestamp"] = response["serverTime"]
        signature: str = hmac.new(
            str.encode(self.secret_key),
            str.encode(parse.urlencode(params)),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def get_avg_price(self, symbol: str) -> AvgPrice:
        data: dict = self._get_public(symbol, "avg_price")
        try:
            price: AvgPrice = AvgPrice(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(data)
            sys.exit()
        return price

    def get_latest_price(self, symbol: str) -> Ticker:
        data: dict = self._get_public(symbol, "last_price")
        try:
            price: Ticker = Ticker(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(data)
            sys.exit()
        return price

    def get_account(self) -> Account:
        response: dict = requests.get(
            url=self.url + private["account"],
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
            url=self.url + private["my_trades"],
            params=self._sign_params({"symbol": symbol}),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        update: Callable[[dict], Trade] = lambda t: Trade(**t)
        try:
            data: List[Trade] = list(map(update, response))
        except pydantic.error_wrappers.ValidationError:
            print("*** ValidationError")
            print(response)
            sys.exit()
        return data

    def get_open_orders(self) -> List[Order]:
        response: dict = requests.get(
            url=self.url + private["open_orders"],
            params=self._sign_params(),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        update: Callable[[dict], Trade] = lambda x: Order(**x)
        try:
            data: List[Order] = list(map(update, response))
        except pydantic.error_wrappers.ValidationError:
            print("*** ValidationError")
            print(response)
            sys.exit()
        return data

    def cancel_open_order(self, symbol: str, order_id: int) -> Order:
        response: dict = requests.delete(
            url=self.url + private["order"],
            params=self._sign_params({"symbol": symbol, "orderId": order_id}),
            headers={"X-MBX-APIKEY": self.api_key},
        ).json()
        return Order(**response)

    def create_order(self, order: NewOrder) -> Order:
        """
        MARKET orders using the ´quantity´:
            Using BTCUSDT for example, sending a MARKET order will
            specify how much BTC the user is buying or selling.
        MARKET orders using ´quoteOrderQty´:
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
            url=self.url + private["order"],
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
