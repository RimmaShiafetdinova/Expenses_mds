import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session

from .. import crud, schemas


def forecast_next_month(db: Session) -> schemas.Forecast:
    monthly = crud.get_monthly(db)
    expenses = [point.expense for point in monthly]

    if len(expenses) < 2:
        average = round(float(np.mean(expenses)), 2) if expenses else 0.0
        return schemas.Forecast(
            next_month_expense=average,
            based_on_months=len(expenses),
            message="Недостаточно данных для модели, показано среднее значение.",
        )

    x = np.arange(len(expenses)).reshape(-1, 1)
    y = np.array(expenses)

    model = LinearRegression()
    model.fit(x, y)

    prediction = model.predict([[len(expenses)]])[0]
    prediction = max(0.0, round(float(prediction), 2))

    return schemas.Forecast(
        next_month_expense=prediction,
        based_on_months=len(expenses),
        message="Прогноз построен линейной регрессией по истории расходов.",
    )
