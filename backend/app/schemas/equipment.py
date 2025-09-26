from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.models.equipment import EquipmentType, OwnershipType

class EquipmentBase(BaseModel):
    name: str
    equipment_type: EquipmentType
    ownership_type: OwnershipType
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    current_value: Optional[float] = Field(None, ge=0)
    years_ownership: Optional[float] = Field(None, ge=0)
    lease_rate: Optional[float] = Field(None, ge=0)
    finance_rate: Optional[float] = Field(None, ge=0)
    down_payment: Optional[float] = Field(None, ge=0)
    monthly_payment: Optional[float] = Field(None, ge=0)
    working_days: Optional[float] = Field(None, ge=0)

class EquipmentCreate(EquipmentBase):
    harvest_season_id: int

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    equipment_type: Optional[EquipmentType] = None
    ownership_type: Optional[OwnershipType] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    current_value: Optional[float] = Field(None, ge=0)
    years_ownership: Optional[float] = Field(None, ge=0)
    lease_rate: Optional[float] = Field(None, ge=0)
    finance_rate: Optional[float] = Field(None, ge=0)
    down_payment: Optional[float] = Field(None, ge=0)
    monthly_payment: Optional[float] = Field(None, ge=0)
    working_days: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None

class EquipmentResponse(EquipmentBase):
    id: int
    harvest_season_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EquipmentCostBase(BaseModel):
    period_start: datetime
    period_end: datetime
    lease_cost: float = Field(default=0.0, ge=0)
    interest_cost: float = Field(default=0.0, ge=0)
    depreciation_cost: float = Field(default=0.0, ge=0)
    total_cost: float = Field(ge=0)
    acres_worked: Optional[float] = Field(None, ge=0)
    cost_per_acre: Optional[float] = Field(None, ge=0)

class EquipmentCostCreate(EquipmentCostBase):
    harvest_season_id: int
    equipment_id: int

class EquipmentCostResponse(EquipmentCostBase):
    id: int
    harvest_season_id: int
    equipment_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
