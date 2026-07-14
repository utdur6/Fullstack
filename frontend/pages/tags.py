import streamlit as st
from api.client import get_all_tags, get_memes_by_tag, get_all_memes


def show():
    st.header("🏷️ Поиск по тегам")

    # Загружаем все теги
    try:
        response = get_all_tags()
        if response and response.ok:
            tags = response.json()

            # Показываем теги в виде кнопок
            st.subheader("Выберите тег:")
            cols = st.columns(4)
            for i, tag in enumerate(tags):
                with cols[i % 4]:
                    if st.button(f"{tag['emoji']} {tag['name']}", key=f"tag_{tag['id']}", use_container_width=True):
                        st.session_state.selected_tag = tag['id']
                        st.session_state.selected_tag_name = tag['name']
                        st.rerun()

            st.divider()

            # Показываем мемы по выбранному тегу
            selected_tag_id = st.session_state.get('selected_tag')
            selected_tag_name = st.session_state.get('selected_tag_name', '')

            if selected_tag_id:
                st.subheader(f"Мемы с тегом: {selected_tag_name}")

                try:
                    response = get_memes_by_tag(selected_tag_id)
                    if response and response.ok:
                        memes = response.json()
                        if memes:
                            for meme in memes:
                                with st.container(border=True):
                                    col1, col2 = st.columns([1, 3])
                                    with col1:
                                        st.image(meme.get('image_url', 'https://via.placeholder.com/150'),
                                                 use_container_width=True)
                                    with col2:
                                        st.subheader(meme.get('title', 'Мем'))
                                        st.caption(meme.get('description', ''))
                                        st.write(f"❤️ {meme.get('votes', 0)} голосов")
                                st.divider()
                        else:
                            st.info("Нет мемов с этим тегом")
                    else:
                        st.error("Не удалось загрузить мемы")
                except:
                    st.error("Ошибка загрузки")
            else:
                st.info("👆 Выберите тег, чтобы увидеть мемы")
        else:
            st.error("Не удалось загрузить теги")
    except:
        st.error("Ошибка загрузки тегов")


if __name__ == "__main__":
    show()