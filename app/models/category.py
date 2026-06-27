from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "misconception"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    # Relationship to cleanly query questions belonging to this category
    #questions = relationship("Question", back_populates="category", cascade="all, delete-orphan")

    # FIXED: Plural match to DiagnosticQuestion, back_populates matches the property name
    questions: Mapped[List["DiagnosticQuestion"]] = relationship(
        "DiagnosticQuestion", 
        back_populates="category", 
        cascade="all, delete-orphan"
    )