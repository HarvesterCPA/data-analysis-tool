export interface User {
  id: number;
  email: string;
  name: string;
  state: string;
  billing_method: 'per_acre' | 'per_bushel' | 'per_hour';
  equipment_owned: boolean;
  equipment_details?: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at?: string;
}

export interface IncomeEntry {
  id: number;
  user_id: number;
  acres_harvested: number;
  rate_per_unit: number;
  total_earned: number;
  client_name?: string;
  notes?: string;
  harvest_date: string;
  created_at: string;
  updated_at?: string;
}

export interface ExpenseEntry {
  id: number;
  user_id: number;
  category: 'fuel' | 'labor' | 'equipment_lease' | 'equipment_repair' | 'equipment_depreciation' | 'rent_interest' | 'taxes' | 'other';
  amount: number;
  description?: string;
  notes?: string;
  expense_date: string;
  created_at: string;
  updated_at?: string;
}

export interface ProfitLossSummary {
  total_income: number;
  total_expenses: number;
  profit_loss: number;
  period_start: string;
  period_end: string;
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
  [key: string]: any; // Add index signature for Recharts compatibility
}

export interface PeerComparison {
  metric: string;
  user_value: number;
  state_average: number;
  national_average: number;
  state_percentile: number;
  national_percentile: number;
}

export interface AnalyticsResponse {
  profit_loss: ProfitLossSummary;
  expense_breakdown: CategoryBreakdown[];
  peer_comparisons: PeerComparison[];
  insights: string[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
  state: string;
  billing_method: 'per_acre' | 'per_bushel' | 'per_hour';
  equipment_owned: boolean;
  equipment_details?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Harvest Profit/Loss System Types
export enum PayCycle {
  WEEKLY = "weekly",
  BI_WEEKLY = "bi_weekly",
  SEMI_MONTHLY = "semi_monthly",
  MONTHLY = "monthly"
}

export enum EquipmentType {
  COMBINE = "combine",
  HEADER = "header",
  TRACTOR = "tractor",
  TRAILER = "trailer",
  TRUCK = "truck",
  CAMPER = "camper",
  OTHER = "other"
}

export enum OwnershipType {
  OWNED = "owned",
  LEASED = "leased",
  FINANCED = "financed"
}

export enum CropType {
  SMALL_GRAIN = "small_grain",
  CORN = "corn",
  COTTON = "cotton",
  SILAGE = "silage"
}

export enum PricingModel {
  PER_ACRE = "per_acre",
  PER_BUSHEL = "per_bushel",
  PER_MINUTE = "per_minute",
  PER_MILE = "per_mile",
  PER_HOUR = "per_hour"
}

export interface HarvestSeason {
  id: number;
  user_id: number;
  business_name: string;
  business_address?: string;
  contact_phone?: string;
  contact_email?: string;
  estimated_start_date?: string;
  estimated_end_date?: string;
  actual_start_date?: string;
  actual_end_date?: string;
  pay_cycle: PayCycle;
  interest_rate: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Equipment {
  id: number;
  harvest_season_id: number;
  name: string;
  equipment_type: EquipmentType;
  ownership_type: OwnershipType;
  purchase_date?: string;
  purchase_price?: number;
  current_value?: number;
  years_ownership?: number;
  lease_rate?: number;
  finance_rate?: number;
  down_payment?: number;
  monthly_payment?: number;
  working_days?: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface RevenueEntry {
  id: number;
  harvest_season_id: number;
  crop_type: CropType;
  pricing_model: PricingModel;
  client_name?: string;
  client_state?: string;
  quantity: number;
  rate: number;
  total_revenue: number;
  harvest_date: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface ProfitLossSummary {
  harvest_duration_days: number;
  acres_billed: number;
  total_revenue: number;
  total_expenses: number;
  gross_profit: number;
  net_profit: number;
  profit_margin: number;
  cost_per_acre: number;
  revenue_per_acre: number;
  profit_per_acre: number;
}

export interface CostBreakdown {
  equipment_cost: number;
  housing_cost: number;
  employee_cost: number;
  fuel_cost: number;
  maintenance_cost: number;
  insurance_cost: number;
  tax_cost: number;
  other_cost: number;
  total_cost: number;
}

export interface RevenueBreakdown {
  total_revenue: number;
  revenue_by_crop: Record<string, number>;
  revenue_per_acre: number;
}

export interface EquipmentAnalysis {
  equipment_cost_breakdown: Record<string, number>;
  cost_per_acre_by_equipment: Record<string, number>;
}
