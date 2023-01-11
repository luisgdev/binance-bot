""" Models """

from typing import List, NamedTuple, Optional

from pydantic import BaseModel

# pylint: disable=too-few-public-methods


class Response(BaseModel):
    """Response error"""

    code: str
    msg: str


class Profit(NamedTuple):
    """Profit for a symbol"""

    symbol: str
    qty: float
    buy_value: float
    current_value: float


class Ticker(BaseModel):
    """Price ticker"""

    symbol: str
    price: str


class AvgPrice(BaseModel):
    """Average price"""

    mins: int
    price: str


class NewOrder(BaseModel):
    """New Order model"""

    symbol: str
    side: str
    type_: str
    qty: float
    price: Optional[float]


class Trade(BaseModel):
    """Trade model"""

    symbol: str
    id_: int
    order_id: int
    order_list_id: int
    price: str
    qty: str
    quote_qty: str
    commission: str
    commission_asset: str
    time: int
    is_buyer: bool
    is_maker: bool
    is_best_match: bool

    class Config:
        """Trade model config"""

        fields: dict = {
            "id_": "id",
            "order_id": "orderId",
            "order_list_id": "orderListId",
            "quote_qty": "quoteQty",
            "commission_asset": "commissionAsset",
            "is_buyer": "isBuyer",
            "is_maker": "isMaker",
            "is_best_match": "isBestMatch",
        }


class Fill(BaseModel):
    """Fill model"""

    price: str
    qty: str
    commission: str
    commission_asset: str

    class Config:
        """Fill model config"""

        fields: dict = {"commission_asset": "commissionAsset"}


class Order(BaseModel):
    """Order model"""

    symbol: str
    order_id: int
    order_list_id: int
    client_order_id: str
    transact_time: Optional[int]
    price: str
    executed_qty: str
    cummulative_quote_qty: str
    status: str
    time_in_force: str
    type_: str
    side: str
    fills: Optional[List[Fill]]
    stop_price: Optional[str]
    iceberg_qty: Optional[str]
    time: Optional[int]
    update_time: Optional[int]
    is_working: Optional[bool]
    orig_quote_order_qty: Optional[str]
    orig_qty: Optional[str]

    class Config:
        """Config for order model"""

        fields: dict = {
            "type_": "type",
            "order_id": "orderId",
            "order_list_id": "orderListId",
            "client_order_id": "clientOrderId",
            "executed_qty": "executedQty",
            "time_in_force": "timeInForce",
            "transact_time": "transactTime",
            "cummulative_quote_qty": "cummulativeQuoteQty",
            "stop_price": "stopPrice",
            "iceberg_qty": "icebergQty",
            "update_time": "updateTime",
            "is_working": "isWorking",
            "orig_quote_order_qty": "origQuoteOrderQty",
            "orig_qty": "origQty",
        }


class Balance(BaseModel):
    """Balance model"""

    asset: str
    free: str
    locked: str


class Account(BaseModel):
    """Account model"""

    maker_commission: int
    taker_commission: int
    buyer_commission: int
    seller_commission: int
    can_trade: bool
    can_withdraw: bool
    can_deposit: bool
    update_time: int
    account_type: str
    balances: List[Balance]
    permissions: List[str]

    class Config:
        """Config for account model"""

        fields: dict = {
            "maker_commission": "makerCommission",
            "taker_commission": "takerCommission",
            "buyer_commission": "buyerCommission",
            "seller_commission": "sellerCommission",
            "can_trade": "canTrade",
            "can_withdraw": "canWithdraw",
            "can_deposit": "canDeposit",
            "update_time": "updateTime",
            "account_type": "accountType",
        }
