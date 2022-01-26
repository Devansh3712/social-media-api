from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response
)
from ..database import Database
from ..oauth2 import get_current_user
from ..schemas import (
    Post,
    PostResponse,
    TokenData
)

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)
db = Database()

@router.get("/", response_model = List[PostResponse])
async def get_posts(user: TokenData = Depends(get_current_user), limit: int = 10):
    posts = db.read(user.username)
    if not posts or limit <= 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    if len(posts) - 1 >= limit:
        return posts[:limit]
    return posts[:-1]

@router.post("/", response_model = PostResponse, status_code = status.HTTP_201_CREATED)
async def create_post(post: Post, user: TokenData = Depends(get_current_user)):
    posts = db.read(user.username)
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict["_id"] = posts[-1]["_id"] + 1
    result = db.insert(user.username, post_dict)
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_dict

@router.get("/{id}", response_model = PostResponse)
async def get_post(id: int, user: TokenData = Depends(get_current_user)):
    posts = db.read(user.username)
    if not posts or id <= 0:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts:
        if post["_id"] == id:
            result = post
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return result

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, user: TokenData = Depends(get_current_user)) -> Response:
    posts = db.read(user.username)
    if not posts or id <= 0:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND)
    result = False
    for post in posts:
        if post["_id"] == id:
            result = db.delete(user.username, post)
            if not result:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = PostResponse)
async def update_post(id: int, updated_post: Post, user: TokenData = Depends(get_current_user)):
    posts = db.read(user.username)
    if not posts or id <= 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts:
        if post["_id"] == id:
            result = db.update(user.username, post, updated_post.dict())
            if not result:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    updated_post_dict = updated_post.dict()
    updated_post_dict["_id"] = id
    return updated_post_dict
