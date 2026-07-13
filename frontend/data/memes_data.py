# Инициализация данных (в реальном проекте здесь будет БД)
memes_db = [
    {
        "id": 1,
        "name": "Первый мем",
        "description": "Описание первого мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag": "Funny",
        "author": "Иван Иванов",
        "created_at": "2026-07-12"
    },
    {
        "id": 2,
        "name": "Второй мем",
        "description": "Описание второго мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag": "Cute",
        "author": "Петр Петров",
        "created_at": "2026-07-11"
    },
    {
        "id": 3,
        "name": "Третий мем",
        "description": "Описание третьего мема",
        "photo": "https://via.placeholder.com/300x200",
        "tag": "Meme",
        "author": "Иван Иванов",
        "created_at": "2026-07-10"
    }
]

# Избранные мемы (храним ID мемов)
favourites_db = [1, 3]

def get_all_memes():
    return memes_db

def get_meme_by_id(meme_id):
    for meme in memes_db:
        if meme["id"] == meme_id:
            return meme
    return None

def add_meme(meme_data):
    new_id = max([m["id"] for m in memes_db]) + 1 if memes_db else 1
    meme_data["id"] = new_id
    memes_db.append(meme_data)
    return meme_data

def get_favourites():
    return [get_meme_by_id(m_id) for m_id in favourites_db if get_meme_by_id(m_id)]

def toggle_favourite(meme_id):
    if meme_id in favourites_db:
        favourites_db.remove(meme_id)
        return False
    else:
        favourites_db.append(meme_id)
        return True

def is_favourite(meme_id):
    return meme_id in favourites_db

# Функции для тегов
def get_all_tags():
    tags = set()
    for meme in memes_db:
        tags.add(meme["tag"])
    return sorted(list(tags))

def get_memes_by_tag(tag):
    return [meme for meme in memes_db if meme["tag"] == tag]