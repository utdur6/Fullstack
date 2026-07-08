from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Memes(Base):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String,unique= True, nullable=False)


    description: Mapped[str] = mapped_column(String,unique= True, nullable=False)

    photo: Mapped[str] = mapped_column(String, nullable=False)

    tag_id = Column(Integer, nullable=True)