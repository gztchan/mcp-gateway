from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import SearchResults

class GammaSearchTools:
    @tool(description="Search Polymarket markets, events, tags, and profiles")
    def search_public(
        self,
        q: str = Field(description="Search query"),
        cache: bool | None = None,
        events_status: str | None = None,
        limit_per_type: int | None = None,
        page: int | None = None,
        events_tag: list[str] | None = None,
        keep_closed_markets: int | None = None,
        sort: str | None = None,
        ascending: bool | None = None,
        search_tags: bool | None = None,
        search_profiles: bool | None = None,
        recurrence: str | None = None,
        exclude_tag_id: list[int] | None = None,
        optimized: bool | None = None,
    ) -> SearchResults:
        response = self.gamma_client.search_public(
            q=q,
            cache=cache,
            events_status=events_status,
            limit_per_type=limit_per_type,
            page=page,
            events_tag=events_tag,
            keep_closed_markets=keep_closed_markets,
            sort=sort,
            ascending=ascending,
            search_tags=search_tags,
            search_profiles=search_profiles,
            recurrence=recurrence,
            exclude_tag_id=exclude_tag_id,
            optimized=optimized,
        )
        return SearchResults(**response)

    @tool(description="Backward-compatible Polymarket search tool")
    def search(self, query: str = Field(description="Search query")) -> SearchResults:
        return self.search_public(q=query)
