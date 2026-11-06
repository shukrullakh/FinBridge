export interface Transaction {
  id: string;
  amount: number;
  type: 'income' | 'expense';
  category: string;
  date: string;
  note?: string;
  source?: string;
}

export interface CategorySpending {
  category: string;
  total_amount: number;
  percentage: number;
  limit_amount?: number;
  is_over_limit: boolean;
}

export interface BudgetLimit {
  id: string;
  category: string;
  limit_amount: number;
  period: string;
  spent_amount: number;
  remaining_amount: number;
  usage_percentage: number;
  is_exceeded: boolean;
}

export interface SavingsGoal {
  id: string;
  name: string;
  target_amount: number;
  current_amount: number;
  total_saved_from_roundups: number;
  round_up_step: number;
  target_date?: string;
  progress_percentage: number;
  is_achieved: boolean;
}

export interface PayoffPlanItem {
  debt_id: string;
  debt_name: string;
  balance: number;
  interest_rate: number;
  minimum_payment: number;
  payoff_order: number;
  estimated_months_to_payoff: number;
  total_interest_estimated: number;
}

export interface StrategyComparison {
  strategy_name: string;
  description: string;
  total_months: number;
  total_interest_paid: number;
  total_amount_paid: number;
  order_of_payoff: PayoffPlanItem[];
  advantages: string[];
}

export interface DebtPlanResponse {
  monthly_budget_allocated: number;
  snowball: StrategyComparison;
  avalanche: StrategyComparison;
  best_strategy_recommendation: string;
  summary_insight: string;
}

export interface Debt {
  id: string;
  name: string;
  balance: number;
  interest_rate: number;
  minimum_payment: number;
  due_date?: string;
  type: 'bank_loan' | 'installment' | 'personal';
  notes?: string;
}

export interface DimensionDetail {
  name: string;
  key: string;
  score: number;
  weight_percentage: number;
  status: string;
  explanation: string;
  recommendation: string;
}

export interface BehaviorScoreResponse {
  total_score: number;
  grade: string;
  grade_label: string;
  has_sufficient_data: boolean;
  dimensions: DimensionDetail[];
  summary_insights: string[];
  disclaimer: string;
}

export interface UpcomingDebtPayment {
  id: string;
  name: string;
  amount: number;
  due_date: string;
}

export interface DashboardSummary {
  currency: string;
  period: string;
  total_income: number;
  total_expenses: number;
  net_balance: number;
  savings_rate_percentage: number;
  categories_breakdown: CategorySpending[];
  recent_transactions: Transaction[];
  active_goals: SavingsGoal[];
  total_simulated_savings: number;
  total_debt_balance: number;
  upcoming_debts: UpcomingDebtPayment[];
  current_behavior_score: number;
  score_grade: string;
}

export interface SmartPauseEvaluateRequest {
  amount: number;
  category: string;
  description?: string;
}

export interface SmartPauseEvaluateResponse {
  is_risky: boolean;
  risk_level: 'safe' | 'moderate' | 'high';
  reasons: string[];
  category: string;
  amount: number;
  category_limit?: number;
  current_category_spent: number;
  projected_category_spent: number;
  current_balance: number;
  projected_balance: number;
  cooling_off_minutes: number;
  reflection_prompts: string[];
  impact_summary: string;
}
