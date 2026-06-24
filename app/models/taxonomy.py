from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from typing import List
from app.database import Base

class MisconceptionTaxonomy(Base):
    __tablename__ = "misconception_taxonomy"
    __table_args__ = {"schema": "misconception"}
    
    # Mapped[str] defines the type hint, mapped_column handles database rules
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    category: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 2.0 typing for relationships: points back to a list of responses
    questions: Mapped[List["DiagnosticQuestion"]] = relationship(back_populates="misconception")


