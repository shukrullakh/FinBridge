from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DecisionOutcome(str, Enum):
    POSTPONED = "postponed"
    CANCELLED = "cancelled"
    PROCEEDED = "proceeded"


class SmartPauseEvaluateRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Proposed purchase amount in UZS")
    category: str
    description: Optional[str] = None


class SmartPauseEvaluateResponse(BaseModel):
    is_risky: bool
    risk_level: str
    reasons: List[str]
    category: str
    amount: Decimal
    category_limit: Optional[Decimal] = None
    current_category_spent: Decimal
    projected_category_spent: Decimal
    current_balance: Decimal
    projected_balance: Decimal
    cooling_off_minutes: int = 15
    reflection_prompts: List[str]
    impact_summary: str


class PurchaseDecisionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category: str
    description: Optional[str] = None
    risk_level: str
    decision: DecisionOutcome
    cooling_off_taken: bool = True
    notes: Optional[str] = None


class PurchaseDecision(PurchaseDecisionCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
