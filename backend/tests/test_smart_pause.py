from decimal import Decimal
import pytest
from app.services.smart_pause_service import SmartPauseService
from app.schemas.smart_pause import SmartPauseEvaluateRequest


def test_smart_pause_safe_purchase():
    req = SmartPauseEvaluateRequest(
        amount=Decimal("150000"),
        category="Oziq-ovqat"
    )
    res = SmartPauseService.evaluate_purchase(
        request=req,
        current_balance=Decimal("5000000"),
        current_category_spent=Decimal("500000"),
        category_limit=Decimal("2000000")
    )
    assert res.is_risky is False
    assert res.risk_level == "safe"
    assert res.projected_balance == Decimal("4850000")


def test_smart_pause_insufficient_balance():
    req = SmartPauseEvaluateRequest(
        amount=Decimal("3000000"),
        category="Elektronika"
    )
    res = SmartPauseService.evaluate_purchase(
        request=req,
        current_balance=Decimal("1000000"),
        current_category_spent=Decimal("0"),
        category_limit=None
    )
    assert res.is_risky is True
    assert res.risk_level == "high"
    assert res.projected_balance == Decimal("-2000000")
    assert any("kassa yetishmovchiligi" in r.lower() for r in res.reasons)


def test_smart_pause_category_limit_exceeded():
    req = SmartPauseEvaluateRequest(
        amount=Decimal("600000"),
        category="Restoran"
    )
    res = SmartPauseService.evaluate_purchase(
        request=req,
        current_balance=Decimal("4000000"),
        current_category_spent=Decimal("700000"),
        category_limit=Decimal("1000000")
    )
    # 700k + 600k = 1.3M > 1.0M
    assert res.is_risky is True
    assert res.risk_level == "high"
    assert any("limit" in r.lower() for r in res.reasons)
