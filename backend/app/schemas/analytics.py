from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ProfitLossSummary(BaseModel):
    total_income: float
    total_expenses: float
    profit_loss: float
    period_start: datetime
    period_end: datetime

class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float

class PeerComparison(BaseModel):
    metric: str
    user_value: float
    state_average: float
    national_average: float
    state_percentile: int
    national_percentile: int

class AnalyticsResponse(BaseModel):
    profit_loss: ProfitLossSummary
    expense_breakdown: List[CategoryBreakdown]
    peer_comparisons: List[PeerComparison]
    insights: List[str]
