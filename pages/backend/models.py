from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Float, Integer, String

from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, default="")
    spent_on = Column(Date, default=date.today, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
