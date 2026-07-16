from sqlalchemy.orm import Session, selectinload
from app.models.tags import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tag: Tag) -> Tag:
        return self._upsert(tag)

    def update(self, tag: Tag) -> Tag:
        return self._upsert(tag)

    def _upsert(self, tag: Tag) -> Tag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_all(self) -> list[Tag]:
        return self.db.query(Tag).all()

    def get_by_id(self, tag_id: int) -> Tag | None:
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_name(self, name: str) -> Tag | None:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def delete(self, tag: Tag) -> None:
        self.db.delete(tag)
        self.db.commit()

    def get_with_memes(self, tag_id: int) -> Tag | None:
        """Получить тег со списком мемов (selectinload для 1:N)"""
        return (
            self.db.query(Tag)
            .options(selectinload(Tag.memes))  # ← selectinload для коллекции
            .filter(Tag.id == tag_id)
            .first()
        )

    def get_by_name_with_memes(self, name: str) -> Tag | None:
        """Получить тег по имени со списком мемов"""
        return (
            self.db.query(Tag)
            .options(selectinload(Tag.memes))
            .filter(Tag.name == name)
            .first()
        )

    def get_all_with_memes(self) -> list[Tag]:
        """Получить все теги с мемами"""
        return (
            self.db.query(Tag)
            .options(selectinload(Tag.memes))
            .all()
        )