from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meme_id = Column(Integer, ForeignKey("memes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())