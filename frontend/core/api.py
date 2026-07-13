"""
Модуль для работы с API бэкенда
"""

import requests
import streamlit as st
from typing import Optional, List, Dict, Any

API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 10

class MemeAPI:
    """Класс для работы с API"""

    @staticmethod
    def _make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Универсальный метод для запросов"""
        url = f"{API_BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=API_TIMEOUT)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=API_TIMEOUT)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}

            if response.status_code >= 400:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text or 'Unknown error'
                return {
                    "success": False,
                    "error": error_detail,
                    "status_code": response.status_code
                }

            return {
                "success": True,
                "data": response.json() if response.text else None,
                "status_code": response.status_code
            }

        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "❌ Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на http://localhost:8000"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "⏰ Превышено время ожидания"}
        except Exception as e:
            return {"success": False, "error": f"❌ Ошибка: {str(e)}"}

    # ========== МЕТОДЫ ДЛЯ МЕМОВ ==========

    @staticmethod
    def get_random_memes(limit: int = 2) -> List[Dict]:
        """Получить случайные мемы для битвы"""
        result = MemeAPI._make_request("GET", f"/memes/random?limit={limit}")
        if result["success"]:
            return result.get("data", [])
        else:
            st.error(result.get("error", "Ошибка загрузки мемов"))
            return []

    @staticmethod
    def get_top_memes(limit: int = 10) -> List[Dict]:
        """Получить топ мемов"""
        result = MemeAPI._make_request("GET", f"/memes/top?limit={limit}")
        return result.get("data", []) if result["success"] else []

    @staticmethod
    def get_meme_stats() -> Dict:
        """Получить статистику"""
        result = MemeAPI._make_request("GET", "/memes/stats")
        if result["success"]:
            return result.get("data", {})
        return {"total_memes": 0, "total_votes": 0, "battles_today": 0}

    @staticmethod
    def vote_for_meme(meme_id: int, user_id: int) -> bool:
        """Проголосовать за мем"""
        result = MemeAPI._make_request("POST", f"/memes/{meme_id}/vote", data={"user_id": user_id})
        if result["success"]:
            return True
        else:
            st.error(result.get("error", "❌ Ошибка при голосовании"))
            return False

    @staticmethod
    def get_meme_by_id(meme_id: int) -> Optional[Dict]:
        """Получить мем по ID"""
        result = MemeAPI._make_request("GET", f"/memes/{meme_id}")
        return result.get("data") if result["success"] else None

    @staticmethod
    def create_meme(meme_data: Dict) -> Optional[Dict]:
        """Создать новый мем"""
        result = MemeAPI._make_request("POST", "/memes", data=meme_data)
        return result.get("data") if result["success"] else None

    @staticmethod
    def delete_meme(meme_id: int) -> bool:
        """Удалить мем"""
        result = MemeAPI._make_request("DELETE", f"/memes/{meme_id}")
        return result["success"]

    # ========== МЕТОДЫ ДЛЯ ТЕГОВ ==========

    @staticmethod
    def get_tags() -> List[Dict]:
        """Получить все теги"""
        result = MemeAPI._make_request("GET", "/tags")
        return result.get("data", []) if result["success"] else []

    @staticmethod
    def create_tag(tag_data: Dict) -> Optional[Dict]:
        """Создать новый тег"""
        result = MemeAPI._make_request("POST", "/tags", data=tag_data)
        return result.get("data") if result["success"] else None

    # ========== МЕТОДЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ==========

    @staticmethod
    def login_user(username: str, password: str) -> Optional[Dict]:
        """Вход пользователя"""
        result = MemeAPI._make_request("POST", "/auth/login", data={"username": username, "password": password})
        if result["success"]:
            return result.get("data")
        else:
            st.error(result.get("error", "❌ Неверный логин или пароль"))
            return None

    @staticmethod
    def register_user(user_data: Dict) -> Optional[Dict]:
        """Регистрация пользователя"""
        result = MemeAPI._make_request("POST", "/auth/register", data=user_data)
        if result["success"]:
            return result.get("data")
        else:
            st.error(result.get("error", "❌ Ошибка при регистрации"))
            return None

    @staticmethod
    def get_user_stats(user_id: int) -> Dict:
        """Получить статистику пользователя"""
        result = MemeAPI._make_request("GET", f"/users/{user_id}/stats")
        return result.get("data", {"votes_count": 0, "rating": 0}) if result["success"] else {}

# Создаем экземпляр для удобства
api = MemeAPI()