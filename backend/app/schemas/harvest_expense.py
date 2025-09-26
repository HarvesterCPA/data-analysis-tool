from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.harvest_expense import ExpenseCategory, HousingType, EmployeeExpenseType

class HarvestExpenseBase(BaseModel):
    category: ExpenseCategory
    subcategory: Optional[str] = None
    description: Optional[str] = None
    amount: float = Field(ge=0)
    period_start: datetime
    period_end: datetime
    harvest_days: Optional[float] = Field(None, ge=0)
    prorated_amount: Optional[float] = Field(None, ge=0)

class HarvestExpenseCreate(HarvestExpenseBase):
    harvest_season_id: int

class HarvestExpenseUpdate(BaseModel):
    category: Optional[ExpenseCategory] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    harvest_days: Optional[float] = Field(None, ge=0)
    prorated_amount: Optional[float] = Field(None, ge=0)

class HarvestExpenseResponse(HarvestExpenseBase):
    id: int
    harvest_season_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HousingExpenseBase(BaseModel):
    housing_type: HousingType
    description: Optional[str] = None
    daily_rate: Optional[float] = Field(None, ge=0)
    total_days: Optional[float] = Field(None, ge=0)
    total_amount: float = Field(ge=0)
    period_start: datetime
    period_end: datetime

class HousingExpenseCreate(HousingExpenseBase):
    harvest_season_id: int

class HousingExpenseResponse(HousingExpenseBase):
    id: int
    harvest_season_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EmployeeExpenseBase(BaseModel):
    expense_type: EmployeeExpenseType
    employee_name: Optional[str] = None
    description: Optional[str] = None
    amount: float = Field(ge=0)
    period_start: datetime
    period_end: datetime

class EmployeeExpenseCreate(EmployeeExpenseBase):
    harvest_season_id: int

class EmployeeExpenseResponse(EmployeeExpenseBase):
    id: int
    harvest_season_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
