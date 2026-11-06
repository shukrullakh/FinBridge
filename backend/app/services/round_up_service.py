from decimal import Decimal
import math
from app.schemas.savings import RoundUpCalculation


class RoundUpService:
    @staticmethod
    def calculate_round_up(amount: Decimal, step: Decimal = Decimal("5000")) -> RoundUpCalculation:
        """
        Calculates simulated round-up for a transaction amount.
        Example: 42,300 UZS with step 5,000 UZS -> rounded to 45,000 UZS (saved: 2,700 UZS).
        """
        if amount <= Decimal("0") or step <= Decimal("0"):
            return RoundUpCalculation(
                original_amount=amount,
                rounded_amount=amount,
                saved_amount=Decimal("0"),
                step=step,
                is_applicable=False
            )

        remainder = amount % step
        if remainder == Decimal("0"):
            # Already a multiple of step
            rounded = amount
            saved = Decimal("0")
            applicable = False
        else:
            rounded = amount + (step - remainder)
            saved = rounded - amount
            applicable = True

        return RoundUpCalculation(
            original_amount=amount,
            rounded_amount=rounded,
            saved_amount=saved,
            step=step,
            is_applicable=applicable
        )
