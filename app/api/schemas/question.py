from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.api.schemas.taxonomy import MisconceptionResponse

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    best_answer: str
    category_id: Optional[int] 

    #misconceptions: List[MisconceptionResponse] = []

class QuestionListRequest(BaseModel):
    question_ids: List[int]  # List of question IDs to fetch

class QuestionListResponse(BaseModel):
    total: int
    questions: List[QuestionResponse]


    class Config:
        from_attributes = True
