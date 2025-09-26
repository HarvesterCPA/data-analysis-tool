from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class SummaryCalculation(Base):
    __tablename__ = "summary_calculations"

    id = Column(Integer, primary_key=True, index=True)
    harvest_season_id = Column(Integer, ForeignKey("harvest_seasons.id"), nullable=False)
    
    # Harvest Summary
    harvest_duration_days = Column(Float, nullable=True)
    acres_billed = Column(Float, nullable=True)
    
    # Cost Breakdown
    total_equipment_cost = Column(Float, default=0.0)
    total_housing_cost = Column(Float, default=0.0)
    total_employee_cost = Column(Float, default=0.0)
    total_fuel_cost = Column(Float, default=0.0)
    total_maintenance_cost = Column(Float, default=0.0)
    total_insurance_cost = Column(Float, default=0.0)
    total_tax_cost = Column(Float, default=0.0)
    total_other_cost = Column(Float, default=0.0)
    total_expenses = Column(Float, default=0.0)
    
    # Revenue Summary
    total_revenue = Column(Float, default=0.0)
    revenue_by_crop = Column(Text, nullable=True)  # JSON string
    
    # Profit/Loss
    gross_profit = Column(Float, default=0.0)
    net_profit = Column(Float, default=0.0)
    profit_margin = Column(Float, default=0.0)
    
    # Per-acre Analysis
    cost_per_acre = Column(Float, default=0.0)
    revenue_per_acre = Column(Float, default=0.0)
    profit_per_acre = Column(Float, default=0.0)
    
    # Equipment Analysis
    equipment_cost_breakdown = Column(Text, nullable=True)  # JSON string
    
    # Calculation timestamp
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    harvest_season = relationship("HarvestSeason", back_populates="summary_calculations")
