from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# Define billing method as a literal type for validation
BillingMethod = Literal["per_acre", "per_bushel", "per_hour"]

class UserBase(BaseModel):
    email: EmailStr
    name: str
    state: str
    billing_method: BillingMethod
    equipment_owned: bool = True
    equipment_details: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    state: Optional[str] = None
    billing_method: Optional[BillingMethod] = None
    equipment_owned: Optional[bool] = None
    equipment_details: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
