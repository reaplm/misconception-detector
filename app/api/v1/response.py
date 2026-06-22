from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import ExamResponse
from app.api.schemas import ExamResponseCreate, ExamResponseRead

router = APIRouter(prefix="/responses", tags=["Exam Evaluations"])

@router.post("/analyze", response_model=ExamResponseRead, status_code=status.HTTP_201_CREATED)
async def analyze_student_response(
    payload: ExamResponseCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Process incoming test responses, compute diagnostics, and log results.
    """
    # --- SIMULATED AI CORE LAYER ---
    # Placeholder: If fractional error pattern is typed, map to taxonomy link
    detected_id = None
    if "2/5" in payload.student_answer:
        detected_id = "MATH_FRAC_02"
    # -------------------------------

    db_response = ExamResponse(
        student_id=payload.student_id,
        question_text=payload.question_text,
        student_answer=payload.student_answer,
        detected_misconception_id=detected_id
    )
    
    db.add(db_response)
    await db.commit()
    
    # Eagerly load the transaction joined with its taxonomy lookup to satisfy the output schema
    query = (
        select(ExamResponse)
        .where(ExamResponse.id == db_response.id)
        .outerjoin(ExamResponse.misconception)
    )
    result = await db.execute(query)
    record = result.scalar_one()
    
    return record
