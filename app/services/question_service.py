import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional, Dict, List, Any
import logging

from app.models.taxonomy import MisconceptionTaxonomy
from app.models.question import DiagnosticQuestion
from app.models.category import Category

logger = logging.getLogger(__name__)

class QuestionService:
    async def get_questions_by_ids(
            self, 
            question_ids: List[int], 
            db: AsyncSession
        ) -> List[Dict[str, Any]]:
            """
            Fetch questions by their IDs.
            
            Args:
                question_ids: List of question IDs to retrieve
                db: Async database session
                
            Returns:
                List of question dictionaries with category info
            """
            if not question_ids:
                return []
            
            # Query questions with their category info
            stmt = select(DiagnosticQuestion).where(DiagnosticQuestion.id.in_(question_ids))
            
            result = await db.execute(stmt)
            questions = result.scalars().all()
            
            return [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "best_answer": q.best_answer,
                    "category_id": None 
                }
                for q in questions
            ]
            
            return questions

    async def get_question_by_id(
            self,
            question_id: int,
            db: AsyncSession
        ) -> Dict[str, Any]:
        """
        Fetch a single question by ID.
        """
        stmt = select(DiagnosticQuestion).where(DiagnosticQuestion.id == question_id)
        
        result = await db.execute(stmt)
        row = result.first()
        
        if not row:
            return None
        
        question, category = row
        return {
            "id": question.id,
            "question_text": question.question_text,
            "best_answer": question.best_answer,
            "category_id": None 
        }

