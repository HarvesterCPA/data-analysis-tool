from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models.harvest_season import HarvestSeason, PayCycle
from app.models.equipment import Equipment, EquipmentCost, OwnershipType
from app.models.harvest_expense import HarvestExpense, HousingExpense, EmployeeExpense
from app.models.revenue import RevenueEntry, CropType, PricingModel
from app.models.summary_calculation import SummaryCalculation
import json

class HarvestCalculationEngine:
    def __init__(self, db: Session):
        self.db = db

    def calculate_harvest_duration(self, harvest_season: HarvestSeason) -> float:
        """Calculate harvest duration in days"""
        if harvest_season.actual_start_date and harvest_season.actual_end_date:
            return (harvest_season.actual_end_date - harvest_season.actual_start_date).days
        elif harvest_season.estimated_start_date and harvest_season.estimated_end_date:
            return (harvest_season.estimated_end_date - harvest_season.estimated_start_date).days
        return 0.0

    def get_pay_periods(self, harvest_season: HarvestSeason) -> List[Dict[str, datetime]]:
        """Get all pay periods based on pay cycle"""
        start_date = harvest_season.actual_start_date or harvest_season.estimated_start_date
        end_date = harvest_season.actual_end_date or harvest_season.estimated_end_date
        
        if not start_date or not end_date:
            return []

        periods = []
        current_date = start_date
        
        if harvest_season.pay_cycle == PayCycle.WEEKLY:
            period_days = 7
        elif harvest_season.pay_cycle == PayCycle.BI_WEEKLY:
            period_days = 14
        elif harvest_season.pay_cycle == PayCycle.SEMI_MONTHLY:
            period_days = 15
        else:  # MONTHLY
            period_days = 30

        while current_date < end_date:
            period_end = min(current_date + timedelta(days=period_days), end_date)
            periods.append({
                'start': current_date,
                'end': period_end
            })
            current_date = period_end

        return periods

    def calculate_equipment_cost(self, equipment: Equipment, harvest_season: HarvestSeason) -> Dict[str, float]:
        """Calculate equipment cost based on ownership type and Excel formulas"""
        harvest_duration = self.calculate_harvest_duration(harvest_season)
        working_days = equipment.working_days or harvest_duration
        
        if equipment.ownership_type == OwnershipType.OWNED:
            # Owned equipment: depreciation + interest
            if equipment.purchase_price and equipment.years_ownership:
                annual_depreciation = equipment.purchase_price / equipment.years_ownership
                daily_depreciation = annual_depreciation / 365
                depreciation_cost = daily_depreciation * working_days
                
                # Interest on remaining value
                remaining_value = equipment.current_value or equipment.purchase_price
                annual_interest = remaining_value * (harvest_season.interest_rate / 100)
                daily_interest = annual_interest / 365
                interest_cost = daily_interest * working_days
                
                return {
                    'lease_cost': 0.0,
                    'interest_cost': interest_cost,
                    'depreciation_cost': depreciation_cost,
                    'total_cost': depreciation_cost + interest_cost
                }
        
        elif equipment.ownership_type == OwnershipType.LEASED:
            # Leased equipment: lease rate + interest
            if equipment.lease_rate:
                lease_cost = equipment.lease_rate * (working_days / 30)  # Monthly rate prorated
                return {
                    'lease_cost': lease_cost,
                    'interest_cost': 0.0,
                    'depreciation_cost': 0.0,
                    'total_cost': lease_cost
                }
        
        elif equipment.ownership_type == OwnershipType.FINANCED:
            # Financed equipment: monthly payment + interest
            if equipment.monthly_payment:
                payment_cost = equipment.monthly_payment * (working_days / 30)
                return {
                    'lease_cost': payment_cost,
                    'interest_cost': 0.0,
                    'depreciation_cost': 0.0,
                    'total_cost': payment_cost
                }
        
        return {
            'lease_cost': 0.0,
            'interest_cost': 0.0,
            'depreciation_cost': 0.0,
            'total_cost': 0.0
        }

    def calculate_period_costs(self, harvest_season: HarvestSeason) -> List[EquipmentCost]:
        """Calculate equipment costs for each pay period"""
        periods = self.get_pay_periods(harvest_season)
        equipment_costs = []
        
        for period in periods:
            for equipment in harvest_season.equipment:
                cost_data = self.calculate_equipment_cost(equipment, harvest_season)
                
                # Create equipment cost record
                equipment_cost = EquipmentCost(
                    harvest_season_id=harvest_season.id,
                    equipment_id=equipment.id,
                    period_start=period['start'],
                    period_end=period['end'],
                    lease_cost=cost_data['lease_cost'],
                    interest_cost=cost_data['interest_cost'],
                    depreciation_cost=cost_data['depreciation_cost'],
                    total_cost=cost_data['total_cost']
                )
                
                equipment_costs.append(equipment_cost)
        
        return equipment_costs

    def calculate_expense_totals(self, harvest_season: HarvestSeason) -> Dict[str, float]:
        """Calculate total expenses by category"""
        totals = {
            'fuel': 0.0,
            'maintenance': 0.0,
            'housing': 0.0,
            'employees': 0.0,
            'insurance': 0.0,
            'taxes': 0.0,
            'other': 0.0
        }
        
        for expense in harvest_season.expenses:
            if expense.category.value in totals:
                totals[expense.category.value] += expense.amount
        
        return totals

    def calculate_revenue_totals(self, harvest_season: HarvestSeason) -> Dict[str, Any]:
        """Calculate total revenue and breakdown by crop"""
        total_revenue = 0.0
        revenue_by_crop = {}
        
        for entry in harvest_season.revenue_entries:
            total_revenue += entry.total_revenue
            
            crop = entry.crop_type.value
            if crop not in revenue_by_crop:
                revenue_by_crop[crop] = 0.0
            revenue_by_crop[crop] += entry.total_revenue
        
        return {
            'total_revenue': total_revenue,
            'revenue_by_crop': revenue_by_crop
        }

    def calculate_profit_loss(self, harvest_season: HarvestSeason) -> SummaryCalculation:
        """Calculate comprehensive profit/loss summary"""
        # Calculate all components
        harvest_duration = self.calculate_harvest_duration(harvest_season)
        expense_totals = self.calculate_expense_totals(harvest_season)
        revenue_data = self.calculate_revenue_totals(harvest_season)
        
        # Calculate equipment costs
        equipment_costs = self.calculate_period_costs(harvest_season)
        total_equipment_cost = sum(cost.total_cost for cost in equipment_costs)
        
        # Calculate total expenses
        total_expenses = (
            total_equipment_cost +
            expense_totals['fuel'] +
            expense_totals['maintenance'] +
            expense_totals['housing'] +
            expense_totals['employees'] +
            expense_totals['insurance'] +
            expense_totals['taxes'] +
            expense_totals['other']
        )
        
        # Calculate profit/loss
        gross_profit = revenue_data['total_revenue'] - total_expenses
        profit_margin = (gross_profit / revenue_data['total_revenue'] * 100) if revenue_data['total_revenue'] > 0 else 0
        
        # Calculate per-acre metrics
        acres_billed = sum(entry.quantity for entry in harvest_season.revenue_entries 
                          if entry.pricing_model == PricingModel.PER_ACRE)
        
        cost_per_acre = total_expenses / acres_billed if acres_billed > 0 else 0
        revenue_per_acre = revenue_data['total_revenue'] / acres_billed if acres_billed > 0 else 0
        profit_per_acre = profit_per_acre = revenue_per_acre - cost_per_acre
        
        # Create summary calculation
        summary = SummaryCalculation(
            harvest_season_id=harvest_season.id,
            harvest_duration_days=harvest_duration,
            acres_billed=acres_billed,
            total_equipment_cost=total_equipment_cost,
            total_housing_cost=expense_totals['housing'],
            total_employee_cost=expense_totals['employees'],
            total_fuel_cost=expense_totals['fuel'],
            total_maintenance_cost=expense_totals['maintenance'],
            total_insurance_cost=expense_totals['insurance'],
            total_tax_cost=expense_totals['taxes'],
            total_other_cost=expense_totals['other'],
            total_expenses=total_expenses,
            total_revenue=revenue_data['total_revenue'],
            revenue_by_crop=json.dumps(revenue_data['revenue_by_crop']),
            gross_profit=gross_profit,
            net_profit=gross_profit,  # Assuming no additional taxes/fees
            profit_margin=profit_margin,
            cost_per_acre=cost_per_acre,
            revenue_per_acre=revenue_per_acre,
            profit_per_acre=profit_per_acre,
            equipment_cost_breakdown=json.dumps({
                equipment.name: sum(cost.total_cost for cost in equipment_costs 
                                  if cost.equipment_id == equipment.id)
                for equipment in harvest_season.equipment
            })
        )
        
        return summary

    def recalculate_harvest_season(self, harvest_season_id: int) -> SummaryCalculation:
        """Recalculate all metrics for a harvest season"""
        harvest_season = self.db.query(HarvestSeason).filter(
            HarvestSeason.id == harvest_season_id
        ).first()
        
        if not harvest_season:
            raise ValueError("Harvest season not found")
        
        # Delete existing calculations
        self.db.query(SummaryCalculation).filter(
            SummaryCalculation.harvest_season_id == harvest_season_id
        ).delete()
        
        # Calculate new summary
        summary = self.calculate_profit_loss(harvest_season)
        
        # Save to database
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        
        return summary
