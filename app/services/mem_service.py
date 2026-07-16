from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.memes import Meme
from app.repositories.memes_repository import MemesRepository
from app.schemas.mem import MemesCreate, MemesUpdate


class MemesService:

    def __init__(self, db: Session):
        self.repository = MemesRepository(db)

    def create_memes(self, schema: MemesCreate) -> Meme:
        """Создать новый мем"""
        meme = Meme(
            name=schema.name,
            description=schema.description,
            photo=schema.photo,  # ← ИСПРАВЛЕНО
            tag_id=schema.tag_id,  # ← ДОБАВЛЕНО
            author_id=schema.author_id,  # ← ДОБАВЛЕНО (если есть)
        )
        return self.repository.create(meme)

    def get_memes(self) -> list[Meme]:
        """Получить все мемы"""
        return self.repository.get_all()

    def get_memes_with_relations(self) -> list[Meme]:
        """Получить все мемы с тегами и авторами"""
        return self.repository.get_all_with_relations()

    def get_mem(self, meme_id: int) -> Meme:
        """Получить мем по ID"""
        meme = self.repository.get_by_id(meme_id)
        if meme is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meme not found",
            )
        return meme

    def get_mem_with_relations(self, meme_id: int) -> Meme:
        """Получить мем по ID с тегом и автором"""
        meme = self.repository.get_with_tag_and_author(meme_id)
        if meme is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meme not found",
            )
        return meme

    def get_memes_by_tag(self, tag_id: int) -> list[Meme]:
        """Получить мемы по тегу"""
        return self.repository.get_by_tag_id(tag_id)

    # ===== ОБНОВЛЕНИЕ =====
    def update_mem(self, meme_id: int, schema: MemesUpdate) -> Meme:
        """Обновить мем"""
        meme = self.get_mem(meme_id)

        if schema.name is None and schema.description is None and schema.photo is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.name is not None:
            meme.name = schema.name
        if schema.description is not None:
            meme.description = schema.description
        if schema.photo is not None:
            meme.photo = schema.photo

        return self.repository.update(meme)

    def vote_for_meme(self, meme_id: int) -> Meme:
        """Увеличить количество голосов за мем"""
        meme = self.get_mem(meme_id)
        meme.votes += 1
        return self.repository.update(meme)

    # ===== УДАЛЕНИЕ =====
    def delete_mem(self, meme_id: int) -> None:
        """Удалить мем"""
        meme = self.get_mem(meme_id)
        self.repository.delete(meme)