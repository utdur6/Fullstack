import streamlit as st
from api.client import register
# ... в начале файла
with st.form("registration_form"):
    # ИСПРАВЛЕНО: full_name вместо username
    full_name = st.text_input("Ваше имя", key="registration_full_name")
    email = st.text_input("Email", key="registration_email")
    password = st.text_input("Пароль", type="password", key="registration_password")
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not full_name.strip() or not email.strip() or not password:
        st.error("Заполните все поля.")
        st.stop()
    try:
        # ИСПРАВЛЕНО: передаем full_name
        response = register(email=email.strip(), password=password, full_name=full_name.strip())
    except requests.RequestException:
        st.error("Backend недоступен.")
        st.stop()
    # ... остальное без изменений
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
            response = register(email, password, username)
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