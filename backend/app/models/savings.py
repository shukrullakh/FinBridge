from sqlalchemy import Column, String, Numeric, Boolean, Date, DateTime
from datetime import datetime, timezone
from app.core.database import Base


class SavingsGoalModel(Base):
    __tablename__ = "savings_goals"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    target_amount = Column(Numeric(15, 2), nullable=False)
    current_amount = Column(Numeric(15, 2), default=0, nullable=False)
    total_saved_from_roundups = Column(Numeric(15, 2), default=0, nullable=False)
    round_up_step = Column(Numeric(15, 2), default=5000, nullable=False)
    target_date = Column(Date, nullable=True)
    is_achieved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SimulatedContributionModel(Base):
    __tablename__ = "simulated_contributions"

    id = Column(String(36), primary_key=True, index=True)
    goal_id = Column(String(36), nullable=False, index=True)
    transaction_id = Column(String(36), nullable=True, index=True)
    original_amount = Column(Numeric(15, 2), nullable=False)
    round_up_amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
