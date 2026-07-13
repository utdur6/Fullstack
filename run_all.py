import subprocess
import sys
import os
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Проверяем, где лежит Streamlit
POSSIBLE_STREAMLIT_DIRS = [
    os.path.join(PROJECT_ROOT, "frontend", "streamlit"),
    os.path.join(PROJECT_ROOT, "frontend"),
    os.path.join(PROJECT_ROOT, "streamlit"),
]

STREAMLIT_DIR = None
for dir_path in POSSIBLE_STREAMLIT_DIRS:
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        # Проверяем, есть ли в папке app.py
        if os.path.exists(os.path.join(dir_path, "app.py")):
            STREAMLIT_DIR = dir_path
            break

if STREAMLIT_DIR is None:
    print("❌ Не найдена папка с Streamlit-приложением!")
    print("Искал в:", POSSIBLE_STREAMLIT_DIRS)
    sys.exit(1)

print(f"✅ Найден Streamlit в: {STREAMLIT_DIR}")


def run_backend():
    """Запуск бэкенда"""
    os.chdir(PROJECT_ROOT)
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    return subprocess.Popen(cmd, shell=True)


def run_frontend():
    """Запуск фронтенда"""
    os.chdir(STREAMLIT_DIR)
    cmd = [
        sys.executable, "-m", "streamlit",
        "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ]
    return subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ЗАПУСК MEME BATTLE")
    print("=" * 50)

    print(f"\n📂 Папка проекта: {PROJECT_ROOT}")
    print(f"📂 Папка фронтенда: {STREAMLIT_DIR}")

    print("\n📦 Запуск бэкенда (FastAPI)...")
    backend = run_backend()
    time.sleep(2)

    print("📦 Запуск фронтенда (Streamlit)...")
    frontend = run_frontend()

    print("\n" + "=" * 50)
    print("✅ СЕРВИСЫ ЗАПУЩЕНЫ!")
    print("=" * 50)
    print(f"   🔹 Бэкенд:  http://127.0.0.1:8000")
    print(f"   🔹 Документация API: http://127.0.0.1:8000/docs")
    print(f"   🔹 Фронтенд: http://localhost:8501")
    print("=" * 50)
    print("\n📝 Нажмите Ctrl+C для остановки...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка сервисов...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("✅ Сервисы остановлены")