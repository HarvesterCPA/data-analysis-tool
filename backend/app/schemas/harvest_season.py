from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.harvest_season import PayCycle

class HarvestSeasonBase(BaseModel):
    business_name: str
    business_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    estimated_start_date: Optional[datetime] = None
    estimated_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    pay_cycle: PayCycle = PayCycle.WEEKLY
    interest_rate: float = Field(default=6.0, ge=0, le=100)

class HarvestSeasonCreate(HarvestSeasonBase):
    pass

class HarvestSeasonUpdate(BaseModel):
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    estimated_start_date: Optional[datetime] = None
    estimated_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    pay_cycle: Optional[PayCycle] = None
    interest_rate: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None

class HarvestSeasonResponse(HarvestSeasonBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
