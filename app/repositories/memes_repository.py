from sqlalchemy.orm import Session

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

    def get_all(self) -> list[Meme]:
        return self.db.query(Meme).all()

    def get_by_id(self, meme_id: int) -> Meme | None:
        return self.db.query(Meme).filter(Meme.id == meme_id).first()

    def get_by_tag_id(self, tag_id: int) -> list[Meme]:
        return self.db.query(Meme).filter(Meme.tag_id == tag_id).all()

    def delete(self, meme: Meme) -> None:
        self.db.delete(meme)
        self.db.commit()