from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from .transaction import Transaction
from .savings import SavingsGoal
from .budget import BudgetLimit


class CategorySpending(BaseModel):
    category: str
    total_amount: Decimal
    percentage: float
    limit_amount: Optional[Decimal] = None
    is_over_limit: bool = False


class UpcomingDebtPayment(BaseModel):
    id: str
    name: str
    amount: Decimal
    due_date: str


class DashboardSummary(BaseModel):
    currency: str = "UZS"
    period: str
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    savings_rate_percentage: float
    categories_breakdown: List[CategorySpending]
    recent_transactions: List[Transaction]
    active_goals: List[SavingsGoal]
    total_simulated_savings: Decimal
    total_debt_balance: Decimal
    upcoming_debts: List[UpcomingDebtPayment]
    current_behavior_score: int
    score_grade: str
