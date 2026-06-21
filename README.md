# Трекер личных расходов 

ML-сервис на **Streamlit** с эндпоинтами на **FastAPI** и связью с БД (SQLite).

## Структура

```
.
├── backend/
│   ├── api.py          # приложение FastAPI и эндпоинты
│   ├── database.py     # подключение к SQLite
│   ├── models.py       # таблица transactions (SQLAlchemy)
│   ├── schemas.py      # схемы данных (Pydantic)
│   ├── crud.py         # операции с базой
│   └── ml/
│       └── forecast.py # прогноз расходов (линейная регрессия)
├── frontend/
│   ├── Main.py         # дашборд
│   ├── common.py       # общий HTTP-клиент к API
│   └── pages/
│       ├── 2_Add.py            # добавить операцию
│       ├── 3_Transactions.py   # все операции
│       └── 4_Forecast.py       # прогноз (ML)
├── utils/
│   └── init_db.py      # создание таблиц в data/expenses.db
├── data/               # здесь лежит база expenses.db
├── seed_data.py        # наполнение базы тестовыми данными
└── requirements.txt
```

## Запуск (из папки проекта)

* > python utils/init_db.py        # (необязательно) создать БД
* > python seed_data.py            # (необязательно) тестовые данные
* > uvicorn backend.api:app --reload
* > streamlit run frontend/Main.py

Смотрим:
* > http://localhost:8501/
* > http://localhost:8000/docs
