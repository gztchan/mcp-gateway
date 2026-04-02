from __future__ import annotations

import os
from typing import Any

from .http import request_json


class DataClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.getenv(
            "DATA_API_URL", "https://data-api.polymarket.com"
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return request_json(base_url=self.base_url, path=path, params=params)

    def list_trades(self, **params: Any) -> Any:
        return self.get("/trades", params)

    def get_holders(self, **params: Any) -> Any:
        return self.get("/holders", params)

    def get_open_interest(self, **params: Any) -> Any:
        return self.get("/oi", params)

    def get_positions(self, **params: Any) -> Any:
        return self.get("/positions", params)

    def get_closed_positions(self, **params: Any) -> Any:
        return self.get("/closed-positions", params)

    def get_activity(self, **params: Any) -> Any:
        return self.get("/activity", params)

    def get_value(self, **params: Any) -> Any:
        return self.get("/value", params)
