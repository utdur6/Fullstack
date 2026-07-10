from __future__ import annotations

from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Связь с Memes (один-ко-многим)
    memes: Mapped[list["Memes"]] = relationship(back_populates="tag")