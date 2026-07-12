import streamlit as st
from core import api


def render_sidebar():
    """Рендеринг боковой панели"""
    with st.sidebar:
        st.title("⚔️ Meme Battle")
        st.markdown("---")

        # Меню
        st.subheader("📋 Меню")
        if st.button("🏠 Главная", use_container_width=True):
            st.switch_page("app.py")
        if st.button("🖼️ Мемы", use_container_width=True):
            st.switch_page("pages/Mem.py")
        if st.button("🏷️ Теги", use_container_width=True):
            st.switch_page("pages/Tags.py")
        if st.button("🏆 Топ", use_container_width=True):
            st.switch_page("pages/Top.py")

        st.divider()

        # Информация о пользователе
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if st.session_state.logged_in and st.session_state.get('user'):
            st.subheader("👤 Пользователь")
            user = st.session_state.user
            st.write(f"👋 {user.get('username', user.get('name', 'Пользователь'))}")
            st.write(f"📧 {user.get('email', '')}")
            if st.button("🚪 Выйти", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
        else:
            st.subheader("🔑 Вход")
            username = st.text_input("Имя пользователя", key="sidebar_username")
            password = st.text_input("Пароль", type="password", key="sidebar_password")
            if st.button("Войти", use_container_width=True):
                if username and password:
                    user = api.login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success("✅ Успешный вход!")
                        st.rerun()
                    else:
                        st.error("❌ Неверный логин или пароль")
                else:
                    st.warning("Заполните все поля")

            if st.button("📝 Регистрация", use_container_width=True):
                st.switch_page("pages/Profile.py")