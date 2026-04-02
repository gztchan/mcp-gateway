from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import TradeRecord


class DataTradesTools:
    @tool(description="List public Polymarket trades from the Data API")
    def list_trades(
        self,
        limit: int = Field(default=100, ge=0, le=10000),
        offset: int = Field(default=0, ge=0, le=10000),
        taker_only: bool | None = Field(default=None, alias="takerOnly"),
        filter_type: str | None = Field(default=None, alias="filterType"),
        filter_amount: float | None = Field(default=None, alias="filterAmount"),
        market: list[str] | None = None,
        event_id: list[int] | None = Field(default=None, alias="eventId"),
        user: str | None = None,
        side: str | None = None,
    ) -> list[TradeRecord]:
        response = self.data_client.list_trades(
            limit=limit,
            offset=offset,
            takerOnly=taker_only,
            filterType=filter_type,
            filterAmount=filter_amount,
            market=market,
            eventId=event_id,
            user=user,
            side=side,
        )
        return [TradeRecord(**item) for item in response]
