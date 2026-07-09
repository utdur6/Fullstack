from sqlalchemy.orm import Session
from app.models.tags import Tag
from typing import List, Optional

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

    def get_all(self) -> List[Tag]:
        return self.db.query(Tag).all()

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def delete(self, tag: Tag) -> None:
        self.db.delete(tag)
        self.db.commit()