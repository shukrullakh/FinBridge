from fastapi import APIRouter
from app.api.v1.endpoints import (
    dashboard,
    transactions,
    budgets,
    smart_pause,
    savings,
    debts,
    score
)

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
api_router.include_router(smart_pause.router, prefix="/smart-pause", tags=["Smart Pause"])
api_router.include_router(savings.router, prefix="/savings", tags=["Invisible Savings"])
api_router.include_router(debts.router, prefix="/debts", tags=["Debt Coach"])
api_router.include_router(score.router, prefix="/behavior-score", tags=["Behavior Score"])
