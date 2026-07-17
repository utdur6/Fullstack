import streamlit as st
import requests
from frontend.api.client import create_meme, get_error_message, get_all_tags
from frontend.auth.state import require_login, is_admin


def show():
    require_login()

    if not is_admin():
        st.error("⛔ Только администратор может добавлять мемы!")
        return

    st.header("➕ Добавить новый мем")

    # Загружаем теги для выбора
    try:
        response = get_all_tags()
        if response and response.ok:
            tags = response.json()
            tag_options = {tag['name']: tag['id'] for tag in tags}
        else:
            tag_options = {"Без тега": 1}
    except:
        tag_options = {"Без тега": 1}

    with st.form("create_meme_form"):
        title = st.text_input("Название мема", placeholder="Введите название")
        description = st.text_area("Описание", placeholder="Краткое описание мема")
        image_url = st.text_input("Ссылка на изображение", placeholder="https://example.com/meme.jpg")
        tag_name = st.selectbox("Тег", options=list(tag_options.keys()))
        submitted = st.form_submit_button("Создать мем", use_container_width=True, type="primary")

    if submitted:
        if not title.strip():
            st.error("❌ Название обязательно!")
            return

        if not image_url.strip():
            st.error("❌ Ссылка на изображение обязательна!")
            return

        tag_id = tag_options.get(tag_name, 1)
        payload = {
            "title": title.strip(),
            "description": description.strip(),
            "image_url": image_url.strip(),
            "tag_id": tag_id
        }

        try:
            response = create_meme(payload)
            if response and response.ok:
                st.success("✅ Мем успешно создан!")
                st.balloons()
                st.session_state.page = "catalog"
                st.rerun()
            else:
                st.error(f"❌ Ошибка: {get_error_message(response)}")
        except requests.RequestException:
            st.error("❌ Не удалось подключиться к бэкенду")


if __name__ == "__main__":
    show()