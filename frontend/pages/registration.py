import streamlit as st
from api.client import register

st.set_page_config(page_title="Регистрация", page_icon="📝", layout="centered")

st.header("📝 Регистрация")

with st.form("registration_form"):
    username = st.text_input("Имя пользователя")
    email = st.text_input("Email", placeholder="user@example.com")
    password = st.text_input("Пароль", type="password")
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if username and email and password:
        response = register(email, password, username)
        if response and response.ok:
            st.success("✅ Регистрация выполнена!")
            st.switch_page("pages/login.py")
        else:
            st.error("❌ Ошибка регистрации")
    else:
        st.warning("Заполните все поля")