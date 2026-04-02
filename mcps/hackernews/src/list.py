from __future__ import annotations

import os
import time
from typing import Optional, Literal
from fastmcp.tools import tool
from playwright.sync_api import sync_playwright
from pydantic import Field

from .models import HackerNewsListSchema, HackerNewsSimpleStorySchema
from .scripts import simple_stories_script, fetch_more_stories_script

class ListToolset:
    @tool(description="Get listing stories from Hacker News")
    def get_listing_stories(
        self,
        cdp_url: str = Field(description="The CDP URL of the browser to get"),
        limit: Optional[int] = Field(default=100, ge=1, le=1000, description="The number of posts to get"),
        type: Literal["news", "ask", "show"] = Field(description="The type of list to get", default="news"),
    ) -> HackerNewsListSchema:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            page = browser.contexts[0].new_page()
            page.goto(f"https://news.ycombinator.com/{type}")

            simple_stories = []
            while len(simple_stories) < limit:
                page.wait_for_selector("#hn_content")
                stories = page.evaluate(simple_stories_script)
                if len(stories) == 0:
                    break
                total = len(stories)
                simple_stories.extend(stories[:limit - total])
                if len(simple_stories) >= limit:
                    break
                page.evaluate(fetch_more_stories_script)
            page.close()
            return HackerNewsListSchema(
                type=type,
                stories=[HackerNewsSimpleStorySchema(
                    **story,
                ) for story in simple_stories],
            )