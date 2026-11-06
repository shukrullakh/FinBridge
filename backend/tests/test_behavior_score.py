from decimal import Decimal
import pytest
from app.services.score_service import ScoreService


def test_score_insufficient_data():
    res = ScoreService.calculate_score(
        total_income=Decimal("0"),
        total_expenses=Decimal("0"),
        over_budget_count=0,
        total_budgets_count=0,
        total_saved=Decimal("0"),
        total_savings_target=Decimal("0"),
        total_monthly_debt_payments=Decimal("0")
    )
    assert res.has_sufficient_data is False
    assert res.total_score == 0
    assert res.grade == "N/A"


def test_score_healthy_financials():
    res = ScoreService.calculate_score(
        total_income=Decimal("10000000"),
        total_expenses=Decimal("5000000"),     # 50% expense ratio
        over_budget_count=0,
        total_budgets_count=4,
        total_saved=Decimal("2500000"),        # 25% savings ratio
        total_savings_target=Decimal("5000000"), # 50% goal progress
        total_monthly_debt_payments=Decimal("1500000") # 15% DTI
    )
    assert res.has_sufficient_data is True
    assert 75 <= res.total_score <= 100
    assert res.grade in ["A", "B"]
    assert len(res.dimensions) == 4
