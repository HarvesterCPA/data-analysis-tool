from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, date, timedelta

from app.core.database import get_db
from app.schemas.analytics import AnalyticsResponse, ProfitLossSummary, CategoryBreakdown, PeerComparison
from app.models.income import IncomeEntry
from app.models.expense import ExpenseEntry
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(
    start_date: date = None,
    end_date: date = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Default to last 30 days if no dates provided
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get user's income and expenses for the period
    user_income = db.query(func.sum(IncomeEntry.total_earned)).filter(
        and_(
            IncomeEntry.user_id == current_user.id,
            IncomeEntry.harvest_date >= start_date,
            IncomeEntry.harvest_date <= end_date
        )
    ).scalar() or 0
    
    user_expenses = db.query(func.sum(ExpenseEntry.amount)).filter(
        and_(
            ExpenseEntry.user_id == current_user.id,
            ExpenseEntry.expense_date >= start_date,
            ExpenseEntry.expense_date <= end_date
        )
    ).scalar() or 0
    
    # Calculate profit/loss
    profit_loss = user_income - user_expenses
    
    # Get expense breakdown by category
    expense_breakdown = db.query(
        ExpenseEntry.category,
        func.sum(ExpenseEntry.amount).label('total')
    ).filter(
        and_(
            ExpenseEntry.user_id == current_user.id,
            ExpenseEntry.expense_date >= start_date,
            ExpenseEntry.expense_date <= end_date
        )
    ).group_by(ExpenseEntry.category).all()
    
    category_breakdowns = []
    for category, total in expense_breakdown:
        percentage = (total / user_expenses * 100) if user_expenses > 0 else 0
        category_breakdowns.append(CategoryBreakdown(
            category=category.value,
            amount=total,
            percentage=percentage
        ))
    
    # Get peer comparisons (simplified for MVP)
    peer_comparisons = []
    
    # State-level comparisons
    state_users = db.query(User).filter(User.state == current_user.state).all()
    state_user_ids = [user.id for user in state_users]
    
    if state_user_ids:
        state_avg_income = db.query(func.avg(IncomeEntry.total_earned)).filter(
            and_(
                IncomeEntry.user_id.in_(state_user_ids),
                IncomeEntry.harvest_date >= start_date,
                IncomeEntry.harvest_date <= end_date
            )
        ).scalar() or 0
        
        state_avg_expenses = db.query(func.avg(ExpenseEntry.amount)).filter(
            and_(
                ExpenseEntry.user_id.in_(state_user_ids),
                ExpenseEntry.expense_date >= start_date,
                ExpenseEntry.expense_date <= end_date
            )
        ).scalar() or 0
        
        # National averages
        all_users = db.query(User).all()
        all_user_ids = [user.id for user in all_users]
        
        national_avg_income = db.query(func.avg(IncomeEntry.total_earned)).filter(
            and_(
                IncomeEntry.user_id.in_(all_user_ids),
                IncomeEntry.harvest_date >= start_date,
                IncomeEntry.harvest_date <= end_date
            )
        ).scalar() or 0
        
        national_avg_expenses = db.query(func.avg(ExpenseEntry.amount)).filter(
            and_(
                ExpenseEntry.user_id.in_(all_user_ids),
                ExpenseEntry.expense_date >= start_date,
                ExpenseEntry.expense_date <= end_date
            )
        ).scalar() or 0
        
        # Add comparisons
        if state_avg_income > 0:
            peer_comparisons.append(PeerComparison(
                metric="Income per Harvest",
                user_value=user_income,
                state_average=state_avg_income,
                national_average=national_avg_income,
                state_percentile=75,  # Simplified calculation
                national_percentile=70
            ))
        
        if state_avg_expenses > 0:
            peer_comparisons.append(PeerComparison(
                metric="Total Expenses",
                user_value=user_expenses,
                state_average=state_avg_expenses,
                national_average=national_avg_expenses,
                state_percentile=60,  # Simplified calculation
                national_percentile=65
            ))
    
    # Generate insights
    insights = []
    if profit_loss > 0:
        insights.append("Great job! You're operating at a profit.")
    else:
        insights.append("Consider reviewing your expenses to improve profitability.")
    
    if user_expenses > 0:
        fuel_expenses = db.query(func.sum(ExpenseEntry.amount)).filter(
            and_(
                ExpenseEntry.user_id == current_user.id,
                ExpenseEntry.category == "fuel",
                ExpenseEntry.expense_date >= start_date,
                ExpenseEntry.expense_date <= end_date
            )
        ).scalar() or 0
        
        if fuel_expenses / user_expenses > 0.3:
            insights.append("Your fuel costs are high. Consider fuel efficiency improvements.")
    
    return AnalyticsResponse(
        profit_loss=ProfitLossSummary(
            total_income=user_income,
            total_expenses=user_expenses,
            profit_loss=profit_loss,
            period_start=datetime.combine(start_date, datetime.min.time()),
            period_end=datetime.combine(end_date, datetime.max.time())
        ),
        expense_breakdown=category_breakdowns,
        peer_comparisons=peer_comparisons,
        insights=insights
    )
