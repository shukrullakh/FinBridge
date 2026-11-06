from decimal import Decimal
from typing import List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import TransactionModel, BudgetModel, SavingsGoalModel, DebtModel
from app.schemas.dashboard import DashboardSummary, CategorySpending, UpcomingDebtPayment
from app.schemas.savings import SavingsGoal
from app.services.score_service import ScoreService
from app.data.seed import seed_initial_data

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Returns comprehensive dashboard summary calculated deterministically from database."""
    transactions = db.query(TransactionModel).all()
    budgets = db.query(BudgetModel).all()
    savings_goals = db.query(SavingsGoalModel).all()
    debts = db.query(DebtModel).all()

    total_income = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "income"),
        Decimal("0")
    )
    total_expenses = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "expense"),
        Decimal("0")
    )
    net_balance = total_income - total_expenses

    # Categories breakdown
    cat_totals: Dict[str, Decimal] = {}
    for t in transactions:
        if t.type == "expense":
            amt = Decimal(str(t.amount))
            cat_totals[t.category] = cat_totals.get(t.category, Decimal("0")) + amt

    budget_limits_map = {b.category: Decimal(str(b.limit_amount)) for b in budgets}
    
    categories_breakdown: List[CategorySpending] = []
    for cat, amount in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = float((amount / total_expenses * 100)) if total_expenses > 0 else 0.0
        limit = budget_limits_map.get(cat)
        is_over = bool(limit and amount > limit)
        categories_breakdown.append(CategorySpending(
            category=cat,
            total_amount=amount,
            percentage=round(percentage, 1),
            limit_amount=limit,
            is_over_limit=is_over
        ))

    # Savings metrics
    total_simulated_savings = sum(
        (Decimal(str(g.total_saved_from_roundups)) for g in savings_goals),
        Decimal("0")
    )
    total_savings_target = sum((Decimal(str(g.target_amount)) for g in savings_goals), Decimal("0"))
    total_current_saved = sum((Decimal(str(g.current_amount)) for g in savings_goals), Decimal("0"))

    savings_rate_pct = float((total_current_saved / total_income * 100)) if total_income > 0 else 0.0

    # Debt metrics
    total_debt_balance = sum((Decimal(str(d.balance)) for d in debts), Decimal("0"))
    total_monthly_debt = sum((Decimal(str(d.minimum_payment)) for d in debts), Decimal("0"))

    upcoming_debts = [
        UpcomingDebtPayment(
            id=d.id,
            name=d.name,
            amount=Decimal(str(d.minimum_payment)),
            due_date=f"Har oyning {d.due_date}-sanasi"
        )
        for d in debts
    ]

    # Calculate behavior score
    over_budget_count = sum(1 for c in categories_breakdown if c.is_over_limit)
    score_res = ScoreService.calculate_score(
        total_income=total_income,
        total_expenses=total_expenses,
        over_budget_count=over_budget_count,
        total_budgets_count=len(budgets),
        total_saved=total_current_saved,
        total_savings_target=total_savings_target,
        total_monthly_debt_payments=total_monthly_debt
    )

    # Convert goals to schema
    active_goals_schema = []
    for g in savings_goals:
        c_amt = Decimal(str(g.current_amount))
        t_amt = Decimal(str(g.target_amount))
        pct = float((c_amt / t_amt * 100)) if t_amt > 0 else 0.0
        active_goals_schema.append(SavingsGoal(
            id=g.id,
            name=g.name,
            target_amount=t_amt,
            current_amount=c_amt,
            total_saved_from_roundups=Decimal(str(g.total_saved_from_roundups)),
            round_up_step=Decimal(str(g.round_up_step)),
            target_date=g.target_date,
            progress_percentage=round(pct, 1),
            is_achieved=g.is_achieved,
            created_at=g.created_at
        ))

    # Recent transactions directly from DB
    recent_txs = (
        db.query(TransactionModel)
        .order_by(TransactionModel.date.desc())
        .limit(6)
        .all()
    )

    return DashboardSummary(
        currency="UZS",
        period="Joriy oy",
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        savings_rate_percentage=round(savings_rate_pct, 1),
        categories_breakdown=categories_breakdown,
        recent_transactions=recent_txs,
        active_goals=active_goals_schema,
        total_simulated_savings=total_simulated_savings,
        total_debt_balance=total_debt_balance,
        upcoming_debts=upcoming_debts,
        current_behavior_score=score_res.total_score,
        score_grade=score_res.grade
    )


@router.post("/reset-demo")
def reset_demo(db: Session = Depends(get_db)):
    """Resets database back to seeded demo data."""
    seed_initial_data(db, force=True)
    return {"message": "Baza muvaffaqiyatli demo holatiga qaytarildi", "success": True}
