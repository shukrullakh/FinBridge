from decimal import Decimal
from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy.orm import Session
from app.core.database import Base, engine
from app.models import (
    TransactionModel,
    BudgetModel,
    SavingsGoalModel,
    DebtModel,
    PurchaseDecisionModel
)


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_initial_data(db: Session, force: bool = False):
    """Populates the database with realistic Uzbek demo data if empty or forced."""
    if force:
        db.query(TransactionModel).delete()
        db.query(BudgetModel).delete()
        db.query(SavingsGoalModel).delete()
        db.query(DebtModel).delete()
        db.query(PurchaseDecisionModel).delete()
        db.commit()

    # Check if already seeded
    if db.query(TransactionModel).first() is not None:
        return

    now = datetime.now(timezone.utc)

    # 1. Transactions
    transactions = [
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("8500000"),
            type="income",
            category="Maosh",
            date=now - timedelta(days=6),
            note="Asosiy oylik maosh",
            source="Humo / Uzcard"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("1500000"),
            type="income",
            category="Frilans",
            date=now - timedelta(days=2),
            note="Telegram bot loyihasi uchun to'lov",
            source="Bank o'tkazmasi"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("432000"),
            type="expense",
            category="Oziq-ovqat",
            date=now - timedelta(days=5),
            note="Korzinka supermarket xaridi",
            source="Plastik karta"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("46500"),
            type="expense",
            category="Transport",
            date=now - timedelta(days=4),
            note="Yandex Go taksi safari",
            source="Plastik karta"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("185000"),
            type="expense",
            category="Restoran va Kafe",
            date=now - timedelta(days=3),
            note="Do'stlar bilan kechki ovqat",
            source="Plastik karta"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("85000"),
            type="expense",
            category="Aloqa va Internet",
            date=now - timedelta(days=3),
            note="Oylik internet tarifi",
            source="Payme"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("350000"),
            type="expense",
            category="Kommunal",
            date=now - timedelta(days=2),
            note="Elektr va gaz to'lovlari",
            source="Click"
        ),
        TransactionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("650000"),
            type="expense",
            category="Kiyim-kechak",
            date=now - timedelta(days=1),
            note="Terra Pro kiyim xaridi",
            source="Plastik karta"
        ),
    ]
    db.add_all(transactions)

    # 2. Budgets
    budgets = [
        BudgetModel(
            id="b1",
            category="Oziq-ovqat",
            limit_amount=Decimal("2500000"),
            period="monthly"
        ),
        BudgetModel(
            id="b2",
            category="Restoran va Kafe",
            limit_amount=Decimal("1000000"),
            period="monthly"
        ),
        BudgetModel(
            id="b3",
            category="Transport",
            limit_amount=Decimal("600000"),
            period="monthly"
        ),
        BudgetModel(
            id="b4",
            category="Kiyim-kechak",
            limit_amount=Decimal("1200000"),
            period="monthly"
        ),
        BudgetModel(
            id="b5",
            category="Ko'ngilochar",
            limit_amount=Decimal("800000"),
            period="monthly"
        ),
    ]
    db.add_all(budgets)

    # 3. Savings Goals
    savings_goals = [
        SavingsGoalModel(
            id="g1",
            name="MacBook Pro uchun jamg'arma",
            target_amount=Decimal("20000000"),
            current_amount=Decimal("4500000"),
            total_saved_from_roundups=Decimal("420000"),
            round_up_step=Decimal("5000"),
            target_date=(now + timedelta(days=120)).date(),
            is_achieved=False,
            created_at=now - timedelta(days=30)
        ),
        SavingsGoalModel(
            id="g2",
            name="Favqulodda xavfsizlik yostig'i",
            target_amount=Decimal("10000000"),
            current_amount=Decimal("2500000"),
            total_saved_from_roundups=Decimal("180000"),
            round_up_step=Decimal("10000"),
            target_date=(now + timedelta(days=180)).date(),
            is_achieved=False,
            created_at=now - timedelta(days=45)
        )
    ]
    db.add_all(savings_goals)

    # 4. Debts
    debts = [
        DebtModel(
            id="d1",
            name="Do'stim Sanjardan qarz",
            balance=Decimal("1000000"),
            interest_rate=Decimal("0"),
            minimum_payment=Decimal("250000"),
            due_date="25",
            type="personal",
            notes="Foizsiz shaxsiy qarz"
        ),
        DebtModel(
            id="d2",
            name="Uzum Nasiya - Maishiy texnika",
            balance=Decimal("1800000"),
            interest_rate=Decimal("26"),
            minimum_payment=Decimal("450000"),
            due_date="15",
            type="installment",
            notes="Muzlatgich uchun muddatli to'lov"
        ),
        DebtModel(
            id="d3",
            name="Anorbank - iPhone muddatli to'lov",
            balance=Decimal("3200000"),
            interest_rate=Decimal("0"),
            minimum_payment=Decimal("800000"),
            due_date="10",
            type="installment",
            notes="Foizsiz muddatli to'lov aksiyasi"
        ),
        DebtModel(
            id="d4",
            name="Iste'mol krediti (Xalq banki)",
            balance=Decimal("7500000"),
            interest_rate=Decimal("28"),
            minimum_payment=Decimal("950000"),
            due_date="20",
            type="bank_loan",
            notes="Bank orqali olingan mikrokredit"
        )
    ]
    db.add_all(debts)

    # 5. Smart Pause past decision
    decisions = [
        PurchaseDecisionModel(
            id=str(uuid.uuid4()),
            amount=Decimal("850000"),
            category="Ko'ngilochar",
            description="Sony PlayStation yangi o'yini",
            risk_level="high",
            decision="cancelled",
            cooling_off_taken=True,
            notes="15 daqiqa sovutish taymeridan so'ng hissiy xarid ekanligi tushunildi va bekor qilindi.",
            created_at=now - timedelta(days=3)
        )
    ]
    db.add_all(decisions)

    db.commit()
