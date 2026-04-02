from typing import Literal, Optional
from pydantic import BaseModel, Field

class HackerNewsAuthorSchema(BaseModel):
    id: str
    username: str
    profile_url: str

class HackerNewsCommentSchema(BaseModel):
    id: str
    content: str = Field(description="The content of the comment")
    author: HackerNewsAuthorSchema = Field(description="The author of the comment")
    created_at: str = Field(description="The date and time the comment was created")

class HackerNewsSimpleStorySchema(BaseModel):
    id: str = Field(description="The ID of the story")
    url: str = Field(description="The URL of the story")
    title: str = Field(description="The title of the story")
    points: Optional[str] = Field(description="The points of the story")
    comments: str = Field(description="The comments of the story")
    created_at: str = Field(description="The date and time the story was created")
    author: Optional[HackerNewsAuthorSchema] = Field(description="The user who posted the story")

class HackerNewsListSchema(BaseModel):
    type: Literal["news", "ask", "show"] = Field(description="The type of list")
    stories: list[HackerNewsSimpleStorySchema] = Field(default=[], description="The stories of the list")

class HackerNewsStorySchema(BaseModel):
    url: str = Field(description="The URL of the story")
    title: str = Field(description="The title of the story")
    resource: str = Field(description="The resource of the story")
    author: HackerNewsAuthorSchema = Field(description="The user who posted the story")
    comments: list[HackerNewsCommentSchema] = Field(default=[], description="The comments of the story")