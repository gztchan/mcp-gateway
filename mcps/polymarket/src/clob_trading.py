from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import ApiCredentials, CancelOrdersResponse, CursorPage, OpenOrderRecord, OrderPlacementResponse, TradeRecord


class ClobTradingTools:
    @tool(description="Create or derive Polymarket CLOB API credentials from the configured private key")
    def create_or_derive_api_credentials(self, nonce: int | None = None) -> ApiCredentials:
        creds = self.clob_trading_client.create_or_derive_api_creds(nonce=nonce)
        return ApiCredentials(
            api_key=getattr(creds, "api_key", None),
            api_secret=getattr(creds, "api_secret", None),
            api_passphrase=getattr(creds, "api_passphrase", None),
        )

    @tool(description="Create a readonly Polymarket CLOB API key")
    def create_readonly_api_key(self) -> dict:
        return self.clob_trading_client.create_readonly_api_key()

    @tool(description="List Polymarket CLOB API keys for the configured trader")
    def list_api_keys(self) -> dict:
        return self.clob_trading_client.get_api_keys()

    @tool(description="Place a signed limit order on the Polymarket CLOB")
    def place_order(
        self,
        token_id: str = Field(description="CLOB token id"),
        price: float = Field(description="Order price"),
        size: float = Field(description="Order size"),
        side: str = Field(description="BUY or SELL"),
        order_type: str = Field(default="GTC", description="GTC, FOK, GTD, or FAK"),
        fee_rate_bps: int = 0,
        nonce: int = 0,
        expiration: int = 0,
        taker: str = "0x0000000000000000000000000000000000000000",
        tick_size: str | None = None,
        neg_risk: bool | None = None,
    ) -> OrderPlacementResponse:
        response = self.clob_trading_client.place_order(
            token_id=token_id,
            price=price,
            size=size,
            side=side,
            order_type=order_type,
            fee_rate_bps=fee_rate_bps,
            nonce=nonce,
            expiration=expiration,
            taker=taker,
            tick_size=tick_size,
            neg_risk=neg_risk,
        )
        return OrderPlacementResponse(**response)

    @tool(description="Create a signed Polymarket market order payload")
    def place_market_order(
        self,
        token_id: str = Field(description="CLOB token id"),
        amount: float = Field(description="Cash or token amount depending on side"),
        side: str = Field(description="BUY or SELL"),
        price: float = 0.0,
        order_type: str = "FOK",
        fee_rate_bps: int = 0,
        nonce: int = 0,
        taker: str = "0x0000000000000000000000000000000000000000",
    ) -> dict:
        return self.clob_trading_client.place_market_order(
            token_id=token_id,
            amount=amount,
            side=side,
            price=price,
            order_type=order_type,
            fee_rate_bps=fee_rate_bps,
            nonce=nonce,
            taker=taker,
        )

    @tool(description="List authenticated open Polymarket orders")
    def list_open_orders(
        self,
        order_id: str | None = None,
        market: str | None = None,
        asset_id: str | None = None,
        next_cursor: str = "MA==",
    ) -> CursorPage:
        response = self.clob_trading_client.get_orders(
            order_id=order_id,
            market=market,
            asset_id=asset_id,
            next_cursor=next_cursor,
        )
        return CursorPage(
            limit=response.get("limit"),
            next_cursor=response.get("next_cursor"),
            count=response.get("count"),
            data=[OpenOrderRecord(**item) for item in response.get("data", [])],
        )

    @tool(description="Get an authenticated Polymarket order by id")
    def get_order(self, order_id: str = Field(description="Order hash")) -> OpenOrderRecord:
        return OpenOrderRecord(**self.clob_trading_client.get_order(order_id))

    @tool(description="List authenticated Polymarket trades")
    def list_trades_private(
        self,
        trade_id: str | None = None,
        maker_address: str | None = None,
        market: str | None = None,
        asset_id: str | None = None,
        before: int | None = None,
        after: int | None = None,
        next_cursor: str = "MA==",
    ) -> CursorPage:
        response = self.clob_trading_client.get_trades(
            trade_id=trade_id,
            maker_address=maker_address,
            market=market,
            asset_id=asset_id,
            before=before,
            after=after,
            next_cursor=next_cursor,
        )
        return CursorPage(
            limit=response.get("limit"),
            next_cursor=response.get("next_cursor"),
            count=response.get("count"),
            data=[TradeRecord(**item) for item in response.get("data", [])],
        )

    @tool(description="Cancel a single Polymarket order")
    def cancel_order(self, order_id: str = Field(description="Order hash")) -> CancelOrdersResponse:
        response = self.clob_trading_client.cancel_order(order_id)
        return CancelOrdersResponse(**response)

    @tool(description="Cancel multiple Polymarket orders")
    def cancel_orders(
        self, order_ids: list[str] = Field(description="Order hashes")
    ) -> CancelOrdersResponse:
        response = self.clob_trading_client.cancel_orders(order_ids)
        return CancelOrdersResponse(**response)

    @tool(description="Cancel all authenticated Polymarket orders")
    def cancel_all_orders(self) -> CancelOrdersResponse:
        response = self.clob_trading_client.cancel_all_orders()
        return CancelOrdersResponse(**response)

    @tool(description="Cancel Polymarket orders for a specific market or asset")
    def cancel_orders_for_market(
        self,
        market: str = Field(default="", description="Condition id"),
        asset_id: str = Field(default="", description="Token id"),
    ) -> CancelOrdersResponse:
        response = self.clob_trading_client.cancel_market_orders(
            market=market,
            asset_id=asset_id,
        )
        return CancelOrdersResponse(**response)

    @tool(description="Send a Polymarket heartbeat to keep automated orders active")
    def post_heartbeat(self, heartbeat_id: str | None = None) -> dict:
        return self.clob_trading_client.post_heartbeat(heartbeat_id)
