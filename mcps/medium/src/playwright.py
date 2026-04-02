from fastmcp.tools import tool

class MediumPlaywright:
    @tool(description="Search for posts related to query in medium")
    def search_posts(
      self,
      query: str,
      topics_limit: int = 10
    ) -> list[str]:
      # Open reddit and search for topics
      # Browse each topic and comments
      return ["topic1", "topic2", "topic3"]

    @tool(description="Get a post content from a medium")
    def get_post(
      self,
      post_url: str,
    ) -> list[str]:
      # Open reddit and search for topics
      # Browse each topic and comments
      return ["topic1", "topic2", "topic3"]