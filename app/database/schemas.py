from pydantic import BaseModel
from datetime import datetime


class Question(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
    collected: datetime
