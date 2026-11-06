from sqlalchemy import Column, String, Numeric
from app.core.database import Base


class DebtModel(Base):
    __tablename__ = "debts"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), default=0, nullable=False)
    minimum_payment = Column(Numeric(15, 2), nullable=False)
    due_date = Column(String(10), default="15", nullable=False)
    type = Column(String(50), default="installment", nullable=False)
    notes = Column(String(255), nullable=True)
