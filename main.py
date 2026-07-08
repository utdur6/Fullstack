from app.database import Base, engine
Base.metadata.create_all(bind=engine)
from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello World"}