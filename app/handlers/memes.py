from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.mem import MemesCreate, MemesResponse, MemesUpdate
from app.services.mem_service import MemesService

router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)

def get_mem_service(
    db: Session = Depends(get_db),
) -> MemesService:
    return MemesService(db)

@router.post(
    "/",
    response_model=MemesResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_mem(
    schema: MemesCreate,
    service: MemesService = Depends(get_mem_service),
):
    return service.create_memes(schema)

@router.get(
    "/{mem_id}",
    response_model=MemesResponse,
)
def get_mem(
    mem_id: int,
    service: MemesService = Depends(get_mem_service),
):
    return service.get_mem(mem_id)

@router.delete(
    "/{mem_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_mem(
    mem_id: int,
    service: MemesService = Depends(get_mem_service),
) -> None:
    service.delete_mem(mem_id)