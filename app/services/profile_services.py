from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.profile_repository = ProfileRepository(db)

    def create_profile(self, user_id: int, name: str = None) -> Profile:
        """Создать профиль для пользователя"""

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        existing_profile = self.profile_repository.get_by_user_id(user_id)
        if existing_profile:
            raise ValueError(f"Profile already exists for user {user_id}")

        if name is None:
            name = user.email.split('@')[0]

        profile = Profile(
            user_id=user_id,
            name=name,
        )

        return self.profile_repository.create(profile)

    def get_profile(self, user_id: int) -> Profile | None:
        """Получить профиль по ID пользователя"""
        return self.profile_repository.get_by_user_id(user_id)

    def get_profile_with_user(self, user_id: int) -> Profile | None:
        """Получить профиль по ID пользователя с загрузкой пользователя"""
        return self.profile_repository.get_by_user_id_with_user(user_id)

    def update_profile(self, user_id: int, **kwargs) -> Profile | None:
        """Обновить профиль пользователя"""
        profile = self.profile_repository.get_by_user_id(user_id)
        if not profile:
            return None

        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)

        return self.profile_repository.update(profile)

    def delete_profile(self, user_id: int) -> bool:
        """Удалить профиль пользователя"""
        profile = self.profile_repository.get_by_user_id(user_id)
        if not profile:
            return False

        self.profile_repository.delete(profile)
        return True