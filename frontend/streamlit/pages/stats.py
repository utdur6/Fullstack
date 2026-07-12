"""
Страница статистики
"""

import streamlit as st
from api.client import get_all_memes

st.set_page_config(
    page_title="Статистика | Meme Battle",
    page_icon="📊",
    layout="wide"
)

st.header("📊 Статистика")

try:
    response = get_all_memes()
    if response and response.ok:
        all_memes = response.json()
        if isinstance(all_memes, list):
            total_memes = len(all_memes)
            total_votes = sum(m.get('votes', 0) for m in all_memes)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Всего мемов", total_memes)
            with col2:
                st.metric("Всего голосов", total_votes)
            with col3:
                st.metric("Средний рейтинг", f"{total_votes / total_memes:.1f}" if total_memes > 0 else "0")

            if total_votes > 0:
                st.subheader("📈 Распределение голосов")
                for meme in sorted(all_memes, key=lambda x: x.get('votes', 0), reverse=True)[:10]:
                    progress = meme.get('votes', 0) / total_votes if total_votes > 0 else 0
                    st.write(f"{meme.get('title', 'Мем')}: {meme.get('votes', 0)} голосов")
                    st.progress(progress)
        else:
            st.info("Нет данных для статистики")
    else:
        st.error("❌ Не удалось загрузить данные")
except:
    st.error("❌ Ошибка загрузки статистики")