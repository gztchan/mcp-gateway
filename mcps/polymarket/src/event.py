from pydantic import BaseModel, Field
from typing import Any, Optional
from pydash import get
from fastmcp.tools import tool
from .utils.gamma import gamma_request

class EventDetails(BaseModel):
    id: int = Field(description="The id of the event")
    title: str = Field(description="The title of the event")
    slug: str = Field(description="The slug of the event")
    description: str = Field(description="The description of the event")
    active: bool = Field(description="Whether the event is active")
    closed: bool = Field(description="Whether the event is closed")
    liquidity: float = Field(description="The liquidity of the event")
    volume: float = Field(description="The volume of the event")
    start_date: str = Field(description="The date and time the event starts")
    end_date: Optional[str] = Field(description="The date and time the event ends")
    created_at: str = Field(description="The date and time the event was created")
    markets: list[str] = Field(description="The slugs of the markets of the event")

class PolymarketEvent:
    def __init__(self):
        pass

    @tool(description="Get details of a polymarket event")
    def get_event_details(
        self,
        slug: str = Field(description="The slug of the event"),
    ) -> EventDetails:
        response = gamma_request(
          path=f"events/slug/{slug}",
          method="GET",
        )
        print(response)
        return EventDetails(
            id=get(response, "id"),
            slug=get(response, "slug"),
            title=get(response, "title"),
            description=get(response, "description"),
            active=get(response, "active"),
            closed=get(response, "closed"),
            liquidity=get(response, "liquidity"),
            volume=get(response, "volume"),
            markets=[get(x, "slug") for x in get(response, "markets", [])],
            start_date=get(response, "startDate"),
            end_date=get(response, "endDate"),
            created_at=get(response, "createdAt"),
        )