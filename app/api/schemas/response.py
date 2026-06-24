from pydantic import BaseModel
from typing import Optional
from app.api.schemas.taxonomy import MisconceptionResponse

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    correct_answer: str
    incorrect_answer_distractor: str
    misconception: Optional[MisconceptionResponse] = None

    class Config:
        from_attributes = True
