from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BudgetLimitBase(BaseModel):
    category: str
    limit_amount: Decimal = Field(..., gt=0, description="Monthly spending limit in UZS")
    period: str = "monthly"


class BudgetLimitCreate(BudgetLimitBase):
    pass


class BudgetLimit(BudgetLimitBase):
    id: str
    spent_amount: Decimal = Decimal("0")
    remaining_amount: Decimal = Decimal("0")
    usage_percentage: float = 0.0
    is_exceeded: bool = False

    model_config = ConfigDict(from_attributes=True)
