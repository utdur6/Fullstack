from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.user_meme import UserMeme  # или Favourite


class FavouriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, favourite: UserMeme) -> UserMeme:
        return self._upsert(favourite)

    def update(self, favourite: UserMeme) -> UserMeme:
        return self._upsert(favourite)

    def _upsert(self, favourite: UserMeme) -> UserMeme:
        self.db.add(favourite)
        self.db.commit()
        self.db.refresh(favourite)
        return favourite

    def get_all(self) -> list[UserMeme]:
        return self.db.query(UserMeme).all()

    def get_by_id(self, favourite_id: int) -> UserMeme | None:
        return self.db.query(UserMeme).filter(UserMeme.id == favourite_id).first()

    def get_by_user_id(self, user_id: int) -> list[UserMeme]:
        return self.db.query(UserMeme).filter(UserMeme.user_id == user_id).all()

    def get_by_meme_id(self, meme_id: int) -> list[UserMeme]:
        return self.db.query(UserMeme).filter(UserMeme.meme_id == meme_id).all()

    # ===== НОВЫЕ МЕТОДЫ =====
    def get_with_user_and_meme(self, favourite_id: int) -> UserMeme | None:
        """Получить запись избранного с пользователем и мемом"""
        return (
            self.db.query(UserMeme)
            .options(
                joinedload(UserMeme.user),  # загружаем пользователя
                joinedload(UserMeme.meme),  # загружаем мем
            )
            .filter(UserMeme.id == favourite_id)
            .first()
        )

    def get_all_with_users_and_memes(self) -> list[UserMeme]:
        """Получить все записи избранного с пользователями и мемами"""
        return (
            self.db.query(UserMeme)
            .options(
                joinedload(UserMeme.user),
                joinedload(UserMeme.meme),
            )
            .all()
        )

    def get_user_favorites_with_memes(self, user_id: int) -> list[UserMeme]:
        """Получить избранные мемы пользователя с деталями мемов"""
        return (
            self.db.query(UserMeme)
            .options(joinedload(UserMeme.meme))  # загружаем мемы
            .filter(UserMeme.user_id == user_id)
            .all()
        )

    def delete(self, favourite: UserMeme) -> None:
        self.db.delete(favourite)
        self.db.commit()

    def delete_by_user_and_meme(self, user_id: int, meme_id: int) -> bool:
        """Удалить запись из избранного по user_id и meme_id"""
        favourite = (
            self.db.query(UserMeme)
            .filter(
                UserMeme.user_id == user_id,
                UserMeme.meme_id == meme_id
            )
            .first()
        )
        if favourite:
            self.db.delete(favourite)
            self.db.commit()
            return True
        return False