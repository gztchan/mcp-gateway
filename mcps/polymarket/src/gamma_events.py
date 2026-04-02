from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import (
    CountResponse,
    EventCreator,
    EventDetails,
    EventTweetCount,
    EventsPaginationResponse,
    KeysetEventsResponse,
    TagDetails,
)


def _to_event_details(payload: dict) -> EventDetails:
    markets = payload.get("markets") or []
    return EventDetails(
        id=payload.get("id"),
        title=payload.get("title"),
        slug=payload.get("slug"),
        description=payload.get("description"),
        active=payload.get("active"),
        closed=payload.get("closed"),
        liquidity=float(payload["liquidity"]) if payload.get("liquidity") is not None else None,
        volume=float(payload["volume"]) if payload.get("volume") is not None else None,
        startDate=payload.get("startDate"),
        endDate=payload.get("endDate"),
        createdAt=payload.get("createdAt") or payload.get("creationDate"),
        markets=markets,
    )


class GammaEventsTools:
    @tool(description="List Polymarket events from the Gamma API")
    def list_events(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        id: list[int] | None = None,
        tag_id: int | None = None,
        exclude_tag_id: list[int] | None = None,
        slug: list[str] | None = None,
        tag_slug: str | None = None,
        related_tags: bool | None = None,
        active: bool | None = None,
        archived: bool | None = None,
        featured: bool | None = None,
        cyom: bool | None = None,
        include_chat: bool | None = None,
        include_template: bool | None = None,
        recurrence: str | None = None,
        closed: bool | None = None,
        liquidity_min: float | None = None,
        liquidity_max: float | None = None,
        volume_min: float | None = None,
        volume_max: float | None = None,
        start_date_min: str | None = None,
        start_date_max: str | None = None,
        end_date_min: str | None = None,
        end_date_max: str | None = None,
    ) -> list[EventDetails]:
        response = self.gamma_client.list_events(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            id=id,
            tag_id=tag_id,
            exclude_tag_id=exclude_tag_id,
            slug=slug,
            tag_slug=tag_slug,
            related_tags=related_tags,
            active=active,
            archived=archived,
            featured=featured,
            cyom=cyom,
            include_chat=include_chat,
            include_template=include_template,
            recurrence=recurrence,
            closed=closed,
            liquidity_min=liquidity_min,
            liquidity_max=liquidity_max,
            volume_min=volume_min,
            volume_max=volume_max,
            start_date_min=start_date_min,
            start_date_max=start_date_max,
            end_date_min=end_date_min,
            end_date_max=end_date_max,
        )
        return [_to_event_details(item) for item in response]

    @tool(description="List Polymarket events using cursor pagination")
    def list_events_keyset(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        after_cursor: str | None = None,
        id: list[int] | None = None,
        slug: list[str] | None = None,
        closed: bool | None = None,
        live: bool | None = None,
        featured: bool | None = None,
        cyom: bool | None = None,
        title_search: str | None = None,
        liquidity_min: float | None = None,
        liquidity_max: float | None = None,
        volume_min: float | None = None,
        volume_max: float | None = None,
        start_date_min: str | None = None,
        start_date_max: str | None = None,
        end_date_min: str | None = None,
        end_date_max: str | None = None,
        start_time_min: str | None = None,
        start_time_max: str | None = None,
        tag_id: list[int] | None = None,
        tag_slug: str | None = None,
        exclude_tag_id: list[int] | None = None,
        related_tags: bool | None = None,
        tag_match: str | None = None,
        series_id: list[int] | None = None,
        game_id: list[int] | None = None,
        event_date: str | None = None,
        event_week: int | None = None,
        featured_order: bool | None = None,
        recurrence: str | None = None,
        created_by: list[str] | None = None,
        parent_event_id: int | None = None,
        include_children: bool | None = None,
        partner_slug: str | None = None,
        include_chat: bool | None = None,
        include_template: bool | None = None,
        include_best_lines: bool | None = None,
        locale: str | None = None,
    ) -> KeysetEventsResponse:
        response = self.gamma_client.list_events_keyset(
            limit=limit,
            order=order,
            ascending=ascending,
            after_cursor=after_cursor,
            id=id,
            slug=slug,
            closed=closed,
            live=live,
            featured=featured,
            cyom=cyom,
            title_search=title_search,
            liquidity_min=liquidity_min,
            liquidity_max=liquidity_max,
            volume_min=volume_min,
            volume_max=volume_max,
            start_date_min=start_date_min,
            start_date_max=start_date_max,
            end_date_min=end_date_min,
            end_date_max=end_date_max,
            start_time_min=start_time_min,
            start_time_max=start_time_max,
            tag_id=tag_id,
            tag_slug=tag_slug,
            exclude_tag_id=exclude_tag_id,
            related_tags=related_tags,
            tag_match=tag_match,
            series_id=series_id,
            game_id=game_id,
            event_date=event_date,
            event_week=event_week,
            featured_order=featured_order,
            recurrence=recurrence,
            created_by=created_by,
            parent_event_id=parent_event_id,
            include_children=include_children,
            partner_slug=partner_slug,
            include_chat=include_chat,
            include_template=include_template,
            include_best_lines=include_best_lines,
            locale=locale,
        )
        return KeysetEventsResponse(
            events=[_to_event_details(item) for item in response.get("events", [])],
            next_cursor=response.get("next_cursor"),
        )

    @tool(description="Get a Polymarket event by numeric id")
    def get_event_by_id(
        self,
        event_id: int = Field(description="Gamma event id"),
        include_chat: bool | None = None,
        include_template: bool | None = None,
    ) -> EventDetails:
        return _to_event_details(
            self.gamma_client.get_event_by_id(
                event_id,
                include_chat=include_chat,
                include_template=include_template,
            )
        )

    @tool(description="List Polymarket events using paginated metadata wrapper")
    def list_events_pagination(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        include_chat: bool | None = None,
        include_template: bool | None = None,
        recurrence: str | None = None,
    ) -> EventsPaginationResponse:
        response = self.gamma_client.list_events_pagination(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            include_chat=include_chat,
            include_template=include_template,
            recurrence=recurrence,
        )
        return EventsPaginationResponse(
            data=[_to_event_details(item) for item in response.get("data", [])],
            pagination=response.get("pagination"),
        )

    @tool(description="List Polymarket sport event results")
    def list_events_results(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
    ) -> list[EventDetails]:
        response = self.gamma_client.list_events_results(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
        )
        return [_to_event_details(item) for item in response]

    @tool(description="Get a Polymarket event by slug")
    def get_event_by_slug(
        self,
        slug: str = Field(description="Gamma event slug"),
        include_chat: bool | None = None,
        include_template: bool | None = None,
    ) -> EventDetails:
        return _to_event_details(
            self.gamma_client.get_event_by_slug(
                slug,
                include_chat=include_chat,
                include_template=include_template,
            )
        )

    @tool(description="Get details of a Polymarket event by slug")
    def get_event_details(self, slug: str = Field(description="Gamma event slug")) -> EventDetails:
        return self.get_event_by_slug(slug)

    @tool(description="Get Polymarket event tweet count")
    def get_event_tweet_count(
        self, event_id: int = Field(description="Gamma event id")
    ) -> EventTweetCount:
        return EventTweetCount(**self.gamma_client.get_event_tweet_count(event_id))

    @tool(description="Get Polymarket event comment count")
    def get_event_comments_count(
        self, event_id: int = Field(description="Gamma event id")
    ) -> CountResponse:
        return CountResponse(**self.gamma_client.get_event_comments_count(event_id))

    @tool(description="Get tags attached to a Polymarket event")
    def get_event_tags(
        self, event_id: int = Field(description="Gamma event id")
    ) -> list[TagDetails]:
        response = self.gamma_client.get_event_tags(event_id)
        return [TagDetails(**item) for item in response]

    @tool(description="List Polymarket event creators")
    def list_event_creators(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        creator_name: str | None = None,
        creator_handle: str | None = None,
    ) -> list[EventCreator]:
        response = self.gamma_client.list_event_creators(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            creator_name=creator_name,
            creator_handle=creator_handle,
        )
        return [EventCreator(**item) for item in response]

    @tool(description="Get a Polymarket event creator by id")
    def get_event_creator(
        self, creator_id: int = Field(description="Gamma event creator id")
    ) -> EventCreator:
        return EventCreator(**self.gamma_client.get_event_creator(creator_id))
