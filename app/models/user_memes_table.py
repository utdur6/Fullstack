from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

user_memes_table = Table(
    'user_memes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('meme_id', Integer, ForeignKey('memes.id'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)