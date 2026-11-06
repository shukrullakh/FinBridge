import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Wallet, 
  PiggyBank, 
  Scale, 
  Award, 
  ShieldAlert, 
  Calendar,
  AlertCircle,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { Navbar } from './components/Navbar';
import { MetricCard } from './components/MetricCard';
import { SmartPauseModal } from './components/SmartPauseModal';
import { InvisibleSavingsCard } from './components/InvisibleSavingsCard';
import { DebtCoachView } from './components/DebtCoachView';
import { BehaviorScoreGauge } from './components/BehaviorScoreGauge';
import { TransactionList } from './components/TransactionList';
import { api, formatUZS } from './services/api';
import { DashboardSummary, BehaviorScoreResponse, Debt, SavingsGoal, Transaction } from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [dashboardData, setDashboardData] = useState<DashboardSummary | null>(null);
  const [scoreData, setScoreData] = useState<BehaviorScoreResponse | null>(null);
  const [debts, setDebts] = useState<Debt[]>([]);
  const [goals, setGoals] = useState<SavingsGoal[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isResetting, setIsResetting] = useState<boolean>(false);

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    try {
      setLoading(true);
      const [dash, sc, dList, gList, tList] = await Promise.all([
        api.getDashboardSummary(),
        api.getBehaviorScore(),
        api.getDebts(),
        api.getSavingsGoals(),
        api.getTransactions(),
      ]);
      setDashboardData(dash);
      setScoreData(sc);
      setDebts(dList);
      setGoals(gList);
      setTransactions(tList);
    } catch (err) {
      console.error('Data loading error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetDemo = async () => {
    setIsResetting(true);
    try {
      await api.resetDemoData();
      await loadAllData();
    } catch (err) {
      console.error(err);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onResetDemo={handleResetDemo}
        isResetting={isResetting}
      />

      {/* Main Content Area */}
      <main className="flex-1 mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
        {/* Hackathon banner */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-2xl bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 px-6 py-4 text-white shadow-lg shadow-emerald-950/20">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 text-emerald-400 backdrop-blur-md">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-extrabold tracking-tight">FinBridge — SMARTMIND</span>
                <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] font-bold text-emerald-300 border border-emerald-400/30">
                  Hackathon MVP
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Faqat pulingizni hisoblab bormang. Moliyaviy xulq-atvoringizni tarbiyalang.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('smart-pause')}
              className="flex items-center gap-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 px-4 py-2 text-xs font-bold transition shadow-md active:scale-95"
            >
              <ShieldAlert className="h-4 w-4" />
              <span>Smart Pause Sinab Koʻrish</span>
            </button>
          </div>
        </div>

        {/* Tab 1: Dashboard */}
        {activeTab === 'dashboard' && dashboardData && (
          <div className="space-y-8">
            {/* KPI Cards Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="Oylik Daromad"
                value={formatUZS(dashboardData.total_income)}
                icon={TrendingUp}
                variant="emerald"
                subtitle="Reja boʻyicha oʻz vaqtida"
              />
              <MetricCard
                title="Oylik Xarajatlar"
                value={formatUZS(dashboardData.total_expenses)}
                icon={TrendingDown}
                variant="rose"
                subtitle={`${dashboardData.categories_breakdown.length} ta toifada`}
              />
              <MetricCard
                title="Mavjud Erkin Balans"
                value={formatUZS(dashboardData.net_balance)}
                icon={Wallet}
                variant="blue"
                subtitle={`Jamgʻarma hissasi: ${dashboardData.savings_rate_percentage}%`}
              />
              <MetricCard
                title="Round-Up Jamgʻarma"
                value={formatUZS(dashboardData.total_simulated_savings)}
                icon={PiggyBank}
                variant="amber"
                subtitle="Sezilmas yaxlitlashdan"
              />
            </div>

            {/* Split Grid: Category Spending vs Upcoming Debts & Behavior Score */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Category Spending with Red Line Limits */}
              <div className="lg:col-span-7 rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">Xarajat Toifalari va Qizil Chiziqlar</h3>
                    <p className="text-xs text-slate-500">Belgilangan oylik chegaralarga rioya qilinishi</p>
                  </div>
                  <span className="text-xs font-semibold text-slate-400">Joriy oy</span>
                </div>

                <div className="mt-6 space-y-4">
                  {dashboardData.categories_breakdown.map((item) => (
                    <div key={item.category} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-800">{item.category}</span>
                        <div className="flex items-center gap-2">
                          <span className="font-extrabold text-slate-900">{formatUZS(item.total_amount)}</span>
                          {item.limit_amount && (
                            <span className="text-slate-400 font-medium">/ {formatUZS(item.limit_amount)}</span>
                          )}
                          {item.is_over_limit && (
                            <span className="rounded bg-rose-100 px-1.5 py-0.5 text-[10px] font-bold text-rose-700">
                              Limitdan oshdi!
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            item.is_over_limit
                              ? 'bg-rose-500'
                              : item.percentage > 75
                              ? 'bg-amber-500'
                              : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(100, item.percentage * 2)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Behavior Score Mini Widget & Upcoming Debts */}
              <div className="lg:col-span-5 space-y-6">
                {/* Score Teaser */}
                <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-emerald-50/50 p-6 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Xulq-atvor Bali</span>
                      <div className="mt-1 flex items-baseline gap-2">
                        <span className="text-3xl font-black text-slate-900">{dashboardData.current_behavior_score}</span>
                        <span className="text-sm font-bold text-slate-400">/ 100</span>
                      </div>
                    </div>
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-600 text-white text-xl font-black shadow-md shadow-emerald-500/20">
                      {dashboardData.score_grade}
                    </div>
                  </div>

                  <p className="mt-3 text-xs text-slate-600 leading-relaxed">
                    Xarajatlaringiz va jamgʻarmangiz intizomiga qarab avtomatik yangilanadi.
                  </p>

                  <button
                    onClick={() => setActiveTab('score')}
                    className="mt-4 flex w-full items-center justify-center gap-1.5 rounded-xl border border-emerald-200 bg-white py-2 text-xs font-bold text-emerald-800 hover:bg-emerald-50 transition"
                  >
                    <span>Toʻliq tahlilni koʻrish</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>
                </div>

                {/* Upcoming Debts */}
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <div className="flex items-center gap-2">
                      <Scale className="h-4 w-4 text-blue-600" />
                      <h4 className="text-sm font-bold text-slate-900">Yaqinlashayotgan Toʻlovlar</h4>
                    </div>
                    <span className="text-xs font-semibold text-slate-400">Jami: {formatUZS(dashboardData.total_debt_balance)}</span>
                  </div>

                  <div className="mt-3 space-y-2.5">
                    {dashboardData.upcoming_debts.slice(0, 3).map((debt) => (
                      <div key={debt.id} className="flex items-center justify-between rounded-xl bg-slate-50 p-3 text-xs">
                        <div>
                          <div className="font-bold text-slate-900">{debt.name}</div>
                          <div className="text-[11px] text-slate-400">{debt.due_date}</div>
                        </div>
                        <span className="font-extrabold text-slate-800">{formatUZS(debt.amount)}</span>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={() => setActiveTab('debt-coach')}
                    className="mt-4 flex w-full items-center justify-center gap-1.5 rounded-xl border border-slate-200 bg-slate-50 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 transition"
                  >
                    <span>Debt Coach Rejasiga oʻtish</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            </div>

            {/* Transactions Section */}
            <TransactionList
              transactions={transactions}
              onTransactionUpdated={loadAllData}
            />
          </div>
        )}

        {/* Tab 2: Smart Pause */}
        {activeTab === 'smart-pause' && (
          <div className="space-y-6">
            <SmartPauseModal onSuccess={loadAllData} />
          </div>
        )}

        {/* Tab 3: Invisible Savings */}
        {activeTab === 'savings' && (
          <div className="space-y-6">
            <InvisibleSavingsCard goals={goals} onGoalCreated={loadAllData} />
          </div>
        )}

        {/* Tab 4: Debt Coach */}
        {activeTab === 'debt-coach' && (
          <div className="space-y-6">
            <DebtCoachView debts={debts} />
          </div>
        )}

        {/* Tab 5: Behavior Score */}
        {activeTab === 'score' && (
          <div className="space-y-6">
            <BehaviorScoreGauge scoreData={scoreData} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white py-6">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <div>
            © 2026 FinBridge (SMARTMIND Concept). Barcha huquqlar himoyalangan.
          </div>
          <div className="flex items-center gap-4">
            <span>Valyuta: Oʻzbekiston soʻmi (UZS)</span>
            <span>•</span>
            <span>Hackathon MVP Baseline</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
