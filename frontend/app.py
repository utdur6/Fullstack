import streamlit as st
from auth.state import is_admin, is_authenticated, current_profile

# Настройка страницы
st.set_page_config(
    page_title="Meme Battle",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== СКРЫВАЕМ СИСТЕМНЫЙ САЙДБАР ==========
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .css-1d391kg {display: none !important;}
    .css-1r6slb0 {display: none !important;}
    .st-emotion-cache-1r6slb0 {display: none !important;}
    .st-emotion-cache-1d391kg {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}

    .main > div {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .block-container {
        padding-top: 0rem !important;
    }

    .custom-nav {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 12px 20px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .custom-nav .brand {
        color: #e94560;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .custom-nav .nav-links {
        display: flex;
        gap: 6px;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 8px;
    }
    .custom-nav .user-badge {
        color: rgba(255,255,255,0.8);
        background: rgba(255,255,255,0.08);
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 14px;
        border: 1px solid rgba(255,255,255,0.05);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }
    @media (min-width: 768px) {
        .custom-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .custom-nav .nav-links {
            margin-top: 0;
        }
        .custom-nav .user-badge {
            margin-top: 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ========== НАВИГАЦИЯ ==========

# Определяем текущую страницу
current_page = st.session_state.get('page', 'catalog')

# Список пунктов меню
menu_items = [
    {"id": "catalog", "label": "⚔️ Битва"},
    {"id": "all-memes", "label": "🖼️ Мемы"},
    {"id": "tags", "label": "🏷️ Теги"},
    {"id": "top", "label": "🏆 Топ"},



]

if is_authenticated():
    menu_items.append({"id": "profile", "label": "👤 Профиль"})
    menu_items.append({"id": "favorites", "label": "⭐ Избранное"})
else:

    menu_items.append({"id": "login", "label": "🔑 Вход"})
    menu_items.append({"id": "registration", "label": "📝 Регистрация"})

if is_admin():
    menu_items.append({"id": "create-meme", "label": "➕ Добавить"})

# Информация о пользователе
user_name = "Гость"
if is_authenticated():
    profile = current_profile()
    if profile:
        user_name = profile.get('username', 'Гость')

# Рендерим навигацию
st.markdown('<div class="custom-nav">', unsafe_allow_html=True)
st.markdown(f'<div class="brand">⚔️ Meme Battle</div>', unsafe_allow_html=True)

# Кнопки навигации в ряд
cols = st.columns(len(menu_items) + 1)
for i, item in enumerate(menu_items):
    with cols[i]:
        button_type = "primary" if current_page == item['id'] else "secondary"
        if st.button(item["label"], key=f"nav_{item['id']}", type=button_type, use_container_width=True):
            st.session_state.page = item['id']
            st.rerun()

with cols[-1]:
    st.markdown(
        f'<div style="color: rgba(255,255,255,0.8); background: rgba(255,255,255,0.08); padding: 6px 16px; border-radius: 25px; font-size: 14px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">👤 {user_name}</div>',
        unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========== ОТОБРАЖЕНИЕ СТРАНИЦ ==========

page = st.session_state.get('page', 'catalog')

if page == 'catalog':
    from pages.catalog import show

    show()
elif page == 'all-memes':
    from pages.all_memes import show

    show()
elif page == 'tags':
    from pages.tags import show

    show()
elif page == 'top':
    from pages.top import show

    show()
elif page == 'profile':
    from pages.profile import show

    show()
elif page == 'favorites':
    from pages.favorites import show

    show()
elif page == 'login':
    from pages.login import show

    show()
elif page == 'registration':
    from pages.registration import show

    show()
elif page == 'create-meme':
    from pages.create_meme import show

    show()
elif page == 'edit-meme':
    from pages.edit_meme import show

    show()
else:
    st.session_state.page = 'catalog'
    st.rerun()