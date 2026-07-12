from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Добавьте CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ЭНДПОИНТ ДЛЯ МЕМОВ ==========
@app.get("/memes")
async def get_memes():
    """Получить все мемы"""
    # Временная заглушка
    return [
        {
            "id": 1,
            "title": "Мем #1",
            "description": "Первый мем",
            "image_url": "https://via.placeholder.com/400x300/667eea/ffffff?text=Meme+1",
            "votes": 15
        },
        {
            "id": 2,
            "title": "Мем #2",
            "description": "Второй мем",
            "image_url": "https://via.placeholder.com/400x300/764ba2/ffffff?text=Meme+2",
            "votes": 10
        },
        {
            "id": 3,
            "title": "Мем #3",
            "description": "Третий мем",
            "image_url": "https://via.placeholder.com/400x300/f093fb/ffffff?text=Meme+3",
            "votes": 8
        }
    ]

@app.post("/memes/{meme_id}/vote")
async def vote_meme(meme_id: int):
    """Проголосовать за мем"""
    return {"message": f"Голос за мем {meme_id} учтён!"}
# Настройка приложения
app = FastAPI(
    title="Meme API",
    version="0.1.0",
    debug=True,
)

# Настройка CORS (для доступа с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic схемы ---
class MemeResponse(BaseModel):
    id: int
    name: str
    description: str
    photo: str
    tag_id: Optional[int] = None
    created_at: Optional[str] = None

class MemeCreate(BaseModel):
    name: str
    description: str
    photo: str
    tag_id: Optional[int] = None

class TagResponse(BaseModel):
    id: int
    name: str

# --- Временное хранилище данных (вместо БД) ---
memes_db = [
    {
        "id": 1,
        "name": "Первый мем",
        "description": "Описание первого мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag_id": 1,
        "created_at": "2026-07-12T10:00:00"
    },
    {
        "id": 2,
        "name": "Второй мем",
        "description": "Описание второго мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag_id": 2,
        "created_at": "2026-07-11T10:00:00"
    },
    {
        "id": 3,
        "name": "Третий мем",
        "description": "Описание третьего мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag_id": 1,
        "created_at": "2026-07-10T10:00:00"
    }
]

tags_db = [
    {"id": 1, "name": "Funny"},
    {"id": 2, "name": "Cute"},
    {"id": 3, "name": "Meme"},
]

next_meme_id = 4
next_tag_id = 4

# --- API для мемов ---
@app.get("/api/memes", response_model=List[MemeResponse])
def get_all_memes():
    """Получить все мемы"""
    return memes_db

@app.get("/api/memes/{meme_id}", response_model=MemeResponse)
def get_meme_by_id(meme_id: int):
    """Получить мем по ID"""
    for meme in memes_db:
        if meme["id"] == meme_id:
            return meme
    raise HTTPException(status_code=404, detail="Meme not found")

@app.post("/api/memes", response_model=MemeResponse)
def create_meme(meme_data: MemeCreate):
    """Создать новый мем"""
    global next_meme_id
    new_meme = {
        "id": next_meme_id,
        "name": meme_data.name,
        "description": meme_data.description,
        "photo": meme_data.photo,
        "tag_id": meme_data.tag_id,
        "created_at": datetime.now().isoformat()
    }
    memes_db.append(new_meme)
    next_meme_id += 1
    return new_meme

@app.delete("/api/memes/{meme_id}")
def delete_meme(meme_id: int):
    """Удалить мем"""
    global memes_db
    memes_db = [m for m in memes_db if m["id"] != meme_id]
    return {"message": "Meme deleted"}

# --- API для тегов ---
@app.get("/api/tags", response_model=List[TagResponse])
def get_all_tags():
    """Получить все теги"""
    return tags_db

@app.post("/api/tags")
def create_tag(name: str):
    """Создать новый тег"""
    global next_tag_id
    new_tag = {"id": next_tag_id, "name": name}
    tags_db.append(new_tag)
    next_tag_id += 1
    return new_tag

# --- Health check ---
@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": "Meme API"}

@app.get("/")
def root():
    return {"message": "Meme API is running"}