"""
Управление состоянием авторизации
"""

import streamlit as st

def save_auth(access_token: str, profile: dict) -> None:
    """Сохраняет токен и профиль в session_state"""
    st.session_state["access_token"] = access_token
    st.session_state["profile"] = profile

def clear_auth() -> None:
    """Очищает данные авторизации"""
    st.session_state.pop("access_token", None)
    st.session_state.pop("profile", None)

def is_authenticated() -> bool:
    """Проверяет, авторизован ли пользователь"""
    return bool(st.session_state.get("access_token"))

def current_profile() -> dict | None:
    """Возвращает профиль текущего пользователя"""
    return st.session_state.get("profile")

def is_admin() -> bool:
    """Проверяет, является ли пользователь администратором"""
    profile = current_profile()
    return bool(profile and profile.get("role") == "admin")

def require_login() -> None:
    """Требует авторизации, иначе останавливает выполнение"""
    if is_authenticated():
        return

    st.warning("⚠️ Сначала войдите в аккаунт.")
    if st.button("🔑 Перейти ко входу"):
        st.session_state.page = "login"
        st.rerun()
    st.stop()

def require_admin() -> None:
    """Требует прав администратора"""
    require_login()

    if not is_admin():
        st.error("⛔ Эта страница доступна только администратору.")
        st.stop()