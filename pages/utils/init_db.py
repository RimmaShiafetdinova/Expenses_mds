"""Создаёт таблицы в SQLite-базе (data/expenses.db)."""
import sys
from pathlib import Path

# чтобы скрипт запускался как `python utils/init_db.py` из корня проекта
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database import Base, engine
from backend import models  # noqa: F401  (регистрирует таблицы в metadata)

Base.metadata.create_all(bind=engine)
print("База данных инициализирована: data/expenses.db")
