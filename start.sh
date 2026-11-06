#!/usr/bin/env bash
set -e

echo "======================================================"
echo "🚀 FinBridge — Moliyaviy Farovonlik Platformasi (MVP)"
echo "======================================================"

# Determine base dir
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="/opt/homebrew/bin:$PATH"

# 1. Start Backend in background
echo "1. Backend (FastAPI) ishga tushirilmoqda (http://127.0.0.1:8000)..."
"$BASE_DIR/backend/.venv/bin/python3" "$BASE_DIR/backend/run.py" &
BACKEND_PID=$!

# Trap Ctrl+C to cleanly terminate both processes
cleanup() {
  echo ""
  echo "FinBridge to'xtatilmoqda..."
  kill $BACKEND_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 2. Start Frontend
echo "2. Frontend (Vite + React) ishga tushirilmoqda (http://localhost:5173)..."
cd "$BASE_DIR/frontend"
npm run dev
