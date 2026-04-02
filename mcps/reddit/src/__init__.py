from fastmcp import FastMCP
from .playwright import RedditPlaywright

class Reddit(RedditPlaywright):
    pass

reddit_mcp = FastMCP("Reddit")
reddit = Reddit()

reddit_mcp.add_tool(reddit.get_topic)
reddit_mcp.add_tool(reddit.get_best_topics)