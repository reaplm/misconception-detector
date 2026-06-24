from pydantic import BaseModel

class MisconceptionResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str

    class Config:
        from_attributes = True

