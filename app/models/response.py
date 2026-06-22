from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.database import Base

class ExamResponse(Base):
    __tablename__ = "exam_responses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    student_answer: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Uses server-side datetime defaults natively
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Optional[str] tells Python this column can accept NULL values safely
    detected_misconception_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("misconception_taxonomy.id"), 
        nullable=True
    )
    
    # Optional relationship means it can load a single taxonomy object or None
    misconception: Mapped[Optional["MisconceptionTaxonomy"]] = relationship(back_populates="responses")