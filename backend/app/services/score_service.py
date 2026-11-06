from decimal import Decimal
from typing import List
from app.schemas.score import BehaviorScoreResponse, DimensionDetail


class ScoreService:
    @staticmethod
    def calculate_score(
        total_income: Decimal,
        total_expenses: Decimal,
        over_budget_count: int,
        total_budgets_count: int,
        total_saved: Decimal,
        total_savings_target: Decimal,
        total_monthly_debt_payments: Decimal
    ) -> BehaviorScoreResponse:
        """
        Calculates transparent Financial Behavior Score.
        Weights:
        - Spending discipline: 30%
        - Saving consistency: 25%
        - Debt payment discipline: 25%
        - Goal progress: 20%
        """
        # Data sufficiency check
        if total_income <= Decimal("0") and total_expenses <= Decimal("0"):
            return BehaviorScoreResponse(
                total_score=0,
                grade="N/A",
                grade_label="Ma'lumot yetarli emas",
                has_sufficient_data=False,
                dimensions=[],
                summary_insights=["Tahlil qilish uchun avval tranzaksiyalarni kiriting."],
            )

        # 1. Spending discipline (30%)
        # Based on expense to income ratio and budget limit violations
        spending_score = 100
        if total_income > Decimal("0"):
            expense_ratio = (total_expenses / total_income) * Decimal("100")
            if expense_ratio > Decimal("100"):
                spending_score -= 50
            elif expense_ratio > Decimal("80"):
                spending_score -= 30
            elif expense_ratio > Decimal("60"):
                spending_score -= 15
        else:
            spending_score -= 40

        if total_budgets_count > 0 and over_budget_count > 0:
            penalty = min(40, (over_budget_count / total_budgets_count) * 40)
            spending_score -= int(penalty)

        spending_score = max(10, min(100, spending_score))

        # 2. Saving consistency (25%)
        # Based on savings amount compared to income
        saving_score = 50
        if total_income > Decimal("0"):
            saving_ratio = (total_saved / total_income) * Decimal("100")
            if saving_ratio >= Decimal("20"):
                saving_score = 100
            elif saving_ratio >= Decimal("10"):
                saving_score = 80
            elif saving_ratio >= Decimal("5"):
                saving_score = 65
            elif saving_ratio > Decimal("0"):
                saving_score = 55
            else:
                saving_score = 30
        else:
            if total_saved > Decimal("0"):
                saving_score = 70

        saving_score = max(10, min(100, saving_score))

        # 3. Debt payment discipline (25%)
        # Based on Debt-to-Income (DTI) ratio
        debt_score = 100
        if total_income > Decimal("0") and total_monthly_debt_payments > Decimal("0"):
            dti = (total_monthly_debt_payments / total_income) * Decimal("100")
            if dti > Decimal("50"):
                debt_score = 30
            elif dti > Decimal("35"):
                debt_score = 60
            elif dti > Decimal("20"):
                debt_score = 80
            else:
                debt_score = 95
        elif total_monthly_debt_payments == Decimal("0"):
            debt_score = 100  # No debts

        debt_score = max(10, min(100, debt_score))

        # 4. Goal progress (20%)
        # Based on savings progress toward targets
        goal_score = 50
        if total_savings_target > Decimal("0"):
            progress = (total_saved / total_savings_target) * Decimal("100")
            if progress >= Decimal("100"):
                goal_score = 100
            elif progress >= Decimal("50"):
                goal_score = 85
            elif progress >= Decimal("25"):
                goal_score = 70
            elif progress > Decimal("0"):
                goal_score = 55
            else:
                goal_score = 35

        goal_score = max(10, min(100, goal_score))

        # Total weighted score
        total = int(
            (spending_score * 0.30) +
            (saving_score * 0.25) +
            (debt_score * 0.25) +
            (goal_score * 0.20)
        )
        total = max(0, min(100, total))

        # Grade determination
        if total >= 85:
            grade = "A"
            grade_label = "A'lo moliyaviy intizom"
        elif total >= 70:
            grade = "B"
            grade_label = "Yaxshi moliyaviy barqarorlik"
        elif total >= 50:
            grade = "C"
            grade_label = "O'rtacha intizom, e'tibor zarur"
        else:
            grade = "D"
            grade_label = "Xavf ostidagi moliyaviy holat"

        def get_status(s: int) -> str:
            if s >= 85: return "A'lo"
            if s >= 70: return "Yaxshi"
            if s >= 50: return "O'rtacha"
            return "E'tibor talab"

        dimensions = [
            DimensionDetail(
                name="Xarajatlar nazorati",
                key="spending_discipline",
                score=spending_score,
                weight_percentage=30,
                status=get_status(spending_score),
                explanation="Oylik daromad va xarajatlar nisbati hamda toifaviy limitlarga amal qilinishi.",
                recommendation="Qizil chiziq (limit) belgilangan xarajat toifalarini me'yorda saqlang."
            ),
            DimensionDetail(
                name="Jamg'arma barqarorligi",
                key="saving_consistency",
                score=saving_score,
                weight_percentage=25,
                status=get_status(saving_score),
                explanation="Daromadning qancha qismi jamg'arib borilayotgani va round-up faolligi.",
                recommendation="Har bir xariddan mayda pullarni jamg'armaga yo'naltirish odatini saqlang."
            ),
            DimensionDetail(
                name="Qarz majburiyatlari yuki",
                key="debt_discipline",
                score=debt_score,
                weight_percentage=25,
                status=get_status(debt_score),
                explanation="Oylik qarz va muddatli to'lovlarning umumiy daromaddagi ulushi (DTI).",
                recommendation="Oylik qarz to'lovlarini daromadingizning 30% idan oshirmaslikka intiling."
            ),
            DimensionDetail(
                name="Maqsadlarga erishish sur'ati",
                key="goal_progress",
                score=goal_score,
                weight_percentage=20,
                status=get_status(goal_score),
                explanation="Qo'yilgan moliyaviy maqsadlarning bosqichma-bosqich bajarilishi.",
                recommendation="Jamg'arma maqsadlaringizni aniq muddat va real summalar bilan belgilang."
            )
        ]

        insights = [
            f"Umumiy ball: {total}/100 ({grade_label}).",
            "Xarajatlaringiz va qarz to'lovlaringiz nisbati doimiy nazoratda.",
            "Round-up jamg'armalari orqali xatti-harakat balingizni yana 10-15 ballga oshirishingiz mumkin."
        ]

        return BehaviorScoreResponse(
            total_score=total,
            grade=grade,
            grade_label=grade_label,
            has_sufficient_data=True,
            dimensions=dimensions,
            summary_insights=insights
        )
