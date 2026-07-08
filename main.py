from fastapi import FastAPI

from app.database import Base, engine
from app.handlers.memes import router as books_router
from app.models.memes import Memes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(books_router)


@app.get("/")
def root():
    return {"message": "Hello World"}