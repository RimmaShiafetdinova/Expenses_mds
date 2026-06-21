from datetime import date
from typing import Optional

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from . import models, schemas


def create_transaction(db: Session, data: schemas.TransactionCreate) -> models.Transaction:
    transaction = models.Transaction(**data.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transactions(
    db: Session,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> list[models.Transaction]:
    query = db.query(models.Transaction)
    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if start:
        query = query.filter(models.Transaction.spent_on >= start)
    if end:
        query = query.filter(models.Transaction.spent_on <= end)
    return query.order_by(models.Transaction.spent_on.desc()).all()


def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transaction]:
    return db.get(models.Transaction, transaction_id)


def delete_transaction(db: Session, transaction_id: int) -> bool:
    transaction = db.get(models.Transaction, transaction_id)
    if transaction is None:
        return False
    db.delete(transaction)
    db.commit()
    return True


def get_summary(db: Session) -> schemas.Summary:
    income = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
        .filter(models.Transaction.type == "income")
        .scalar()
    )
    expense = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
        .filter(models.Transaction.type == "expense")
        .scalar()
    )

    rows = (
        db.query(
            models.Transaction.category,
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(models.Transaction.type == "expense")
        .group_by(models.Transaction.category)
        .order_by(func.sum(models.Transaction.amount).desc())
        .all()
    )
    by_category = [schemas.CategorySummary(category=c, total=t) for c, t in rows]

    return schemas.Summary(
        total_income=round(income, 2),
        total_expense=round(expense, 2),
        balance=round(income - expense, 2),
        by_category=by_category,
    )


def get_categories(db: Session) -> list[str]:
    rows = db.query(models.Transaction.category).distinct().all()
    return sorted(row[0] for row in rows)


def get_monthly(db: Session) -> list[schemas.MonthlyPoint]:
    month = func.strftime("%Y-%m", models.Transaction.spent_on)
    rows = (
        db.query(
            month.label("month"),
            func.sum(
                case((models.Transaction.type == "income", models.Transaction.amount), else_=0.0)
            ).label("income"),
            func.sum(
                case((models.Transaction.type == "expense", models.Transaction.amount), else_=0.0)
            ).label("expense"),
        )
        .group_by(month)
        .order_by(month)
        .all()
    )
    return [
        schemas.MonthlyPoint(month=m, income=round(i, 2), expense=round(e, 2))
        for m, i, e in rows
    ]
