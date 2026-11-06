from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import SessionLocal
from app.api.v1.router import api_router
from app.data.seed import init_db, seed_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database schema and initial seed data on startup
    init_db()
    db = SessionLocal()
    try:
        seed_initial_data(db, force=False)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FinBridge — AI-powered behavioral finance platform for Hackathon MVP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 API
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "default_currency": settings.DEFAULT_CURRENCY,
        "database": settings.DATABASE_URL
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "FinBridge API ga xush kelibsiz!",
        "docs": "/docs",
        "version": "1.0.0",
        "currency": "UZS"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
