from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

# Define expense category as a literal type for validation
ExpenseCategory = Literal["fuel", "labor", "equipment_lease", "equipment_repair", "equipment_depreciation", "rent_interest", "taxes", "other"]

class ExpenseEntryBase(BaseModel):
    category: ExpenseCategory
    amount: float
    description: Optional[str] = None
    notes: Optional[str] = None
    expense_date: datetime

class ExpenseEntryCreate(ExpenseEntryBase):
    pass

class ExpenseEntryUpdate(BaseModel):
    category: Optional[ExpenseCategory] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    expense_date: Optional[datetime] = None

class ExpenseEntryResponse(ExpenseEntryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
