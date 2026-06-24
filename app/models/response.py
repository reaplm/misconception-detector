from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.database import Base

class DiagnosticQuestion(Base):
    __tablename__ = "diagnostic_questions"
    __table_args__ = {"schema": "misconception"}
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    question_text: Mapped[str] = mapped_column(nullable=False, index=True)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    incorrect_answer_distractor: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Uses server-side datetime defaults natively
    # created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Optional[str] tells Python this column can accept NULL values safely
    misconception_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("misconception.misconception_taxonomy.id"), 
        nullable=True
    )
    
    # Optional relationship means it can load a single taxonomy object or None
    misconception: Mapped[Optional["MisconceptionTaxonomy"]] = relationship(back_populates="questions")