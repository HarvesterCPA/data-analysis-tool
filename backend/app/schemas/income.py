from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncomeEntryBase(BaseModel):
    acres_harvested: float
    rate_per_unit: float
    total_earned: float
    client_name: Optional[str] = None
    notes: Optional[str] = None
    harvest_date: datetime

class IncomeEntryCreate(IncomeEntryBase):
    pass

class IncomeEntryUpdate(BaseModel):
    acres_harvested: Optional[float] = None
    rate_per_unit: Optional[float] = None
    total_earned: Optional[float] = None
    client_name: Optional[str] = None
    notes: Optional[str] = None
    harvest_date: Optional[datetime] = None

class IncomeEntryResponse(IncomeEntryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
