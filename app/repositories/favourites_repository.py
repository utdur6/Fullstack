from sqlalchemy.orm import Session

from app.models.favourites import Favourite


class FavouriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, favourite: Favourite) -> Favourite:
        return self._upsert(favourite)

    def update(self, favourite: Favourite) -> Favourite:
        return self._upsert(favourite)

    def _upsert(self, favourite: Favourite) -> Favourite:
        self.db.add(favourite)
        self.db.commit()
        self.db.refresh(favourite)
        return favourite

    def get_all(self) -> list[Favourite]:
        return self.db.query(Favourite).all()

    def get_by_id(self, favourite_id: int) -> Favourite | None:
        return self.db.query(Favourite).filter(Favourite.id == favourite_id).first()

    def get_by_user_id(self, user_id: int) -> list[Favourite]:
        return self.db.query(Favourite).filter(Favourite.user_id == user_id).all()

    def get_by_meme_id(self, meme_id: int) -> list[Favourite]:
        return self.db.query(Favourite).filter(Favourite.meme_id == meme_id).all()

    def delete(self, favourite: Favourite) -> None:
        self.db.delete(favourite)
        self.db.commit()