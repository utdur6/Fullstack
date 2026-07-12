"""
Главный файл приложения с навигацией
"""
import sys
import os

# Добавляем текущую папку в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from auth.state import is_admin


st.set_page_config(
    page_title="Meme Battle",
    page_icon="⚔️",
    layout="wide",
)

# Определяем страницы
pages = {
    "Главная": [
        st.Page("pages/catalog.py", title="Битва мемов", icon="⚔️", url_path="catalog", default=True),
    ],
    "Пользователь": [
        st.Page("pages/profile.py", title="Профиль", icon="👤", url_path="profile"),
    ],
    "Авторизация": [
        st.Page("pages/login.py", title="Вход", icon="🔑", url_path="login"),
        st.Page("pages/registration.py", title="Регистрация", icon="📝", url_path="registration"),
    ],
}

if is_admin():
    pages["Администрирование"] = [
        st.Page("pages/create_meme.py", title="Добавить мем", icon="➕", url_path="create-meme"),
        st.Page("pages/edit_meme.py", title="Редактировать мем", icon="✏️", url_path="edit-meme"),
    ]

# Создаем и запускаем навигацию
navigation = st.navigation(pages)
navigation.run()