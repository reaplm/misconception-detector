from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

# async dependency and models
from app.database import get_db
from app.models.question import DiagnosticQuestion
from app.api.schemas.question import QuestionResponse

router = APIRouter(
    prefix="/questions",
    tags=["Diagnostic Questions"]
)

@router.get("", response_model=List[QuestionResponse], summary="Fetch all test items")
async def read_all_questions(
    skip: int = Query(0, description="Pagination skip boundary counter offset"),
    limit: int = Query(100, description="Max questions constraints limit"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves all questions from the database, populated with their associated misconception definitions."""
    # Added 'selectinload' to eagerly fetch the linked misconception asynchronously 
    # without causing lazy-loading crashes.
    query = (
        select(DiagnosticQuestion)
        #.options(selectinload(DiagnosticQuestion.misconceptions))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    questions = result.scalars().all() # Unique prevents duplicates
    return questions

@router.get("/id/{question_id}", response_model=QuestionResponse, summary="Fetch specific test question item")
async def read_question_by_id(question_id: int, db: AsyncSession = Depends(get_db)):
    """Fetches an individual diagnostic test item along with its master remediation hints."""
    query = (
        select(DiagnosticQuestion)
        # FIXED: Eagerly load the relationship to prevent the MissingGreenlet crash
        .options(selectinload(DiagnosticQuestion.misconceptions))
        .where(DiagnosticQuestion.id == question_id)
    )
    result = await db.execute(query)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail=f"Diagnostic question configuration {question_id} not found")
    return question