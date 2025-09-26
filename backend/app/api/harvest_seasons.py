from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.schemas.harvest_season import HarvestSeasonCreate, HarvestSeasonUpdate, HarvestSeasonResponse
from app.models.harvest_season import HarvestSeason
from app.models.user import User
from app.utils.auth import get_current_active_user
from app.services.calculation_engine import HarvestCalculationEngine

router = APIRouter()

@router.post("/", response_model=HarvestSeasonResponse)
def create_harvest_season(
    harvest_season: HarvestSeasonCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_harvest_season = HarvestSeason(
        user_id=current_user.id,
        **harvest_season.dict()
    )
    db.add(db_harvest_season)
    db.commit()
    db.refresh(db_harvest_season)
    return db_harvest_season

@router.get("/", response_model=List[HarvestSeasonResponse])
def get_harvest_seasons(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    harvest_seasons = db.query(HarvestSeason).filter(
        HarvestSeason.user_id == current_user.id
    ).all()
    return harvest_seasons

@router.get("/{harvest_season_id}", response_model=HarvestSeasonResponse)
def get_harvest_season(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    return harvest_season

@router.put("/{harvest_season_id}", response_model=HarvestSeasonResponse)
def update_harvest_season(
    harvest_season_id: int,
    harvest_season_update: HarvestSeasonUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    update_data = harvest_season_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(harvest_season, field, value)
    
    db.commit()
    db.refresh(harvest_season)
    return harvest_season

@router.delete("/{harvest_season_id}")
def delete_harvest_season(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db.delete(harvest_season)
    db.commit()
    return {"message": "Harvest season deleted successfully"}

@router.post("/{harvest_season_id}/calculate")
def calculate_profit_loss(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Recalculate profit/loss for a harvest season"""
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    calculation_engine = HarvestCalculationEngine(db)
    summary = calculation_engine.recalculate_harvest_season(harvest_season_id)
    
    return {"message": "Profit/loss calculation completed", "summary_id": summary.id}
