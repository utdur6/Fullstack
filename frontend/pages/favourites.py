import streamlit as st
from auth.state import require_login

def show():
    require_login()
    st.header("⭐ Избранное")
    st.info("📝 Здесь будут отображаться избранные мемы")

if __name__ == "__main__":
    show()