import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI


from app.config.config import get_settings
from app.database import Base, engine
from app.handlers.auth import router as auth_router
from app.handlers.memes import router as books_router
from app.handlers.users import router as users_router
from app.models.tags import Tag
from app.models.memes import Memes
from app.models.users import User

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(users_router)



@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=8000)