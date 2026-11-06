from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SavingsGoalBase(BaseModel):
    name: str
    target_amount: Decimal = Field(..., gt=0, description="Target amount in UZS")
    round_up_step: Decimal = Field(default=Decimal("5000"), description="Round up step (1000, 5000, 10000 UZS)")
    target_date: Optional[date] = None


class SavingsGoalCreate(SavingsGoalBase):
    initial_deposit: Optional[Decimal] = Decimal("0")


class SavingsGoal(SavingsGoalBase):
    id: str
    current_amount: Decimal = Decimal("0")
    total_saved_from_roundups: Decimal = Decimal("0")
    progress_percentage: float = 0.0
    is_achieved: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)


class RoundUpCalculation(BaseModel):
    original_amount: Decimal
    rounded_amount: Decimal
    saved_amount: Decimal
    step: Decimal
    is_applicable: bool


class SimulatedContribution(BaseModel):
    id: str
    goal_id: str
    transaction_id: Optional[str] = None
    original_amount: Decimal
    round_up_amount: Decimal
    created_at: datetime = Field(default_factory=datetime.now)
