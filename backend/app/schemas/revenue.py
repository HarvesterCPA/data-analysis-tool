from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.revenue import CropType, PricingModel

class RevenueEntryBase(BaseModel):
    crop_type: CropType
    pricing_model: PricingModel
    client_name: Optional[str] = None
    client_state: Optional[str] = None
    quantity: float = Field(ge=0)
    rate: float = Field(ge=0)
    total_revenue: float = Field(ge=0)
    harvest_date: datetime
    notes: Optional[str] = None

class RevenueEntryCreate(RevenueEntryBase):
    harvest_season_id: int

class RevenueEntryUpdate(BaseModel):
    crop_type: Optional[CropType] = None
    pricing_model: Optional[PricingModel] = None
    client_name: Optional[str] = None
    client_state: Optional[str] = None
    quantity: Optional[float] = Field(None, ge=0)
    rate: Optional[float] = Field(None, ge=0)
    total_revenue: Optional[float] = Field(None, ge=0)
    harvest_date: Optional[datetime] = None
    notes: Optional[str] = None

class RevenueEntryResponse(RevenueEntryBase):
    id: int
    harvest_season_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IncomeRateStructureBase(BaseModel):
    crop_type: CropType
    state: str
    per_acre_rate: Optional[float] = Field(None, ge=0)
    per_bushel_rate: Optional[float] = Field(None, ge=0)
    per_minute_rate: Optional[float] = Field(None, ge=0)
    per_mile_rate: Optional[float] = Field(None, ge=0)
    per_hour_rate: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

class IncomeRateStructureCreate(IncomeRateStructureBase):
    harvest_season_id: int

class IncomeRateStructureResponse(IncomeRateStructureBase):
    id: int
    harvest_season_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
