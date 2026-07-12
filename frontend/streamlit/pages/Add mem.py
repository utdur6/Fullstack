import streamlit as st
from components.header import render_header
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Добавить мем | Meme Battle",
    page_icon="➕",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()
render_header()

st.title("➕ Добавить новый мем")
st.info("Здесь будет форма добавления мема")