from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.api.schemas.taxonomy import MisconceptionRead

# The exact JSON structure the student's browser frontend must POST to your API
class ExamResponseCreate(BaseModel):
    student_id: str
    question_text: str
    student_answer: str

# The JSON structure your API returns after running your analysis engine
class ExamResponseRead(BaseModel):
    id: int
    student_id: str
    question_text: str
    student_answer: str
    created_at: datetime
    detected_misconception_id: Optional[str] = None
    
    # Nested DTO: automatically includes the full hint text if an issue is found!
    misconception: Optional[MisconceptionRead] = None

    class Config:
        from_attributes = True
