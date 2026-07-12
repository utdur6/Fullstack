"""
Главная страница - Битва мемов
"""

import random
import requests
import streamlit as st
from api.client import get_all_memes, vote_for_meme, get_error_message
from auth.state import is_authenticated

st.set_page_config(
    page_title="Битва мемов | Meme Battle",
    page_icon="⚔️",
    layout="wide"
)

# ========== ПРОСТАЯ НАВИГАЦИЯ ==========
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Главная", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("👤 Профиль", use_container_width=True):
        if is_authenticated():
            st.switch_page("pages/profile.py")
        else:
            st.warning("Войдите в аккаунт")
with col3:
    if st.button("🚪 Вход", use_container_width=True):
        st.switch_page("pages/login.py")

st.divider()

# ========== ОСНОВНОЙ КОНТЕНТ ==========
st.header("⚔️ Битва мемов")
st.caption("Голосуй за лучший мем!")

# Инициализация состояния
if 'meme1' not in st.session_state:
    st.session_state.meme1 = None
if 'meme2' not in st.session_state:
    st.session_state.meme2 = None

def load_memes():
    """Загружает два случайных мема для битвы"""
    try:
        response = get_all_memes()
        if response and response.ok:
            all_memes = response.json()
            if isinstance(all_memes, list) and len(all_memes) >= 2:
                selected = random.sample(all_memes, 2)
                st.session_state.meme1 = selected[0]
                st.session_state.meme2 = selected[1]
                return True
            else:
                st.warning("⚠️ Недостаточно мемов для битвы (нужно минимум 2).")
                st.session_state.meme1 = None
                st.session_state.meme2 = None
                return False
        else:
            st.error("❌ Не удалось загрузить мемы.")
            return False
    except Exception as e:
        st.error(f"❌ Ошибка: {e}")
        return False

# Кнопка обновления
if st.button("🔄 Обновить битву", use_container_width=True):
    st.session_state.meme1 = None
    st.session_state.meme2 = None
    st.rerun()

# Загружаем мемы, если их нет
if st.session_state.meme1 is None or st.session_state.meme2 is None:
    load_memes()

meme1 = st.session_state.meme1
meme2 = st.session_state.meme2

if meme1 and meme2:
    col1, col_vs, col2 = st.columns([2, 0.5, 2])

    with col1:
        with st.container(border=True):
            st.image(meme1.get('image_url', 'https://via.placeholder.com/400x300/667eea/ffffff?text=Meme+1'),
                    use_container_width=True)
            st.subheader(meme1.get('title', 'Мем #1'))
            st.caption(f"❤️ {meme1.get('votes', 0)} голосов")

            if st.button(f"⬆️ Голосовать за #1", key=f"vote_{meme1['id']}",
                        use_container_width=True, type="primary"):
                if is_authenticated():
                    try:
                        response = vote_for_meme(meme1['id'])
                        if response and response.ok:
                            st.success("✅ Голос учтён!")
                            st.session_state.meme1 = None
                            st.session_state.meme2 = None
                            st.rerun()
                        else:
                            st.error(get_error_message(response) if response else "Ошибка")
                    except requests.RequestException:
                        st.error("❌ Не удалось подключиться к бэкенду")
                else:
                    st.warning("⚠️ Войдите, чтобы голосовать!")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #FF4500; font-size: 4rem;'>⚡VS⚡</h1>",
                   unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.image(meme2.get('image_url', 'https://via.placeholder.com/400x300/764ba2/ffffff?text=Meme+2'),
                    use_container_width=True)
            st.subheader(meme2.get('title', 'Мем #2'))
            st.caption(f"❤️ {meme2.get('votes', 0)} голосов")

            if st.button(f"⬆️ Голосовать за #2", key=f"vote_{meme2['id']}",
                        use_container_width=True, type="primary"):
                if is_authenticated():
                    try:
                        response = vote_for_meme(meme2['id'])
                        if response and response.ok:
                            st.success("✅ Голос учтён!")
                            st.session_state.meme1 = None
                            st.session_state.meme2 = None
                            st.rerun()
                        else:
                            st.error(get_error_message(response) if response else "Ошибка")
                    except requests.RequestException:
                        st.error("❌ Не удалось подключиться к бэкенду")
                else:
                    st.warning("⚠️ Войдите, чтобы голосовать!")

    # Прогресс голосов
    votes1 = meme1.get('votes', 0)
    votes2 = meme2.get('votes', 0)
    total = votes1 + votes2

    if total > 0:
        st.progress(votes1 / total, text=f"📊 {meme1.get('title')}: {votes1} голосов ({votes1/total*100:.0f}%)")

        if votes1 > votes2:
            st.success(f"🏆 Лидирует: {meme1.get('title')}!")
        elif votes2 > votes1:
            st.success(f"🏆 Лидирует: {meme2.get('title')}!")
        else:
            st.info("⚖️ Ничья!")

else:
    st.info("📝 Добавьте мемы через админ-панель, чтобы начать битву!")

# ========== ТОП МЕМОВ ==========
st.divider()
st.subheader("🏆 Топ мемов")

try:
    response = get_all_memes()
    if response and response.ok:
        all_memes = response.json()
        if isinstance(all_memes, list) and all_memes:
            sorted_memes = sorted(all_memes, key=lambda x: x.get('votes', 0), reverse=True)[:5]
            for i, meme in enumerate(sorted_memes, 1):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                    st.write(f"### {medal}")
                with col2:
                    st.write(f"**{meme.get('title', 'Мем')}**")
                with col3:
                    st.write(f"❤️ {meme.get('votes', 0)}")
                st.divider()
        else:
            st.write("Нет мемов для отображения")
    else:
        st.write("Не удалось загрузить топ мемов")
except:
    st.write("Не удалось загрузить топ мемов")