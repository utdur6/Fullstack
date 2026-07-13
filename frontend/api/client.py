"""
Клиент для работы с API бэкенда
"""
# api/client.py
import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

# ========== ЭНДПОИНТЫ ==========
# Проверьте, какой путь используется в вашем бэкенде!
# Возможно, у вас /api/memes или /memes/
MEMES_ENDPOINT = f"{BACKEND_URL}/memes"  # Или /api/memes

def get_all_memes():
    """Получить все мемы"""
    try:
        # Попробуйте разные варианты
        response = requests.get(f"{BACKEND_URL}/memes")  # основной
        # Если не работает, попробуйте:
        # response = requests.get(f"{BACKEND_URL}/api/memes")
        # response = requests.get(f"{BACKEND_URL}/memes/")
        return response
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
        return None
import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

# Эндпоинты
LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me"
MEMES_ENDPOINT = f"{BACKEND_URL}/memes"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites"


# ========== ПУБЛИЧНЫЕ ЗАПРОСЫ ==========

def register(email: str, password: str, username: str) -> requests.Response:
    """Регистрация пользователя"""
    data = {
        "email": email,
        "password": password,
        "username": username,
    }
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email: str, password: str) -> requests.Response:
    """Вход пользователя"""
    data = {
        "email": email,
        "password": password,
    }
    return requests.post(LOGIN_ENDPOINT, json=data)


def get_all_memes() -> requests.Response:
    """Получить все мемы (публичный запрос)"""
    return requests.get(MEMES_ENDPOINT)


def get_meme(meme_id: int) -> requests.Response:
    """Получить один мем по ID"""
    return requests.get(f"{MEMES_ENDPOINT}/{meme_id}")


# ========== АВТОРИЗОВАННЫЕ ЗАПРОСЫ ==========

def _request_with_auth(method: str, url: str, **kwargs) -> requests.Response:
    """Внутренняя функция для запросов с JWT-токеном"""
    headers = {"Authorization": f"Bearer {session_state.get('access_token')}"}

    if 'headers' in kwargs:
        kwargs['headers'].update(headers)
    else:
        kwargs['headers'] = headers

    response = requests.request(method, url, **kwargs)

    # Если токен невалиден - чистим сессию
    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)

    return response


def get_profile() -> requests.Response:
    """Получить профиль пользователя"""
    return _request_with_auth("GET", PROFILE_ENDPOINT)


def vote_for_meme(meme_id: int) -> requests.Response:
    """Проголосовать за мем"""
    return _request_with_auth("POST", f"{MEMES_ENDPOINT}/{meme_id}/vote")


def create_meme(payload: dict) -> requests.Response:
    """Создать новый мем (только админ)"""
    return _request_with_auth("POST", MEMES_ENDPOINT, json=payload)


def update_meme(meme_id: int, payload: dict) -> requests.Response:
    """Обновить мем (только админ)"""
    return _request_with_auth("PATCH", f"{MEMES_ENDPOINT}/{meme_id}", json=payload)


def delete_meme(meme_id: int) -> requests.Response:
    """Удалить мем (только админ)"""
    return _request_with_auth("DELETE", f"{MEMES_ENDPOINT}/{meme_id}")


# ========== ИЗБРАННОЕ ==========

def get_favorites() -> requests.Response:
    """Получить избранные мемы"""
    return _request_with_auth("GET", FAVORITES_ENDPOINT)


def add_favorite(meme_id: int) -> requests.Response:
    """Добавить в избранное"""
    return _request_with_auth("POST", f"{FAVORITES_ENDPOINT}/{meme_id}")


def remove_favorite(meme_id: int) -> requests.Response:
    """Удалить из избранного"""
    return _request_with_auth("DELETE", f"{FAVORITES_ENDPOINT}/{meme_id}")


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def get_error_message(response: requests.Response) -> str:
    """Извлекает сообщение об ошибке из ответа бэкенда"""
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка HTTP {response.status_code}"