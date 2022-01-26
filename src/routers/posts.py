from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Response
)
from ..database import Database
from ..schemas import (
    Post,
    PostResponse
)

router = APIRouter(prefix = "/posts")
db = Database()

@router.get("/{user}", response_model = List[PostResponse])
async def get_posts(user: str):
    posts = db.read(user)
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return posts[1:]

@router.post("/{user}", response_model = PostResponse, status_code = status.HTTP_201_CREATED)
async def create_post(user: str, post: Post):
    posts = db.read(user)
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict["_id"] = posts[-1]["_id"] + 1
    result = db.insert(user, post_dict)
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_dict

@router.get("/{user}/{id}", response_model = PostResponse)
async def get_post(user: str, id: int):
    posts = db.read(user)
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

@router.delete("/{user}/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(user: str, id: int) -> Response:
    posts = db.read(user)
    if not posts or id <= 0:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND)
    result = False
    for post in posts:
        if post["_id"] == id:
            result = db.delete(user, post)
            if not result:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{user}/{id}", response_model = PostResponse)
async def update_post(user: str, id: int, updated_post: Post):
    posts = db.read(user)
    if not posts or id <= 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts:
        if post["_id"] == id:
            result = db.update(user, post, updated_post.dict())
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
