from decimal import Decimal
import pytest
from app.schemas.debt import Debt, DebtType
from app.services.debt_service import DebtService


def test_snowball_vs_avalanche_sorting():
    debts = [
        Debt(
            id="1",
            name="Kredit karta",
            balance=Decimal("5000000"),
            interest_rate=Decimal("30"),
            minimum_payment=Decimal("500000"),
            type=DebtType.BANK_LOAN
        ),
        Debt(
            id="2",
            name="Do'stimdan qarz",
            balance=Decimal("1000000"),
            interest_rate=Decimal("0"),
            minimum_payment=Decimal("200000"),
            type=DebtType.PERSONAL
        ),
        Debt(
            id="3",
            name="Muddatli to'lov",
            balance=Decimal("2000000"),
            interest_rate=Decimal("20"),
            minimum_payment=Decimal("400000"),
            type=DebtType.INSTALLMENT
        )
    ]

    res = DebtService.calculate_strategies(debts, extra_monthly_budget=Decimal("500000"))
    
    # Snowball should pay smallest balance first: Do'st (1M), then Nasiya (2M), then Karta (5M)
    snowball_order = [item.debt_id for item in res.snowball.order_of_payoff]
    assert snowball_order == ["2", "3", "1"]

    # Avalanche should pay highest interest first: Karta (30%), then Nasiya (20%), then Do'st (0%)
    avalanche_order = [item.debt_id for item in res.avalanche.order_of_payoff]
    assert avalanche_order == ["1", "3", "2"]

    # Avalanche total interest should be less than or equal to Snowball total interest
    assert res.avalanche.total_interest_paid <= res.snowball.total_interest_paid
    assert res.snowball.total_months > 0
    assert res.avalanche.total_months > 0
