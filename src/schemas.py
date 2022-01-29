from typing import (
    List,
    Optional
)
from datetime import datetime
from pydantic import (
    BaseModel,
    conint,
    Field
)
from pydantic.class_validators import root_validator

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
    followers: List[str] = []
    following: List[str] = []
    followers_count: int = 0
    following_count: int = 0
    private: bool = False
    timestamp: datetime = datetime.now()

class UserResponse(BaseModel):
    username: str
    posts: int
    followers: Optional[List[str]]
    following: Optional[List[str]]
    followers_count: int
    following_count: int
    private: bool
    timestamp: datetime
    
    @root_validator
    def account_privacy(cls, values):
        if values["private"]:
            values["followers"] = None
            values["following"] = None
        return values

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class Vote(BaseModel):
    username: str
    id: int
    dir: conint(ge = 0, le = 1) # type: ignore
