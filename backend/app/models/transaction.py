from sqlalchemy import Column, String, Numeric, DateTime
from datetime import datetime, timezone
from app.core.database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    type = Column(String(20), nullable=False, index=True)  # "income" or "expense"
    category = Column(String(100), nullable=False, index=True)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    note = Column(String(255), nullable=True)
    source = Column(String(100), default="Plastik karta", nullable=True)
