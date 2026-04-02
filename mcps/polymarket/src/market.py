from pydantic import BaseModel, Field
from typing import Any, Optional
from pydash import get
from json import loads
from .utils.gamma import gamma_request

class MarketDetails(BaseModel):
    id: int = Field(description="The id of the market")
    condition_id: str = Field(description="The condition id of the market")
    slug: str = Field(description="The slug of the market")
    question: str = Field(description="The question of the market")
    yes_token: str = Field(description="The clob token ids of the market")
    no_token: str = Field(description="The clob token ids of the market")
    volume: float = Field(description="The volume of the market")
    active: bool = Field(description="Whether the market is active")
    closed: bool = Field(description="Whether the market is closed")

class PolymarketMarket:
    def __init__(self):
        pass

    def get_market_details(
        self,
        slug: str = Field(description="The slug of the market"),
    ) -> MarketDetails:
        response = gamma_request(
          path=f"/markets/slug/{slug}",
          method="GET",
        )
        clob_token_ids = get(response, "clobTokenIds")
        tokens = loads(clob_token_ids)
        return MarketDetails(
          id=get(response, "id"),
          condition_id=get(response, "conditionId"),
          slug=slug,
          question=get(response, "question"),
          active=get(response, "active"),
          closed=get(response, "closed"),
          yes_token=tokens[0],
          no_token=tokens[1],
          volume=float(get(response, "volume", "0")),
        )