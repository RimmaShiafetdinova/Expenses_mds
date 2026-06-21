from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    type: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=50)
    amount: float = Field(gt=0)
    description: str = Field(default="", max_length=200)
    spent_on: date


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class CategorySummary(BaseModel):
    category: str
    total: float


class Summary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    by_category: list[CategorySummary]


class Forecast(BaseModel):
    next_month_expense: float
    based_on_months: int
    message: str


class MonthlyPoint(BaseModel):
    month: str
    income: float
    expense: float
