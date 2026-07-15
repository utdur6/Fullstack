from enum import Enum
from sqlalchemy import Boolean, String, Column, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(50), default=UserRole.USER.value, nullable=False)

    profile = relationship("Profile", backref="user", uselist=False)

    favorite_memes = relationship(
        "Meme",
        secondary="user_memes",
        backref="favorited_by",
        lazy="selectin"
    )

    created_memes = relationship("Meme", backref="author")