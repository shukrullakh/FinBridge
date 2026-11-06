from decimal import Decimal
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import SavingsGoalModel
from app.schemas.savings import (
    SavingsGoal,
    SavingsGoalCreate,
    RoundUpCalculation
)
from app.services.round_up_service import RoundUpService

router = APIRouter()


@router.get("/goals", response_model=List[SavingsGoal])
def get_savings_goals(db: Session = Depends(get_db)):
    goals = db.query(SavingsGoalModel).all()
    results = []
    for g in goals:
        c_amt = Decimal(str(g.current_amount))
        t_amt = Decimal(str(g.target_amount))
        pct = float((c_amt / t_amt * 100)) if t_amt > 0 else 0.0
        results.append(SavingsGoal(
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
    return results


@router.post("/goals", response_model=SavingsGoal)
def create_savings_goal(payload: SavingsGoalCreate, db: Session = Depends(get_db)):
    initial = payload.initial_deposit or Decimal("0")
    pct = float((initial / payload.target_amount * 100)) if payload.target_amount > 0 else 0.0

    new_goal = SavingsGoalModel(
        id=str(uuid.uuid4()),
        name=payload.name,
        target_amount=payload.target_amount,
        current_amount=initial,
        total_saved_from_roundups=Decimal("0"),
        round_up_step=payload.round_up_step,
        target_date=payload.target_date,
        is_achieved=(initial >= payload.target_amount)
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return SavingsGoal(
        id=new_goal.id,
        name=new_goal.name,
        target_amount=Decimal(str(new_goal.target_amount)),
        current_amount=Decimal(str(new_goal.current_amount)),
        total_saved_from_roundups=Decimal(str(new_goal.total_saved_from_roundups)),
        round_up_step=Decimal(str(new_goal.round_up_step)),
        target_date=new_goal.target_date,
        progress_percentage=round(pct, 1),
        is_achieved=new_goal.is_achieved,
        created_at=new_goal.created_at
    )


@router.get("/calculate-roundup", response_model=RoundUpCalculation)
def preview_round_up(
    amount: Decimal = Query(..., gt=0),
    step: Decimal = Query(Decimal("5000"), gt=0)
):
    return RoundUpService.calculate_round_up(amount=amount, step=step)


@router.post("/goals/{goal_id}/contribute", response_model=SavingsGoal)
def contribute_to_goal(goal_id: str, amount: Decimal = Query(..., gt=0), db: Session = Depends(get_db)):
    goal = db.query(SavingsGoalModel).filter(SavingsGoalModel.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Jamg'arma maqsadi topilmadi")

    goal.current_amount += amount
    goal.total_saved_from_roundups += amount
    if goal.current_amount >= goal.target_amount:
        goal.is_achieved = True

    db.commit()
    db.refresh(goal)

    c_amt = Decimal(str(goal.current_amount))
    t_amt = Decimal(str(goal.target_amount))
    pct = float((c_amt / t_amt * 100)) if t_amt > 0 else 0.0

    return SavingsGoal(
        id=goal.id,
        name=goal.name,
        target_amount=t_amt,
        current_amount=c_amt,
        total_saved_from_roundups=Decimal(str(goal.total_saved_from_roundups)),
        round_up_step=Decimal(str(goal.round_up_step)),
        target_date=goal.target_date,
        progress_percentage=round(pct, 1),
        is_achieved=goal.is_achieved,
        created_at=goal.created_at
    )
