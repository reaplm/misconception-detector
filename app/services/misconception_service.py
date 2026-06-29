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

class MisconceptionDetectionService:
    def __init__(self):
        # Load the embedding model once at startup
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = 0.65  # Confidence threshold
        
    async def detect_misconception(
        self, 
        question_id: int,
        student_answer: str, 
        db: AsyncSession,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a student answer and detect if it matches a known misconception.
        
        Args:
            student_answer: The student's response text
            db: Async database session
            category_filter: Optional category to limit search (e.g., 'Science', 'Health')
            
        Returns:
            Dictionary with detection results
        """
         # 1. First, verify the question exists and get its details
        question_stmt = select(DiagnosticQuestion).where(DiagnosticQuestion.id == question_id)
        question_result = await db.execute(question_stmt)
        question = question_result.scalar_one_or_none()

        if not question:
            return {
                "detected": False,
                "message": f"Question with ID {question_id} not found",
                "highest_score": 0.0,
                "threshold": self.threshold,
                "question_id": question_id,
                "student_answer": student_answer
            }

        # 2. Generate embedding for the student's answer
        student_embedding = self.model.encode(
            student_answer, 
            convert_to_tensor=False
        )
        
        # 3. Query the database for misconceptions using async SQLAlchemy 2.0 style
        stmt = select(MisconceptionTaxonomy).where(
            MisconceptionTaxonomy.question_id == question_id
        )
        
        # Optionally filter by category
        if category_filter:
            stmt = stmt.join(DiagnosticQuestion).join(Category).where(Category.name == category_filter)
        
        # Execute the query
        result = await db.execute(stmt)
        misconceptions = result.scalars().all()
        
        # 4. Handle case where no misconceptions exist for this question
        if not misconceptions:
            return {
                "detected": False,
                "message": f"No misconceptions found in database for question ID {question_id}",
                "highest_score": 0.0,
                "threshold": self.threshold,
                "question_id": question_id,
                "question_text": question.question_text,
                "student_answer": student_answer
            }
        
        # 5. Extract embeddings and texts
        db_embeddings = np.array([m.embedding for m in misconceptions])
        db_texts = [m.misconception_text for m in misconceptions]
        db_question_ids = [m.question_id for m in misconceptions]
        
        # 6. Calculate cosine similarity
        # Reshape student embedding for matrix multiplication
        student_vector = student_embedding.reshape(1, -1)
        similarity_scores = cosine_similarity(student_vector, db_embeddings)[0]
        
        # 7. Find best match
        best_match_idx = np.argmax(similarity_scores)
        highest_score = similarity_scores[best_match_idx]
        
        # 8. Get the best match details
        best_misconception = misconceptions[best_match_idx]
        
        # Fetch the associated question
        question_stmt = select(DiagnosticQuestion).where(DiagnosticQuestion.id == best_misconception.question_id)
        question_result = await db.execute(question_stmt)
        best_question = question_result.scalar_one_or_none()
        
        # 9. Prepare result
        result = {
            "detected": highest_score >= self.threshold,
            "highest_score": float(highest_score),
            "threshold": self.threshold,
            "question_id": question_id,
            "question_text": question.question_text,
            "best_answer": question.best_answer,
            "student_answer": student_answer
        }
        
        if highest_score >= self.threshold:
            result.update({
                "misconception": {
                    "id": best_misconception.id,
                    "text": best_misconception.misconception_text,
                    "question_id": best_misconception.question_id
                }
            })
        else:
            result["message"] = "No systematic misconception detected"
            
        return result
    
    async def batch_detect_misconceptions(
        self,
        question_id: int,
        student_answers: List[str],
        db: AsyncSession,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple student answers in batch.
        """
        results = []
        for answer in student_answers:
            result = await self.detect_misconception(
                question_id=question_id,
                student_answer=answer,
                db=db,
                category_filter=category_filter
            )
            results.append(result)

        return results

    async def get_question_misconceptions(
        self,
        question_id: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Get all misconceptions for a specific question (helper method).
        """
        stmt = select(MisconceptionTaxonomy).where(
            MisconceptionTaxonomy.question_id == question_id
        )
        result = await db.execute(stmt)
        misconceptions = result.scalars().all()
        
        return [
            {
                "id": m.id,
                "text": m.misconception_text,
                "question_id": m.question_id
            }
            for m in misconceptions
        ]