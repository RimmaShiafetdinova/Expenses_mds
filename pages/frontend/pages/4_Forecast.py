import streamlit as st

from common import api_get, require_api

st.title("Прогноз (ML)")

require_api()

st.write(
    "Модель линейной регрессии анализирует расходы по месяцам и "
    "предсказывает сумму на следующий месяц."
)

forecast = api_get("/ml/forecast")
st.metric("Прогноз расходов", f"{forecast['next_month_expense']:.2f} ₽")
st.caption(f"Учтено месяцев: {forecast['based_on_months']}")
st.info(forecast["message"])
