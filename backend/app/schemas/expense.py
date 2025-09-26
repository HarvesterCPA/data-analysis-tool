from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.expense import ExpenseCategory

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
