from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse, EquipmentCostCreate, EquipmentCostResponse
from app.models.equipment import Equipment, EquipmentCost
from app.models.harvest_season import HarvestSeason
from app.models.user import User
from app.utils.auth import get_current_active_user
from app.services.calculation_engine import HarvestCalculationEngine

router = APIRouter()

@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    equipment: EquipmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == equipment.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.get("/harvest-season/{harvest_season_id}", response_model=List[EquipmentResponse])
def get_equipment_by_harvest_season(
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
    
    equipment = db.query(Equipment).filter(
        Equipment.harvest_season_id == harvest_season_id
    ).all()
    return equipment

@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    equipment = db.query(Equipment).join(HarvestSeason).filter(
        Equipment.id == equipment_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return equipment

@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment_update: EquipmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    equipment = db.query(Equipment).join(HarvestSeason).filter(
        Equipment.id == equipment_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    update_data = equipment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipment, field, value)
    
    db.commit()
    db.refresh(equipment)
    return equipment

@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    equipment = db.query(Equipment).join(HarvestSeason).filter(
        Equipment.id == equipment_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}

@router.post("/costs/", response_model=EquipmentCostResponse)
def create_equipment_cost(
    equipment_cost: EquipmentCostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == equipment_cost.harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    db_equipment_cost = EquipmentCost(**equipment_cost.dict())
    db.add(db_equipment_cost)
    db.commit()
    db.refresh(db_equipment_cost)
    return db_equipment_cost

@router.get("/costs/harvest-season/{harvest_season_id}", response_model=List[EquipmentCostResponse])
def get_equipment_costs_by_harvest_season(
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
    
    equipment_costs = db.query(EquipmentCost).filter(
        EquipmentCost.harvest_season_id == harvest_season_id
    ).all()
    return equipment_costs

@router.post("/{equipment_id}/calculate-costs")
def calculate_equipment_costs(
    equipment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Calculate equipment costs for all periods"""
    equipment = db.query(Equipment).join(HarvestSeason).filter(
        Equipment.id == equipment_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    calculation_engine = HarvestCalculationEngine(db)
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == equipment.harvest_season_id
    ).first()
    
    # Calculate costs for this equipment
    costs = calculation_engine.calculate_period_costs(harvest_season)
    equipment_costs = [cost for cost in costs if cost.equipment_id == equipment_id]
    
    # Save to database
    for cost in equipment_costs:
        db.add(cost)
    db.commit()
    
    return {"message": f"Equipment costs calculated for {len(equipment_costs)} periods"}
