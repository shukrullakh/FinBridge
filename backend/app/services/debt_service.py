from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
import copy
from app.schemas.debt import (
    Debt,
    PayoffPlanItem,
    StrategyComparison,
    DebtPlanResponse
)


class DebtService:
    @staticmethod
    def _simulate_payoff(
        debts_ordered: List[Debt],
        extra_monthly_budget: Decimal = Decimal("0")
    ) -> StrategyComparison:
        if not debts_ordered:
            return StrategyComparison(
                strategy_name="",
                description="",
                total_months=0,
                total_interest_paid=Decimal("0"),
                total_amount_paid=Decimal("0"),
                order_of_payoff=[],
                advantages=[]
            )

        # Working copies of balances
        balances: Dict[str, Decimal] = {d.id: d.balance for d in debts_ordered}
        rates: Dict[str, Decimal] = {d.id: (d.interest_rate or Decimal("0")) for d in debts_ordered}
        min_payments: Dict[str, Decimal] = {d.id: d.minimum_payment for d in debts_ordered}
        names: Dict[str, Decimal] = {d.id: d.name for d in debts_ordered}

        total_interest_accrued: Dict[str, Decimal] = {d.id: Decimal("0") for d in debts_ordered}
        months_to_pay: Dict[str, int] = {d.id: 0 for d in debts_ordered}

        total_months = 0
        max_months_safety = 360  # 30 years safety cap

        while any(balances[d_id] > Decimal("0.01") for d_id in balances) and total_months < max_months_safety:
            total_months += 1
            available_snowball_cash = extra_monthly_budget

            # 1. Accrue monthly interest on active debts
            for d in debts_ordered:
                d_id = d.id
                if balances[d_id] > Decimal("0.01"):
                    monthly_rate = (rates[d_id] / Decimal("100")) / Decimal("12")
                    monthly_interest = (balances[d_id] * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    balances[d_id] += monthly_interest
                    total_interest_accrued[d_id] += monthly_interest

            # 2. Pay minimums first for all active debts
            for d in debts_ordered:
                d_id = d.id
                if balances[d_id] > Decimal("0.01"):
                    min_pay = min_payments[d_id]
                    if balances[d_id] <= min_pay:
                        # Paid off with less than min payment
                        available_snowball_cash += (min_pay - balances[d_id])
                        balances[d_id] = Decimal("0")
                        if months_to_pay[d_id] == 0:
                            months_to_pay[d_id] = total_months
                    else:
                        balances[d_id] -= min_pay
                else:
                    # Debt already paid off previously, roll its minimum payment into snowball cash!
                    available_snowball_cash += min_payments[d_id]

            # 3. Apply accumulated extra cash to the primary target debt
            for d in debts_ordered:
                d_id = d.id
                if balances[d_id] > Decimal("0.01") and available_snowball_cash > Decimal("0"):
                    if balances[d_id] <= available_snowball_cash:
                        available_snowball_cash -= balances[d_id]
                        balances[d_id] = Decimal("0")
                        if months_to_pay[d_id] == 0:
                            months_to_pay[d_id] = total_months
                    else:
                        balances[d_id] -= available_snowball_cash
                        available_snowball_cash = Decimal("0")
                        break

            # Check if any debt just reached 0
            for d in debts_ordered:
                d_id = d.id
                if balances[d_id] <= Decimal("0.01") and months_to_pay[d_id] == 0:
                    months_to_pay[d_id] = total_months

        # Build payoff plan items
        plan_items: List[PayoffPlanItem] = []
        for idx, d in enumerate(debts_ordered, start=1):
            d_id = d.id
            plan_items.append(PayoffPlanItem(
                debt_id=d_id,
                debt_name=d.name,
                balance=d.balance,
                interest_rate=rates[d_id],
                minimum_payment=min_payments[d_id],
                payoff_order=idx,
                estimated_months_to_payoff=months_to_pay[d_id] if months_to_pay[d_id] > 0 else total_months,
                total_interest_estimated=total_interest_accrued[d_id].quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            ))

        total_interest_sum = sum(total_interest_accrued.values()).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        total_initial_principal = sum(d.balance for d in debts_ordered)
        total_amount_paid = total_initial_principal + total_interest_sum

        return StrategyComparison(
            strategy_name="",
            description="",
            total_months=total_months,
            total_interest_paid=total_interest_sum,
            total_amount_paid=total_amount_paid,
            order_of_payoff=plan_items,
            advantages=[]
        )

    @classmethod
    def calculate_strategies(
        cls,
        debts: List[Debt],
        extra_monthly_budget: Decimal = Decimal("0")
    ) -> DebtPlanResponse:
        total_min_payments = sum(d.minimum_payment for d in debts)
        monthly_budget = total_min_payments + extra_monthly_budget

        # 1. Snowball strategy: sort ascending by current balance
        snowball_ordered = sorted(debts, key=lambda d: d.balance)
        snowball_result = cls._simulate_payoff(snowball_ordered, extra_monthly_budget)
        snowball_result.strategy_name = "Snowball (Qor to'pi)"
        snowball_result.description = (
            "Eng kichik qoldiqqa ega qarzdan boshlab to'lash. "
            "Har bir yopilgan qarz sizga psixologik g'alaba hissini beradi va intizomni kuchaytiradi."
        )
        snowball_result.advantages = [
            "Tezkor ko'rinadigan natija va motivatsiya",
            "Qarzlar sonini tezroq qisqartirish",
            "Oylik majburiy to'lovlar ro'yxatini tezroq kamaytirish"
        ]

        # 2. Avalanche strategy: sort descending by interest rate, then ascending by balance
        avalanche_ordered = sorted(
            debts,
            key=lambda d: (-(d.interest_rate or Decimal("0")), d.balance)
        )
        avalanche_result = cls._simulate_payoff(avalanche_ordered, extra_monthly_budget)
        avalanche_result.strategy_name = "Avalanche (Qor ko'chkisi)"
        avalanche_result.description = (
            "Eng yuqori foiz stavkasiga ega qarzni birinchi o'rinda yopish. "
            "Matematik jihatdan foizlar uchun to'lanadigan umumiy ortiqcha pulni maksimal darajada kamaytiradi."
        )
        avalanche_result.advantages = [
            "Bank va kredit foizlaridan maksimal tejash",
            "Umumiy to'lanadigan yakuniy summaning eng kam bo'lishi",
            "Mantiqiy va moliyaviy tejamkor yondashuv"
        ]

        # Recommendation
        interest_diff = snowball_result.total_interest_paid - avalanche_result.total_interest_paid
        if interest_diff > Decimal("100000"):
            recommendation = (
                f"Avalanche strategiyasi tavsiya etiladi: siz jami {interest_diff:,.0f} UZS "
                f"miqdorida foiz to'lovlarini tejab qolasiz."
            )
        else:
            recommendation = (
                "Snowball strategiyasi tavsiya etiladi: foizlar o'rtasida katta farq yo'q, "
                "ammo kichik qarzlarni tezda yopish sizga ruhiy yengillik va yuqori motivatsiya beradi."
            )

        summary_insight = (
            f"Jami {len(debts)} ta qarz bo'yicha oylik jami to'lov: {monthly_budget:,.0f} UZS. "
            f"Qarzdan to'liq qutilish muddati: taxminan {min(snowball_result.total_months, avalanche_result.total_months)} oy."
        )

        return DebtPlanResponse(
            monthly_budget_allocated=monthly_budget,
            snowball=snowball_result,
            avalanche=avalanche_result,
            best_strategy_recommendation=recommendation,
            summary_insight=summary_insight
        )
