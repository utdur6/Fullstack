import streamlit as st


def render_header():
    """Красивый хедер с навигацией"""

    # Стили для хедера
    st.markdown("""
        <style>
        .custom-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .custom-header .logo {
            color: white;
            font-size: 1.8rem;
            font-weight: bold;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }
        .custom-header .logo:hover {
            transform: scale(1.05);
            transition: 0.3s;
        }
        .custom-header .nav-menu {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .custom-header .nav-item {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 25px;
            transition: all 0.3s;
            font-size: 1rem;
            cursor: pointer;
            background: rgba(255,255,255,0.1);
            border: none;
        }
        .custom-header .nav-item:hover {
            background: rgba(255,255,255,0.25);
            color: white;
            transform: translateY(-2px);
        }
        .custom-header .nav-item.active {
            background: white;
            color: #667eea;
            font-weight: bold;
        }
        .custom-header .user-info {
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255,255,255,0.15);
            padding: 8px 16px;
            border-radius: 25px;
        }
        @media (max-width: 768px) {
            .custom-header {
                flex-direction: column;
                gap: 10px;
                padding: 1rem;
            }
            .custom-header .nav-menu {
                flex-wrap: wrap;
                justify-content: center;
            }
            .custom-header .nav-item {
                font-size: 0.9rem;
                padding: 6px 12px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Данные пользователя
    user_name = "Гость"
    if 'user' in st.session_state and st.session_state.user:
        user_name = st.session_state.user.get('username', 'Гость')

    # Определяем активную страницу
    current_page = st.session_state.get('page', 'home')

    # Создаем хедер
    header_html = f"""
        <div class="custom-header">
            <div class="logo" onclick="window.location.href='?page=home'">
                ⚔️ Meme Battle
            </div>
            <div class="nav-menu">
                <button class="nav-item {'active' if current_page == 'home' else ''}" 
                        onclick="window.location.href='?page=home'">
                    🏠 Главная
                </button>
                <button class="nav-item {'active' if current_page == 'memes' else ''}"
                        onclick="window.location.href='?page=memes'">
                    🎭 Мемы
                </button>
                <button class="nav-item {'active' if current_page == 'tags' else ''}"
                        onclick="window.location.href='?page=tags'">
                    🏷️ Теги
                </button>
                <button class="nav-item {'active' if current_page == 'top' else ''}"
                        onclick="window.location.href='?page=top'">
                    🏆 Топ
                </button>
                <div class="user-info">
                    👤 {user_name}
                </div>
            </div>
        </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)