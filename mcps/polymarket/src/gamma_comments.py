from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import CommentRecord


class GammaCommentsTools:
    @tool(description="List Polymarket comments")
    def list_comments(
        self,
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
        parent_entity_type: str | None = None,
        parent_entity_id: int | None = None,
        get_positions: bool | None = None,
        holders_only: bool | None = None,
    ) -> list[CommentRecord]:
        response = self.gamma_client.list_comments(
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
            parent_entity_type=parent_entity_type,
            parent_entity_id=parent_entity_id,
            get_positions=get_positions,
            holders_only=holders_only,
        )
        return [CommentRecord(**item) for item in response]

    @tool(description="Get Polymarket comments by comment id")
    def get_comments_by_id(
        self,
        comment_id: int = Field(description="Gamma comment id"),
        get_positions: bool | None = None,
    ) -> list[CommentRecord]:
        response = self.gamma_client.get_comments_by_id(
            comment_id,
            get_positions=get_positions,
        )
        return [CommentRecord(**item) for item in response]

    @tool(description="Get Polymarket comments by user address")
    def get_comments_by_user_address(
        self,
        user_address: str = Field(description="Wallet address"),
        limit: int = Field(default=20, ge=1, le=500),
        offset: int = Field(default=0, ge=0),
        order: str | None = Field(default=None, description="Comma-separated sort fields"),
        ascending: bool | None = None,
    ) -> list[CommentRecord]:
        response = self.gamma_client.get_comments_by_user_address(
            user_address,
            limit=limit,
            offset=offset,
            order=order,
            ascending=ascending,
        )
        return [CommentRecord(**item) for item in response]
