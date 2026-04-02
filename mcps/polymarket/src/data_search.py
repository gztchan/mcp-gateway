from pydantic import BaseModel, Field
from typing import Any, Optional
from pydash import get
from .utils.gamma import gamma_request
from fastmcp.tools import tool

class PolymarketSearch:
    def __init__(self):
        pass

    @tool(description="Search for events and markets on Polymarket")
    def search(self, query: str) -> dict:
        gamma_request(
          path="/public-search",
          method="GET",
        )