from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class EquipmentType(str, enum.Enum):
    COMBINE = "combine"
    HEADER = "header"
    TRACTOR = "tractor"
    TRAILER = "trailer"
    TRUCK = "truck"
    CAMPER = "camper"
    OTHER = "other"

class OwnershipType(str, enum.Enum):
    OWNED = "owned"
    LEASED = "leased"
    FINANCED = "financed"

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Equipment Details
    name = Column(String, nullable=False)
    equipment_type = Column(Enum(EquipmentType), nullable=False)
    ownership_type = Column(Enum(OwnershipType), nullable=False)
    
    # Financial Information
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    years_ownership = Column(Float, nullable=True)
    
    # Lease/Finance Information
    lease_rate = Column(Float, nullable=True)  # Monthly lease rate
    finance_rate = Column(Float, nullable=True)  # Annual finance rate
    down_payment = Column(Float, nullable=True)
    monthly_payment = Column(Float, nullable=True)
    
    # Working Days
    working_days = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason", back_populates="equipment")
    equipment_costs = relationship("EquipmentCost", back_populates="equipment", cascade="all, delete-orphan")

class EquipmentCost(Base):
    __tablename__ = "equipment_costs"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    
    # Cost Details
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Cost Components
    lease_cost = Column(Float, default=0.0)
    interest_cost = Column(Float, default=0.0)
    depreciation_cost = Column(Float, default=0.0)
    total_cost = Column(Float, nullable=False)
    
    # Per-acre calculations
    acres_worked = Column(Float, nullable=True)
    cost_per_acre = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason", back_populates="equipment_costs")
    equipment = relationship("Equipment", back_populates="equipment_costs")
