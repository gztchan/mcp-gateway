from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import ActivityRecord, ClosedPositionRecord, PositionRecord, ValueRecord


class DataUserAnalyticsTools:
    @tool(description="Get current Polymarket positions for a user")
    def get_positions(
        self,
        user: str = Field(description="Wallet address"),
        market: list[str] | None = None,
        event_id: list[int] | None = Field(default=None, alias="eventId"),
        size_threshold: float | None = Field(default=None, alias="sizeThreshold"),
        redeemable: bool | None = None,
        mergeable: bool | None = None,
        limit: int = Field(default=100, ge=0, le=500),
        offset: int = Field(default=0, ge=0, le=10000),
        sort_by: str | None = Field(default=None, alias="sortBy"),
        sort_direction: str | None = Field(default=None, alias="sortDirection"),
        title: str | None = None,
    ) -> list[PositionRecord]:
        response = self.data_client.get_positions(
            user=user,
            market=market,
            eventId=event_id,
            sizeThreshold=size_threshold,
            redeemable=redeemable,
            mergeable=mergeable,
            limit=limit,
            offset=offset,
            sortBy=sort_by,
            sortDirection=sort_direction,
            title=title,
        )
        return [PositionRecord(**item) for item in response]

    @tool(description="Get closed Polymarket positions for a user")
    def get_closed_positions(
        self,
        user: str = Field(description="Wallet address"),
        market: list[str] | None = None,
        title: str | None = None,
        event_id: list[int] | None = Field(default=None, alias="eventId"),
        limit: int = Field(default=10, ge=0, le=50),
        offset: int = Field(default=0, ge=0, le=100000),
        sort_by: str | None = Field(default=None, alias="sortBy"),
        sort_direction: str | None = Field(default=None, alias="sortDirection"),
    ) -> list[ClosedPositionRecord]:
        response = self.data_client.get_closed_positions(
            user=user,
            market=market,
            title=title,
            eventId=event_id,
            limit=limit,
            offset=offset,
            sortBy=sort_by,
            sortDirection=sort_direction,
        )
        return [ClosedPositionRecord(**item) for item in response]

    @tool(description="Get Polymarket user activity")
    def get_activity(
        self,
        user: str = Field(description="Wallet address"),
        limit: int = Field(default=100, ge=0, le=500),
        offset: int = Field(default=0, ge=0, le=10000),
        market: list[str] | None = None,
        event_id: list[int] | None = Field(default=None, alias="eventId"),
        type: list[str] | None = None,
        start: int | None = None,
        end: int | None = None,
        sort_by: str | None = Field(default=None, alias="sortBy"),
        sort_direction: str | None = Field(default=None, alias="sortDirection"),
        side: str | None = None,
    ) -> list[ActivityRecord]:
        response = self.data_client.get_activity(
            user=user,
            limit=limit,
            offset=offset,
            market=market,
            eventId=event_id,
            type=type,
            start=start,
            end=end,
            sortBy=sort_by,
            sortDirection=sort_direction,
            side=side,
        )
        return [ActivityRecord(**item) for item in response]

    @tool(description="Get total value of a user's Polymarket positions")
    def get_value(
        self,
        user: str = Field(description="Wallet address"),
        market: list[str] | None = None,
    ) -> list[ValueRecord]:
        response = self.data_client.get_value(user=user, market=market)
        return [ValueRecord(**item) for item in response]
