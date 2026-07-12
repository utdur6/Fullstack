import subprocess
import sys
import os
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STREAMLIT_DIR = os.path.join(PROJECT_ROOT, "frontend", "streamlit")

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
    print("🚀 Запуск бэкенда...")
    backend = run_backend()
    time.sleep(2)

    print("🚀 Запуск фронтенда...")
    frontend = run_frontend()

    print("\n✅ Сервисы запущены:")
    print("   Бэкенд:  http://127.0.0.1:8000")
    print("   Фронтенд: http://localhost:8501")
    print("\nНажмите Ctrl+C для остановки...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервисов...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("✅ Сервисы остановлены")