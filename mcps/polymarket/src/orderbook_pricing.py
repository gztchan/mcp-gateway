from pydantic import BaseModel, Field
from typing import Any, Optional
from pydash import get
from .utils.gamma import gamma_request, clob_request

class Pricing(BaseModel):
    price: float = Field(description="The price of the pricing")
    size: float = Field(description="The size of the pricing")

class Orderbook(BaseModel):
    market: str = Field(description="The market of this orderbook")
    neg_risk: bool = Field(description="Whether the pricing is negative risk")
    min_order_size: int = Field(description="The minimum order size of the pricing")
    last_trade_price: float = Field(description="The last trade price of the pricing")
    bids: list[Pricing] = Field(description="The bids of the market")
    asks: list[Pricing] = Field(description="The asks of the market")

class OrderBookError(BaseModel):
    error: str = Field(description="The error of the orderbook")

class PolymarketOrderbook:
    def __init__(self):
        pass

    def get_market_orderbook(
        self,
        token_id: str = Field(description="The yes or no clob token id of the market"),
    ) -> Orderbook | OrderBookError:
        response = clob_request(
            path=f"/book",
            method="GET",
            params={
                "token_id": token_id,
            },
        )
        # print(response)
        if "error" in response: 
            return OrderBookError(
                error=response["error"],
            )
        return Orderbook(
            market=get(response, "market"),
            neg_risk=get(response, "neg_risk", False),
            min_order_size=int(get(response, "min_order_size")),
            last_trade_price=float(get(response, "last_trade_price")),
            bids=[Pricing(**x) for x in [{ "price": float(x["price"]), "size": float(x["size"]) } for x in get(response, "bids", [])]],
            asks=[Pricing(**x) for x in [{ "price": float(x["price"]), "size": float(x["size"]) } for x in get(response, "asks", [])]],
        )