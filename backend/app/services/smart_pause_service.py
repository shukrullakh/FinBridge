from decimal import Decimal
from typing import List, Optional
from app.schemas.smart_pause import (
    SmartPauseEvaluateRequest,
    SmartPauseEvaluateResponse,
)


class SmartPauseService:
    @staticmethod
    def evaluate_purchase(
        request: SmartPauseEvaluateRequest,
        current_balance: Decimal,
        current_category_spent: Decimal,
        category_limit: Optional[Decimal] = None
    ) -> SmartPauseEvaluateResponse:
        reasons: List[str] = []
        is_risky = False
        risk_level = "safe"

        projected_category_spent = current_category_spent + request.amount
        projected_balance = current_balance - request.amount

        # 1. Check against overall balance
        if projected_balance < Decimal("0"):
            is_risky = True
            risk_level = "high"
            reasons.append(
                f"Kutilayotgan xarid joriy balansingizdan ({current_balance:,.0f} UZS) oshib ketadi. "
                f"Kassa yetishmovchiligi: {abs(projected_balance):,.0f} UZS."
            )
        elif projected_balance < Decimal("200000"):
            # Less than 200k buffer left
            is_risky = True
            if risk_level != "high":
                risk_level = "moderate"
            reasons.append(
                f"Ushbu xariddan so'ng xavfsizlik yostig'i sifatida balansingizda atigi "
                f"{projected_balance:,.0f} UZS qoladi."
            )

        # 2. Check against category limit ("red line")
        if category_limit and category_limit > Decimal("0"):
            if projected_category_spent > category_limit:
                is_risky = True
                risk_level = "high"
                excess = projected_category_spent - category_limit
                reasons.append(
                    f"'{request.category}' toifasi uchun oylik belgilangan "
                    f"{category_limit:,.0f} UZS limit {excess:,.0f} UZS ga oshib ketadi "
                    f"({(projected_category_spent / category_limit * 100):.1f}% sarf)."
                )
            elif (projected_category_spent / category_limit) >= Decimal("0.85"):
                is_risky = True
                if risk_level != "high":
                    risk_level = "moderate"
                reasons.append(
                    f"Xariddan so'ng '{request.category}' toifasidagi oylik limitning "
                    f"{(projected_category_spent / category_limit * 100):.0f}% qismi sarflanadi."
                )

        # 3. Check for high impulse share of balance (> 25% of liquid balance)
        if current_balance > Decimal("0") and (request.amount / current_balance) > Decimal("0.30"):
            if not is_risky:
                is_risky = True
                risk_level = "moderate"
            reasons.append(
                f"Bir martalik xarid umumiy qoldiq mablag'ingizning "
                f"{(request.amount / current_balance * 100):.0f}% qismini tashkil qilmoqda."
            )

        # Default reflection prompts
        reflection_prompts = [
            "Bu xarid sizga hozir rostdan ham zarurmi yoki hissiyot ta'siridami?",
            "Ushbu xaridni 24 soatga kechiktirsangiz sizga jiddiy noqulaylik tug'diradimi?",
            "Ushbu mablag'ni jamg'arma maqsadiga yo'naltirganingizda maqsadingizga qanchalik yaqinlashardingiz?"
        ]

        if not is_risky:
            reasons.append("Ushbu xarid byudjet chegaralari va mavjud balansingizga mos keladi.")
            impact_summary = (
                f"Xariddan keyin balansingiz {projected_balance:,.0f} UZS bo'ladi. "
                "Moliyaviy xavf aniqlanmadi."
            )
        else:
            impact_summary = (
                f"Ushbu xarid moliyaviy barqarorligingizga ta'sir qilishi mumkin. "
                f"Qoldiq balans: {projected_balance:,.0f} UZS. "
                "15 daqiqalik tanaffus qilib, qaroringizni qayta o'ylab ko'rishingizni tavsiya qilamiz."
            )

        return SmartPauseEvaluateResponse(
            is_risky=is_risky,
            risk_level=risk_level,
            reasons=reasons,
            category=request.category,
            amount=request.amount,
            category_limit=category_limit,
            current_category_spent=current_category_spent,
            projected_category_spent=projected_category_spent,
            current_balance=current_balance,
            projected_balance=projected_balance,
            cooling_off_minutes=15,
            reflection_prompts=reflection_prompts,
            impact_summary=impact_summary
        )
