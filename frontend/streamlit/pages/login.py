"""
Страница входа
"""

import requests
import streamlit as st
from api.client import login, get_profile, get_error_message
from auth.state import save_auth, clear_auth, is_authenticated

st.set_page_config(
    page_title="Вход | Meme Battle",
    page_icon="🔑",
    layout="centered"
)

st.header("🔑 Вход")

# Если уже авторизован - перенаправляем
if is_authenticated():
    st.info("Вы уже вошли в аккаунт.")
    if st.button("Перейти в профиль"):
        st.switch_page("pages/profile.py")
    st.stop()

with st.form("login_form"):
    email = st.text_input("📧 Email", placeholder="user@example.com")
    password = st.text_input("🔒 Пароль", type="password", placeholder="Введите пароль")
    submitted = st.form_submit_button("Войти", use_container_width=True)

if submitted:
    if not email.strip() or not password:
        st.error("❌ Заполните все поля.")
        st.stop()

    try:
        response = login(email.strip(), password)
    except requests.RequestException:
        st.error("❌ Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if not response.ok:
        st.error(get_error_message(response))
        st.stop()

    access_token = response.json().get("access_token")
    if not access_token:
        st.error("❌ Backend не вернул токен.")
        st.stop()

    # Временно сохраняем токен для запроса профиля
    st.session_state["access_token"] = access_token

    try:
        profile_response = get_profile()
    except requests.RequestException:
        clear_auth()
        st.error("❌ Не удалось получить профиль.")
        st.stop()

    if not profile_response.ok:
        clear_auth()
        st.error(get_error_message(profile_response))
        st.stop()

    # Сохраняем данные авторизации
    save_auth(access_token, profile_response.json())
    st.success("✅ Вход выполнен!")
    st.switch_page("pages/catalog.py")

st.divider()
st.page_link("pages/registration.py", label="📝 Нет аккаунта? Зарегистрироваться")