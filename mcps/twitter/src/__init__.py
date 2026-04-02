from fastmcp import FastMCP
from .playwright import TwitterPlaywright

class Twitter(TwitterPlaywright):
    pass

twitter_mcp = FastMCP("Twitter")
twitter = Twitter()

# twitter_mcp.add_tool(twitter.search_tweets)
twitter_mcp.add_tool(twitter.get_tweet)
twitter_mcp.add_tool(twitter.search_tweets)