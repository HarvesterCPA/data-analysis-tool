from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class BillingMethod(str, enum.Enum):
    PER_ACRE = "per_acre"
    PER_BUSHEL = "per_bushel"
    PER_HOUR = "per_hour"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    state = Column(String, nullable=False)
    billing_method = Column(Enum(BillingMethod), nullable=False)
    equipment_owned = Column(Boolean, default=True)
    equipment_details = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    income_entries = relationship("IncomeEntry", back_populates="user")
    expense_entries = relationship("ExpenseEntry", back_populates="user")
