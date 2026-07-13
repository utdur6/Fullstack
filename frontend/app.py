import streamlit as st
from auth.state import is_admin, is_authenticated, current_profile

# Настройка страницы
st.set_page_config(
    page_title="Meme Battle",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== ПОЛНОСТЬЮ СКРЫВАЕМ СИСТЕМНОЕ МЕНЮ ==========
st.markdown("""
    <style>
    /* Скрываем всё системное меню */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    /* Скрываем системный сайдбар */
    .css-1d391kg {display: none !important;}
    .css-1r6slb0 {display: none !important;}
    .st-emotion-cache-1r6slb0 {display: none !important;}
    .st-emotion-cache-1d391kg {display: none !important;}

    /* Скрываем верхнюю панель */
    .st-emotion-cache-6qob1r {display: none !important;}
    .st-emotion-cache-1v0mbdj {display: none !important;}

    /* Скрываем кнопки */
    button[data-testid="baseButton-header"] {display: none !important;}
    button[kind="header"] {display: none !important;}
    .st-emotion-cache-1wivap2 {display: none !important;}

    /* Скрываем навигацию, которую создает st.navigation */
    .st-emotion-cache-1v0mbdj {display: none !important;}
    .st-emotion-cache-1r6slb0 {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}

    /* Убираем отступы */
    .main > div {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Стили для кастомной навигации */
    .nav-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .nav-container .logo {
        color: #e94560;
        font-size: 1.8rem;
        font-weight: bold;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        background: none;
        border: none;
    }
    .nav-container .logo:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
    .nav-container .nav-menu {
        display: flex;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
    }
    .nav-container .nav-item {
        color: rgba(255,255,255,0.7);
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 25px;
        transition: all 0.3s;
        font-size: 0.95rem;
        cursor: pointer;
        background: rgba(255,255,255,0.05);
        border: 1px solid transparent;
    }
    .nav-container .nav-item:hover {
        background: rgba(233, 69, 96, 0.2);
        color: #e94560;
        border-color: #e94560;
        transform: translateY(-2px);
    }
    .nav-container .nav-item.active {
        background: #e94560;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
    }
    .nav-container .user-info {
        color: rgba(255,255,255,0.8);
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255,255,255,0.08);
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    @media (max-width: 768px) {
        .nav-container {
            flex-direction: column;
            align-items: stretch;
            padding: 1rem;
        }
        .nav-container .nav-menu {
            justify-content: center;
        }
        .nav-container .nav-item {
            font-size: 0.85rem;
            padding: 6px 12px;
        }
    }
    </style>
""", unsafe_allow_html=True)


# ========== КАСТОМНАЯ НАВИГАЦИЯ ==========
def render_navigation():
    """Рендерит кастомную навигацию сверху"""

    # Получаем текущую страницу из URL
    current = st.query_params.get('page', 'catalog')

    # Информация о пользователе
    user_name = "Гость"
    if is_authenticated():
        profile = current_profile()
        if profile:
            user_name = profile.get('username', 'Гость')

    # Создаем кнопки навигации
    nav_items = [
        {"id": "catalog", "label": "⚔️ Битва"},
        {"id": "all-memes", "label": "🖼️ Мемы"},
        {"id": "tags", "label": "🏷️ Теги"},
        {"id": "top", "label": "🏆 Топ"},
    ]

    if is_authenticated():
        nav_items.append({"id": "profile", "label": "👤 Профиль"})
        nav_items.append({"id": "favorites", "label": "⭐ Избранное"})
    else:
        nav_items.append({"id": "login", "label": "🔑 Вход"})

    if is_admin():
        nav_items.append({"id": "create-meme", "label": "➕ Добавить"})

    # Создаем HTML для навигации
    nav_html = '<div class="nav-container"><div class="logo" onclick="window.location.href=\'/?page=catalog\'">⚔️ Meme Battle</div><div class="nav-menu">'

    for item in nav_items:
        active_class = 'active' if current == item['id'] else ''
        nav_html += f'<button class="nav-item {active_class}" onclick="window.location.href=\'/?page={item["id"]}\'">{item["label"]}</button>'

    nav_html += f'<div class="user-info">👤 {user_name}</div>'
    nav_html += '</div></div>'

    st.markdown(nav_html, unsafe_allow_html=True)


# ========== ОСНОВНАЯ ЛОГИКА ==========

# Рендерим кастомную навигацию
render_navigation()

# Получаем текущую страницу из URL (по умолчанию catalog)
page = st.query_params.get('page', 'catalog')

# Отображаем нужную страницу
if page == 'catalog':
    # Импортируем и запускаем catalog.py
    from pages import catalog

    catalog.show()

elif page == 'all-memes':
    from pages import all_memes

    all_memes.show()

elif page == 'tags':
    from pages import tags

    tags.show()

elif page == 'top':
    from pages import top

    top.show()

elif page == 'profile':
    from pages import profile

    profile.show()

elif page == 'favorites':
    from pages import favorites

    favorites.show()

elif page == 'login':
    from pages import login

    login.show()

elif page == 'registration':
    from pages import registration

    registration.show()

elif page == 'create-meme':
    from pages import create_meme

    create_meme.show()

elif page == 'edit-meme':
    from pages import edit_meme

    edit_meme.show()

else:
    # Если страница не найдена - перенаправляем на catalog
    st.query_params.page = 'catalog'
    st.rerun()