from copy import deepcopy
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from ..database import Database
from ..oauth2 import get_current_user
from ..schemas import (
    Vote,
    TokenData
)

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)
db = Database()

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: Vote, user: TokenData = Depends(get_current_user)):
    if vote.id <= 0:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)
    result = db.read(vote.username, queries = [{ "_id": vote.id }])
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {vote.id} does not exist."
        )
    data = deepcopy(result[0])
    if vote.dir == 1:
        if user.username in result[0]["voters"]:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"{user.username} has already voted on the post."
            )
        data["voters"].append(user.username)
    else:
        try:
            data["voters"].remove(user.username)
        except:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"{user.username} has not voted on the post."
            )
    data["votes"] = len(data["voters"])
    update_result = db.update(vote.username, result[0], data)
    if not result:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
