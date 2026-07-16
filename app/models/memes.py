from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user_memes_table import user_memes_table


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    photo = Column(String, nullable=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    tag = relationship("Tag", back_populates="memes")
    author = relationship("User", back_populates="created_memes")

    favorited_by = relationship(
        "User",
        secondary=user_memes_table,
        back_populates="favorite_memes",
        lazy="selectin"
    )