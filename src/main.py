from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Optional
)
from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Response
)
from .database import Database
from .schemas import (
    Post,
    PostResponse
)

app = FastAPI()

@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Social-Media-API is working.",
        "timestamp": datetime.now()
    }

@app.get("/posts", response_model = List[PostResponse])
async def get_posts():
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return posts

@app.post("/posts", response_model = PostResponse, status_code = status.HTTP_201_CREATED)
async def create_post(post: Post):
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict["_id"] = posts[-1]["_id"] + 1
    result = Database().insert("posts", post_dict)
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_dict

@app.get("/posts/{id}", response_model = PostResponse)
async def get_post(id: int):
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
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

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> Response:
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = False
    for post in posts:
        if post["_id"] == id:
            result = Database().delete("posts", post)
            if not result:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model = PostResponse)
async def update_post(id: int, updated_post: Post):
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts:
        if post["_id"] == id:
            result = Database().update("posts", post, updated_post.dict())
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
