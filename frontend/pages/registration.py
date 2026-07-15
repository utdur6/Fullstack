import streamlit as st
from api.client import register

def show():
    st.set_page_config(page_title="Регистрация", page_icon="📝", layout="centered")
    st.header("📝 Регистрация")

    # ИЗМЕНЕНО: уникальный ключ формы
    with st.form("registration_form_unique"):  # ← добавлено _unique
        username = st.text_input("Имя пользователя")
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Зарегистрироваться")

    if submitted:
        if username and email and password:
            response = register(email, password, username)
            if response and response.ok:
                st.success("✅ Регистрация выполнена!")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ Ошибка регистрации")
        else:
            st.warning("Заполните все поля")

def show():
    st.set_page_config(page_title="Регистрация", page_icon="📝", layout="centered")
    st.header("📝 Регистрация")

    with st.form("registration_form"):
        username = st.text_input("Имя пользователя")
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Зарегистрироваться")

    if submitted:
        if username and email and password:
            response = register(email, password)
            if response and response.ok:
                st.success("✅ Регистрация выполнена!")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ Ошибка регистрации")
        else:
            st.warning("Заполните все поля")

if __name__ == "__main__":
    show()