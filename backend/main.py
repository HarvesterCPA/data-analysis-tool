from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import uvicorn

from app.core.config import settings
from app.core.database import get_db
from app.api import auth, users, income, expenses, analytics, admin, harvest_seasons, equipment, harvest_expenses, harvest_revenue, summary

app = FastAPI(
    title="Harvester Tracking API",
    description="API for tracking harvester income, expenses, and peer comparisons",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(income.router, prefix="/api/income", tags=["income"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Harvest Profit/Loss System
app.include_router(harvest_seasons.router, prefix="/api/harvest-seasons", tags=["harvest-seasons"])
app.include_router(equipment.router, prefix="/api/equipment", tags=["equipment"])
app.include_router(harvest_expenses.router, prefix="/api/harvest-expenses", tags=["harvest-expenses"])
app.include_router(harvest_revenue.router, prefix="/api/harvest-revenue", tags=["harvest-revenue"])
app.include_router(summary.router, prefix="/api/summary", tags=["summary"])

@app.get("/")
async def root():
    return {"message": "Harvester Tracking API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
