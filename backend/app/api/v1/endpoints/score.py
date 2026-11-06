from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import TransactionModel, BudgetModel, SavingsGoalModel, DebtModel
from app.schemas.score import BehaviorScoreResponse
from app.services.score_service import ScoreService

router = APIRouter()


@router.get("/current", response_model=BehaviorScoreResponse)
def get_current_behavior_score(db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).all()
    budgets = db.query(BudgetModel).all()
    goals = db.query(SavingsGoalModel).all()
    debts = db.query(DebtModel).all()

    total_income = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "income"),
        Decimal("0")
    )
    total_expenses = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "expense"),
        Decimal("0")
    )

    # Categories spent vs limit
    cat_spent = {}
    for t in transactions:
        if t.type == "expense":
            amt = Decimal(str(t.amount))
            cat_spent[t.category.lower()] = cat_spent.get(t.category.lower(), Decimal("0")) + amt

    over_budget_count = 0
    for b in budgets:
        spent = cat_spent.get(b.category.lower(), Decimal("0"))
        if spent > Decimal(str(b.limit_amount)):
            over_budget_count += 1

    total_saved = sum((Decimal(str(g.current_amount)) for g in goals), Decimal("0"))
    total_target = sum((Decimal(str(g.target_amount)) for g in goals), Decimal("0"))
    total_monthly_debt = sum((Decimal(str(d.minimum_payment)) for d in debts), Decimal("0"))

    return ScoreService.calculate_score(
        total_income=total_income,
        total_expenses=total_expenses,
        over_budget_count=over_budget_count,
        total_budgets_count=len(budgets),
        total_saved=total_saved,
        total_savings_target=total_target,
        total_monthly_debt_payments=total_monthly_debt
    )
