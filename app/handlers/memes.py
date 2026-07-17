from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.mem import MemesCreate, MemesResponse, MemesUpdate
from app.services.mem_service import MemesService
from app.models.memes import Meme

router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)


def get_mem_service(
    db: Session = Depends(get_db),
) -> MemesService:
    return MemesService(db)


@router.get("/", response_model=list[MemesResponse])
def get_memes(
    db: Session = Depends(get_db),
):
    """Получить все мемы"""
    memes = db.query(Meme).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "image_url": m.photo,
            "votes": m.votes,
            "tag_id": m.tag_id
        }
        for m in memes
    ]


@router.post(
    "/",
    response_model=MemesResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_meme(
    meme_data: MemesCreate,  # ← ИСПРАВЛЕНО: meme_data вместо schema
    service: MemesService = Depends(get_mem_service),
):
    """Создать новый мем"""
    return service.create_memes(meme_data)



@router.get(
    "/{mem_id}",
    response_model=MemesResponse,
)
def get_mem(
    mem_id: int,
    service: MemesService = Depends(get_mem_service),
):
    """Получить мем по ID"""
    return service.get_mem(mem_id)



@router.patch(
    "/{mem_id}",
    response_model=MemesResponse,
)
def update_mem(
    mem_id: int,
    meme_data: MemesUpdate,
    service: MemesService = Depends(get_mem_service),
):
    """Обновить мем"""
    return service.update_mem(mem_id, meme_data)


@router.delete(
    "/{mem_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_mem(
    mem_id: int,
    service: MemesService = Depends(get_mem_service),
) -> None:
    """Удалить мем"""
    service.delete_mem(mem_id)


@router.post(
    "/{mem_id}/vote",
    response_model=MemesResponse,
)
def vote_for_meme(
    mem_id: int,
    service: MemesService = Depends(get_mem_service),
):
    """Проголосовать за мем"""
    return service.vote_for_meme(mem_id)