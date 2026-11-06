from decimal import Decimal
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import DebtModel
from app.schemas.debt import Debt, DebtCreate, DebtPlanResponse, DebtType
from app.services.debt_service import DebtService

router = APIRouter()


@router.get("", response_model=List[Debt])
def get_debts(db: Session = Depends(get_db)):
    debts = db.query(DebtModel).all()
    return [
        Debt(
            id=d.id,
            name=d.name,
            balance=Decimal(str(d.balance)),
            interest_rate=Decimal(str(d.interest_rate)),
            minimum_payment=Decimal(str(d.minimum_payment)),
            due_date=d.due_date,
            type=DebtType(d.type),
            notes=d.notes
        )
        for d in debts
    ]


@router.post("", response_model=Debt)
def add_debt(payload: DebtCreate, db: Session = Depends(get_db)):
    new_debt = DebtModel(
        id=str(uuid.uuid4()),
        name=payload.name,
        balance=payload.balance,
        interest_rate=payload.interest_rate or Decimal("0"),
        minimum_payment=payload.minimum_payment,
        due_date=payload.due_date,
        type=payload.type.value,
        notes=payload.notes
    )
    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)

    return Debt(
        id=new_debt.id,
        name=new_debt.name,
        balance=Decimal(str(new_debt.balance)),
        interest_rate=Decimal(str(new_debt.interest_rate)),
        minimum_payment=Decimal(str(new_debt.minimum_payment)),
        due_date=new_debt.due_date,
        type=DebtType(new_debt.type),
        notes=new_debt.notes
    )


@router.delete("/{debt_id}")
def delete_debt(debt_id: str, db: Session = Depends(get_db)):
    debt = db.query(DebtModel).filter(DebtModel.id == debt_id).first()
    if not debt:
        raise HTTPException(status_code=404, detail="Qarz topilmadi")
    db.delete(debt)
    db.commit()
    return {"message": "Qarz o'chirildi", "id": debt_id}


@router.post("/plan", response_model=DebtPlanResponse)
def calculate_repayment_plan(
    extra_monthly_budget: Decimal = Query(
        Decimal("500000"),
        ge=0,
        description="Extra monthly budget to accelerate repayment (UZS)"
    ),
    db: Session = Depends(get_db)
):
    debt_models = db.query(DebtModel).all()
    if not debt_models:
        raise HTTPException(status_code=400, detail="Qarzlar mavjud emas")

    debts_schema = [
        Debt(
            id=d.id,
            name=d.name,
            balance=Decimal(str(d.balance)),
            interest_rate=Decimal(str(d.interest_rate)),
            minimum_payment=Decimal(str(d.minimum_payment)),
            due_date=d.due_date,
            type=DebtType(d.type),
            notes=d.notes
        )
        for d in debt_models
    ]

    return DebtService.calculate_strategies(
        debts=debts_schema,
        extra_monthly_budget=extra_monthly_budget
    )
