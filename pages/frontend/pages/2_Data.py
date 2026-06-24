from datetime import date

import streamlit as st

from common import CATEGORIES, api_post, require_api

st.title("Добавить операцию")

require_api()

with st.form("add_form", clear_on_submit=True):
    op_type = st.selectbox(
        "Тип", ["expense", "income"],
        format_func=lambda v: "Расход" if v == "expense" else "Доход",
    )
    category = st.selectbox("Категория", CATEGORIES)
    amount = st.number_input("Сумма", min_value=0.01, step=100.0, value=100.0)
    spent_on = st.date_input("Дата", value=date.today())
    description = st.text_input("Описание (необязательно)", max_chars=200)
    submitted = st.form_submit_button("Сохранить")

if submitted:
    payload = {
        "type": op_type,
        "category": category,
        "amount": amount,
        "description": description,
        "spent_on": spent_on.isoformat(),
    }
    api_post("/transactions", payload)
    st.success("Операция сохранена!")
