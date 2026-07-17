import streamlit as st
from frontend.auth.state import require_login, current_profile, clear_auth


def show():
    require_login()
    st.header("👤 Профиль")

    profile = current_profile()
    if profile:
        st.write(f"**Имя пользователя:** {profile.get('username', 'Не указано')}")
        st.write(f"**Email:** {profile.get('email', 'Не указан')}")
        st.write(f"**Роль:** {profile.get('role', 'user')}")

        if st.button("🚪 Выйти", use_container_width=True, type="primary"):
            clear_auth()
            st.success("Вы вышли из системы")
            st.session_state.page = "login"
            st.rerun()
    else:
        st.warning("Профиль не найден")


if __name__ == "__main__":
    show()