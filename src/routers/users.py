from copy import deepcopy
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from ..database import Database
from ..schemas import (
    TokenData,
    User,
    UserResponse
)
from ..oauth2 import get_current_user
from ..utils import hash_password

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)
db = Database()

@router.post("/", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def create_user(user: User):
    if not db.collection_exists(user.username):
        user_dict = user.dict()
        user_dict["password"] = hash_password(user_dict["password"])
        user_dict["_id"] = 0
        result = db.insert(user.username, user_dict)
        return user.dict()
    raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{username}", response_model = UserResponse)
async def get_user(username: str):
    result = db.read(username, [{ "_id": 0 }])
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User {username} doesn't exist in database."
        )
    return result[0]

@router.post("/follow/{username}", status_code = status.HTTP_201_CREATED)
async def follow_user(username: str, user: TokenData = Depends(get_current_user)):
    follower = db.read(user.username, [{ "_id": 0 }])
    following = db.read(username, [{ "_id": 0 }])
    if not following:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User {username} doesn't exist in database."
        )
    if username == user.username:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Cannot follow yourself."
        )
    if username in follower[0]["following"]:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"User already followed."
        )
    update_follower = deepcopy(follower[0])
    update_following = deepcopy(following[0])
    update_follower["following"].append(username)
    update_following["followers"].append(user.username)
    update_follower["following_count"] += 1
    update_following["followers_count"] += 1
    result_follower = db.update(user.username, follower[0], update_follower)
    result_following = db.update(username, following[0], update_following)
    if not result_follower or not result_following:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/unfollow/{username}", status_code = status.HTTP_201_CREATED)
async def unfollow_user(username: str, user: TokenData = Depends(get_current_user)):
    follower = db.read(user.username, [{ "_id": 0 }])
    following = db.read(username, [{ "_id": 0 }])
    if not following:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User {username} doesn't exist in database."
        )
    if username == user.username:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Cannot unfollow yourself."
        )
    if username not in follower[0]["following"]:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"User not followed."
        )
    update_follower = deepcopy(follower[0])
    update_following = deepcopy(following[0])
    update_follower["following"].remove(username)
    update_following["followers"].remove(user.username)
    update_follower["following_count"] -= 1
    update_following["followers_count"] -= 1
    result_follower = db.update(user.username, follower[0], update_follower)
    result_following = db.update(username, following[0], update_following)
    if not result_follower or not result_following:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/private", status_code = status.HTTP_201_CREATED)
async def make_user_private(user: TokenData = Depends(get_current_user)):
    result = db.read(user.username, [{ "_id": 0 }])
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if result[0]["private"]:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"User account already private."
        )
    updated_result = deepcopy(result[0])
    updated_result["private"] = True
    update_result = db.update(user.username, result[0], updated_result)
    if not update_result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/public", status_code = status.HTTP_201_CREATED)
async def make_user_public(user: TokenData = Depends(get_current_user)):
    result = db.read(user.username, [{ "_id": 0 }])
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result[0]["private"]:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = f"User account already public."
        )
    updated_result = deepcopy(result[0])
    updated_result["private"] = False
    update_result = db.update(user.username, result[0], updated_result)
    if not update_result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
