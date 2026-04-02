import os
import json
from fastmcp import FastMCP
from fastmcp.server import create_proxy

from remote import remote_mcps_provider
from mcps_hackernews import hackernews_mcp
from mcps_reddit import reddit_mcp
# from local_mcps_twitter import twitter_mcp
#from local_mcps_polymarket import polymarket_mcp

mcp = FastMCP("Orchestrator")

mcp.mount(remote_mcps_provider, namespace="remote")

mcp.mount(hackernews_mcp, namespace="hackernews")
mcp.mount(reddit_mcp, namespace="reddit")
# mcp.mount(twitter_mcp, namespace="twitter")
# mcp.mount(polymarket_mcp, namespace="polymarket")

if __name__ == "__main__":
    mcp.run(
        host="0.0.0.0",
        port=9090,
        transport="streamable-http",
        show_banner=False,
    )
