from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.schemas.expense import ExpenseEntryCreate, ExpenseEntryUpdate, ExpenseEntryResponse
from app.models.expense import ExpenseEntry
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ExpenseEntryResponse)
def create_expense_entry(
    expense_entry: ExpenseEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_expense = ExpenseEntry(
        user_id=current_user.id,
        **expense_entry.dict()
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/", response_model=List[ExpenseEntryResponse])
def get_expense_entries(
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseEntry).filter(ExpenseEntry.user_id == current_user.id)
    
    if start_date:
        query = query.filter(ExpenseEntry.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseEntry.expense_date <= end_date)
    if category:
        query = query.filter(ExpenseEntry.category == category)
    
    expense_entries = query.offset(skip).limit(limit).all()
    return expense_entries

@router.get("/{expense_id}", response_model=ExpenseEntryResponse)
def get_expense_entry(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense_entry = db.query(ExpenseEntry).filter(
        ExpenseEntry.id == expense_id,
        ExpenseEntry.user_id == current_user.id
    ).first()
    
    if not expense_entry:
        raise HTTPException(status_code=404, detail="Expense entry not found")
    
    return expense_entry

@router.put("/{expense_id}", response_model=ExpenseEntryResponse)
def update_expense_entry(
    expense_id: int,
    expense_update: ExpenseEntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense_entry = db.query(ExpenseEntry).filter(
        ExpenseEntry.id == expense_id,
        ExpenseEntry.user_id == current_user.id
    ).first()
    
    if not expense_entry:
        raise HTTPException(status_code=404, detail="Expense entry not found")
    
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense_entry, field, value)
    
    db.commit()
    db.refresh(expense_entry)
    return expense_entry

@router.delete("/{expense_id}")
def delete_expense_entry(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    expense_entry = db.query(ExpenseEntry).filter(
        ExpenseEntry.id == expense_id,
        ExpenseEntry.user_id == current_user.id
    ).first()
    
    if not expense_entry:
        raise HTTPException(status_code=404, detail="Expense entry not found")
    
    db.delete(expense_entry)
    db.commit()
    return {"message": "Expense entry deleted successfully"}
