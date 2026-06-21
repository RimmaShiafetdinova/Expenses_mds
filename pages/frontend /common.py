"""Общие настройки и HTTP-клиент для всех страниц Streamlit."""
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

CATEGORIES = [
    "Продукты",
    "Кафе и рестораны",
    "Транспорт",
    "Жильё",
    "Развлечения",
    "Здоровье",
    "Одежда",
    "Зарплата",
    "Подработка",
    "Прочее",
]


def api_get(path, params=None):
    response = requests.get(f"{API_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def api_post(path, payload):
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def api_delete(path):
    response = requests.delete(f"{API_URL}{path}", timeout=10)
    response.raise_for_status()


def check_connection():
    try:
        api_get("/")
        return True
    except requests.RequestException:
        return False


def require_api():
    """Останавливает страницу, если бэкенд недоступен."""
    if not check_connection():
        st.error(
            f"Не удаётся подключиться к API ({API_URL}). "
            "Запусти бэкенд командой: uvicorn backend.api:app --reload"
        )
        st.stop()
