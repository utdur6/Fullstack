"""
Страница регистрации
"""

import requests
import streamlit as st
from api.client import register, get_error_message

st.set_page_config(
    page_title="Регистрация | Meme Battle",
    page_icon="📝",
    layout="centered"
)

st.header("📝 Регистрация")

with st.form("registration_form"):
    username = st.text_input("👤 Имя пользователя")
    email = st.text_input("📧 Email", placeholder="user@example.com")
    password = st.text_input("🔒 Пароль", type="password")
    submitted = st.form_submit_button("Зарегистрироваться", use_container_width=True)

if submitted:
    if not username.strip() or not email.strip() or not password:
        st.error("❌ Заполните все поля.")
        st.stop()

    try:
        response = register(email.strip(), password, username.strip())
    except requests.RequestException:
        st.error("❌ Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("✅ Регистрация выполнена! Теперь войдите.")
        st.switch_page("pages/login.py")
    else:
        st.error(get_error_message(response))

st.divider()
st.page_link("pages/login.py", label="🔑 Уже есть аккаунт? Войти")