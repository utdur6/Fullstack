"""
Страница профиля пользователя
"""

import requests
import streamlit as st
from api.client import get_profile, get_error_message
from auth.state import require_login, save_auth, clear_auth, current_profile

st.set_page_config(
    page_title="Профиль | Meme Battle",
    page_icon="👤",
    layout="centered"
)

require_login()

st.header("👤 Профиль")

try:
    response = get_profile()
except requests.RequestException:
    st.error("❌ Не удалось выполнить запрос к бэкенду.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

profile = response.json()
save_auth(st.session_state["access_token"], profile)

st.write(f"**👤 Имя пользователя:** {profile.get('username', 'Не указано')}")
st.write(f"**📧 Email:** {profile.get('email', 'Не указан')}")
st.write(f"**👑 Роль:** {profile.get('role', 'user')}")

st.divider()

if st.button("🚪 Выйти", type="primary", use_container_width=True):
    clear_auth()
    st.success("Вы вышли из системы.")
    st.switch_page("pages/login.py")