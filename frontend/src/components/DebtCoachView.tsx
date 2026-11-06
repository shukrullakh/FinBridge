import React, { useState, useEffect } from 'react';
import { 
  Scale, 
  TrendingUp, 
  CheckCircle2, 
  ArrowRight, 
  AlertCircle,
  Sparkles,
  Zap
} from 'lucide-react';
import { Debt, DebtPlanResponse } from '../types';
import { api, formatUZS } from '../services/api';

interface DebtCoachViewProps {
  debts: Debt[];
}

export const DebtCoachView: React.FC<DebtCoachViewProps> = ({ debts }) => {
  const [extraPayment, setExtraPayment] = useState<number>(500000);
  const [plan, setPlan] = useState<DebtPlanResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeStrategyTab, setActiveStrategyTab] = useState<'snowball' | 'avalanche'>('snowball');

  useEffect(() => {
    fetchPlan(extraPayment);
  }, [extraPayment]);

  const fetchPlan = async (extra: number) => {
    setLoading(true);
    try {
      const res = await api.calculateDebtPlan(extra);
      setPlan(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
              <Scale className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Debt Coach — Qarzlarni Oqilona Toʻlash</h2>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            Qarz va muddatli toʻlovlaringizni Snowball (psixologik intizom) va Avalanche (foizdan maksimal tejash) strategiyalari orqali taqqoslang.
          </p>
        </div>

        {/* Extra budget input */}
        <div className="flex items-center gap-3 rounded-2xl bg-slate-50 p-2 border border-slate-200">
          <span className="text-xs font-bold text-slate-600 pl-2">Qoʻshimcha oylik toʻlov:</span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setExtraPayment(Math.max(0, extraPayment - 200000))}
              className="h-7 w-7 rounded-lg bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-100"
            >
              -
            </button>
            <span className="min-w-[110px] text-center text-xs font-extrabold text-slate-900">
              {formatUZS(extraPayment)}
            </span>
            <button
              onClick={() => setExtraPayment(extraPayment + 200000)}
              className="h-7 w-7 rounded-lg bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-100"
            >
              +
            </button>
          </div>
        </div>
      </div>

      {/* AI / Smart Recommendation Banner */}
      {plan && (
        <div className="mt-6 flex items-start gap-3 rounded-2xl bg-gradient-to-r from-blue-50 via-indigo-50 to-emerald-50 p-4 border border-blue-100">
          <Sparkles className="h-5 w-5 text-indigo-600 flex-shrink-0 mt-0.5" />
          <div>
            <div className="text-xs font-extrabold uppercase tracking-wide text-indigo-900">
              {plan.best_strategy_recommendation}
            </div>
            <p className="mt-1 text-xs text-slate-600">{plan.summary_insight}</p>
          </div>
        </div>
      )}

      {/* Strategy Selector Tabs */}
      <div className="mt-6 flex border-b border-slate-200">
        <button
          onClick={() => setActiveStrategyTab('snowball')}
          className={`flex items-center gap-2 border-b-2 px-5 py-3 text-sm font-bold transition ${
            activeStrategyTab === 'snowball'
              ? 'border-emerald-600 text-emerald-800'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <span>Snowball (Qor toʻpi)</span>
          <span className="rounded bg-emerald-100 px-1.5 py-0.5 text-[10px] text-emerald-800">
            Motivatsiya
          </span>
        </button>
        <button
          onClick={() => setActiveStrategyTab('avalanche')}
          className={`flex items-center gap-2 border-b-2 px-5 py-3 text-sm font-bold transition ${
            activeStrategyTab === 'avalanche'
              ? 'border-blue-600 text-blue-800'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <span>Avalanche (Qor koʻchkisi)</span>
          <span className="rounded bg-blue-100 px-1.5 py-0.5 text-[10px] text-blue-800">
            Maksimal Tejov
          </span>
        </button>
      </div>

      {/* Strategy Detail View */}
      {plan && (
        <div className="mt-6">
          {(() => {
            const current = activeStrategyTab === 'snowball' ? plan.snowball : plan.avalanche;
            const isSnowball = activeStrategyTab === 'snowball';
            return (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <span className="text-xs font-semibold text-slate-500">Qarzdan qutilish muddati:</span>
                    <div className="mt-1 text-2xl font-bold text-slate-900">{current.total_months} oy</div>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <span className="text-xs font-semibold text-slate-500">Jami toʻlanadigan foiz:</span>
                    <div className="mt-1 text-2xl font-bold text-rose-600">{formatUZS(current.total_interest_paid)}</div>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <span className="text-xs font-semibold text-slate-500">Jami yakuniy toʻlov:</span>
                    <div className="mt-1 text-2xl font-bold text-slate-900">{formatUZS(current.total_amount_paid)}</div>
                  </div>
                </div>

                <div className="text-xs text-slate-600 leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                  {current.description}
                </div>

                {/* Payoff Order Timeline */}
                <div>
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
                    Qarzlarni yopish ketma-ketligi:
                  </h4>
                  <div className="space-y-2">
                    {current.order_of_payoff.map((item, idx) => (
                      <div
                        key={item.debt_id}
                        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
                      >
                        <div className="flex items-center gap-3">
                          <span className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-extrabold ${
                            idx === 0 
                              ? 'bg-emerald-600 text-white' 
                              : 'bg-slate-100 text-slate-600'
                          }`}>
                            #{item.payoff_order}
                          </span>
                          <div>
                            <div className="text-sm font-bold text-slate-900">{item.debt_name}</div>
                            <div className="text-xs text-slate-500">
                              Yillik foiz: <span className="font-semibold">{item.interest_rate}%</span> | 
                              Oylik min toʻlov: <span className="font-semibold">{formatUZS(item.minimum_payment)}</span>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-6 sm:text-right">
                          <div>
                            <div className="text-[11px] text-slate-400">Qoldiq qarz:</div>
                            <div className="text-sm font-bold text-slate-900">{formatUZS(item.balance)}</div>
                          </div>
                          <div className="rounded-lg bg-emerald-50 px-3 py-1.5 border border-emerald-100">
                            <div className="text-[10px] font-bold text-emerald-800 uppercase">Yopilish muddati:</div>
                            <div className="text-xs font-extrabold text-emerald-700">~{item.estimated_months_to_payoff} oyda</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
};
