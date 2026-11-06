from sqlalchemy import Column, String, Numeric
from app.core.database import Base


class BudgetModel(Base):
    __tablename__ = "budgets"

    id = Column(String(36), primary_key=True, index=True)
    category = Column(String(100), unique=True, nullable=False, index=True)
    limit_amount = Column(Numeric(15, 2), nullable=False)
    period = Column(String(50), default="monthly", nullable=False)
