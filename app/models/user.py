import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL native UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # 1. Primary key is now a UUID. 
    # default=uuid.uuid4 tells SQLAlchemy to create a new unique ID for every new user.
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        nullable=False
    )

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)