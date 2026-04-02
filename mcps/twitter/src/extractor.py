from pydantic import BaseModel, Field
from typing import Any, Optional
from local_playwright import Page
from pydash import get

class TwitterContent(BaseModel):
    title: str = Field(description="The title of the tweet")
    content: str = Field(description="The content of the tweet")

class TwitterMetadata(BaseModel):
    tweet_id: str = Field(description="The ID of the tweet")
    author: str = Field(description="The author of the tweet")
    created_at: str = Field(description="The date and time the tweet was created")
    likes: int = Field(description="The number of likes the tweet has")
    replies: int = Field(description="The number of replies to the tweet")
    retweets: int = Field(description="The number of retweets the tweet has")
    quotes: int = Field(description="The number of quotes the tweet has")
    bookmark_count: int = Field(description="The number of bookmarks the tweet has")

class TwitterComment(BaseModel):
    comment_id: str = Field(description="The ID of the comment")
    full_text: str = Field(description="The full text of the comment")
    likes: int = Field(description="The number of likes the comment has")
    replies: int = Field(description="The number of replies to the comment")
    retweets: int = Field(description="The number of retweets the comment has")
    quotes: int = Field(description="The number of quotes the comment has")
    bookmark_count: int = Field(description="The number of bookmarks the comment has")
    created_at: str = Field(description="The date and time the comment was created")

class TwitterResult(BaseModel):
    content: Optional[TwitterContent] = None
    metadata: Optional[TwitterMetadata] = None
    comments: list[TwitterComment] = []

class TwitterSearchTweet(BaseModel):
    tweet_id: str = Field(description="The ID of the tweet")
    url: str = Field(description="The url of the tweet")
    full_text: str = Field(description="The full text of the tweet")
    likes: int = Field(description="The number of likes the tweet has")
    replies: int = Field(description="The number of replies to the tweet")
    retweets: int = Field(description="The number of retweets the tweet has")
    quotes: int = Field(description="The number of quotes the tweet has")
    bookmark_count: int = Field(description="The number of bookmarks the tweet has")

class TwitterSearchResult(BaseModel):
    tweets: list[TwitterSearchTweet] = []

class TwitterExtractor:
    def __init__(self):
        self.result = TwitterResult()
        self.search_result = TwitterSearchResult()

    def extract_twitter_content(self, page: Page):
        article = page.evaluate("""() => {
            const article = document.querySelector('article');
            return article.innerHTML;
        }""")
        self.result.content = TwitterContent(
            title=page.title(),
            content=article
        )

    def extract_twitter_metadata(self, response: dict):
        user = get(response, "data.tweetResult.result.core.user_results.result")
        legacy = get(response, "data.tweetResult.result.legacy")
        self.result.metadata = TwitterMetadata(
            tweet_id=get(legacy, "id_str"),
            author=get(user, "core.screen_name"),
            created_at=get(legacy, "created_at"),
            likes=get(legacy, "favorite_count"),
            replies=get(legacy, "reply_count"),
            quotes=get(legacy, "quote_count"),
            retweets=get(legacy, "retweet_count"),
            bookmark_count=get(legacy, "bookmark_count"),
        )

    def extract_tweet_comments(self, response: dict):
        entries = []
        for instruction in get(response, "data.threaded_conversation_with_injections_v2.instructions"):
            if instruction.get("type") == "TimelineAddEntries":
                entries.extend(instruction.get("entries", []))

        comments = []

        for entry in entries:
            typename = get(entry, "content.__typename")
            if typename != "TimelineTimelineModule":
                continue

            tweet = get(entry, "content.items.0.item.itemContent")
            result = get(tweet, "tweet_results.result")
            legacy = get(result, "legacy")

            if legacy is None:
                continue
        
            comments.append(TwitterComment(
                comment_id=get(legacy, "id_str"),
                full_text=get(legacy, "full_text"),
                likes=get(legacy, "favorite_count"),
                replies=get(legacy, "reply_count"),
                retweets=get(legacy, "retweet_count"),
                quotes=get(legacy, "quote_count"),
                bookmark_count=get(legacy, "bookmark_count"),
                created_at=get(legacy, "created_at"),
            ))

        self.result.comments.extend(comments)
    
    def fetch_more_comments(self, page: Page):
        def is_no_more_comments(page: Page):
            return page.evaluate("""() => {
                const comments = Array.from(document.querySelectorAll("[data-testid='cellInnerDiv']"))
                if (comments.length <= 3) {
                    return true;
                }
                const potential_spam_bottom = comments[comments.length - 2].textContent
                return potential_spam_bottom.includes("Show probable spam");
            }""")
        if (is_no_more_comments(page)):
            return False
        page.evaluate("""() => {
            window.scrollTo(0, document.body.scrollHeight);
        }""")
        return True

    def result_to_json(self):
        return self.result.model_dump()

    def extract_search_tweets(self, response: dict):
        entries = get(response, "data.search_by_raw_query.search_timeline.timeline.instructions.0.entries")
        tweets = []
        for entry in entries:
            if get(entry, "content.__typename") == "TimelineTimelineItem":
                result = get(entry, "content.itemContent.tweet_results.result")
                legacy = get(result, "legacy")
                user = get(result, "core.user_results.result")
                tweets.append(TwitterSearchTweet(
                    tweet_id=get(legacy, "id_str"),
                    url=f"https://x.com/{get(user, "core.screen_name")}/status/{get(legacy, "id_str")}",
                    full_text=get(legacy, "full_text"),
                    likes=get(legacy, "favorite_count"),
                    replies=get(legacy, "reply_count"),
                    retweets=get(legacy, "retweet_count"),
                    quotes=get(legacy, "quote_count"),
                    bookmark_count=get(legacy, "bookmark_count"),
                ))

        self.search_result.tweets = tweets

    def search_result_to_json(self):
        return self.search_result.model_dump()