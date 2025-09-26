from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from app.core.database import get_db
from app.schemas.summary_calculation import SummaryCalculationResponse, ProfitLossSummary, CostBreakdown, RevenueBreakdown, EquipmentAnalysis
from app.models.summary_calculation import SummaryCalculation
from app.models.harvest_season import HarvestSeason
from app.models.user import User
from app.utils.auth import get_current_active_user
from app.services.calculation_engine import HarvestCalculationEngine

router = APIRouter()

@router.get("/harvest-season/{harvest_season_id}", response_model=SummaryCalculationResponse)
def get_summary_calculation(
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
    
    summary = db.query(SummaryCalculation).filter(
        SummaryCalculation.harvest_season_id == harvest_season_id
    ).order_by(SummaryCalculation.calculated_at.desc()).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary calculation found for this harvest season")
    
    return summary

@router.get("/harvest-season/{harvest_season_id}/profit-loss", response_model=ProfitLossSummary)
def get_profit_loss_summary(
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
    
    summary = db.query(SummaryCalculation).filter(
        SummaryCalculation.harvest_season_id == harvest_season_id
    ).order_by(SummaryCalculation.calculated_at.desc()).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary calculation found for this harvest season")
    
    return ProfitLossSummary(
        harvest_duration_days=summary.harvest_duration_days or 0,
        acres_billed=summary.acres_billed or 0,
        total_revenue=summary.total_revenue,
        total_expenses=summary.total_expenses,
        gross_profit=summary.gross_profit,
        net_profit=summary.net_profit,
        profit_margin=summary.profit_margin,
        cost_per_acre=summary.cost_per_acre,
        revenue_per_acre=summary.revenue_per_acre,
        profit_per_acre=summary.profit_per_acre
    )

@router.get("/harvest-season/{harvest_season_id}/cost-breakdown", response_model=CostBreakdown)
def get_cost_breakdown(
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
    
    summary = db.query(SummaryCalculation).filter(
        SummaryCalculation.harvest_season_id == harvest_season_id
    ).order_by(SummaryCalculation.calculated_at.desc()).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary calculation found for this harvest season")
    
    return CostBreakdown(
        equipment_cost=summary.total_equipment_cost,
        housing_cost=summary.total_housing_cost,
        employee_cost=summary.total_employee_cost,
        fuel_cost=summary.total_fuel_cost,
        maintenance_cost=summary.total_maintenance_cost,
        insurance_cost=summary.total_insurance_cost,
        tax_cost=summary.total_tax_cost,
        other_cost=summary.total_other_cost,
        total_cost=summary.total_expenses
    )

@router.get("/harvest-season/{harvest_season_id}/revenue-breakdown", response_model=RevenueBreakdown)
def get_revenue_breakdown(
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
    
    summary = db.query(SummaryCalculation).filter(
        SummaryCalculation.harvest_season_id == harvest_season_id
    ).order_by(SummaryCalculation.calculated_at.desc()).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary calculation found for this harvest season")
    
    revenue_by_crop = {}
    if summary.revenue_by_crop:
        try:
            revenue_by_crop = json.loads(summary.revenue_by_crop)
        except json.JSONDecodeError:
            revenue_by_crop = {}
    
    return RevenueBreakdown(
        total_revenue=summary.total_revenue,
        revenue_by_crop=revenue_by_crop,
        revenue_per_acre=summary.revenue_per_acre
    )

@router.get("/harvest-season/{harvest_season_id}/equipment-analysis", response_model=EquipmentAnalysis)
def get_equipment_analysis(
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
    
    summary = db.query(SummaryCalculation).filter(
        SummaryCalculation.harvest_season_id == harvest_season_id
    ).order_by(SummaryCalculation.calculated_at.desc()).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary calculation found for this harvest season")
    
    equipment_cost_breakdown = {}
    if summary.equipment_cost_breakdown:
        try:
            equipment_cost_breakdown = json.loads(summary.equipment_cost_breakdown)
        except json.JSONDecodeError:
            equipment_cost_breakdown = {}
    
    # Calculate cost per acre by equipment
    cost_per_acre_by_equipment = {}
    acres_billed = summary.acres_billed or 1
    for equipment_name, cost in equipment_cost_breakdown.items():
        cost_per_acre_by_equipment[equipment_name] = cost / acres_billed
    
    return EquipmentAnalysis(
        equipment_cost_breakdown=equipment_cost_breakdown,
        cost_per_acre_by_equipment=cost_per_acre_by_equipment
    )

@router.post("/harvest-season/{harvest_season_id}/recalculate")
def recalculate_summary(
    harvest_season_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Recalculate all summary metrics for a harvest season"""
    # Verify harvest season belongs to user
    harvest_season = db.query(HarvestSeason).filter(
        HarvestSeason.id == harvest_season_id,
        HarvestSeason.user_id == current_user.id
    ).first()
    
    if not harvest_season:
        raise HTTPException(status_code=404, detail="Harvest season not found")
    
    calculation_engine = HarvestCalculationEngine(db)
    summary = calculation_engine.recalculate_harvest_season(harvest_season_id)
    
    return {
        "message": "Summary calculation completed successfully",
        "summary_id": summary.id,
        "calculated_at": summary.calculated_at
    }
