from pydantic import BaseModel

class MisconceptionResponse(BaseModel):
    id: int
    misconception_text: str
    question_id: int


    class Config:
        from_attributes = True

