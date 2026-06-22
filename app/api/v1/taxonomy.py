from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import MisconceptionTaxonomy
from app.api.schemas import MisconceptionCreate, MisconceptionRead

# APIRouter acts like Java's @RequestMapping("/taxonomy")
router = APIRouter(prefix="/taxonomy", tags=["Taxonomy Encyclopedia"])

@router.post("/", response_model=MisconceptionRead, status_code=status.HTTP_201_CREATED)
async def create_taxonomy_record(
    payload: MisconceptionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Seed a new structural conceptual error into the encyclopedia.
    """
    existing = await db.get(MisconceptionTaxonomy, payload.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Taxonomy ID already registered."
        )
        
    new_error = MisconceptionTaxonomy(**payload.model_dump())
    db.add(new_error)
    await db.commit()
    await db.refresh(new_error)
    return new_error
