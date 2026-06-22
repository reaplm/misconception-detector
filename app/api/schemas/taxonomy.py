from pydantic import BaseModel

# Base fields shared across creation and reading tasks
class MisconceptionBase(BaseModel):
    id: str
    subject: str
    category: str
    description: str
    remediation_hint: str

# Use this when seeding or creating a new taxonomy record via API
class MisconceptionCreate(MisconceptionBase):
    pass

# Use this when sending taxonomy data back out to the frontend
class MisconceptionRead(MisconceptionBase):
    class Config:
        # Crucial for SQLAlchemy: tells Pydantic to read data 
        # straight from database models instead of a standard dictionary
        from_attributes = True 
