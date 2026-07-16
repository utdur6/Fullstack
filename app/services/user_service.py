from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.users import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, schema: UserCreate) -> User:
        existing_user = self.repository.get_by_email(schema.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        user = User(
            email=schema.email,
            hashed_password=hash_password(schema.password),
            is_active=True,
            role=UserRole.USER.value,
        )
        return self.repository.create(user)


    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def get_user_with_profile(self, user_id: int) -> User:
        """Получить пользователя с профилем"""
        user = self.repository.get_with_profile(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def get_user_with_favorites(self, user_id: int) -> User:
        """Получить пользователя с избранными мемами"""
        user = self.repository.get_with_favorite_memes(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def get_user_with_all_relations(self, user_id: int) -> User:
        """Получить пользователя со всеми связями"""
        user = self.repository.get_with_all_relations(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def update_user(self, user_id: int, email: str = None, is_active: bool = None) -> User:
        """Обновить данные пользователя"""
        user = self.get_user(user_id)

        if email is not None:
            existing_user = self.repository.get_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )
            user.email = email

        if is_active is not None:
            user.is_active = is_active

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя"""
        user = self.get_user(user_id)
        self.repository.delete(user)