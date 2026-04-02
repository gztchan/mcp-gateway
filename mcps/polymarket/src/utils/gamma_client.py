from __future__ import annotations

import os
from typing import Any

from .http import request_json, request_text


class GammaClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.getenv(
            "GAMMA_API_URL", "https://gamma-api.polymarket.com"
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return request_json(base_url=self.base_url, path=path, params=params)

    def post(self, path: str, json: Any) -> Any:
        return request_json(base_url=self.base_url, path=path, method="POST", json=json)

    def get_text(self, path: str, params: dict[str, Any] | None = None) -> str:
        return request_text(base_url=self.base_url, path=path, params=params)

    def get_status(self) -> str:
        return self.get_text("/status")

    def get_team_by_id(self, team_id: int) -> Any:
        return self.get(f"/teams/{team_id}")

    def list_events(self, **params: Any) -> Any:
        return self.get("/events", params)

    def list_events_pagination(self, **params: Any) -> Any:
        return self.get("/events/pagination", params)

    def list_events_results(self, **params: Any) -> Any:
        return self.get("/events/results", params)

    def get_event_by_id(self, event_id: int, **params: Any) -> Any:
        return self.get(f"/events/{event_id}", params)

    def get_event_tweet_count(self, event_id: int) -> Any:
        return self.get(f"/events/{event_id}/tweet-count")

    def get_event_comments_count(self, event_id: int) -> Any:
        return self.get(f"/events/{event_id}/comments/count")

    def get_event_tags(self, event_id: int) -> Any:
        return self.get(f"/events/{event_id}/tags")

    def get_event_by_slug(self, slug: str, **params: Any) -> Any:
        return self.get(f"/events/slug/{slug}", params)

    def list_event_creators(self, **params: Any) -> Any:
        return self.get("/events/creators", params)

    def get_event_creator(self, creator_id: int) -> Any:
        return self.get(f"/events/creators/{creator_id}")

    def list_markets(self, **params: Any) -> Any:
        return self.get("/markets", params)

    def list_markets_keyset(self, **params: Any) -> Any:
        return self.get("/markets/keyset", params)

    def get_markets_information(self, filters: dict[str, Any]) -> Any:
        return self.post("/markets/information", filters)

    def get_abridged_markets(self, filters: dict[str, Any]) -> Any:
        return self.post("/markets/abridged", filters)

    def get_market_by_id(self, market_id: int | str, **params: Any) -> Any:
        return self.get(f"/markets/{market_id}", params)

    def get_market_description(self, market_id: int | str) -> Any:
        return self.get(f"/markets/{market_id}/description")

    def get_market_tags(self, market_id: int | str) -> Any:
        return self.get(f"/markets/{market_id}/tags")

    def get_market_by_slug(self, slug: str, **params: Any) -> Any:
        return self.get(f"/markets/slug/{slug}", params)

    def list_events_keyset(self, **params: Any) -> Any:
        return self.get("/events/keyset", params)

    def search_public(self, **params: Any) -> Any:
        return self.get("/public-search", params)

    def list_tags(self, **params: Any) -> Any:
        return self.get("/tags", params)

    def get_tag_by_id(self, tag_id: int, **params: Any) -> Any:
        return self.get(f"/tags/{tag_id}", params)

    def get_tag_by_slug(self, slug: str, **params: Any) -> Any:
        return self.get(f"/tags/slug/{slug}", params)

    def get_related_tags_by_id(self, tag_id: int, **params: Any) -> Any:
        return self.get(f"/tags/{tag_id}/related-tags", params)

    def get_related_tags_by_slug(self, slug: str, **params: Any) -> Any:
        return self.get(f"/tags/slug/{slug}/related-tags", params)

    def get_tags_related_to_tag_by_id(self, tag_id: int, **params: Any) -> Any:
        return self.get(f"/tags/{tag_id}/related-tags/tags", params)

    def get_tags_related_to_tag_by_slug(self, slug: str, **params: Any) -> Any:
        return self.get(f"/tags/slug/{slug}/related-tags/tags", params)

    def list_series(self, **params: Any) -> Any:
        return self.get("/series", params)

    def get_series_by_id(self, series_id: int, **params: Any) -> Any:
        return self.get(f"/series/{series_id}", params)

    def get_series_comments_count(self, series_id: int) -> Any:
        return self.get(f"/series/{series_id}/comments/count")

    def get_series_summary_by_id(self, series_id: int) -> Any:
        return self.get(f"/series-summary/{series_id}")

    def get_series_summary_by_slug(self, slug: str) -> Any:
        return self.get(f"/series-summary/slug/{slug}")

    def list_comments(self, **params: Any) -> Any:
        return self.get("/comments", params)

    def get_comments_by_id(self, comment_id: int, **params: Any) -> Any:
        return self.get(f"/comments/{comment_id}", params)

    def get_comments_by_user_address(self, user_address: str, **params: Any) -> Any:
        return self.get(f"/comments/user_address/{user_address}", params)

    def get_public_profile(self, address: str) -> Any:
        return self.get("/public-profile", {"address": address})

    def get_public_profile_by_user_address(self, user_address: str) -> Any:
        return self.get(f"/profiles/user_address/{user_address}")

    def list_sports(self) -> Any:
        return self.get("/sports")

    def list_sports_market_types(self) -> Any:
        return self.get("/sports/market-types")

    def list_teams(self, **params: Any) -> Any:
        return self.get("/teams", params)
