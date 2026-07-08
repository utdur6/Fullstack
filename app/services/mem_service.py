from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.memes import Memes
from app.repositories.memes_repository import MemesRepository
from app.schemas.mem import MemesCreate, MemesUpdate


class MemesService:

    def __init__(self, db: Session):
        self.repository = MemesRepository(db)

    def create_memes(self, schema: MemesCreate) -> Memes:
        mem = Memes(
            name=schema.name,
            description=schema.description,
        )

        return self.repository.create(mem)

    def get_memes(self) -> list[Memes]:
        return self.repository.get_all()

    def get_mem(self, memes_id: int) -> Memes:
        mem = self.repository.get_by_id(memes_id)

        if mem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mem not found",
            )

        return mem

    def update_mem(
            self,
            book_id: int,
            schema: MemesUpdate,
    ) -> Memes:

        mem = self.get_mem(book_id)

        if schema.name is None and schema.description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.name is not None:
            mem.name = schema.name

        if schema.description is not None:
            mem.description = schema.description

        return self.repository.update(mem)

    def delete_mem(self, mem_id: int) -> None:
        mem = self.get_mem(mem_id)

        self.repository.delete(mem)