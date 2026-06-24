# Трекер личных расходов 

ML-сервис на **Streamlit** с эндпоинтами на **FastAPI** и связью с БД (SQLite).

## Структура

```text
pages/
├── backend/
│   ├── api.py              # приложение FastAPI и эндпоинты
│   ├── database.py         # подключение к SQLite
│   ├── models.py           # модели SQLAlchemy
│   ├── schemas.py          # схемы данных Pydantic
│   ├── crud.py             # операции с базой данных
│   └── ml/
│       └── forecast.py     # прогноз расходов (линейная регрессия)
│
├── frontend/
│   ├── Main.py             # главная страница Streamlit
│   ├── common.py           # HTTP-клиент для API
│   └── pages/
│       ├── 2_Data.py       # добавление операции
│       ├── 3_Transactions.py
│       └── 4_Forecast.py
│
├── utils/
│   └── init_db.py          # создание таблиц
│
├── data/
│   ├── expenses.db
│
├── seed_data.py            # заполнение тестовыми данными
├── requirements.txt
├── README.md
└── .gitignore
```

## Запуск (из папки проекта)

* > python utils/init_db.py        # (необязательно) создать БД
* > python seed_data.py            # (необязательно) тестовые данные
* > uvicorn backend.api:app --reload
* > streamlit run frontend/Main.py

Смотрим:
* > http://localhost:8501/
* > http://localhost:8000/docs
