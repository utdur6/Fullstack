import streamlit as st
from api.client import login as api_login, get_profile
from auth.state import save_auth, is_authenticated

def show():
    st.set_page_config(page_title="Вход", page_icon="🔑", layout="centered")
    st.header("🔑 Вход")

    if is_authenticated():
        st.info("Вы уже вошли в аккаунт.")
        if st.button("Перейти в профиль"):
            st.session_state.page = "profile"
            st.rerun()
        return

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Войти")

    if submitted:
        if email and password:
            response = api_login(email, password)
            if response and response.ok:
                data = response.json()
                access_token = data.get("access_token")
                if access_token:
                    st.session_state["access_token"] = access_token
                    profile_response = get_profile()
                    if profile_response and profile_response.ok:
                        save_auth(access_token, profile_response.json())
                        st.success("✅ Вход выполнен!")
                        st.session_state.page = "catalog"
                        st.rerun()
                    else:
                        st.error("❌ Не удалось получить профиль")
                else:
                    st.error("❌ Неверный ответ от сервера")
            else:
                st.error("❌ Неверный логин или пароль")
        else:
            st.warning("Заполните все поля")

if __name__ == "__main__":
    show()