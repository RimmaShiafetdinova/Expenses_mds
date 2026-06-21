import random
from datetime import date, timedelta

from backend import crud, models, schemas
from backend.database import SessionLocal, engine

EXPENSE_CATEGORIES = {
    "Продукты": (1500, 6000),
    "Кафе и рестораны": (500, 3000),
    "Транспорт": (300, 2000),
    "Жильё": (15000, 25000),
    "Развлечения": (500, 4000),
    "Здоровье": (500, 5000),
    "Одежда": (1000, 8000),
    "Прочее": (200, 2500),
}


def run():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(models.Transaction).count() > 0:
        print("В базе уже есть данные, наполнение пропущено.")
        db.close()
        return

    today = date.today()
    start = today.replace(day=1) - timedelta(days=150)
    rng = random.Random(42)

    current = start
    while current <= today:
        crud.create_transaction(
            db,
            schemas.TransactionCreate(
                type="income",
                category="Зарплата",
                amount=float(rng.randint(60000, 80000)),
                description="Месячная зарплата",
                spent_on=current.replace(day=5),
            ),
        )

        for _ in range(rng.randint(12, 20)):
            category = rng.choice(list(EXPENSE_CATEGORIES))
            low, high = EXPENSE_CATEGORIES[category]
            day = rng.randint(1, 28)
            crud.create_transaction(
                db,
                schemas.TransactionCreate(
                    type="expense",
                    category=category,
                    amount=float(rng.randint(low, high)),
                    description="",
                    spent_on=current.replace(day=day),
                ),
            )

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    count = db.query(models.Transaction).count()
    db.close()
    print(f"Готово. Добавлено операций: {count}")


if __name__ == "__main__":
    run()
