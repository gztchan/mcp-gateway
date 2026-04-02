from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import MarketHolders, OpenInterestRecord


class DataMarketAnalyticsTools:
    @tool(description="Get top Polymarket holders for one or more markets")
    def get_holders(
        self,
        market: list[str] = Field(description="Condition ids"),
        limit: int = Field(default=20, ge=0, le=20),
        min_balance: int | None = Field(default=None, alias="minBalance"),
    ) -> list[MarketHolders]:
        response = self.data_client.get_holders(
            market=market,
            limit=limit,
            minBalance=min_balance,
        )
        return [MarketHolders(**item) for item in response]

    @tool(description="Get Polymarket open interest for one or more markets")
    def get_open_interest(
        self,
        market: list[str] = Field(description="Condition ids"),
    ) -> list[OpenInterestRecord]:
        response = self.data_client.get_open_interest(market=market)
        return [OpenInterestRecord(**item) for item in response]
