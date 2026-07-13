import streamlit as st


def show():
    st.header("⚔️ Битва мемов")
    st.caption("Голосуй за лучший мем!")

    # Тестовые данные
    if 'meme1' not in st.session_state:
        st.session_state.meme1 = {
            "id": 1,
            "title": "Тестовый мем #1",
            "image_url": "https://via.placeholder.com/400x300/667eea/ffffff?text=Meme+1",
            "votes": 15
        }
        st.session_state.meme2 = {
            "id": 2,
            "title": "Тестовый мем #2",
            "image_url": "https://via.placeholder.com/400x300/764ba2/ffffff?text=Meme+2",
            "votes": 10
        }

    meme1 = st.session_state.meme1
    meme2 = st.session_state.meme2

    col1, col_vs, col2 = st.columns([2, 0.5, 2])

    with col1:
        with st.container(border=True):
            st.image(meme1['image_url'], use_container_width=True)
            st.subheader(meme1['title'])
            st.caption(f"❤️ {meme1['votes']} голосов")
            if st.button("⬆️ Голосовать за #1", key="vote1", use_container_width=True, type="primary"):
                st.success("✅ Голос учтён!")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #FF4500; font-size: 4rem;'>⚡VS⚡</h1>",
                    unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.image(meme2['image_url'], use_container_width=True)
            st.subheader(meme2['title'])
            st.caption(f"❤️ {meme2['votes']} голосов")
            if st.button("⬆️ Голосовать за #2", key="vote2", use_container_width=True, type="primary"):
                st.success("✅ Голос учтён!")

    votes1 = meme1['votes']
    votes2 = meme2['votes']
    total = votes1 + votes2

    if total > 0:
        st.progress(votes1 / total, text=f"📊 {meme1['title']}: {votes1} голосов ({votes1 / total * 100:.0f}%)")

        if votes1 > votes2:
            st.success(f"🏆 Лидирует: {meme1['title']}!")
        elif votes2 > votes1:
            st.success(f"🏆 Лидирует: {meme2['title']}!")
        else:
            st.info("⚖️ Ничья!")


# Для совместимости со старым кодом
if __name__ == "__main__":
    show()