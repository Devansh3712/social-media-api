from typing import List
from datetime import datetime
from pydantic import (
    BaseModel,
    conint,
    Field
)

class Post(BaseModel):
    title: str
    content: str
    timestamp: datetime = datetime.now()
    votes: int = 0
    voters: List[str] = []

class PostResponse(BaseModel):
    id: int = Field(..., alias = "_id")
    title: str
    content: str
    votes: int

class User(BaseModel):
    username: str
    password: str
    posts: int = 0
    timestamp: datetime = datetime.now()

class UserResponse(BaseModel):
    username: str
    posts: int
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class Vote(BaseModel):
    username: str
    id: int
    dir: conint(ge = 0, le = 1) # type: ignore