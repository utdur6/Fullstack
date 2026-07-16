from sqlalchemy.orm import Session, joinedload
from app.models.profile import Profile
from typing import List, Optional


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, profile: Profile) -> Profile:
        return self._upsert(profile)

    def update(self, profile: Profile) -> Profile:
        return self._upsert(profile)

    def _upsert(self, profile: Profile) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    # ===== БАЗОВЫЕ МЕТОДЫ =====
    def get_all(self) -> List[Profile]:
        return self.db.query(Profile).all()

    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        return self.db.query(Profile).filter(Profile.id == profile_id).first()

    def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()

    def delete(self, profile: Profile) -> None:
        self.db.delete(profile)
        self.db.commit()

    # ===== МЕТОДЫ С ЗАГРУЗКОЙ СВЯЗЕЙ =====
    def get_with_user(self, profile_id: int) -> Optional[Profile]:
        """Получить профиль с пользователем (JOIN)"""
        return (
            self.db.query(Profile)
            .options(joinedload(Profile.user))  # ← joinedload для 1:1
            .filter(Profile.id == profile_id)
            .first()
        )

    def get_by_user_id_with_user(self, user_id: int) -> Optional[Profile]:
        """Получить профиль по user_id с пользователем"""
        return (
            self.db.query(Profile)
            .options(joinedload(Profile.user))
            .filter(Profile.user_id == user_id)
            .first()
        )

    def get_all_with_users(self) -> List[Profile]:
        """Получить все профили с пользователями"""
        return (
            self.db.query(Profile)
            .options(joinedload(Profile.user))
            .all()
        )