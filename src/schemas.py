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

class User(BaseModel):
    username: str
    password: str
    timestamp: datetime = datetime.now()

class UserResponse(BaseModel):
    username: str
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str