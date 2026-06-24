import pandas as pd
import plotly.express as px
import streamlit as st

from common import api_get, require_api

st.set_page_config(page_title="Трекер расходов", layout="wide")

st.title("Трекер личных расходов")

require_api()

summary = api_get("/stats/summary")

col1, col2, col3 = st.columns(3)
col1.metric("Доходы", f"{summary['total_income']:.2f} ₽")
col2.metric("Расходы", f"{summary['total_expense']:.2f} ₽")
col3.metric("Баланс", f"{summary['balance']:.2f} ₽")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Расходы по категориям")
    by_category = summary["by_category"]
    if by_category:
        df = pd.DataFrame(by_category)
        fig = px.pie(df, names="category", values="total", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Пока нет расходов для отображения.")

with right:
    st.subheader("Доходы и расходы по месяцам")
    monthly = api_get("/stats/monthly")
    if monthly:
        df = pd.DataFrame(monthly)
        fig = px.bar(
            df,
            x="month",
            y=["income", "expense"],
            barmode="group",
            labels={"value": "Сумма", "month": "Месяц", "variable": "Тип"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Пока нет данных по месяцам.")
