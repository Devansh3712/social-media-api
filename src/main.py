from datetime import datetime
from fastapi import FastAPI
from .routers import (
    auth,
    posts,
    users
)
from .utils import hash_password

app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Social-Media-API is working.",
        "source_code": "https://github.com/Devansh3712/social-media-api",
        "timestamp": datetime.now()
    }
