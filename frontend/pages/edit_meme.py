import streamlit as st
from auth.state import require_login

def show():
    require_login()
    st.header("✏️ Редактировать мем")
    st.info("📝 Форма редактирования мема в разработке")

if __name__ == "__main__":
    show()