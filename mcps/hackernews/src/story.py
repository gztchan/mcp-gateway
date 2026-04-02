from __future__ import annotations

from fastmcp.tools import tool
from playwright.sync_api import sync_playwright
from pydantic import Field

from .models import HackerNewsStorySchema
from .scripts import story_script

class StoryToolset:
    @tool(description="Read a story from Hacker News")
    def read_story(
        self,
        cdp_url: str = Field(description="The CDP URL of the browser to get"),
        # https://news.ycombinator.com/item?id=48080201
        hackernews_story_url: str = Field(description="The URL of the story to get")
    ) -> HackerNewsStorySchema:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            page = browser.contexts[0].new_page()
            try:
                page.goto(hackernews_story_url)
                page.wait_for_selector("#hn_content")
                story = page.evaluate(story_script)
            except Exception as e:
                # page.close()
                raise e
            finally:
                page.close()
            return HackerNewsStorySchema(
                **story,
            )