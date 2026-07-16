from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.users import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        return self._save(user)

    def _save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def update(self, user: User) -> User:
        return self._save(user)

    def get_with_profile(self, user_id: int) -> User | None:
        """Получить пользователя с профилем (JOIN для 1:1)"""
        return (
            self.db.query(User)
            .options(joinedload(User.profile))  # ← joinedload для 1:1
            .filter(User.id == user_id)
            .first()
        )

    def get_with_favorite_memes(self, user_id: int) -> User | None:
        """Получить пользователя с избранными мемами (selectinload для N:N)"""
        return (
            self.db.query(User)
            .options(selectinload(User.favorite_memes))  # ← selectinload для N:N
            .filter(User.id == user_id)
            .first()
        )

    def get_with_created_memes(self, user_id: int) -> User | None:
        """Получить пользователя с созданными мемами (selectinload для 1:N)"""
        return (
            self.db.query(User)
            .options(selectinload(User.created_memes))  # ← selectinload для коллекции
            .filter(User.id == user_id)
            .first()
        )

    def get_with_all_relations(self, user_id: int) -> User | None:
        """Получить пользователя со всеми связями"""
        return (
            self.db.query(User)
            .options(
                joinedload(User.profile),              # 1:1
                selectinload(User.favorite_memes),     # N:N
                selectinload(User.created_memes),      # 1:N
            )
            .filter(User.id == user_id)
            .first()
        )

    def get_all_with_profiles(self) -> list[User]:
        """Получить всех пользователей с профилями"""
        return (
            self.db.query(User)
            .options(joinedload(User.profile))
            .all()
        )

    def get_by_email_with_profile(self, email: str) -> User | None:
        """Получить пользователя по email с профилем"""
        return (
            self.db.query(User)
            .options(joinedload(User.profile))
            .filter(User.email == email)
            .first()
        )

    def get_by_email_with_all_relations(self, email: str) -> User | None:
        """Получить пользователя по email со всеми связями"""
        return (
            self.db.query(User)
            .options(
                joinedload(User.profile),
                selectinload(User.favorite_memes),
                selectinload(User.created_memes),
            )
            .filter(User.email == email)
            .first()
        )