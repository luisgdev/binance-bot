""" Binance API functions """

import hashlib
import hmac
import sys
from os import environ
from typing import Callable, Dict, List, Optional
from urllib import parse

import pydantic
import requests
from dotenv import load_dotenv

from models import Account, AvgPrice, NewOrder, Order, Response, Ticker, Trade

load_dotenv()

TIMEOUT: int = 30
API_KEY_HEADER: str = "X-MBX-APIKEY"


class Public:
    """
    Binance API Endpoints which don't require auth.
    Public endpoints.
    """

    avg_price: str = "/api/v3/avgPrice"
    candle: str = "/api/v3/klines"
    last_price: str = "/api/v3/ticker/price"
    ticker_24h: str = "/api/v3/ticker/24hr"
    time: str = "/api/v3/time"


class Private:
    """
    Binance API Endpoints which require auth.
    Private endpoints, signed requests are nedded.
    """

    account: str = "/api/v3/account"
    my_trades: str = "/api/v3/myTrades"
    open_orders: str = "/api/v3/openOrders"
    order: str = "/api/v3/order"
    order_test: str = "/api/v3/order/test"


class Binance:
    """
    Binance HTTP API v3
    """

    def __init__(self):
        self.base_url: str = "https://api3.binance.com"
        self.api_key: str = environ["API_KEY"]
        self.secret_key: str = environ["SECRET_KEY"]

    def _get_url(self, endpoint: str) -> str:
        """
        Return a URL for a given endpoint.
        :param endpoint: String with the endpoint name.
        :return: String with endpoint URL.
        """
        return self.base_url + endpoint

    def _get_public(self, api_endpoint: str, params: dict = {}) -> dict:
        """
        Make a request to a public ednpoint and return the response data.
        :param api_endpoint: String with the endpoint name.
        :param params: Dict with the params.
        :return: Dict with the data.
        """
        response: dict = requests.get(
            url=self._get_url(api_endpoint), params=params, timeout=TIMEOUT
        ).json()
        return response

    def _sign_params(self, params: dict = {}) -> dict:
        """
        Generate signature with params.
        :param params: Dict with the params.
        :return: Dict with the signed params.
        """
        response: dict = self._get_public(api_endpoint=Public.time)
        print(f"Server time response: {response}")
        params["timestamp"] = response["serverTime"]
        signature: str = hmac.new(
            str.encode(self.secret_key),
            str.encode(parse.urlencode(params)),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def get_avg_price(self, symbol: str) -> AvgPrice:
        """
        Get average price of a cryptocurrency.
        :param symbol: String with the symbol.
        :return: AvgPrice object.
        """
        data: dict = self._get_public(
            params={"symbol": symbol}, api_endpoint=Public.avg_price
        )
        try:
            return AvgPrice(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(Response(**data))
            sys.exit()

    def get_latest_price(self, symbol: str) -> Ticker:
        """
        Get latest price of a cryptocurrency.
        :param symbol: String with the symbol.
        :return: Ticker object.
        """
        data: dict = self._get_public(
            params={"symbol": symbol}, api_endpoint=Public.last_price
        )
        try:
            return Ticker(**data)
        except pydantic.error_wrappers.ValidationError:
            print(f"*** ValidationError")
            print(Response(**data))
            sys.exit()

    def get_candlesticks(self, symbol: str) -> None:
        """
        Show candlesticks of a cryptocurrency.
        :param symbol: String with the symbol.
        :return: None.
        """
        # TODO: Determine lowest and highest values for a coin.
        params = dict(symbol=symbol, interval="1M", startTime=1617249600)
        data: dict = self._get_public(params, Public.candle)
        for item in data:
            print(f"H: {item[2]} L: {item[3]}")

    def get_account(self) -> Account:
        """
        Get account information.
        :return: Account object.
        """
        params: dict = {"recvWindow": 10000}
        response: dict = requests.get(
            url=self._get_url(Private.account),
            params=self._sign_params(params=params),
            headers={API_KEY_HEADER: self.api_key},
            timeout=TIMEOUT,
        ).json()
        try:
            return Account(**response)
        except pydantic.error_wrappers.ValidationError as ex:
            print(f"*** ValidationError")
            print(Response(**response))
            sys.exit()

    def get_trades(self, symbol: str) -> List[Trade]:
        """
        Get trades of a cryptocurrency.
        :param symbol: String with the symbol.
        :return: List of Trade object.
        """
        response: dict = requests.get(
            url=self._get_url(Private.my_trades),
            params=self._sign_params({"symbol": symbol}),
            headers={API_KEY_HEADER: self.api_key},
            timeout=TIMEOUT,
        ).json()
        try:
            update: Callable[[dict], Trade] = lambda t: Trade(**t)
            return list(map(update, response))
        except pydantic.error_wrappers.ValidationError as ex:
            print(f"*** ValidationError")
            print(Response(**response))
            sys.exit()

    def get_open_orders(self) -> List[Order]:
        """
        Get open orders.
        :return: List of Order object.
        """
        response: dict = requests.get(
            url=self._get_url(Private.open_orders),
            params=self._sign_params(),
            headers={API_KEY_HEADER: self.api_key},
            timeout=TIMEOUT,
        ).json()
        try:
            update: Callable[[dict], Order] = lambda x: Order(**x)
            return list(map(update, response))
        except pydantic.error_wrappers.ValidationError:
            print("*** ValidationError")
            print(Response(**response))
            sys.exit()

    def cancel_open_order(self, symbol: str, order_id: int) -> Order:
        """
        Cancel an open order.
        :param symbol: String with the symbol.
        :param order_id: Int with the Order id.
        :return: Order object.
        """
        response: dict = requests.delete(
            url=self._get_url(Private.order),
            params=self._sign_params({"symbol": symbol, "orderId": order_id}),
            headers={API_KEY_HEADER: self.api_key},
            timeout=TIMEOUT,
        ).json()
        try:
            return Order(**response)
        except pydantic.error_wrappers.ValidationError as ex:
            print("*** ValidationError")
            print(Response(**response))
            sys.exit()

    def create_order(self, order: NewOrder) -> Order:
        """
        MARKET orders using the `quantity`:
        Using BTCUSDT for example, sending a MARKET order will
        specify how much BTC the user is buying or selling.
        MARKET orders using `quoteOrderQty`:
        Using BTCUSDT for example, sending a MARKET order will
        specify how much USDT the user is going to spend or receive.
        \f
        :param order: New order object.
        :return: Order object.
        """
        params: dict = {"symbol": order.symbol, "side": order.side}
        # Let's use MARKET orders to BUY...
        # ... And LIMIT orders to SELL
        if order.type_.upper() in ["M", "MARKET"]:
            params["type"] = "MARKET"
            # params["quoteOrderQty"] = order.qty
        elif order.type_.upper() in ["L", "LIMIT"]:
            params["type"] = "LIMIT"
            params["timeInForce"] = "GTC"
            params["price"] = order.price
        params["quantity"] = order.qty
        response: dict = requests.post(
            url=self._get_url(Private.order),
            params=self._sign_params(params),
            headers={API_KEY_HEADER: self.api_key},
            timeout=TIMEOUT,
        ).json()
        try:
            return Order(**response)
        except pydantic.error_wrappers.ValidationError as ex:
            print("*** ValidationError")
            print(Response(**response))
            sys.exit()


if __name__ == "__main__":
    pass
