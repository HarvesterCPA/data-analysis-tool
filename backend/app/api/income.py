from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from app.core.database import get_db
from app.schemas.income import IncomeEntryCreate, IncomeEntryUpdate, IncomeEntryResponse
from app.models.income import IncomeEntry
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=IncomeEntryResponse)
def create_income_entry(
    income_entry: IncomeEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_income = IncomeEntry(
        user_id=current_user.id,
        **income_entry.dict()
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

@router.get("/", response_model=List[IncomeEntryResponse])
def get_income_entries(
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(IncomeEntry).filter(IncomeEntry.user_id == current_user.id)
    
    if start_date:
        query = query.filter(IncomeEntry.harvest_date >= start_date)
    if end_date:
        query = query.filter(IncomeEntry.harvest_date <= end_date)
    
    income_entries = query.offset(skip).limit(limit).all()
    return income_entries

@router.get("/{income_id}", response_model=IncomeEntryResponse)
def get_income_entry(
    income_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    income_entry = db.query(IncomeEntry).filter(
        IncomeEntry.id == income_id,
        IncomeEntry.user_id == current_user.id
    ).first()
    
    if not income_entry:
        raise HTTPException(status_code=404, detail="Income entry not found")
    
    return income_entry

@router.put("/{income_id}", response_model=IncomeEntryResponse)
def update_income_entry(
    income_id: int,
    income_update: IncomeEntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    income_entry = db.query(IncomeEntry).filter(
        IncomeEntry.id == income_id,
        IncomeEntry.user_id == current_user.id
    ).first()
    
    if not income_entry:
        raise HTTPException(status_code=404, detail="Income entry not found")
    
    update_data = income_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(income_entry, field, value)
    
    db.commit()
    db.refresh(income_entry)
    return income_entry

@router.delete("/{income_id}")
def delete_income_entry(
    income_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    income_entry = db.query(IncomeEntry).filter(
        IncomeEntry.id == income_id,
        IncomeEntry.user_id == current_user.id
    ).first()
    
    if not income_entry:
        raise HTTPException(status_code=404, detail="Income entry not found")
    
    db.delete(income_entry)
    db.commit()
    return {"message": "Income entry deleted successfully"}
