from sqlalchemy.orm import Session
from app.models.memes import Memes
from typing import List, Optional

class MemesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, meme: Memes) -> Memes:
        return self._upsert(meme)

    def update(self, meme: Memes) -> Memes:
        return self._upsert(meme)

    def _upsert(self, meme: Memes) -> Memes:
        self.db.add(meme)
        self.db.commit()
        self.db.refresh(meme)
        return meme

    def get_all(self) -> List[Memes]:
        return self.db.query(Memes).all()

    def get_by_id(self, meme_id: int) -> Optional[Memes]:
        return self.db.query(Memes).filter(Memes.id == meme_id).first()

    def get_by_tag_id(self, tag_id: int) -> List[Memes]:
        return self.db.query(Memes).filter(Memes.tag_id == tag_id).all()

    def delete(self, meme: Memes) -> None:
        self.db.delete(meme)
        self.db.commit()