import {
  DashboardSummary,
  Transaction,
  BudgetLimit,
  SavingsGoal,
  Debt,
  DebtPlanResponse,
  BehaviorScoreResponse,
  SmartPauseEvaluateRequest,
  SmartPauseEvaluateResponse
} from '../types';

const API_BASE = '/api/v1';

export const formatUZS = (value: number | string | undefined | null): string => {
  if (value === undefined || value === null) return '0 UZS';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '0 UZS';
  return new Intl.NumberFormat('uz-UZ').format(Math.round(num)) + ' UZS';
};

export const api = {
  // Dashboard
  getDashboardSummary: async (): Promise<DashboardSummary> => {
    const res = await fetch(`${API_BASE}/dashboard/summary`);
    if (!res.ok) throw new Error('Dashboard maʼlumotlarini yuklashda xatolik');
    return res.json();
  },

  resetDemoData: async (): Promise<void> => {
    const res = await fetch(`${API_BASE}/dashboard/reset-demo`, { method: 'POST' });
    if (!res.ok) throw new Error('Demoni qayta yuklashda xatolik');
  },

  // Transactions
  getTransactions: async (type?: string, category?: string): Promise<Transaction[]> => {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    if (category) params.append('category', category);
    const res = await fetch(`${API_BASE}/transactions?${params.toString()}`);
    if (!res.ok) throw new Error('Tranzaksiyalarni yuklashda xatolik');
    return res.json();
  },

  createTransaction: async (data: Omit<Transaction, 'id'>, applyRoundUp = true) => {
    const res = await fetch(`${API_BASE}/transactions?apply_round_up=${applyRoundUp}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Tranzaksiya qoʻshishda xatolik');
    return res.json();
  },

  deleteTransaction: async (id: string) => {
    const res = await fetch(`${API_BASE}/transactions/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Tranzaksiyani oʻchirishda xatolik');
    return res.json();
  },

  // Budgets
  getBudgets: async (): Promise<BudgetLimit[]> => {
    const res = await fetch(`${API_BASE}/budgets`);
    if (!res.ok) throw new Error('Limitlarni yuklashda xatolik');
    return res.json();
  },

  createOrUpdateBudget: async (data: { category: string; limit_amount: number }) => {
    const res = await fetch(`${API_BASE}/budgets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Limitni saqlashda xatolik');
    return res.json();
  },

  // Smart Pause
  evaluateSmartPause: async (payload: SmartPauseEvaluateRequest): Promise<SmartPauseEvaluateResponse> => {
    const res = await fetch(`${API_BASE}/smart-pause/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Xaridni baholashda xatolik');
    return res.json();
  },

  recordDecision: async (decision: any) => {
    const res = await fetch(`${API_BASE}/smart-pause/decisions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(decision),
    });
    if (!res.ok) throw new Error('Qarorni saqlashda xatolik');
    return res.json();
  },

  // Savings
  getSavingsGoals: async (): Promise<SavingsGoal[]> => {
    const res = await fetch(`${API_BASE}/savings/goals`);
    if (!res.ok) throw new Error('Maqsadlarni yuklashda xatolik');
    return res.json();
  },

  createSavingsGoal: async (data: any) => {
    const res = await fetch(`${API_BASE}/savings/goals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Maqsad yaratishda xatolik');
    return res.json();
  },

  // Debts
  getDebts: async (): Promise<Debt[]> => {
    const res = await fetch(`${API_BASE}/debts`);
    if (!res.ok) throw new Error('Qarzlarni yuklashda xatolik');
    return res.json();
  },

  addDebt: async (data: any) => {
    const res = await fetch(`${API_BASE}/debts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Qarz qoʻshishda xatolik');
    return res.json();
  },

  calculateDebtPlan: async (extraMonthlyBudget: number): Promise<DebtPlanResponse> => {
    const res = await fetch(`${API_BASE}/debts/plan?extra_monthly_budget=${extraMonthlyBudget}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Qarz toʻlov rejasini hisoblashda xatolik');
    return res.json();
  },

  // Behavior Score
  getBehaviorScore: async (): Promise<BehaviorScoreResponse> => {
    const res = await fetch(`${API_BASE}/behavior-score/current`);
    if (!res.ok) throw new Error('Moliyaviy ballni yuklashda xatolik');
    return res.json();
  },
};
