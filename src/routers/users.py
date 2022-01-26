from fastapi import (
    APIRouter,
    HTTPException,
    status
)
from ..database import Database
from ..schemas import (
    User,
    UserResponse
)
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
    if result == [] or result == False:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User {username} doesn't exist in database."
        )
    return result[0]
