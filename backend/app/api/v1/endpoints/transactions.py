from decimal import Decimal
from datetime import datetime, timezone
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import TransactionModel, SavingsGoalModel
from app.schemas.transaction import (
    Transaction,
    TransactionCreate,
    TransactionType,
    CreateTransactionResponse
)
from app.schemas.savings import RoundUpCalculation
from app.services.round_up_service import RoundUpService

router = APIRouter()


@router.get("", response_model=List[Transaction])
def get_transactions(
    type: Optional[TransactionType] = Query(None, description="Filter by type (income/expense)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(TransactionModel)
    if type:
        query = query.filter(TransactionModel.type == type.value)
    if category:
        query = query.filter(func.lower(TransactionModel.category) == category.lower())
    
    # SQL level deterministic ordering prevents offset-naive vs offset-aware comparisons
    return query.order_by(TransactionModel.date.desc()).all()


@router.post("", response_model=CreateTransactionResponse)
def create_transaction(
    payload: TransactionCreate,
    apply_round_up: bool = Query(True, description="Automatically calculate and apply round-up to first savings goal"),
    db: Session = Depends(get_db)
):
    # Ensure timezone awareness
    tx_date = payload.date
    if tx_date.tzinfo is None:
        tx_date = tx_date.replace(tzinfo=timezone.utc)

    new_id = str(uuid.uuid4())
    transaction = TransactionModel(
        id=new_id,
        amount=payload.amount,
        type=payload.type.value,
        category=payload.category,
        date=tx_date,
        note=payload.note,
        source=payload.source
    )
    db.add(transaction)

    round_up_info = None
    if payload.type == TransactionType.EXPENSE and apply_round_up:
        first_goal = db.query(SavingsGoalModel).first()
        if first_goal:
            calc: RoundUpCalculation = RoundUpService.calculate_round_up(
                amount=payload.amount,
                step=Decimal(str(first_goal.round_up_step))
            )
            if calc.saved_amount > Decimal("0"):
                first_goal.current_amount += calc.saved_amount
                first_goal.total_saved_from_roundups += calc.saved_amount
                if first_goal.current_amount >= first_goal.target_amount:
                    first_goal.is_achieved = True
                round_up_info = {
                    "saved_amount": float(calc.saved_amount),
                    "goal_name": first_goal.name,
                    "rounded_amount": float(calc.rounded_amount)
                }

    db.commit()
    db.refresh(transaction)

    return CreateTransactionResponse(
        transaction=Transaction.model_validate(transaction),
        round_up=round_up_info
    )


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    tx = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Tranzaksiya topilmadi")
    db.delete(tx)
    db.commit()
    return {"message": "Tranzaksiya o'chirildi", "id": transaction_id}
