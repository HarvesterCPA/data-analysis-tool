from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.core.database import get_db
from app.schemas.user import UserResponse
from app.models.user import User
from app.models.income import IncomeEntry
from app.models.expense import ExpenseEntry
from app.utils.auth import get_current_admin_user

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/stats")
def get_platform_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_income_entries = db.query(IncomeEntry).count()
    total_expense_entries = db.query(ExpenseEntry).count()
    
    total_income = db.query(func.sum(IncomeEntry.total_earned)).scalar() or 0
    total_expenses = db.query(func.sum(ExpenseEntry.amount)).scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_income_entries": total_income_entries,
        "total_expense_entries": total_expense_entries,
        "total_income_tracked": total_income,
        "total_expenses_tracked": total_expenses
    }

@router.delete("/users/{user_id}")
def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}
