import streamlit as st
import random
import requests
from api.client import get_all_memes, vote_for_meme, get_error_message
from auth.state import is_authenticated, is_admin


def show():
    st.header("⚔️ Битва мемов")
    st.caption("Голосуй за лучший мем!")

    if 'meme1' not in st.session_state:
        st.session_state.meme1 = None
    if 'meme2' not in st.session_state:
        st.session_state.meme2 = None

    def load_memes():
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
                    st.warning("⚠️ Нужно минимум 2 мема")
                    return False
            else:
                st.error("❌ Не удалось загрузить мемы")
                return False
        except Exception as e:
            st.error(f"❌ Ошибка: {e}")
            return False

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Обновить битву", use_container_width=True):
            st.session_state.meme1 = None
            st.session_state.meme2 = None
            st.rerun()

    if st.session_state.meme1 is None or st.session_state.meme2 is None:
        load_memes()

    meme1 = st.session_state.meme1
    meme2 = st.session_state.meme2

    if meme1 and meme2:
        col1, col_vs, col2 = st.columns([2, 0.5, 2])

        with col1:
            with st.container(border=True):
                st.image(meme1.get('image_url', 'https://via.placeholder.com/400x300'), use_container_width=True)
                st.subheader(meme1.get('title', 'Мем #1'))
                st.caption(f"❤️ {meme1.get('votes', 0)} голосов")
                if st.button(f"⬆️ Голосовать", key=f"vote1", use_container_width=True, type="primary"):
                    if is_authenticated():
                        response = vote_for_meme(meme1['id'])
                        if response and response.ok:
                            st.success("✅ Голос учтён!")
                            st.session_state.meme1 = None
                            st.session_state.meme2 = None
                            st.rerun()
                        else:
                            st.error("❌ Ошибка голосования")
                    else:
                        st.warning("⚠️ Войдите, чтобы голосовать!")

        with col_vs:
            st.markdown("<h1 style='text-align:center;color:#e94560;font-size:3rem;'>⚡VS⚡</h1>", unsafe_allow_html=True)

        with col2:
            with st.container(border=True):
                st.image(meme2.get('image_url', 'https://via.placeholder.com/400x300'), use_container_width=True)
                st.subheader(meme2.get('title', 'Мем #2'))
                st.caption(f"❤️ {meme2.get('votes', 0)} голосов")
                if st.button(f"⬆️ Голосовать", key=f"vote2", use_container_width=True, type="primary"):
                    if is_authenticated():
                        response = vote_for_meme(meme2['id'])
                        if response and response.ok:
                            st.success("✅ Голос учтён!")
                            st.session_state.meme1 = None
                            st.session_state.meme2 = None
                            st.rerun()
                        else:
                            st.error("❌ Ошибка голосования")
                    else:
                        st.warning("⚠️ Войдите, чтобы голосовать!")

        votes1 = meme1.get('votes', 0)
        votes2 = meme2.get('votes', 0)
        total = votes1 + votes2

        if total > 0:
            st.progress(votes1 / total, text=f"{meme1.get('title')}: {votes1} голосов ({votes1 / total * 100:.0f}%)")
            if votes1 > votes2:
                st.success(f"🏆 Лидирует: {meme1.get('title')}!")
            elif votes2 > votes1:
                st.success(f"🏆 Лидирует: {meme2.get('title')}!")
            else:
                st.info("⚖️ Ничья!")
    else:
        st.info("📝 Добавьте мемы через админ-панель!")


if __name__ == "__main__":
    show()