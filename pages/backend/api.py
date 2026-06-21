from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db
from .ml import forecast as ml

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API", version="1.0.0")


@app.get("/")
def root():
    return {"status": "ok", "service": "expense-tracker"}


@app.post("/transactions", response_model=schemas.Transaction, status_code=201)
def add_transaction(data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, data)


@app.get("/transactions", response_model=list[schemas.Transaction])
def list_transactions(
    type: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    start: Optional[date] = Query(default=None),
    end: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.get_transactions(db, type=type, category=category, start=start, end=end)


@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction


@app.delete("/transactions/{transaction_id}", status_code=204)
def remove_transaction(transaction_id: int, db: Session = Depends(get_db)):
    if not crud.delete_transaction(db, transaction_id):
        raise HTTPException(status_code=404, detail="Транзакция не найдена")


@app.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.get("/stats/summary", response_model=schemas.Summary)
def summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)


@app.get("/stats/monthly", response_model=list[schemas.MonthlyPoint])
def monthly(db: Session = Depends(get_db)):
    return crud.get_monthly(db)


@app.get("/ml/forecast", response_model=schemas.Forecast)
def get_forecast(db: Session = Depends(get_db)):
    return ml.forecast_next_month(db)
