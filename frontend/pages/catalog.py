import streamlit as st
import random
import requests
from api.client import get_all_memes, vote_for_meme, get_error_message
from auth.state import is_authenticated


def show():
    # Заголовок
    st.markdown("""
        <style>
        .meme-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .meme-card:hover {
            transform: scale(1.02);
        }
        .meme-card img {
            max-width: 100%;
            border-radius: 8px;
            height: 200px;
            object-fit: cover;
        }
        .vs-text {
            font-size: 48px;
            font-weight: bold;
            color: #ff6b6b;
            text-align: center;
            padding: 20px;
        }
        .vote-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .vote-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            transition: width 0.5s;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("⚔️ Битва мемов")
    st.caption("Голосуй за лучший мем!")

    # Инициализация состояния
    if 'meme1' not in st.session_state:
        st.session_state.meme1 = None
    if 'meme2' not in st.session_state:
        st.session_state.meme2 = None

    def load_memes():
        """Загружает два случайных мема"""
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

    # Кнопка обновления
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
        # Отображаем два мема с VS между ними
        col1, col_vs, col2 = st.columns([2, 0.5, 2])

        with col1:
            with st.container():
                st.markdown(f"""
                    <div class="meme-card">
                        <img src="{meme1.get('image_url', 'https://via.placeholder.com/400x300')}" 
                             alt="{meme1.get('title', 'Мем')}">
                        <h4>{meme1.get('title', 'Мем #1')}</h4>
                        <p>{meme1.get('description', '')}</p>
                        <p style="font-size:18px; font-weight:bold;">❤️ {meme1.get('votes', 0)} голосов</p>
                    </div>
                """, unsafe_allow_html=True)

                if st.button(f"⬆️ Голосовать за #1", key=f"vote1", use_container_width=True, type="primary"):
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
            st.markdown('<div class="vs-text">⚡VS⚡</div>', unsafe_allow_html=True)

        with col2:
            with st.container():
                st.markdown(f"""
                    <div class="meme-card">
                        <img src="{meme2.get('image_url', 'https://via.placeholder.com/400x300')}" 
                             alt="{meme2.get('title', 'Мем')}">
                        <h4>{meme2.get('title', 'Мем #2')}</h4>
                        <p>{meme2.get('description', '')}</p>
                        <p style="font-size:18px; font-weight:bold;">❤️ {meme2.get('votes', 0)} голосов</p>
                    </div>
                """, unsafe_allow_html=True)

                if st.button(f"⬆️ Голосовать за #2", key=f"vote2", use_container_width=True, type="primary"):
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

        # Шкала голосов
        votes1 = meme1.get('votes', 0)
        votes2 = meme2.get('votes', 0)
        total = votes1 + votes2

        if total > 0:
            percent1 = (votes1 / total) * 100
            percent2 = (votes2 / total) * 100

            st.markdown(f"""
                <div>
                    <div style="display:flex; justify-content:space-between;">
                        <span><strong>{meme1.get('title', 'Мем #1')}</strong> {votes1} голосов</span>
                        <span><strong>{meme2.get('title', 'Мем #2')}</strong> {votes2} голосов</span>
                    </div>
                    <div class="vote-bar">
                        <div class="vote-fill" style="width: {percent1}%;"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:14px; color:#666;">
                        <span>{percent1:.0f}%</span>
                        <span>{percent2:.0f}%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if votes1 > votes2:
                st.success(f"🏆 Лидирует: {meme1.get('title')}!")
            elif votes2 > votes1:
                st.success(f"🏆 Лидирует: {meme2.get('title')}!")
            else:
                st.info("⚖️ Ничья!")
        else:
            st.info("🤔 Пока никто не проголосовал. Будь первым!")
    else:
        st.info("📝 Добавьте мемы через админ-панель, чтобы начать битву!")


if __name__ == "__main__":
    show()