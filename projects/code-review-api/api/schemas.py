from pydantic import BaseModel, Field
from typing import Optional

REVIEW_FOCUSES = ["bugs", "style", "security", "performance", "all"]

class ReviewRequest(BaseModel):
    code: str = Field(min_length=1, max_length=10000)
    language: str = Field(default="python", max_length=32)
    focus: str = Field(default="all")

class ReviewResponse(BaseModel):
    feedback: str
    language: str
    focus: str
    line_count: int
