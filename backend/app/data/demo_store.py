from decimal import Decimal
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional
from app.schemas.transaction import Transaction, TransactionType
from app.schemas.budget import BudgetLimit
from app.schemas.savings import SavingsGoal, SimulatedContribution
from app.schemas.debt import Debt, DebtType
from app.schemas.smart_pause import PurchaseDecision, DecisionOutcome


class DemoStore:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.budgets: List[BudgetLimit] = []
        self.savings_goals: List[SavingsGoal] = []
        self.simulated_contributions: List[SimulatedContribution] = []
        self.debts: List[Debt] = []
        self.decisions: List[PurchaseDecision] = []
        self.reset_to_demo_data()

    def reset_to_demo_data(self):
        """Resets the in-memory store to realistic Uzbek demo dataset."""
        now = datetime.now()

        # 1. Transactions
        self.transactions = [
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("8500000"),
                type=TransactionType.INCOME,
                category="Maosh",
                date=now - timedelta(days=6),
                note="Asosiy oylik maosh",
                source="Humo / Uzcard"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("1500000"),
                type=TransactionType.INCOME,
                category="Frilans",
                date=now - timedelta(days=2),
                note="Telegram bot loyihasi uchun to'lov",
                source="Bank o'tkazmasi"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("432000"),
                type=TransactionType.EXPENSE,
                category="Oziq-ovqat",
                date=now - timedelta(days=5),
                note="Korzinka supermarket xaridi",
                source="Plastik karta"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("46500"),
                type=TransactionType.EXPENSE,
                category="Transport",
                date=now - timedelta(days=4),
                note="Yandex Go taksi safari",
                source="Plastik karta"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("185000"),
                type=TransactionType.EXPENSE,
                category="Restoran va Kafe",
                date=now - timedelta(days=3),
                note="Do'stlar bilan kechki ovqat",
                source="Plastik karta"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("85000"),
                type=TransactionType.EXPENSE,
                category="Aloqa va Internet",
                date=now - timedelta(days=3),
                note="Oylik internet tarifi",
                source="Payme"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("350000"),
                type=TransactionType.EXPENSE,
                category="Kommunal",
                date=now - timedelta(days=2),
                note="Elektr va gaz to'lovlari",
                source="Click"
            ),
            Transaction(
                id=str(uuid.uuid4()),
                amount=Decimal("650000"),
                type=TransactionType.EXPENSE,
                category="Kiyim-kechak",
                date=now - timedelta(days=1),
                note="Terra Pro kiyim xaridi",
                source="Plastik karta"
            ),
        ]

        # 2. Category Budgets ("Red Lines")
        self.budgets = [
            BudgetLimit(
                id="b1",
                category="Oziq-ovqat",
                limit_amount=Decimal("2500000"),
                period="monthly"
            ),
            BudgetLimit(
                id="b2",
                category="Restoran va Kafe",
                limit_amount=Decimal("1000000"),
                period="monthly"
            ),
            BudgetLimit(
                id="b3",
                category="Transport",
                limit_amount=Decimal("600000"),
                period="monthly"
            ),
            BudgetLimit(
                id="b4",
                category="Kiyim-kechak",
                limit_amount=Decimal("1200000"),
                period="monthly"
            ),
            BudgetLimit(
                id="b5",
                category="Ko'ngilochar",
                limit_amount=Decimal("800000"),
                period="monthly"
            )
        ]

        # 3. Savings Goals
        self.savings_goals = [
            SavingsGoal(
                id="g1",
                name="MacBook Pro uchun jamg'arma",
                target_amount=Decimal("20000000"),
                current_amount=Decimal("4500000"),
                total_saved_from_roundups=Decimal("420000"),
                round_up_step=Decimal("5000"),
                target_date=(now + timedelta(days=120)).date(),
                progress_percentage=22.5
            ),
            SavingsGoal(
                id="g2",
                name="Favqulodda xavfsizlik yostig'i",
                target_amount=Decimal("10000000"),
                current_amount=Decimal("2500000"),
                total_saved_from_roundups=Decimal("180000"),
                round_up_step=Decimal("10000"),
                target_date=(now + timedelta(days=180)).date(),
                progress_percentage=25.0
            )
        ]

        # 4. Debts for Debt Coach
        self.debts = [
            Debt(
                id="d1",
                name="Do'stim Sanjardan qarz",
                balance=Decimal("1000000"),
                interest_rate=Decimal("0"),
                minimum_payment=Decimal("250000"),
                due_date="25",
                type=DebtType.PERSONAL,
                notes="Foizsiz shaxsiy qarz"
            ),
            Debt(
                id="d2",
                name="Uzum Nasiya - Maishiy texnika",
                balance=Decimal("1800000"),
                interest_rate=Decimal("26"),
                minimum_payment=Decimal("450000"),
                due_date="15",
                type=DebtType.INSTALLMENT,
                notes="Muzlatgich uchun muddatli to'lov"
            ),
            Debt(
                id="d3",
                name="Anorbank - iPhone muddatli to'lov",
                balance=Decimal("3200000"),
                interest_rate=Decimal("0"),
                minimum_payment=Decimal("800000"),
                due_date="10",
                type=DebtType.INSTALLMENT,
                notes="Foizsiz muddatli to'lov aksiyasi"
            ),
            Debt(
                id="d4",
                name="Iste'mol krediti (Xalq banki)",
                balance=Decimal("7500000"),
                interest_rate=Decimal("28"),
                minimum_payment=Decimal("950000"),
                due_date="20",
                type=DebtType.BANK_LOAN,
                notes="Bank orqali olingan mikrokredit"
            )
        ]

        # 5. Past Smart Pause decisions
        self.decisions = [
            PurchaseDecision(
                id=str(uuid.uuid4()),
                amount=Decimal("850000"),
                category="Ko'ngilochar",
                description="Sony PlayStation yangi o'yini",
                risk_level="high",
                decision=DecisionOutcome.CANCELLED,
                cooling_off_taken=True,
                notes="15 daqiqa sovutish taymeridan so'ng hissiy xarid ekanligi tushunildi va bekor qilindi.",
                created_at=now - timedelta(days=3)
            )
        ]

        self.simulated_contributions = []


demo_store = DemoStore()
