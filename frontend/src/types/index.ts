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
