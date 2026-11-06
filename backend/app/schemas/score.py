from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class DimensionDetail(BaseModel):
    name: str
    key: str
    score: int = Field(..., ge=0, le=100)
    weight_percentage: int
    status: str  # "A'lo", "Yaxshi", "O'rtacha", "E'tibor talab"
    explanation: str
    recommendation: str


class BehaviorScoreResponse(BaseModel):
    total_score: int = Field(..., ge=0, le=100)
    grade: str  # "A", "B", "C", "D"
    grade_label: str  # masalan: "Moliyaviy intizom yuqori darajada"
    has_sufficient_data: bool = True
    dimensions: List[DimensionDetail]
    summary_insights: List[str]
    disclaimer: str = (
        "FinBridge bali kredit skoringi yoki rasmiy baholash emas, "
        "balki shaxsiy moliyaviy xatti-harakatlaringizni yaxshilash uchun yo'naltiruvchi ko'rsatkichdir."
    )
