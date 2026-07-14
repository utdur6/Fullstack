import streamlit as st
from api.client import get_all_memes


def show():
    st.header("🏆 Топ мемов")

    try:
        response = get_all_memes()
        if response and response.ok:
            all_memes = response.json()
            if isinstance(all_memes, list) and all_memes:
                sorted_memes = sorted(all_memes, key=lambda x: x.get('votes', 0), reverse=True)
                for i, meme in enumerate(sorted_memes, 1):
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                    with col1:
                        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                        st.write(f"### {medal}")
                    with col2:
                        st.write(f"**{meme.get('title', 'Мем')}**")
                    with col3:
                        st.write(f"❤️ {meme.get('votes', 0)} голосов")
                    with col4:
                        max_votes = sorted_memes[0].get('votes', 1) if sorted_memes else 1
                        progress = min(meme.get('votes', 0) / max_votes, 1.0)
                        st.progress(progress)
                    st.divider()
            else:
                st.info("📝 Нет мемов для отображения")
        else:
            st.error("❌ Не удалось загрузить мемы")
    except:
        st.error("❌ Ошибка загрузки")


if __name__ == "__main__":
    show()