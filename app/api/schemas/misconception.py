from pydantic import BaseModel
from typing import Optional, List

class MisconceptionMatch(BaseModel):
    id: int
    text: str
    question_id: int
    question_text: Optional[str] = None
    best_answer: Optional[str] = None

class MisconceptionDetectionRequest(BaseModel):
    question_id: int
    student_answer: str
    category_filter: Optional[str] = None  # Optional: 'Science', 'Health', etc.

class MisconceptionDetectionResponse(BaseModel):
    detected: bool
    highest_score: float
    threshold: float
    student_answer: str
    misconception: Optional[MisconceptionMatch] = None
    message: Optional[str] = None

class BatchDetectionRequest(BaseModel):
    question_id: int
    student_answers: List[str]
    category_filter: Optional[str] = None