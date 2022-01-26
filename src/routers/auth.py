from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import Database
from ..oauth2 import create_access_token
from ..schemas import Token
from ..utils import (
    hash_password,
    verify_password
)

router = APIRouter(tags = ["Authentication"])
db = Database()

@router.post("/login", response_model = Token)
async def login_user(user: OAuth2PasswordRequestForm = Depends()):
    result = db.read(user.username, [{ "_id": 0 }])
    if not result:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Invalid credentials."
        )
    if not verify_password(user.password, result[0]["password"]):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Invalid credentials."
        )
    access_token = create_access_token({"username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
