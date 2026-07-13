"""
Модуль для управления авторизацией пользователей
"""

import streamlit as st
from typing import Optional, Dict
from .api import MemeAPI

class AuthManager:
    """Класс для управления авторизацией"""

    def __init__(self):
        self.api = MemeAPI()

    def login(self, username: str, password: str) -> bool:
        """Вход пользователя"""
        user_data = self.api.login_user(username, password)
        if user_data:
            st.session_state.user = user_data
            st.session_state.logged_in = True
            return True
        return False

    def logout(self):
        """Выход пользователя"""
        st.session_state.user = None
        st.session_state.logged_in = False
        st.rerun()

    def register(self, username: str, email: str, password: str) -> bool:
        """Регистрация пользователя"""
        user_data = self.api.register_user({
            "username": username,
            "email": email,
            "password": password
        })
        return user_data is not None

    @staticmethod
    def is_authenticated() -> bool:
        """Проверка авторизации"""
        return st.session_state.get('logged_in', False) and st.session_state.get('user') is not None

    @staticmethod
    def get_current_user() -> Optional[Dict]:
        """Получить текущего пользователя"""
        return st.session_state.get('user', None)

    @staticmethod
    def get_user_id() -> Optional[int]:
        """Получить ID текущего пользователя"""
        user = st.session_state.get('user', None)
        return user.get('id') if user else None