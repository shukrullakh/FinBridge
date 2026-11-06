from decimal import Decimal
from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DebtType(str, Enum):
    BANK_LOAN = "bank_loan"
    INSTALLMENT = "installment"
    PERSONAL = "personal"


class DebtBase(BaseModel):
    name: str
    balance: Decimal = Field(..., gt=0, description="Current balance in UZS")
    interest_rate: Optional[Decimal] = Field(default=Decimal("0"), ge=0, description="Annual interest rate in %")
    minimum_payment: Decimal = Field(..., gt=0, description="Minimum monthly payment in UZS")
    due_date: Optional[str] = Field(default="15", description="Due day of month (e.g. 15)")
    type: DebtType = DebtType.INSTALLMENT
    notes: Optional[str] = None


class DebtCreate(DebtBase):
    pass


class Debt(DebtBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


class PayoffPlanItem(BaseModel):
    debt_id: str
    debt_name: str
    balance: Decimal
    interest_rate: Decimal
    minimum_payment: Decimal
    payoff_order: int
    estimated_months_to_payoff: int
    total_interest_estimated: Decimal


class StrategyComparison(BaseModel):
    strategy_name: str
    description: str
    total_months: int
    total_interest_paid: Decimal
    total_amount_paid: Decimal
    order_of_payoff: List[PayoffPlanItem]
    advantages: List[str]


class DebtPlanResponse(BaseModel):
    monthly_budget_allocated: Decimal
    snowball: StrategyComparison
    avalanche: StrategyComparison
    best_strategy_recommendation: str
    summary_insight: str
