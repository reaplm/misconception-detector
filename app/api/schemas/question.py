from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.api.schemas.taxonomy import MisconceptionResponse

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    best_answer: str
    category_id: Optional[int] 

    misconceptions: List[MisconceptionResponse] = []

    class Config:
        from_attributes = True
