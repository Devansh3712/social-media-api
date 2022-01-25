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
from schema import Post

app = FastAPI()

posts = [
    {
        "id": 0,
        "title": "post 1",
        "content": "lorem ipsum"
    },
    {
        "id": 1,
        "title": "post 2",
        "content": "lorem ipsum"
    }
]

@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Social-Media-API is working.",
        "timestamp": datetime.now()
    }

@app.get("/posts")
async def get_posts() -> Dict[str, List[Dict[str, Any]]]:
    return {
        "data": posts
    }

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: Post) -> Dict[str, Any]:
    post_dict = post.dict()
    post_dict["id"] = posts[-1]["id"] + 1 # type: ignore
    posts.append(post_dict)
    return {
        "message": "Post added successfully.",
        "title": post.title,
        "timestamp": post.timestamp
    }

@app.get("/posts/{id}")
async def get_post(id: int) -> Dict[str, Any]:
    result: Optional[Dict[str, Any]] = None
    for post in posts:
        if post["id"] == id:
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
    result: bool = False
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
            result = True
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post):
    result: Optional[int] = None
    for post in posts:
        if post["id"] == id:
            result = posts.index(post)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with ID {id} doesn't exist in database."
        )
    post_dict = updated_post.dict()
    post_dict["id"] = id
    posts[result] = post_dict
    return {
        "message": "Post updated successfully.",
        "title": updated_post.title,
        "timestamp": datetime.now()
    }
