from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from pgvector.sqlalchemy import Vector
from app.database import Base

class MisconceptionTaxonomy(Base):
    __tablename__ = "misconception_taxonomy"
    __table_args__ = {"schema": "misconception"}
    
   
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    misconception_text: Mapped[str] = mapped_column(nullable=False)

    # Matches all-MiniLM-L6-v2 dimensions. 
    # pgvector maps Python lists of floats straight into the DB vector array.
    embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=False)

    # FIXED: Added the missing foreign key column from your raw DDL schema
    question_id: Mapped[int] = mapped_column(
        ForeignKey("misconception.questions.id", ondelete="CASCADE"),
        nullable=False
    )
    # Clean 1-to-Many back-populate linking down to DiagnosticQuestions
    question: Mapped["DiagnosticQuestion"] = relationship(
        "DiagnosticQuestion",
        back_populates="misconceptions"
    )

    

