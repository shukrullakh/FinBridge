from decimal import Decimal
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.data.seed import init_db, seed_initial_data

client = TestClient(app)


def setup_function():
    init_db()
    db = SessionLocal()
    try:
        seed_initial_data(db, force=True)
    finally:
        db.close()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["default_currency"] == "UZS"


def test_dashboard_summary():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "UZS"
    assert Decimal(str(data["total_income"])) > Decimal("0")
    assert len(data["categories_breakdown"]) > 0
    assert len(data["recent_transactions"]) > 0
    assert data["current_behavior_score"] > 0


def test_transactions_flow_and_timezone_handling():
    # 1. Get transactions (should succeed without offset-naive/aware error)
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    initial_txs = response.json()
    initial_count = len(initial_txs)

    # 2. Add transaction with ISO string timezone date (like frontend sends)
    new_tx = {
        "amount": "43200",
        "type": "expense",
        "category": "Oziq-ovqat",
        "note": "Non va choy",
        "date": datetime.now(timezone.utc).isoformat(),
        "source": "Plastik karta"
    }
    create_res = client.post("/api/v1/transactions?apply_round_up=true", json=new_tx)
    assert create_res.status_code == 200
    res_data = create_res.json()
    assert "transaction" in res_data
    assert res_data["transaction"]["category"] == "Oziq-ovqat"
    assert res_data["round_up"] is not None
    assert Decimal(str(res_data["round_up"]["saved_amount"])) == Decimal("1800")

    # 3. Check get_transactions again (must sort correctly without crash)
    list_res = client.get("/api/v1/transactions")
    assert list_res.status_code == 200
    assert len(list_res.json()) == initial_count + 1


def test_smart_pause_evaluation():
    req = {
        "amount": "1500000",
        "category": "Restoran va Kafe",
        "description": "Hashamatli ziyofat"
    }
    response = client.post("/api/v1/smart-pause/evaluate", json=req)
    assert response.status_code == 200
    data = response.json()
    assert data["is_risky"] is True
    assert data["risk_level"] == "high"
    assert len(data["reflection_prompts"]) > 0


def test_debts_plan():
    response = client.post("/api/v1/debts/plan?extra_monthly_budget=500000")
    assert response.status_code == 200
    data = response.json()
    assert "snowball" in data
    assert "avalanche" in data
    assert len(data["snowball"]["order_of_payoff"]) == 4
    assert len(data["avalanche"]["order_of_payoff"]) == 4


def test_behavior_score_current():
    response = client.get("/api/v1/behavior-score/current")
    assert response.status_code == 200
    data = response.json()
    assert data["has_sufficient_data"] is True
    assert 0 <= data["total_score"] <= 100
    assert len(data["dimensions"]) == 4
