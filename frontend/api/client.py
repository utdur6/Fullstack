import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

# ---- ПУБЛИЧНЫЕ ЗАПРОСЫ ----
def register(email: str, password: str):
    try:
        return requests.post(f"{BACKEND_URL}/auth/register", json={"email": email, "password": password})
    except requests.RequestException:
        return None

def login(email: str, password: str):
    try:
        return requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})
    except requests.RequestException:
        return None

def get_all_memes():
    try:
        return requests.get(f"{BACKEND_URL}/memes")
    except requests.RequestException:
        return None

# ---- АВТОРИЗОВАННЫЕ ЗАПРОСЫ ----
def _request_with_auth(method: str, endpoint: str, payload: dict = None):
    token = session_state.get("access_token")
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if method == "GET":
            return requests.get(endpoint, headers=headers)
        elif method == "POST":
            return requests.post(endpoint, headers=headers, json=payload)
        elif method == "DELETE":
            return requests.delete(endpoint, headers=headers)
    except requests.RequestException:
        return None

def get_profile():
    return _request_with_auth("GET", f"{BACKEND_URL}/users/me")

def vote_for_meme(meme_id: int):
    return _request_with_auth("POST", f"{BACKEND_URL}/memes/{meme_id}/vote/")

def create_meme(payload: dict):
    return _request_with_auth("POST", f"{BACKEND_URL}/memes", payload=payload)

def delete_meme(meme_id: int):
    return _request_with_auth("DELETE", f"{BACKEND_URL}/memes/{meme_id}")

def get_error_message(response):
    if response is None:
        return "Бэкенд недоступен"
    try:
        return response.json().get("detail", f"Ошибка {response.status_code}")
    except:
        return f"Ошибка {response.status_code}"