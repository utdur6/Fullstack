from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"


# ========== БАЗА ДАННЫХ ==========
def get_db():
    conn = sqlite3.connect("memes.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            hashed_password TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Таблица тегов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            emoji TEXT
        )
    ''')

    # Таблица мемов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            image_url TEXT,
            votes INTEGER DEFAULT 0,
            tag_id INTEGER,
            created_by INTEGER,
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # Добавляем теги
    cursor.execute("SELECT COUNT(*) FROM tags")
    if cursor.fetchone()[0] == 0:
        tags = [
            ("Смешные", "😂"),
            ("Животные", "🐱"),
            ("Программирование", "💻"),
            ("Мемы", "🤣"),
            ("Фильмы", "🎬"),
        ]
        cursor.executemany("INSERT INTO tags (name, emoji) VALUES (?, ?)", tags)

    # Добавляем тестового администратора
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    if cursor.fetchone()[0] == 0:
        hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
            ("admin", "admin@example.com", hashed, "admin")
        )

    # Добавляем тестовые мемы
    cursor.execute("SELECT COUNT(*) FROM memes")
    if cursor.fetchone()[0] == 0:
        test_memes = [
            ("Кот-программист", "Кот смотрит в код", "https://via.placeholder.com/400x300/667eea/ffffff?text=Кот", 1,
             1),
            ("Собака-баг", "Собака ищет баги", "https://via.placeholder.com/400x300/764ba2/ffffff?text=Собака", 2, 1),
            ("Хаски-разработчик", "Хаски пишет код", "https://via.placeholder.com/400x300/f093fb/ffffff?text=Хаски", 3,
             1),
            ("Мем-день", "Смешной мем", "https://via.placeholder.com/400x300/4CAF50/ffffff?text=Мем", 4, 1),
        ]
        cursor.executemany(
            "INSERT INTO memes (title, description, image_url, tag_id, created_by) VALUES (?, ?, ?, ?, ?)",
            test_memes
        )

    conn.commit()
    conn.close()


init_db()


# ========== СХЕМЫ ==========
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class MemeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    tag_id: int = 1


class TagResponse(BaseModel):
    id: int
    name: str
    emoji: str


# ========== ФУНКЦИИ ==========
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ========== ЭНДПОИНТЫ ==========

@app.get("/")
def root():
    return {"message": "Meme Battle API"}


# ---- АВТОРИЗАЦИЯ ----
@app.post("/auth/register")
def register(user: UserRegister):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (user.email, user.username))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(400, "Пользователь уже существует")

    hashed = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
        (user.username, user.email, hashed, "user")
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return {"id": user_id, "username": user.username, "email": user.email, "role": "user"}


@app.post("/auth/login")
def login(user: UserLogin):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(401, "Неверный email или пароль")

    token = create_token({"sub": db_user["email"], "user_id": db_user["id"], "role": db_user["role"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user["id"],
            "username": db_user["username"],
            "email": db_user["email"],
            "role": db_user["role"]
        }
    }


@app.get("/users/me")
def get_current_user():
    # Простая заглушка — возвращаем первого пользователя
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(404, "Пользователь не найден")

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }


# ---- ТЕГИ ----
@app.get("/tags")
def get_tags():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags")
    tags = cursor.fetchall()
    conn.close()

    return [{"id": t["id"], "name": t["name"], "emoji": t["emoji"]} for t in tags]


# ---- МЕМЫ ----
@app.get("/memes")
def get_memes(tag_id: Optional[int] = None):
    conn = get_db()
    cursor = conn.cursor()

    if tag_id:
        cursor.execute("SELECT * FROM memes WHERE tag_id = ?", (tag_id,))
    else:
        cursor.execute("SELECT * FROM memes")

    memes = cursor.fetchall()
    conn.close()

    return [{"id": m["id"], "title": m["title"], "description": m["description"],
             "image_url": m["image_url"], "votes": m["votes"], "tag_id": m["tag_id"]} for m in memes]


@app.post("/memes")
def create_meme(meme: MemeCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memes (title, description, image_url, tag_id) VALUES (?, ?, ?, ?)",
        (meme.title, meme.description, meme.image_url, meme.tag_id)
    )
    conn.commit()
    meme_id = cursor.lastrowid
    conn.close()

    return {"id": meme_id, "title": meme.title, "description": meme.description,
            "image_url": meme.image_url, "votes": 0, "tag_id": meme.tag_id}


@app.post("/memes/{meme_id}/vote")
def vote_meme(meme_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE memes SET votes = votes + 1 WHERE id = ?", (meme_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(404, "Мем не найден")
    conn.commit()

    cursor.execute("SELECT votes FROM memes WHERE id = ?", (meme_id,))
    votes = cursor.fetchone()
    conn.close()

    return {"id": meme_id, "votes": votes["votes"]}


@app.delete("/memes/{meme_id}")
def delete_meme(meme_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memes WHERE id = ?", (meme_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(404, "Мем не найден")
    conn.commit()
    conn.close()
    return {"message": "Мем удален"}