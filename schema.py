from datetime import datetime
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    timestamp: datetime = datetime.now()
