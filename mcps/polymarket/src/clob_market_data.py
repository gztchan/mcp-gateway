from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import (
    ClobMarketByToken,
    MidpointQuote,
    Orderbook,
    PriceHistoryResponse,
    PriceLevel,
    PriceQuote,
    SpreadQuote,
)


def _to_orderbook(payload: dict) -> Orderbook:
    return Orderbook(
        market=payload.get("market"),
        asset_id=payload.get("asset_id"),
        timestamp=payload.get("timestamp"),
        hash=payload.get("hash"),
        neg_risk=payload.get("neg_risk"),
        min_order_size=str(payload.get("min_order_size")) if payload.get("min_order_size") is not None else None,
        tick_size=str(payload.get("tick_size")) if payload.get("tick_size") is not None else None,
        last_trade_price=str(payload.get("last_trade_price")) if payload.get("last_trade_price") is not None else None,
        bids=[PriceLevel(price=float(item["price"]), size=float(item["size"])) for item in payload.get("bids", [])],
        asks=[PriceLevel(price=float(item["price"]), size=float(item["size"])) for item in payload.get("asks", [])],
    )


class ClobMarketDataTools:
    @tool(description="Get a Polymarket CLOB order book by token id")
    def get_book(self, token_id: str = Field(description="CLOB token id")) -> Orderbook:
        return _to_orderbook(self.clob_public_client.get_book(token_id))

    @tool(description="Get multiple Polymarket CLOB order books")
    def get_books(
        self, token_ids: list[str] = Field(description="List of CLOB token ids")
    ) -> list[Orderbook]:
        return [_to_orderbook(item) for item in self.clob_public_client.get_books(token_ids)]

    @tool(description="Get a Polymarket best market price")
    def get_price(
        self,
        token_id: str = Field(description="CLOB token id"),
        side: str = Field(description="BUY or SELL"),
    ) -> PriceQuote:
        response = self.clob_public_client.get_price(token_id, side)
        return PriceQuote(token_id=token_id, side=side, price=response.get("price"))

    @tool(description="Get multiple Polymarket best market prices")
    def get_prices(
        self,
        token_ids: list[str] = Field(description="CLOB token ids"),
        side: str = Field(description="BUY or SELL applied to all token ids"),
    ) -> list[PriceQuote]:
        return [self.get_price(token_id=token_id, side=side) for token_id in token_ids]

    @tool(description="Get midpoint price for a Polymarket token")
    def get_midpoint(self, token_id: str = Field(description="CLOB token id")) -> MidpointQuote:
        response = self.clob_public_client.get_midpoint(token_id)
        midpoint = response.get("midpoint", response.get("price"))
        return MidpointQuote(token_id=token_id, midpoint=midpoint)

    @tool(description="Get bid/ask midpoint prices for multiple Polymarket tokens")
    def get_midpoints(
        self, token_ids: list[str] = Field(description="CLOB token ids")
    ) -> list[MidpointQuote]:
        return [self.get_midpoint(token_id=token_id) for token_id in token_ids]

    @tool(description="Get spread for a Polymarket token")
    def get_spread(self, token_id: str = Field(description="CLOB token id")) -> SpreadQuote:
        response = self.clob_public_client.get_spread(token_id)
        return SpreadQuote(token_id=token_id, spread=response.get("spread"))

    @tool(description="Get spreads for multiple Polymarket tokens")
    def get_spreads(
        self, token_ids: list[str] = Field(description="CLOB token ids")
    ) -> list[SpreadQuote]:
        return [self.get_spread(token_id=token_id) for token_id in token_ids]

    @tool(description="Get Polymarket price history for a token or market asset id")
    def get_price_history(
        self,
        market: str = Field(description="Asset id used by /prices-history"),
        start_ts: float | None = None,
        end_ts: float | None = None,
        interval: str | None = None,
        fidelity: int | None = None,
    ) -> PriceHistoryResponse:
        response = self.clob_public_client.get_prices_history(
            market=market,
            start_ts=start_ts,
            end_ts=end_ts,
            interval=interval,
            fidelity=fidelity,
        )
        return PriceHistoryResponse(**response)

    @tool(description="Resolve a Polymarket market from a token id")
    def get_market_by_token(
        self, token_id: str = Field(description="CLOB token id")
    ) -> ClobMarketByToken:
        return ClobMarketByToken(**self.clob_public_client.get_market_by_token(token_id))

    @tool(description="Get CLOB market metadata for a condition id")
    def get_clob_market_info(
        self, condition_id: str = Field(description="Condition id")
    ) -> dict:
        return self.clob_public_client.get_clob_market_info(condition_id)

    @tool(description="Get simplified CLOB markets with cursor pagination")
    def get_simplified_markets(self, next_cursor: str | None = None) -> dict:
        return self.clob_public_client.get_simplified_markets(next_cursor=next_cursor)

    @tool(description="Backward-compatible Polymarket order book tool")
    def get_market_orderbook(
        self, token_id: str = Field(description="CLOB token id")
    ) -> Orderbook:
        return self.get_book(token_id)
