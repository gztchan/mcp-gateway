from __future__ import annotations

import json

from fastmcp.tools import tool
from pydantic import Field

from .models import KeysetMarketsResponse, MarketDescription, MarketDetails, MarketOutcomeToken, TagDetails


def _parse_market_tokens(payload: dict) -> tuple[list[MarketOutcomeToken], str | None, str | None]:
    tokens: list[MarketOutcomeToken] = []

    raw_tokens = payload.get("tokens")
    if isinstance(raw_tokens, list):
        tokens = [MarketOutcomeToken(**token) for token in raw_tokens]
    elif payload.get("clobTokenIds"):
        try:
            token_ids = json.loads(payload["clobTokenIds"])
        except (TypeError, json.JSONDecodeError):
            token_ids = []
        labels = ["YES", "NO"]
        tokens = [
            MarketOutcomeToken(token_id=str(token_id), outcome=labels[index] if index < 2 else None)
            for index, token_id in enumerate(token_ids)
        ]

    yes_token = tokens[0].token_id if len(tokens) > 0 else None
    no_token = tokens[1].token_id if len(tokens) > 1 else None
    return tokens, yes_token, no_token


def _to_market_details(payload: dict) -> MarketDetails:
    tokens, yes_token, no_token = _parse_market_tokens(payload)
    return MarketDetails(
        id=payload.get("id"),
        conditionId=payload.get("conditionId"),
        slug=payload.get("slug"),
        question=payload.get("question"),
        active=payload.get("active"),
        closed=payload.get("closed"),
        archived=payload.get("archived"),
        volume=float(payload["volume"]) if payload.get("volume") is not None else None,
        liquidity=float(payload["liquidity"]) if payload.get("liquidity") is not None else None,
        yes_token=yes_token,
        no_token=no_token,
        tokens=tokens,
    )


