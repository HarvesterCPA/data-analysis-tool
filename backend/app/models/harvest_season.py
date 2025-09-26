from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class PayCycle(str, enum.Enum):
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    SEMI_MONTHLY = "semi_monthly"
    MONTHLY = "monthly"

class HarvestSeason(Base):
    __tablename__ = "harvest_seasons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Business Information
    business_name = Column(String, nullable=False)
    business_address = Column(Text, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    
    # Harvest Dates
    estimated_start_date = Column(DateTime, nullable=True)
    estimated_end_date = Column(DateTime, nullable=True)
    actual_start_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)
    
    # Financial Settings
    pay_cycle = Column(Enum(PayCycle), nullable=False, default=PayCycle.WEEKLY)
    interest_rate = Column(Float, nullable=False, default=6.0)  # 6% default
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="harvest_seasons")
    equipment = relationship("Equipment", back_populates="harvest_season", cascade="all, delete-orphan")
    equipment_costs = relationship("EquipmentCost", back_populates="harvest_season", cascade="all, delete-orphan")
    expenses = relationship("HarvestExpense", back_populates="harvest_season", cascade="all, delete-orphan")
    revenue_entries = relationship("RevenueEntry", back_populates="harvest_season", cascade="all, delete-orphan")
    summary_calculations = relationship("SummaryCalculation", back_populates="harvest_season", cascade="all, delete-orphan")
