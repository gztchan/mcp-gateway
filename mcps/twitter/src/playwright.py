from fastmcp.tools import tool
from local_playwright import PlaywrightBrowser
from .extractor import TwitterExtractor
from time import sleep
from pydantic import Field

class TwitterPlaywright(TwitterExtractor):
    @tool(description="Search for tweets")
    def search_tweets(
      self,
      query: str = Field(description="The query to search for"),
      tweets_limit: int = Field(description="The number of tweets to fetch", default=60)
    ) -> dict:
        browser = PlaywrightBrowser()
        browser.connect_browser()
        page = browser.create_page()

        def handle_response(response):
            if "SearchTimeline?variables=" in response.url:
                self.extract_search_tweets(response.json())

        page.goto(f"https://x.com/search?q={query}&src=typed_query", wait_until="domcontentloaded")
        page.wait_for_selector("main")

        while len(self.search_result.tweets) < tweets_limit:
            page.evaluate("""() => {
                window.scrollTo(0, document.body.scrollHeight);
            }""")
            sleep(3)

        page.remove_listener("response", handle_response)
        page.close()
        browser.disconnect_browser()
        return self.search_result_to_json()


    @tool(description="Fetch content of a tweet")
    def get_tweet(
      self,
      url: str = Field(description="The url of the tweet"),
      comments_limit: int = Field(description="The number of comments to fetch", default=100)
    ) -> dict:
        browser = PlaywrightBrowser()
        browser.connect_browser()
        page = browser.create_page()

        response_dict = {
            "detail": None,
            "has_more": True,
        }

        def handle_response(response):
            global detail
            if "TweetResultByRestId" in response.url:
                response_dict["detail"] = response.json()
            if "TweetDetail?variables=" in response.url:
                self.extract_tweet_comments(response.json())

        page.on("response", handle_response)

        page.goto(url, wait_until="domcontentloaded")
        # page.goto(f"https://x.com/thedankoe/status/2036824811712942576", wait_until="domcontentloaded")
        page.wait_for_selector("article")

        page.evaluate("""() => {
            window.scrollTo(0, document.body.scrollHeight);
        }""")
        sleep(3)

        self.extract_twitter_content(page)
        self.extract_twitter_metadata(response_dict["detail"])

        # TODO: 如果测试 3 次都是同样的 comments，则退出
        while len(self.result.comments) < comments_limit and response_dict["has_more"] is True:
            has_more = self.fetch_more_comments(page)
            response_dict["has_more"] = has_more
            sleep(3)

        page.remove_listener("response", handle_response)
        page.close()
        browser.disconnect_browser()
        return self.result_to_json()