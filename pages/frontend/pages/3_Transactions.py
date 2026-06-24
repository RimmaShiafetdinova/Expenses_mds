import pandas as pd
import streamlit as st

from common import api_delete, api_get, require_api

st.title("Все операции")

require_api()

col1, col2 = st.columns(2)
type_filter = col1.selectbox(
    "Тип",
    ["Все", "expense", "income"],
    format_func=lambda v: {"Все": "Все", "expense": "Расход", "income": "Доход"}[v],
)
categories = ["Все"] + api_get("/categories")
category_filter = col2.selectbox("Категория", categories)

params = {}
if type_filter != "Все":
    params["type"] = type_filter
if category_filter != "Все":
    params["category"] = category_filter

transactions = api_get("/transactions", params=params)

if not transactions:
    st.info("Операций пока нет.")
else:
    df = pd.DataFrame(transactions)
    df = df[["id", "spent_on", "type", "category", "amount", "description"]]
    df.columns = ["ID", "Дата", "Тип", "Категория", "Сумма", "Описание"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    to_delete = st.number_input("ID операции для удаления", min_value=0, step=1, value=0)
    if st.button("Удалить") and to_delete > 0:
        api_delete(f"/transactions/{int(to_delete)}")
        st.success(f"Операция {int(to_delete)} удалена.")
        st.rerun()
