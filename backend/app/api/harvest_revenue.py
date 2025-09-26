from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.revenue import (
    RevenueEntryCreate, RevenueEntryUpdate, RevenueEntryResponse,
    IncomeRateStructureCreate, IncomeRateStructureResponse
)
from app.models.revenue import RevenueEntry, IncomeRateStructure
from app.models.harvest_season import HarvestSeason
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()

# Revenue Entries
@router.post("/", response_model=RevenueEntryResponse)
def create_revenue_entry(
    revenue_entry: RevenueEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == revenue_entry.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_revenue = RevenueEntry(**revenue_entry.dict())
    db.add(db_revenue)
    db.commit()
    db.refresh(db_revenue)
    return db_revenue

@router.get("/harvest-season/{harvest_season_id}", response_model=List[RevenueEntryResponse])
def get_revenue_entries_by_season(
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
    
    revenue_entries = db.query(RevenueEntry).filter(
        RevenueEntry.harvest_season_id == harvest_season_id
    ).all()
    return revenue_entries

@router.get("/{revenue_id}", response_model=RevenueEntryResponse)
def get_revenue_entry(
    revenue_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    revenue_entry = db.query(RevenueEntry).join(HarvestSeason).filter(
        RevenueEntry.id == revenue_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not revenue_entry:
        raise HTTPException(status_code=404, detail="Revenue entry not found")
    
    return revenue_entry

@router.put("/{revenue_id}", response_model=RevenueEntryResponse)
def update_revenue_entry(
    revenue_id: int,
    revenue_update: RevenueEntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    revenue_entry = db.query(RevenueEntry).join(HarvestSeason).filter(
        RevenueEntry.id == revenue_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not revenue_entry:
        raise HTTPException(status_code=404, detail="Revenue entry not found")
    
    update_data = revenue_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(revenue_entry, field, value)
    
    db.commit()
    db.refresh(revenue_entry)
    return revenue_entry

@router.delete("/{revenue_id}")
def delete_revenue_entry(
    revenue_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    revenue_entry = db.query(RevenueEntry).join(HarvestSeason).filter(
        RevenueEntry.id == revenue_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not revenue_entry:
        raise HTTPException(status_code=404, detail="Revenue entry not found")
    
    db.delete(revenue_entry)
    db.commit()
    return {"message": "Revenue entry deleted successfully"}

# Income Rate Structures
@router.post("/rate-structures/", response_model=IncomeRateStructureResponse)
def create_income_rate_structure(
    rate_structure: IncomeRateStructureCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == rate_structure.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_rate_structure = IncomeRateStructure(**rate_structure.dict())
    db.add(db_rate_structure)
    db.commit()
    db.refresh(db_rate_structure)
    return db_rate_structure

@router.get("/rate-structures/harvest-season/{harvest_season_id}", response_model=List[IncomeRateStructureResponse])
def get_income_rate_structures_by_season(
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
    
    rate_structures = db.query(IncomeRateStructure).filter(
        IncomeRateStructure.harvest_season_id == harvest_season_id
    ).all()
    return rate_structures
