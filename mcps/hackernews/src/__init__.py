from __future__ import annotations
from fastmcp import FastMCP

from .list import ListToolset
from .story import StoryToolset

list_toolset = ListToolset()
story_toolset = StoryToolset()

hackernews_mcp = FastMCP("HackerNews")

hackernews_mcp.add_tool(list_toolset.get_listing_stories)
hackernews_mcp.add_tool(story_toolset.read_story)