from decimal import Decimal
import uuid
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import BudgetModel, TransactionModel
from app.schemas.budget import BudgetLimit, BudgetLimitCreate

router = APIRouter()


@router.get("", response_model=List[BudgetLimit])
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(BudgetModel).all()
    transactions = db.query(TransactionModel).filter(TransactionModel.type == "expense").all()

    # Calculate spent amounts dynamically
    cat_spent = {}
    for t in transactions:
        amt = Decimal(str(t.amount))
        cat_spent[t.category.lower()] = cat_spent.get(t.category.lower(), Decimal("0")) + amt

    result = []
    for b in budgets:
        limit_amt = Decimal(str(b.limit_amount))
        spent = cat_spent.get(b.category.lower(), Decimal("0"))
        remaining = max(Decimal("0"), limit_amt - spent)
        usage_pct = float((spent / limit_amt * 100)) if limit_amt > 0 else 0.0
        is_exceeded = spent > limit_amt

        result.append(BudgetLimit(
            id=b.id,
            category=b.category,
            limit_amount=limit_amt,
            period=b.period,
            spent_amount=spent,
            remaining_amount=remaining,
            usage_percentage=round(usage_pct, 1),
            is_exceeded=is_exceeded
        ))
    return result


@router.post("", response_model=BudgetLimit)
def create_or_update_budget(payload: BudgetLimitCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(BudgetModel)
        .filter(func.lower(BudgetModel.category) == payload.category.lower())
        .first()
    )
    if existing:
        existing.limit_amount = payload.limit_amount
        existing.period = payload.period
        db.commit()
        db.refresh(existing)
        return BudgetLimit(
            id=existing.id,
            category=existing.category,
            limit_amount=Decimal(str(existing.limit_amount)),
            period=existing.period
        )

    new_id = str(uuid.uuid4())
    new_budget = BudgetModel(
        id=new_id,
        category=payload.category,
        limit_amount=payload.limit_amount,
        period=payload.period
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return BudgetLimit(
        id=new_budget.id,
        category=new_budget.category,
        limit_amount=Decimal(str(new_budget.limit_amount)),
        period=new_budget.period
    )
