from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CropType(str, enum.Enum):
    SMALL_GRAIN = "small_grain"
    CORN = "corn"
    COTTON = "cotton"
    SILAGE = "silage"

class PricingModel(str, enum.Enum):
    PER_ACRE = "per_acre"
    PER_BUSHEL = "per_bushel"
    PER_MINUTE = "per_minute"
    PER_MILE = "per_mile"
    PER_HOUR = "per_hour"

class RevenueEntry(Base):
    __tablename__ = "revenue_entries"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Revenue Details
    crop_type = Column(Enum(CropType), nullable=False)
    pricing_model = Column(Enum(PricingModel), nullable=False)
    
    # Client Information
    client_name = Column(String, nullable=True)
    client_state = Column(String, nullable=True)
    
    # Financial Information
    quantity = Column(Float, nullable=False)  # Acres, bushels, hours, etc.
    rate = Column(Float, nullable=False)  # Rate per unit
    total_revenue = Column(Float, nullable=False)
    
    # Date Information
    harvest_date = Column(DateTime, nullable=False)
    
    # Additional Details
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason", back_populates="revenue_entries")

class IncomeRateStructure(Base):
    __tablename__ = "income_rate_structures"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Rate Structure
    crop_type = Column(Enum(CropType), nullable=False)
    state = Column(String, nullable=False)
    
    # Pricing Models
    per_acre_rate = Column(Float, nullable=True)
    per_bushel_rate = Column(Float, nullable=True)
    per_minute_rate = Column(Float, nullable=True)
    per_mile_rate = Column(Float, nullable=True)
    per_hour_rate = Column(Float, nullable=True)
    
    # Additional Information
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason")
