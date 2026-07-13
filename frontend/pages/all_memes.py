import streamlit as st
from api.client import get_all_memes

st.set_page_config(page_title="Все мемы", page_icon="🖼️", layout="wide")
st.header("🖼️ Все мемы")

try:
    response = get_all_memes()
    if response and response.ok:
        memes = response.json()
        if isinstance(memes, list) and memes:
            for meme in memes:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(meme.get('image_url', 'https://via.placeholder.com/150'), use_container_width=True)
                    with col2:
                        st.subheader(meme.get('title', 'Мем'))
                        st.caption(meme.get('description', ''))
                        st.write(f"❤️ {meme.get('votes', 0)} голосов")
                st.divider()
        else:
            st.info("📝 Нет мемов для отображения")
    else:
        st.error("❌ Не удалось загрузить мемы")
except:
    st.error("❌ Ошибка загрузки")