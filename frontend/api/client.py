import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

def get_all_memes():
    """Получить все мемы"""
    try:
        # Пробуем с разными вариантами URL
        response = requests.get(f"{BACKEND_URL}/memes")
        if response.status_code == 405:
            # Если /memes не работает, пробуем /memes/
            response = requests.get(f"{BACKEND_URL}/memes/")
        return response
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        print(f"Ошибка в get_all_memes: {e}")
        return None