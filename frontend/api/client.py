import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me/"
MEMES_ENDPOINT = f"{BACKEND_URL}/memes/"
TAGS_ENDPOINT = f"{BACKEND_URL}/tags/"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites/"


def register(email: str, password: str, username: str):
    data = {"email": email, "password": password, "username": username}
    try:
        return requests.post(REGISTER_ENDPOINT, json=data)
    except requests.RequestException:
        return None


def login(email: str, password: str):
    data = {"email": email, "password": password}
    try:
        return requests.post(LOGIN_ENDPOINT, json=data)
    except requests.RequestException:
        return None


def get_all_memes():
    try:
        return requests.get(MEMES_ENDPOINT)
    except requests.RequestException:
        return None


def get_all_tags():
    """Получить все теги"""
    try:
        return requests.get(TAGS_ENDPOINT)
    except requests.RequestException:
        return None


def get_memes_by_tag(tag_id: int):
    """Получить мемы по тегу"""
    try:
        return requests.get(f"{MEMES_ENDPOINT}?tag_id={tag_id}")
    except requests.RequestException:
        return None


def _request_with_auth(method: str, endpoint: str, params: dict = None, payload: dict = None):
    token = session_state.get("access_token")
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    try:
        if method == "GET":
            response = requests.get(endpoint, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(endpoint, headers=headers, params=params, json=payload)
        elif method == "PATCH":
            response = requests.patch(endpoint, headers=headers, params=params, json=payload)
        elif method == "DELETE":
            response = requests.delete(endpoint, headers=headers, params=params)
        else:
            raise ValueError("Неизвестный метод")
    except requests.RequestException:
        return None

    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)
    return response


def get_profile():
    return _request_with_auth("GET", PROFILE_ENDPOINT)


def vote_for_meme(meme_id: int):
    return _request_with_auth("POST", f"{MEMES_ENDPOINT}{meme_id}/vote/")


def create_meme(payload: dict):
    return _request_with_auth("POST", MEMES_ENDPOINT, payload=payload)


def get_error_message(response):
    if response is None:
        return "Не удалось подключиться к серверу."
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка HTTP {response.status_code}"