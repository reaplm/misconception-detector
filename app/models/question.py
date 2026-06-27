from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
from app.database import Base

class DiagnosticQuestion(Base):
    __tablename__ = "questions"
    __table_args__ = {"schema": "misconception"}
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False) # Dropped index here to avoid PG string limits
    best_answer: Mapped[str] = mapped_column(Text, nullable=False)

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("misconception.categories.id", ondelete="SET NULL"), 
        nullable=True
    )

    #category = relationship("Category", back_populates="questions")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="questions")

    # FIXED: A Question can have multiple misconceptions based on your DDL schema.
    # If a question only has ONE misconception, change List["MisconceptionTaxonomy"] to "MisconceptionTaxonomy"
    misconceptions: Mapped[List["MisconceptionTaxonomy"]] = relationship(
        "MisconceptionTaxonomy",
        back_populates="question",
        cascade="all, delete-orphan"
    )