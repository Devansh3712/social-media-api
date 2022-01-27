from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    auth,
    posts,
    users,
    vote
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {
        "message": "Social-Media-API is working.",
        "source_code": "https://github.com/Devansh3712/social-media-api",
        "timestamp": datetime.now()
    }
