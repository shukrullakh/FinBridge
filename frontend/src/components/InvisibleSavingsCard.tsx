import React, { useState } from 'react';
import { PiggyBank, Target, ArrowUpRight, Plus, Sparkles, Check } from 'lucide-react';
import { SavingsGoal } from '../types';
import { api, formatUZS } from '../services/api';

interface InvisibleSavingsCardProps {
  goals: SavingsGoal[];
  onGoalCreated?: () => void;
}

export const InvisibleSavingsCard: React.FC<InvisibleSavingsCardProps> = ({
  goals,
  onGoalCreated,
}) => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [newGoalName, setNewGoalName] = useState('');
  const [newTargetAmount, setNewTargetAmount] = useState('15000000');
  const [roundUpStep, setRoundUpStep] = useState('5000');
  const [creating, setCreating] = useState(false);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newGoalName || !newTargetAmount) return;
    setCreating(true);
    try {
      await api.createSavingsGoal({
        name: newGoalName,
        target_amount: parseFloat(newTargetAmount),
        round_up_step: parseFloat(roundUpStep),
      });
      setShowAddModal(false);
      setNewGoalName('');
      if (onGoalCreated) onGoalCreated();
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-50 text-teal-600">
              <PiggyBank className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Invisible Savings — Sezilmas Jamgʻarma</h2>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            Kundalik xarajatlaringizdan qolgan mayda pullar (1 000 yoki 5 000 UZS gacha yaxlitlanib) avtomatik jamgʻarmangizga yoʻnaltiriladi.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-slate-800 transition active:scale-95"
        >
          <Plus className="h-4 w-4" />
          <span>Yangi maqsad qoʻshish</span>
        </button>
      </div>

      {/* Round-up explanation pill */}
      <div className="mt-6 flex items-center gap-3 rounded-2xl bg-gradient-to-r from-teal-50 to-emerald-50 p-4 border border-teal-100">
        <Sparkles className="h-5 w-5 text-teal-600 flex-shrink-0" />
        <p className="text-xs text-teal-900 leading-relaxed font-medium">
          Masalan, <strong>43 200 UZS</strong> supermarket xaridi <strong>45 000 UZS</strong> ga yaxlitlanadi. 
          Oraliqdagi <strong>1 800 UZS</strong> avtomatik ravishda jamgʻarma maqsadiga oʻtkaziladi!
        </p>
      </div>

      {/* Goals list */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {goals.map((goal) => {
          const pct = Math.min(100, Math.round(goal.progress_percentage || 0));
          return (
            <div
              key={goal.id}
              className="relative overflow-hidden rounded-2xl border border-slate-200 bg-slate-50/60 p-5 transition hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-1.5">
                    <Target className="h-4 w-4 text-emerald-600" />
                    <h3 className="font-bold text-slate-900 text-sm">{goal.name}</h3>
                  </div>
                  <div className="mt-1 text-xs text-slate-500 font-medium">
                    Yaxlitlash qadami: <span className="font-bold text-slate-700">{formatUZS(goal.round_up_step)}</span>
                  </div>
                </div>

                <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-bold text-emerald-800">
                  {pct}%
                </span>
              </div>

              {/* Progress bar */}
              <div className="mt-4">
                <div className="h-2.5 w-full rounded-full bg-slate-200 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>

              {/* Amounts */}
              <div className="mt-4 flex items-center justify-between text-xs">
                <div>
                  <span className="text-slate-400">Yigʻilgan: </span>
                  <span className="font-bold text-slate-900">{formatUZS(goal.current_amount)}</span>
                </div>
                <div className="text-right">
                  <span className="text-slate-400">Maqsad: </span>
                  <span className="font-bold text-slate-900">{formatUZS(goal.target_amount)}</span>
                </div>
              </div>

              {goal.total_saved_from_roundups > 0 && (
                <div className="mt-3 rounded-lg bg-white px-3 py-1.5 text-[11px] font-semibold text-emerald-700 border border-emerald-100 flex items-center justify-between">
                  <span>Yaxlitlashdan yigʻilgan:</span>
                  <span>+{formatUZS(goal.total_saved_from_roundups)}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Add Goal Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-200">
            <h3 className="text-lg font-bold text-slate-900">Yangi Jamgʻarma Maqsadi</h3>
            <form onSubmit={handleCreate} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Maqsad nomi</label>
                <input
                  type="text"
                  value={newGoalName}
                  onChange={(e) => setNewGoalName(e.target.value)}
                  placeholder="Masalan: Ta'til uchun sayohat"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Kerakli summa (UZS)</label>
                <input
                  type="number"
                  value={newTargetAmount}
                  onChange={(e) => setNewTargetAmount(e.target.value)}
                  placeholder="15000000"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Yaxlitlash qadami</label>
                <select
                  value={roundUpStep}
                  onChange={(e) => setRoundUpStep(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                >
                  <option value="1000">1 000 UZS gacha</option>
                  <option value="5000">5 000 UZS gacha (Tavsiya etiladi)</option>
                  <option value="10000">10 000 UZS gacha</option>
                </select>
              </div>

              <div className="mt-6 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="rounded-xl border border-slate-300 px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50"
                >
                  Bekor qilish
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="rounded-xl bg-emerald-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-emerald-700"
                >
                  {creating ? 'Saqlanmoqda...' : 'Maqsadni Yaratish'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
