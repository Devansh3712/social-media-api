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
from src.database import Database
from src.schema import Post

app = FastAPI()

@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Social-Media-API is working.",
        "timestamp": datetime.now()
    }

@app.get("/posts")
async def get_posts() -> Dict[str, List[Dict[str, Any]]]:
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return {
        "data": posts # type: ignore
    }

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: Post) -> Dict[str, Any]:
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict["_id"] = posts[-1]["_id"] + 1 # type: ignore
    result = Database().insert("posts", post_dict)
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {
        "message": "Post added successfully.",
        "title": post.title,
        "timestamp": post.timestamp
    }

@app.get("/posts/{id}")
async def get_post(id: int) -> Dict[str, Any]:
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts: # type: ignore
        if post["_id"] == id:
            result = post
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return {
        "data": result
    }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> Response:
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = False
    for post in posts: # type: ignore
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

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post):
    posts = Database().read("posts")
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    result = None
    for post in posts: # type: ignore
        if post["_id"] == id:
            result = Database().update("posts", post, updated_post.dict())
            if not result:
                raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return {
        "message": "Post updated successfully.",
        "title": updated_post.title,
        "timestamp": datetime.now()
    }
