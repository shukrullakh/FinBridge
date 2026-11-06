from decimal import Decimal
import pytest
from app.services.round_up_service import RoundUpService


def test_round_up_standard():
    # 42,300 with step 5,000 -> 45,000 (saved 2,700)
    calc = RoundUpService.calculate_round_up(Decimal("42300"), Decimal("5000"))
    assert calc.rounded_amount == Decimal("45000")
    assert calc.saved_amount == Decimal("2700")
    assert calc.is_applicable is True


def test_round_up_exact_multiple():
    # 45,000 with step 5,000 -> no extra round-up
    calc = RoundUpService.calculate_round_up(Decimal("45000"), Decimal("5000"))
    assert calc.rounded_amount == Decimal("45000")
    assert calc.saved_amount == Decimal("0")
    assert calc.is_applicable is False


def test_round_up_small_step():
    # 14,200 with step 1,000 -> 15,000 (saved 800)
    calc = RoundUpService.calculate_round_up(Decimal("14200"), Decimal("1000"))
    assert calc.rounded_amount == Decimal("15000")
    assert calc.saved_amount == Decimal("800")
    assert calc.is_applicable is True


def test_round_up_zero_or_negative():
    calc = RoundUpService.calculate_round_up(Decimal("0"), Decimal("5000"))
    assert calc.saved_amount == Decimal("0")
    assert calc.is_applicable is False

    calc_neg = RoundUpService.calculate_round_up(Decimal("-1000"), Decimal("5000"))
    assert calc_neg.saved_amount == Decimal("0")
    assert calc_neg.is_applicable is False
