from pydantic import BaseModel, Field
from typing import Any, Optional
from playwright.sync_api import Page
from pydash import get

class RedditContent(BaseModel):
    title: str = Field(description="The title of the reddit topic")
    content: str = Field(description="The content of the reddit topic")

class RedditMetadata(BaseModel):
    url: str = Field(description="The url of the reddit topic")
    author: str = Field(description="The author of the reddit topic")
    created_at: str = Field(description="The date and time the reddit topic was created")
    likes: int = Field(description="The number of likes the reddit topic has")
    comments: int = Field(description="The number of comments the reddit topic has")

class RedditComment(BaseModel):
    author: Optional[str] = Field(description="The author of the comment")
    reply_to: Optional[str] = Field(description="The comment the comment is replying to")
    content: Optional[str] = Field(description="The full text of the comment")
    likes: int = Field(description="The number of likes the comment has")
    created_at: str = Field(description="The date and time the comment was created")

class RedditResult(BaseModel):
    content: Optional[RedditContent] = None
    metadata: Optional[RedditMetadata] = None
    comments: list[RedditComment] = []

class RedditSubreddit(BaseModel):
    url: str = Field(description="The url of the reddit subreddit")
    title: str = Field(description="The title of the reddit subreddit")

class RedditExtractor:
    def __init__(self):
        self.result = RedditResult()
        self.last_thingid = None

    def extract_reddit_content(self, page: Page):
        data = page.evaluate("""() => {
            const post = document.querySelector('shreddit-post');
            return {
                "title": post.querySelector("h1").innerText,
                "content": post.innerHTML,
            }
        }""")
        self.result.content = RedditContent(
            title=data["title"],
            content=data["content"]
        )

    def extract_reddit_metadata(self, page: Page):
        data = page.evaluate("""() => {
            const post = document.querySelector("shreddit-post");
            const likesStr = post.shadowRoot.querySelector("shreddit-vote-animations faceplate-number").getAttribute("number")
            const commentsStr = post.shadowRoot.querySelector("[data-post-click-location='comments-button'] faceplate-number").getAttribute("number")
            return {
                "url": location.href,
                "author": post.querySelector("#pdp-credit-bar").querySelector("[slot='authorName']").querySelector('faceplate-tracker').textContent,
                "created_at": post.querySelector("time").getAttribute("datetime"),
                "likes": likesStr ? parseInt(likesStr) : 0,
                "comments": commentsStr ? parseInt(commentsStr) : 0,
            }
        }""")
        self.result.metadata = RedditMetadata(
            url=get(data, "url"),
            author=get(data, "author"),
            created_at=get(data, "created_at"),
            likes=get(data, "likes"),
            comments=get(data, "comments"),
        )

    def extract_reddit_comments(self, page: Page, comments_limit: int):
        comments = page.evaluate("""(data) => {
            function recurse_comment(root_comment) {
                const comments = []
                const stack = [{ comment: root_comment, reply_to: null }]
                while (stack.length > 0) {
                    const { comment, reply_to } = stack.pop()
                    const author = comment.querySelector("[slot='commentMeta']")?.querySelector("rpl-hovercard")?.querySelector("faceplate-tracker")?.textContent?.trim() || "[deleted]"
                    const content = comment.querySelector("div[slot='comment']")?.textContent?.trim() || null
                    const likes = comment.querySelector("div[slot='actionRow'] > shreddit-comment-action-row")?.shadowRoot?.querySelector("shreddit-vote-animations faceplate-number")?.getAttribute("number") ?? 0
                    const created_at = comment.querySelector("[slot='commentMeta']")?.querySelector("time")?.getAttribute("datetime") ?? null
                    comments.push({
                        "author": author,
                        "reply_to": reply_to,
                        "content": content,
                        "likes": likes ? parseInt(likes) : 0,
                        "created_at": created_at,
                    })
                    for (let i = 0; i < comment.children.length; i++) {
                        const child = comment.children[i]
                        if (child.getAttribute("thingid")) {
                            stack.push({ comment: child, reply_to: author })
                        }
                    }
                }
                return comments;
            }
            let user_comments = []
            const comments = Array.from(document.querySelector("#comment-tree").children)
            for (let i = 0; i < comments.length; i++) {
                const thingid = comments[i].getAttribute("thingid")
                if (!!thingid) {
                    user_comments = user_comments.concat(recurse_comment(comments[i]))
                }
                if (user_comments.length >= data.comments_limit) {
                    break;
                }
            }
            return user_comments;
        }""", { "comments_limit": comments_limit })

        reddit_comments = []
        for comment in comments:        
            reddit_comments.append(RedditComment(
                author=get(comment, "author"),
                reply_to=get(comment, "reply_to"),
                content=get(comment, "content"),
                likes=get(comment, "likes"),
                created_at=get(comment, "created_at"),
            ))

        self.result.comments.extend(reddit_comments)
    
    def get_more_comments(self, page: Page, comments_limit: int):
        response = page.evaluate("""(data) => {
                let last_thingid = null;
                const comments = Array.from(document.querySelector("#comment-tree").children)
                if (comments.length >= data.comments_limit) {
                    return {
                        "has_more": false,
                        "last_thingid": null,
                        "action": null,
                        "comments": comments.length,
                    }
                }
                for (let i = 0; i < comments.length; i++) {
                    const thingid = comments[i].getAttribute("thingid")
                    last_thingid = thingid ?? null;
                }
                const button = document.querySelector("#comment-tree > faceplate-partial")?.querySelector("faceplate-tracker > button")
                return {
                    "has_more": !!button ? true : (last_thingid === null ? false: last_thingid !== data.last_thingid),
                    "last_thingid": last_thingid,
                    "action": button ? "click" : "scroll",
                    "comments": comments.length,
                }
            }""", { "last_thingid": self.last_thingid, "comments_limit": comments_limit })
        self.last_thingid = get(response, "last_thingid", None)
        return {
            "has_more": get(response, "has_more"),
            "action": get(response, "action"),
            "comments": get(response, "comments"),
        }
        

    def result_to_json(self):
        return self.result.model_dump()