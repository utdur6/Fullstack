from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.users import User


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, user_id: int, username: str = None) -> Profile:
        """Создать профиль для пользователя"""
        # Проверяем, существует ли пользователь
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        # Проверяем, есть ли уже профиль
        if user.profile:
            raise ValueError(f"Profile already exists for user {user_id}")

        # Если username не передан, генерируем из email
        if username is None:
            username = user.email.split('@')[0]

        # Создаём профиль
        profile = Profile(
            user_id=user_id,
            username=username,
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile(self, user_id: int) -> Profile | None:
        """Получить профиль по ID пользователя"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return user.profile

    def update_profile(self, user_id: int, **kwargs) -> Profile | None:
        """Обновить профиль пользователя"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return None

        profile = user.profile
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)

        self.db.commit()
        self.db.refresh(profile)
        return profile