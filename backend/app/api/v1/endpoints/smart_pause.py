from decimal import Decimal
import uuid
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import TransactionModel, BudgetModel, PurchaseDecisionModel
from app.schemas.smart_pause import (
    SmartPauseEvaluateRequest,
    SmartPauseEvaluateResponse,
    PurchaseDecisionCreate,
    PurchaseDecision
)
from app.services.smart_pause_service import SmartPauseService

router = APIRouter()


@router.post("/evaluate", response_model=SmartPauseEvaluateResponse)
def evaluate_purchase(payload: SmartPauseEvaluateRequest, db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).all()

    # Calculate current balance from DB
    total_income = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "income"),
        Decimal("0")
    )
    total_expenses = sum(
        (Decimal(str(t.amount)) for t in transactions if t.type == "expense"),
        Decimal("0")
    )
    current_balance = total_income - total_expenses

    # Calculate current category spent from DB
    current_category_spent = sum(
        (
            Decimal(str(t.amount))
            for t in transactions
            if t.type == "expense" and t.category.lower() == payload.category.lower()
        ),
        Decimal("0")
    )

    # Find category limit from DB
    budget = (
        db.query(BudgetModel)
        .filter(func.lower(BudgetModel.category) == payload.category.lower())
        .first()
    )
    category_limit = Decimal(str(budget.limit_amount)) if budget else None

    return SmartPauseService.evaluate_purchase(
        request=payload,
        current_balance=current_balance,
        current_category_spent=current_category_spent,
        category_limit=category_limit
    )


@router.post("/decisions", response_model=PurchaseDecision)
def record_decision(payload: PurchaseDecisionCreate, db: Session = Depends(get_db)):
    decision_model = PurchaseDecisionModel(
        id=str(uuid.uuid4()),
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        risk_level=payload.risk_level,
        decision=payload.decision.value,
        cooling_off_taken=payload.cooling_off_taken,
        notes=payload.notes
    )
    db.add(decision_model)
    db.commit()
    db.refresh(decision_model)

    return PurchaseDecision(
        id=decision_model.id,
        amount=Decimal(str(decision_model.amount)),
        category=decision_model.category,
        description=decision_model.description,
        risk_level=decision_model.risk_level,
        decision=decision_model.decision,
        cooling_off_taken=decision_model.cooling_off_taken,
        notes=decision_model.notes,
        created_at=decision_model.created_at
    )


@router.get("/decisions", response_model=List[PurchaseDecision])
def get_decisions(db: Session = Depends(get_db)):
    decisions = db.query(PurchaseDecisionModel).order_by(PurchaseDecisionModel.created_at.desc()).all()
    return [
        PurchaseDecision(
            id=d.id,
            amount=Decimal(str(d.amount)),
            category=d.category,
            description=d.description,
            risk_level=d.risk_level,
            decision=d.decision,
            cooling_off_taken=d.cooling_off_taken,
            notes=d.notes,
            created_at=d.created_at
        )
        for d in decisions
    ]