class GammaMarketsTools:
    @tool(description="List Polymarket markets from the Gamma API")
    def list_markets(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        id: list[int] | None = None,
        slug: list[str] | None = None,
        clob_token_ids: list[str] | None = None,
        condition_ids: list[str] | None = None,
        market_maker_address: list[str] | None = None,
        liquidity_num_min: float | None = None,
        liquidity_num_max: float | None = None,
        volume_num_min: float | None = None,
        volume_num_max: float | None = None,
        start_date_min: str | None = None,
        start_date_max: str | None = None,
        end_date_min: str | None = None,
        end_date_max: str | None = None,
        tag_id: int | None = None,
        related_tags: bool | None = None,
        cyom: bool | None = None,
        uma_resolution_status: str | None = None,
        game_id: str | None = None,
        sports_market_types: list[str] | None = None,
        rewards_min_size: float | None = None,
        question_ids: list[str] | None = None,
        include_tag: bool | None = None,
        closed: bool | None = None,
    ) -> list[MarketDetails]:
        response = self.gamma_client.list_markets(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            id=id,
            slug=slug,
            clob_token_ids=clob_token_ids,
            condition_ids=condition_ids,
            market_maker_address=market_maker_address,
            liquidity_num_min=liquidity_num_min,
            liquidity_num_max=liquidity_num_max,
            volume_num_min=volume_num_min,
            volume_num_max=volume_num_max,
            start_date_min=start_date_min,
            start_date_max=start_date_max,
            end_date_min=end_date_min,
            end_date_max=end_date_max,
            tag_id=tag_id,
            related_tags=related_tags,
            cyom=cyom,
            uma_resolution_status=uma_resolution_status,
            game_id=game_id,
            sports_market_types=sports_market_types,
            rewards_min_size=rewards_min_size,
            question_ids=question_ids,
            include_tag=include_tag,
            closed=closed,
        )
        return [_to_market_details(item) for item in response]

    @tool(description="Get a Polymarket market by numeric id")
    def get_market_by_id(
        self,
        market_id: int = Field(description="Gamma market id"),
        include_tag: bool | None = None,
    ) -> MarketDetails:
        return _to_market_details(self.gamma_client.get_market_by_id(market_id, include_tag=include_tag))

    @tool(description="Get a Polymarket market by slug")
    def get_market_by_slug(
        self,
        slug: str = Field(description="Gamma market slug"),
        include_tag: bool | None = None,
    ) -> MarketDetails:
        return _to_market_details(self.gamma_client.get_market_by_slug(slug, include_tag=include_tag))

    @tool(description="Get details of a Polymarket market by slug")
    def get_market_details(
        self, slug: str = Field(description="Gamma market slug")
    ) -> MarketDetails:
        return self.get_market_by_slug(slug)

    @tool(description="Get Polymarket market description by id")
    def get_market_description(
        self, market_id: int = Field(description="Gamma market id")
    ) -> MarketDescription:
        return MarketDescription(**self.gamma_client.get_market_description(market_id))

    @tool(description="Get tags attached to a Polymarket market")
    def get_market_tags(
        self, market_id: int = Field(description="Gamma market id")
    ) -> list[TagDetails]:
        response = self.gamma_client.get_market_tags(market_id)
        return [TagDetails(**item) for item in response]

    @tool(description="Query Polymarket markets using information filters")
    def get_markets_information(self, filters: dict) -> list[MarketDetails]:
        response = self.gamma_client.get_markets_information(filters)
        return [_to_market_details(item) for item in response]

    @tool(description="Query abridged Polymarket markets using information filters")
    def get_abridged_markets(self, filters: dict) -> list[MarketDetails]:
        response = self.gamma_client.get_abridged_markets(filters)
        return [_to_market_details(item) for item in response]

    @tool(description="List Polymarket markets using cursor pagination")
    def list_markets_keyset(
        self,
        limit: int = Field(default=20, ge=1, le=1000),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        after_cursor: str | None = None,
        id: list[int] | None = None,
        slug: list[str] | None = None,
        closed: bool | None = None,
        decimalized: bool | None = None,
        clob_token_ids: list[str] | None = None,
        condition_ids: list[str] | None = None,
        question_ids: list[str] | None = None,
        market_maker_address: list[str] | None = None,
        liquidity_num_min: float | None = None,
        liquidity_num_max: float | None = None,
        volume_num_min: float | None = None,
        volume_num_max: float | None = None,
        start_date_min: str | None = None,
        start_date_max: str | None = None,
        end_date_min: str | None = None,
        end_date_max: str | None = None,
        tag_id: list[int] | None = None,
        related_tags: bool | None = None,
        tag_match: str | None = None,
        cyom: bool | None = None,
        rfq_enabled: bool | None = None,
        uma_resolution_status: str | None = None,
        game_id: str | None = None,
        sports_market_types: list[str] | None = None,
        include_tag: bool | None = None,
        locale: str | None = None,
    ) -> KeysetMarketsResponse:
        response = self.gamma_client.list_markets_keyset(
            limit=limit,
            order=order,
            ascending=ascending,
            after_cursor=after_cursor,
            id=id,
            slug=slug,
            closed=closed,
            decimalized=decimalized,
            clob_token_ids=clob_token_ids,
            condition_ids=condition_ids,
            question_ids=question_ids,
            market_maker_address=market_maker_address,
            liquidity_num_min=liquidity_num_min,
            liquidity_num_max=liquidity_num_max,
            volume_num_min=volume_num_min,
            volume_num_max=volume_num_max,
            start_date_min=start_date_min,
            start_date_max=start_date_max,
            end_date_min=end_date_min,
            end_date_max=end_date_max,
            tag_id=tag_id,
            related_tags=related_tags,
            tag_match=tag_match,
            cyom=cyom,
            rfq_enabled=rfq_enabled,
            uma_resolution_status=uma_resolution_status,
            game_id=game_id,
            sports_market_types=sports_market_types,
            include_tag=include_tag,
            locale=locale,
        )
        return KeysetMarketsResponse(
            markets=[_to_market_details(item) for item in response.get("markets", [])],
            next_cursor=response.get("next_cursor"),
        )
