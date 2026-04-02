from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import (
    CountResponse,
    RelatedTag,
    SeriesDetails,
    SeriesSummary,
    SportsMarketTypesResponse,
    SportsMetadata,
    TagDetails,
    TagSummary,
    TeamSummary,
)


class GammaTaxonomyTools:
    @tool(description="List Polymarket tags")
    def list_tags(
        self,
        limit: int = Field(default=50, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = None,
        ascending: bool | None = None,
        include_template: bool | None = None,
        is_carousel: bool | None = None,
    ) -> list[TagSummary]:
        response = self.gamma_client.list_tags(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            include_template=include_template,
            is_carousel=is_carousel,
        )
        return [TagSummary(**item) for item in response]

    @tool(description="Get a Polymarket tag by id")
    def get_tag_by_id(
        self,
        tag_id: int = Field(description="Gamma tag id"),
        include_template: bool | None = None,
    ) -> TagDetails:
        return TagDetails(**self.gamma_client.get_tag_by_id(tag_id, include_template=include_template))

    @tool(description="Get a Polymarket tag by slug")
    def get_tag_by_slug(
        self,
        slug: str = Field(description="Gamma tag slug"),
        include_template: bool | None = None,
    ) -> TagDetails:
        return TagDetails(**self.gamma_client.get_tag_by_slug(slug, include_template=include_template))

    @tool(description="Get related tag relationships for a tag id")
    def get_related_tags_by_id(
        self,
        tag_id: int = Field(description="Gamma tag id"),
        omit_empty: bool | None = None,
        status: str | None = None,
    ) -> list[RelatedTag]:
        response = self.gamma_client.get_related_tags_by_id(
            tag_id,
            omit_empty=omit_empty,
            status=status,
        )
        return [RelatedTag(**item) for item in response]

    @tool(description="Get related tag relationships for a tag slug")
    def get_related_tags_by_slug(
        self,
        slug: str = Field(description="Gamma tag slug"),
        omit_empty: bool | None = None,
        status: str | None = None,
    ) -> list[RelatedTag]:
        response = self.gamma_client.get_related_tags_by_slug(
            slug,
            omit_empty=omit_empty,
            status=status,
        )
        return [RelatedTag(**item) for item in response]

    @tool(description="Get tags related to a Polymarket tag id")
    def get_tags_related_to_tag_by_id(
        self,
        tag_id: int = Field(description="Gamma tag id"),
        omit_empty: bool | None = None,
        status: str | None = None,
    ) -> list[TagDetails]:
        response = self.gamma_client.get_tags_related_to_tag_by_id(
            tag_id,
            omit_empty=omit_empty,
            status=status,
        )
        return [TagDetails(**item) for item in response]

    @tool(description="Get tags related to a Polymarket tag slug")
    def get_tags_related_to_tag_by_slug(
        self,
        slug: str = Field(description="Gamma tag slug"),
        omit_empty: bool | None = None,
        status: str | None = None,
    ) -> list[TagDetails]:
        response = self.gamma_client.get_tags_related_to_tag_by_slug(
            slug,
            omit_empty=omit_empty,
            status=status,
        )
        return [TagDetails(**item) for item in response]

    @tool(description="List Polymarket series")
    def list_series(
        self,
        limit: int = Field(default=50, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = None,
        ascending: bool | None = None,
        slug: list[str] | None = None,
        categories_ids: list[int] | None = None,
        categories_labels: list[str] | None = None,
        closed: bool | None = None,
        include_chat: bool | None = None,
        recurrence: str | None = None,
        exclude_events: bool | None = None,
    ) -> list[SeriesSummary]:
        response = self.gamma_client.list_series(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            slug=slug,
            categories_ids=categories_ids,
            categories_labels=categories_labels,
            closed=closed,
            include_chat=include_chat,
            recurrence=recurrence,
            exclude_events=exclude_events,
        )
        return [SeriesSummary(**item) for item in response]

    @tool(description="Get a Polymarket series by id")
    def get_series_by_id(
        self,
        series_id: int = Field(description="Gamma series id"),
        include_chat: bool | None = None,
    ) -> SeriesDetails:
        return SeriesDetails(**self.gamma_client.get_series_by_id(series_id, include_chat=include_chat))

    @tool(description="Get Polymarket series comment count")
    def get_series_comments_count(
        self, series_id: int = Field(description="Gamma series id")
    ) -> CountResponse:
        return CountResponse(**self.gamma_client.get_series_comments_count(series_id))

    @tool(description="Get a Polymarket series summary by id")
    def get_series_summary_by_id(
        self, series_id: int = Field(description="Gamma series id")
    ) -> SeriesSummary:
        return SeriesSummary(**self.gamma_client.get_series_summary_by_id(series_id))

    @tool(description="Get a Polymarket series summary by slug")
    def get_series_summary_by_slug(
        self, slug: str = Field(description="Gamma series slug")
    ) -> SeriesSummary:
        return SeriesSummary(**self.gamma_client.get_series_summary_by_slug(slug))

    @tool(description="Get Polymarket sports metadata")
    def list_sports(self) -> list[SportsMetadata]:
        response = self.gamma_client.list_sports()
        return [SportsMetadata(**item) for item in response]

    @tool(description="Get valid Polymarket sports market types")
    def list_sports_market_types(self) -> SportsMarketTypesResponse:
        return SportsMarketTypesResponse(**self.gamma_client.list_sports_market_types())

    @tool(description="List Polymarket teams")
    def list_teams(
        self,
        limit: int = Field(default=50, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = None,
        ascending: bool | None = None,
        league: list[str] | None = None,
        name: list[str] | None = None,
        abbreviation: list[str] | None = None,
    ) -> list[TeamSummary]:
        response = self.gamma_client.list_teams(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            league=league,
            name=name,
            abbreviation=abbreviation,
        )
        return [TeamSummary(**item) for item in response]

    @tool(description="Get a Polymarket team by id")
    def get_team_by_id(self, team_id: int = Field(description="Gamma team id")) -> TeamSummary:
        return TeamSummary(**self.gamma_client.get_team_by_id(team_id))
