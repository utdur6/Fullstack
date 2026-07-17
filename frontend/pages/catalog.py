import streamlit as st
import random
import requests
from frontend.api.client import get_all_memes, vote_for_meme, get_error_message
from frontend.auth.state import is_authenticated


def show():
    st.header("⚔️ Битва мемов")
    st.caption("Голосуй за лучший мем!")

    # ===== ОТЛАДКА: показываем статус подключения =====
    with st.expander("🔍 Отладка (статус подключения к бэкенду)"):
        try:
            response = requests.get("http://127.0.0.1:8000/memes", timeout=5)
            st.write(f"**Статус:** {response.status_code}")
            if response.ok:
                data = response.json()
                st.success(f"✅ Бэкенд доступен. Найдено мемов: {len(data)}")
                if data:
                    st.write(f"**Первый мем:** {data[0]}")
            else:
                st.error(f"❌ Ошибка: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Не удалось подключиться к бэкенду. Убедитесь, что он запущен на http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"❌ Ошибка: {e}")

    # Инициализация состояния
    if 'meme1' not in st.session_state:
        st.session_state.meme1 = None
    if 'meme2' not in st.session_state:
        st.session_state.meme2 = None

    def load_memes():
        try:
            response = get_all_memes()
            if response is None:
                st.error("❌ Бэкенд не отвечает. Проверьте, запущен ли сервер.")
                return False

            if response.status_code == 404:
                st.error("❌ Эндпоинт /memes не найден. Проверьте бэкенд.")
                return False

            if not response.ok:
                st.error(f"❌ Ошибка бэкенда: {response.status_code}")
                return False

            all_memes = response.json()
            if not isinstance(all_memes, list):
                st.error("❌ Бэкенд вернул неверный формат данных")
                return False

            if len(all_memes) < 2:
                st.warning(f"⚠️ Недостаточно мемов. Найдено: {len(all_memes)}. Нужно минимум 2.")
                return False

            selected = random.sample(all_memes, 2)
            st.session_state.meme1 = selected[0]
            st.session_state.meme2 = selected[1]
            return True

        except requests.exceptions.ConnectionError:
            st.error("❌ Не удалось подключиться к бэкенду. Проверьте, запущен ли сервер.")
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
        col1, col_vs, col2 = st.columns([2, 0.5, 2])

        with col1:
            with st.container(border=True):
                st.image(meme1.get('image_url', 'https://via.placeholder.com/400x300'), use_container_width=True)
                st.subheader(meme1.get('name', 'Мем #1'))
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
                st.subheader(meme2.get('name', 'Мем #2'))
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

        # Шкала голосов
        votes1 = meme1.get('votes', 0)
        votes2 = meme2.get('votes', 0)
        total = votes1 + votes2

        if total > 0:
            percent1 = (votes1 / total) * 100
            st.progress(percent1 / 100, text=f"{meme1.get('name')}: {votes1} голосов ({percent1:.0f}%)")
            if votes1 > votes2:
                st.success(f"🏆 Лидирует: {meme1.get('name')}!")
            elif votes2 > votes1:
                st.success(f"🏆 Лидирует: {meme2.get('name')}!")
            else:
                st.info("⚖️ Ничья!")
        else:
            st.info("🤔 Пока никто не проголосовал. Будь первым!")
    else:
        st.info("📝 Добавьте мемы через админ-панель, чтобы начать битву!")


if __name__ == "__main__":
    show()