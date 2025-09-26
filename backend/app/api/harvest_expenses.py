from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.harvest_expense import (
    HarvestExpenseCreate, HarvestExpenseUpdate, HarvestExpenseResponse,
    HousingExpenseCreate, HousingExpenseResponse,
    EmployeeExpenseCreate, EmployeeExpenseResponse
)
from app.models.harvest_expense import HarvestExpense, HousingExpense, EmployeeExpense
from app.models.harvest_season import HarvestSeason
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()

# Harvest Expenses
@router.post("/", response_model=HarvestExpenseResponse)
def create_harvest_expense(
    expense: HarvestExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == expense.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_expense = HarvestExpense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/harvest-season/{harvest_season_id}", response_model=List[HarvestExpenseResponse])
def get_harvest_expenses_by_season(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    expenses = db.query(HarvestExpense).filter(
        HarvestExpense.harvest_season_id == harvest_season_id
    ).all()
    return expenses

@router.get("/{expense_id}", response_model=HarvestExpenseResponse)
def get_harvest_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense = db.query(HarvestExpense).join(HarvestSeason).filter(
        HarvestExpense.id == expense_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return expense

@router.put("/{expense_id}", response_model=HarvestExpenseResponse)
def update_harvest_expense(
    expense_id: int,
    expense_update: HarvestExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense = db.query(HarvestExpense).join(HarvestSeason).filter(
        HarvestExpense.id == expense_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}")
def delete_harvest_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense = db.query(HarvestExpense).join(HarvestSeason).filter(
        HarvestExpense.id == expense_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

# Housing Expenses
@router.post("/housing/", response_model=HousingExpenseResponse)
def create_housing_expense(
    expense: HousingExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == expense.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_expense = HousingExpense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/housing/harvest-season/{harvest_season_id}", response_model=List[HousingExpenseResponse])
def get_housing_expenses_by_season(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    expenses = db.query(HousingExpense).filter(
        HousingExpense.harvest_season_id == harvest_season_id
    ).all()
    return expenses

# Employee Expenses
@router.post("/employees/", response_model=EmployeeExpenseResponse)
def create_employee_expense(
    expense: EmployeeExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == expense.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_expense = EmployeeExpense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/employees/harvest-season/{harvest_season_id}", response_model=List[EmployeeExpenseResponse])
def get_employee_expenses_by_season(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    expenses = db.query(EmployeeExpense).filter(
        EmployeeExpense.harvest_season_id == harvest_season_id
    ).all()
    return expenses
