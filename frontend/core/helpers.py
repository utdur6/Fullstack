"""
Вспомогательные функции для приложения
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict

def format_date(date_str: Optional[str]) -> str:
    """Форматирование даты"""
    if not date_str:
        return "Неизвестно"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return date_str

def get_vote_percent(votes: int, total_votes: int) -> float:
    """Вычислить процент голосов"""
    if total_votes == 0:
        return 50.0
    return (votes / total_votes) * 100

def get_medal(index: int) -> str:
    """Получить эмодзи медали по индексу"""
    medals = ["🥇", "🥈", "🥉"]
    if index < len(medals):
        return medals[index]
    return f"#{index + 1}"

def show_loading(message: str = "Загрузка..."):
    """Показать индикатор загрузки"""
    with st.spinner(message):
        return

def handle_api_error(error: Exception) -> None:
    """Обработка ошибок API"""
    error_str = str(error)
    if "ConnectionError" in error_str or "Connection refused" in error_str:
        st.error("❌ Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на http://localhost:8000")
    elif "Timeout" in error_str:
        st.error("⏰ Превышено время ожидания ответа от сервера.")
    elif "404" in error_str:
        st.error("❌ Запрашиваемый ресурс не найден.")
    else:
        st.error(f"❌ Произошла ошибка: {error_str}")

def truncate_text(text: str, max_length: int = 50) -> str:
    """Обрезать текст до определенной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_winner(meme1: Dict, meme2: Dict) -> Optional[Dict]:
    """Определить победителя между двумя мемами"""
    votes1 = meme1.get('votes', 0)
    votes2 = meme2.get('votes', 0)

    if votes1 > votes2:
        return meme1
    elif votes2 > votes1:
        return meme2
    return None

def get_vote_color(votes: int, total_votes: int) -> str:
    """Получить цвет для полоски голосов"""
    if total_votes == 0:
        return "#e0e0e0"

    percent = (votes / total_votes) * 100

    if percent >= 70:
        return "#4CAF50"
    elif percent >= 50:
        return "#FF9800"
    elif percent >= 30:
        return "#F44336"
    else:
        return "#9E9E9E"