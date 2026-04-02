from __future__ import annotations

import os
from typing import Any

from .http import request_json


class ClobPublicClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.getenv(
            "CLOB_API_URL", "https://clob.polymarket.com"
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return request_json(base_url=self.base_url, path=path, params=params)

    def post(self, path: str, json: Any) -> Any:
        return request_json(base_url=self.base_url, path=path, method="POST", json=json)

    def get_book(self, token_id: str) -> Any:
        return self.get("/book", {"token_id": token_id})

    def get_books(self, token_ids: list[str]) -> Any:
        return self.post("/books", [{"token_id": token_id} for token_id in token_ids])

    def get_price(self, token_id: str, side: str) -> Any:
        return self.get("/price", {"token_id": token_id, "side": side})

    def get_midpoint(self, token_id: str) -> Any:
        return self.get("/midpoint", {"token_id": token_id})

    def get_spread(self, token_id: str) -> Any:
        return self.get("/spread", {"token_id": token_id})

    def get_prices_history(
        self,
        market: str,
        start_ts: float | None = None,
        end_ts: float | None = None,
        interval: str | None = None,
        fidelity: int | None = None,
    ) -> Any:
        return self.get(
            "/prices-history",
            {
                "market": market,
                "startTs": start_ts,
                "endTs": end_ts,
                "interval": interval,
                "fidelity": fidelity,
            },
        )

    def get_market_by_token(self, token_id: str) -> Any:
        return self.get(f"/markets-by-token/{token_id}")

    def get_clob_market_info(self, condition_id: str) -> Any:
        return self.get(f"/clob-markets/{condition_id}")

    def get_simplified_markets(self, next_cursor: str | None = None) -> Any:
        return self.get("/simplified-markets", {"next_cursor": next_cursor})
