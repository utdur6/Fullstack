from __future__ import annotations

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.users import user_memes


class Memes(Base):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Связь с Tag (один-ко-многим)
    tag = relationship("Tag", back_populates="memes")

    # Связь многие-ко-многим с User через user_memes
    users = relationship("User", secondary=user_memes, back_populates="memes")