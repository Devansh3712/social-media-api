from datetime import datetime
from pydantic import (
    BaseModel,
    Field
)

class Post(BaseModel):
    title: str
    content: str
    timestamp: datetime = datetime.now()

class PostResponse(BaseModel):
    id: int = Field(..., alias = "_id")
    title: str
    content: str