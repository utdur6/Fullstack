from sqlalchemy.orm import Session

from app.models.memes import Memes


class MemesRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, memes: Memes) -> Memes:
        return self._upsert(memes)

    def update(self, memes: Memes) -> Memes:
        return self._upsert(memes)

    def _upsert(self, memes: Memes) -> Memes:
        self.db.add(memes)
        self.db.commit()
        self.db.refresh(memes)
        return memes


    def get_all(self) -> list[Memes]:
        return self.db.query(Memes).all()

    def get_by_id(
        self,
        book_id: int,
        ) -> Memes | None:

        return (
        self.db.query(Memes)
        .filter(Memes.id == book_id)
        .first()
        )

    def delete(self, memes: Memes) -> None:
        self.db.delete(memes)
        self.db.commit()

