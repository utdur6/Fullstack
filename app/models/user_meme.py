from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class UserMeme(Base):
    __tablename__ = "user_memes"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ← ДОБАВИТЬ ID
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    meme_id = Column(
        Integer,
        ForeignKey("memes.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="favorite_links")
    meme = relationship("Meme", back_populates="favorite_links")