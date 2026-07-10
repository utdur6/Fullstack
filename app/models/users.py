from __future__ import annotations

from enum import Enum

from sqlalchemy import Boolean, String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# Связующая таблица для many-to-many
user_memes = Table(
    "user_memes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("meme_id", ForeignKey("memes.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str] = mapped_column(
        String(50),
        default=UserRole.USER.value,
        nullable=False,
    )

    # Связь многие-ко-многим с Memes через user_memes
    memes = relationship("Memes", secondary=user_memes, back_populates="users")