from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.api.schemas.misconception import (
    MisconceptionDetectionRequest,
    MisconceptionDetectionResponse,
    BatchDetectionRequest
)
from app.services.misconception_service import MisconceptionDetectionService

router = APIRouter(
    prefix="/misconception",
    tags=["Misconception Detection"]
)

# Initialize service (can be made singleton)
service = MisconceptionDetectionService()

@router.post("/detect", response_model=MisconceptionDetectionResponse)
async def detect_misconception(
    request: MisconceptionDetectionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Detect if a student's answer matches a known misconception.
    """
    if not request.student_answer or len(request.student_answer.strip()) == 0:
        raise HTTPException(status_code=400, detail="Student answer cannot be empty")
    
    if request.question_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid question_id")
    
    result = await service.detect_misconception(
        question_id=request.question_id,
        student_answer=request.student_answer,
        db=db,
        category_filter=request.category_filter
    )
    
    return result

@router.post("/batch-detect", response_model=List[MisconceptionDetectionResponse])
async def batch_detect_misconceptions(
    request: BatchDetectionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Detect misconceptions for multiple student answers.
    """
    if not request.student_answers:
        raise HTTPException(status_code=400, detail="Student answers list cannot be empty")
    
    if request.question_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid question_id")
    
    results = await service.batch_detect_misconceptions(
        question_id=request.question_id,
        student_answers=request.student_answers,
        db=db,
        category_filter=request.category_filter
    )
    
    return results

@router.get("/question/{question_id}/misconceptions")
async def get_question_misconceptions(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all known misconceptions for a specific question.
    Useful for previewing what misconceptions exist for a question.
    """
    if question_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid question_id")
    
    misconceptions = await service.get_question_misconceptions(
        question_id=question_id,
        db=db
    )
    
    return {
        "question_id": question_id,
        "total": len(misconceptions),
        "misconceptions": misconceptions
    }

@router.get("/health")
async def health_check():
    """
    Check if the misconception detection service is healthy.
    """
    return {
        "status": "healthy",
        "model": "all-MiniLM-L6-v2",
        "threshold": service.threshold
    }