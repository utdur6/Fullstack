from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.memes import Meme


class MemesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, meme: Meme) -> Meme:
        return self._upsert(meme)

    def update(self, meme: Meme) -> Meme:
        return self._upsert(meme)

    def _upsert(self, meme: Meme) -> Meme:
        self.db.add(meme)
        self.db.commit()
        self.db.refresh(meme)
        return meme

    # ===== БАЗОВЫЕ МЕТОДЫ =====
    def get_all(self) -> list[Meme]:
        return self.db.query(Meme).all()

    def get_by_id(self, meme_id: int) -> Meme | None:
        return self.db.query(Meme).filter(Meme.id == meme_id).first()

    def get_by_tag_id(self, tag_id: int) -> list[Meme]:
        return self.db.query(Meme).filter(Meme.tag_id == tag_id).all()

    def delete(self, meme: Meme) -> None:
        self.db.delete(meme)
        self.db.commit()

    # ===== МЕТОДЫ С ЗАГРУЗКОЙ СВЯЗЕЙ =====
    def get_with_tag(self, meme_id: int) -> Meme | None:
        """Получить мем с тегом (JOIN для 1:1)"""
        return (
            self.db.query(Meme)
            .options(joinedload(Meme.tag))  # ← joinedload для 1:1
            .filter(Meme.id == meme_id)
            .first()
        )

    def get_with_author(self, meme_id: int) -> Meme | None:
        """Получить мем с автором (JOIN для 1:1)"""
        return (
            self.db.query(Meme)
            .options(joinedload(Meme.author))  # ← joinedload для 1:1
            .filter(Meme.id == meme_id)
            .first()
        )

    def get_with_tag_and_author(self, meme_id: int) -> Meme | None:
        """Получить мем с тегом и автором"""
        return (
            self.db.query(Meme)
            .options(
                joinedload(Meme.tag),
                joinedload(Meme.author),
            )
            .filter(Meme.id == meme_id)
            .first()
        )

    def get_with_favorited_by(self, meme_id: int) -> Meme | None:
        """Получить мем с пользователями, добавившими в избранное"""
        return (
            self.db.query(Meme)
            .options(selectinload(Meme.favorited_by))  # ← selectinload для N:N
            .filter(Meme.id == meme_id)
            .first()
        )

    def get_with_all_relations(self, meme_id: int) -> Meme | None:
        """Получить мем со всеми связями"""
        return (
            self.db.query(Meme)
            .options(
                joinedload(Meme.tag),
                joinedload(Meme.author),
                selectinload(Meme.favorited_by),
            )
            .filter(Meme.id == meme_id)
            .first()
        )

    def get_all_with_relations(self) -> list[Meme]:
        """Получить все мемы со связями"""
        return (
            self.db.query(Meme)
            .options(
                joinedload(Meme.tag),
                joinedload(Meme.author),
                selectinload(Meme.favorited_by),
            )
            .all()
        )

    def get_by_tag_with_relations(self, tag_id: int) -> list[Meme]:
        """Получить мемы по тегу со всеми связями"""
        return (
            self.db.query(Meme)
            .filter(Meme.tag_id == tag_id)
            .options(
                joinedload(Meme.tag),
                joinedload(Meme.author),
                selectinload(Meme.favorited_by),
            )
            .all()
        )

    def get_most_voted(self, limit: int = 10) -> list[Meme]:
        """Получить топ мемов по голосам"""
        return (
            self.db.query(Meme)
            .order_by(Meme.votes.desc())
            .limit(limit)
            .options(
                joinedload(Meme.tag),
                joinedload(Meme.author),
            )
            .all()
        )