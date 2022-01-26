from datetime import (
    datetime,
    timedelta
)
from typing import (
    Dict,
    Any
)
from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    jwt,
    JWTError
)
from .schemas import TokenData

SECRET_KEY = "ce85781e6e8a4165d22841578d66ec3283d0e899b87d43b0ec63939f607d2137"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data: Dict[Any, Any]):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )
    return encoded_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        username: str = payload.get("username")
        if not username:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials.",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)
