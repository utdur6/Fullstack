"""
Страница избранного
"""

import streamlit as st
from auth.state import require_login

require_login()

st.set_page_config(
    page_title="Избранное | Meme Battle",
    page_icon="⭐",
    layout="wide"
)

st.header("⭐ Избранное")
st.info("Здесь будут отображаться избранные мемы")