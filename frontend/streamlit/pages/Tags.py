"""
Страница тегов
"""

import streamlit as st

st.set_page_config(
    page_title="Теги | Meme Battle",
    page_icon="🏷️",
    layout="wide"
)

st.header("🏷️ Теги")
st.info("Здесь будут отображаться все теги")

# Заглушка с примерами
tags = [
    {"name": "Смешные", "count": 15, "emoji": "😂"},
    {"name": "Животные", "count": 12, "emoji": "🐱"},
    {"name": "Программирование", "count": 8, "emoji": "💻"},
    {"name": "Мемы", "count": 20, "emoji": "🤣"},
    {"name": "Фильмы", "count": 5, "emoji": "🎬"},
]

for tag in tags:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write(f"{tag['emoji']}")
    with col2:
        st.write(f"**{tag['name']}**")
    with col3:
        st.write(f"{tag['count']} мемов")
    st.divider()