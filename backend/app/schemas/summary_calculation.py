from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class SummaryCalculationBase(BaseModel):
    harvest_duration_days: Optional[float] = Field(None, ge=0)
    acres_billed: Optional[float] = Field(None, ge=0)
    total_equipment_cost: float = Field(default=0.0, ge=0)
    total_housing_cost: float = Field(default=0.0, ge=0)
    total_employee_cost: float = Field(default=0.0, ge=0)
    total_fuel_cost: float = Field(default=0.0, ge=0)
    total_maintenance_cost: float = Field(default=0.0, ge=0)
    total_insurance_cost: float = Field(default=0.0, ge=0)
    total_tax_cost: float = Field(default=0.0, ge=0)
    total_other_cost: float = Field(default=0.0, ge=0)
    total_expenses: float = Field(default=0.0, ge=0)
    total_revenue: float = Field(default=0.0, ge=0)
    revenue_by_crop: Optional[str] = None  # JSON string
    gross_profit: float = Field(default=0.0)
    net_profit: float = Field(default=0.0)
    profit_margin: float = Field(default=0.0)
    cost_per_acre: float = Field(default=0.0, ge=0)
    revenue_per_acre: float = Field(default=0.0, ge=0)
    profit_per_acre: float = Field(default=0.0)
    equipment_cost_breakdown: Optional[str] = None  # JSON string

class SummaryCalculationResponse(SummaryCalculationBase):
    id: int
    harvest_season_id: int
    calculated_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProfitLossSummary(BaseModel):
    harvest_duration_days: float
    acres_billed: float
    total_revenue: float
    total_expenses: float
    gross_profit: float
    net_profit: float
    profit_margin: float
    cost_per_acre: float
    revenue_per_acre: float
    profit_per_acre: float

class CostBreakdown(BaseModel):
    equipment_cost: float
    housing_cost: float
    employee_cost: float
    fuel_cost: float
    maintenance_cost: float
    insurance_cost: float
    tax_cost: float
    other_cost: float
    total_cost: float

class RevenueBreakdown(BaseModel):
    total_revenue: float
    revenue_by_crop: Dict[str, float]
    revenue_per_acre: float

class EquipmentAnalysis(BaseModel):
    equipment_cost_breakdown: Dict[str, float]
    cost_per_acre_by_equipment: Dict[str, float]
