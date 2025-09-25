from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ExpenseCategory(str, enum.Enum):
    FUEL = "fuel"
    LABOR = "labor"
    EQUIPMENT_LEASE = "equipment_lease"
    EQUIPMENT_REPAIR = "equipment_repair"
    EQUIPMENT_DEPRECIATION = "equipment_depreciation"
    RENT_INTEREST = "rent_interest"
    TAXES = "taxes"
    OTHER = "other"

class ExpenseEntry(Base):
    __tablename__ = "expense_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    expense_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="expense_entries")
