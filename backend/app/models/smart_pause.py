from sqlalchemy import Column, String, Numeric, Boolean, DateTime
from datetime import datetime, timezone
from app.core.database import Base


class PurchaseDecisionModel(Base):
    __tablename__ = "purchase_decisions"

    id = Column(String(36), primary_key=True, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    risk_level = Column(String(50), nullable=False)
    decision = Column(String(50), nullable=False)
    cooling_off_taken = Column(Boolean, default=True, nullable=False)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
