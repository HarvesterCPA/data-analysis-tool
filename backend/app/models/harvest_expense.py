from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ExpenseCategory(str, enum.Enum):
    FUEL = "fuel"
    MAINTENANCE = "maintenance"
    REPAIRS = "repairs"
    HOUSING = "housing"
    EMPLOYEES = "employees"
    INSURANCE = "insurance"
    TAXES = "taxes"
    PERMITS = "permits"
    OTHER = "other"

class HousingType(str, enum.Enum):
    CAMPER = "camper"
    HOTEL = "hotel"
    LOT_RENT = "lot_rent"
    UTILITIES = "utilities"

class EmployeeExpenseType(str, enum.Enum):
    WAGES = "wages"
    BENEFITS = "benefits"
    TRAINING = "training"
    MEALS = "meals"
    ENTERTAINMENT = "entertainment"

class HarvestExpense(Base):
    __tablename__ = "harvest_expenses"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Expense Details
    category = Column(Enum(ExpenseCategory), nullable=False)
    subcategory = Column(String, nullable=True)  # For housing type, employee type, etc.
    description = Column(Text, nullable=True)
    
    # Financial Information
    amount = Column(Float, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Prorated calculations
    harvest_days = Column(Float, nullable=True)
    prorated_amount = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason", back_populates="expenses")

class HousingExpense(Base):
    __tablename__ = "housing_expenses"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Housing Details
    housing_type = Column(Enum(HousingType), nullable=False)
    description = Column(Text, nullable=True)
    
    # Financial Information
    daily_rate = Column(Float, nullable=True)
    total_days = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=False)
    
    # Period tracking
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason")

class EmployeeExpense(Base):
    __tablename__ = "employee_expenses"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Employee Details
    expense_type = Column(Enum(EmployeeExpenseType), nullable=False)
    employee_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Financial Information
    amount = Column(Float, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason")
