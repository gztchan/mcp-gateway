from __future__ import annotations

import os
from typing import Any

from .errors import PolymarketError


class ClobTradingClient:
    def __init__(self) -> None:
        self._client = None

    def _import_types(self) -> tuple[Any, Any]:
        try:
            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import (
                ApiCreds,
                MarketOrderArgs,
                OpenOrderParams,
                OrderArgs,
                PartialCreateOrderOptions,
                TradeParams,
            )
        except ImportError as exc:
            raise PolymarketError(
                "py-clob-client is required for authenticated Polymarket trading tools"
            ) from exc

        return (
            ClobClient,
            {
                "ApiCreds": ApiCreds,
                "MarketOrderArgs": MarketOrderArgs,
                "OpenOrderParams": OpenOrderParams,
                "OrderArgs": OrderArgs,
                "PartialCreateOrderOptions": PartialCreateOrderOptions,
                "TradeParams": TradeParams,
            },
        )

    def _build_client(self):
        if self._client is not None:
            return self._client

        ClobClient, types = self._import_types()
        private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
        if not private_key:
            raise PolymarketError(
                "Missing POLYMARKET_PRIVATE_KEY for authenticated CLOB trading tools"
            )

        creds = None
        api_key = os.getenv("POLYMARKET_API_KEY")
        api_secret = os.getenv("POLYMARKET_API_SECRET")
        api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")
        if api_key and api_secret and api_passphrase:
            creds = types["ApiCreds"](
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase,
            )

        chain_id = int(os.getenv("POLYMARKET_CHAIN_ID", "137"))
        signature_type = (
            int(os.getenv("POLYMARKET_SIGNATURE_TYPE"))
            if os.getenv("POLYMARKET_SIGNATURE_TYPE")
            else None
        )

        self._client = ClobClient(
            host=os.getenv("CLOB_API_URL", "https://clob.polymarket.com"),
            chain_id=chain_id,
            key=private_key,
            creds=creds,
            signature_type=signature_type,
            funder=os.getenv("POLYMARKET_FUNDER_ADDRESS")
            or os.getenv("POLYMARKET_PROXY_ADDRESS"),
        )
        return self._client

    def create_or_derive_api_creds(self, nonce: int | None = None) -> Any:
        return self._build_client().create_or_derive_api_creds(nonce=nonce)

    def create_readonly_api_key(self) -> Any:
        return self._build_client().create_readonly_api_key()

    def get_api_keys(self) -> Any:
        return self._build_client().get_api_keys()

    def get_orders(
        self,
        *,
        order_id: str | None = None,
        market: str | None = None,
        asset_id: str | None = None,
        next_cursor: str = "MA==",
    ) -> Any:
        _, types = self._import_types()
        params = types["OpenOrderParams"](id=order_id, market=market, asset_id=asset_id)
        return self._build_client().get_orders(params=params, next_cursor=next_cursor)

    def get_order(self, order_id: str) -> Any:
        return self._build_client().get_order(order_id)

    def get_trades(
        self,
        *,
        trade_id: str | None = None,
        maker_address: str | None = None,
        market: str | None = None,
        asset_id: str | None = None,
        before: int | None = None,
        after: int | None = None,
        next_cursor: str = "MA==",
    ) -> Any:
        _, types = self._import_types()
        params = types["TradeParams"](
            id=trade_id,
            maker_address=maker_address,
            market=market,
            asset_id=asset_id,
            before=before,
            after=after,
        )
        return self._build_client().get_trades(params=params, next_cursor=next_cursor)

    def place_order(
        self,
        *,
        token_id: str,
        price: float,
        size: float,
        side: str,
        order_type: str = "GTC",
        fee_rate_bps: int = 0,
        nonce: int = 0,
        expiration: int = 0,
        taker: str = "0x0000000000000000000000000000000000000000",
        tick_size: str | None = None,
        neg_risk: bool | None = None,
    ) -> Any:
        client = self._build_client()
        _, types = self._import_types()
        if tick_size is None:
            tick_size = client.get_tick_size(token_id)
        if neg_risk is None:
            neg_risk = client.get_neg_risk(token_id)

        order_args = types["OrderArgs"](
            token_id=token_id,
            price=price,
            size=size,
            side=side,
            fee_rate_bps=fee_rate_bps,
            nonce=nonce,
            expiration=expiration,
            taker=taker,
        )
        options = types["PartialCreateOrderOptions"](
            tick_size=tick_size,
            neg_risk=neg_risk,
        )
        return client.create_and_post_order(order_args, options)

    def place_market_order(
        self,
        *,
        token_id: str,
        amount: float,
        side: str,
        price: float = 0.0,
        order_type: str = "FOK",
        fee_rate_bps: int = 0,
        nonce: int = 0,
        taker: str = "0x0000000000000000000000000000000000000000",
    ) -> Any:
        client = self._build_client()
        _, types = self._import_types()
        order_args = types["MarketOrderArgs"](
            token_id=token_id,
            amount=amount,
            side=side,
            price=price,
            fee_rate_bps=fee_rate_bps,
            nonce=nonce,
            taker=taker,
            order_type=order_type,
        )
        return client.create_market_order(order_args)

    def cancel_order(self, order_id: str) -> Any:
        return self._build_client().cancel(order_id)

    def cancel_orders(self, order_ids: list[str]) -> Any:
        return self._build_client().cancel_orders(order_ids)

    def cancel_all_orders(self) -> Any:
        return self._build_client().cancel_all()

    def cancel_market_orders(self, market: str = "", asset_id: str = "") -> Any:
        return self._build_client().cancel_market_orders(market=market, asset_id=asset_id)

    def post_heartbeat(self, heartbeat_id: str | None = None) -> Any:
        return self._build_client().post_heartbeat(heartbeat_id)
