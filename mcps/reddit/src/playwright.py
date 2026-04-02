from fastmcp.tools import tool
from local_playwright import PlaywrightBrowser
from .extractor import RedditExtractor, RedditSubreddit
from time import sleep
from pydantic import Field

class RedditPlaywright(RedditExtractor):
    @tool(description="Best reddit topics of a community or subreddit")
    def get_best_topics(
      self,
      community_url: str = Field(description="The url of the reddit subreddit"),
      topics_limit: int = Field(description="The number of topics to fetch", default=50)
    ) -> list[dict]:
        browser = PlaywrightBrowser()
        browser.connect_browser()
        page = browser.create_page()

        page.goto(community_url + "?feedViewType=compactView", wait_until="domcontentloaded")
        # page.goto("https://www.reddit.com/r/PressonNail_Addict/best/", wait_until="domcontentloaded")
        page.wait_for_selector("shreddit-feed")

        def get_subreddits():
            # TODO: 记录 data-post-id
            return page.evaluate("""() => {
                const articles = []
                const children = Array.from(document.querySelector("shreddit-feed").children);
                for (let i = 0; i < children.length; i++) {
                    const child = children[i];
                    if (child.getAttribute("data-post-id")) {
                        const post = child.querySelector("shreddit-post");
                        const url = post.getAttribute("permalink")
                        articles.push({
                            "url": "https://www.reddit.com" + url,
                            "title": post.getAttribute("post-title"),
                        });
                    }
                }
                return articles;
            }""")

        count = 0
        try_count = 0
        while True and try_count < 3:
            articles = get_subreddits()
            if len(articles) >= topics_limit:
                break;
            elif len(articles) == count:
                try_count += 1
                break;
            count = len(articles)
            page.evaluate("""() => {
                window.scrollTo(0, document.body.scrollHeight);
            }""")
            sleep(3)

        browser.disconnect_browser()
        return [RedditSubreddit(url=article["url"], title=article["title"]).model_dump() for article in articles]

    @tool(description="Fetch content and comments of a reddit topic")
    def get_topic(
      self,
      topic_url: str = Field(description="The url of the reddit topic"),
      comments_limit: int = Field(description="The number of comments to fetch", default=100)
    ) -> dict:
        browser = PlaywrightBrowser()
        browser.connect_browser()
        page = browser.create_page()

        response_dict = {
            "detail": None,
            "has_more": True,
        }

        # page.goto("https://www.reddit.com/r/LocalLLaMA/comments/1salgre/gemma_4_has_been_released/", wait_until="domcontentloaded")
        page.goto(topic_url, wait_until="domcontentloaded")
        page.wait_for_selector(".main-container")
        page.wait_for_selector("#comment-tree")

        self.extract_reddit_content(page)
        self.extract_reddit_metadata(page)

        count = 0
        while True and count < 3:
            response = self.get_more_comments(page, comments_limit)
            if response["has_more"] is False:
                count += 1
            if response["action"] == "click":
                page.click("#comment-tree > faceplate-partial").click()
                page.evaluate("""() => {
                    document.querySelector("#comment-tree > faceplate-partial").querySelector("faceplate-tracker > button").click()
                }""")
            elif response["action"] == "scroll":
                page.evaluate("""() => {
                    window.scrollTo(0, document.body.scrollHeight);
                }""")
            else:
                count += 1
            sleep(3)

        self.extract_reddit_comments(page, comments_limit)

        page.close()
        browser.disconnect_browser()
        return self.result_to_json()