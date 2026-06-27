from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

# Import your modern async dependency and models
from app.database import get_db
from app.models.taxonomy import MisconceptionTaxonomy
from app.api.schemas.taxonomy import MisconceptionResponse

router = APIRouter(
    prefix="/misconceptions",
    tags=["Misconception Taxonomy"]
)

# 'async def' to support your async session handler
@router.get("", response_model=List[MisconceptionResponse], summary="Fetch all misconceptions")
async def read_all_misconceptions(db: AsyncSession = Depends(get_db)):
    """Retrieves the complete master dictionary mapping student logic flaws."""
    # Modern SQLAlchemy 2.0 Async Query Syntax
    query = select(MisconceptionTaxonomy)
    result = await db.execute(query)
    taxonomy_list = result.scalars().all()
    return taxonomy_list

@router.get("/id/{misconception_id}", response_model=MisconceptionResponse, summary="Fetch single misconception by ID")
async def read_misconception_by_id(misconception_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a single abstract misconception record from the taxonomy database table."""
    query = select(MisconceptionTaxonomy).filter(MisconceptionTaxonomy.id == misconception_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail=f"Misconception point {misconception_id} not found")
    return item
