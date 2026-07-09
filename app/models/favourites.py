from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    meme_id: Mapped[int] = mapped_column(ForeignKey("memes.id"), nullable=False)



    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    meme = relationship("Memes", back_populates="favourites")


