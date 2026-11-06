import React, { useState } from 'react';
import { 
  ArrowDownLeft, 
  ArrowUpRight, 
  Plus, 
  Trash2, 
  Sparkles,
  ShoppingBag,
  Car,
  Utensils,
  Smartphone,
  Home,
  Briefcase,
  HelpCircle
} from 'lucide-react';
import { Transaction } from '../types';
import { api, formatUZS } from '../services/api';

interface TransactionListProps {
  transactions: Transaction[];
  onTransactionUpdated?: () => void;
}

export const TransactionList: React.FC<TransactionListProps> = ({
  transactions,
  onTransactionUpdated,
}) => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [amount, setAmount] = useState('');
  const [type, setType] = useState<'income' | 'expense'>('expense');
  const [category, setCategory] = useState('Oziq-ovqat');
  const [note, setNote] = useState('');
  const [applyRoundUp, setApplyRoundUp] = useState(true);
  const [loading, setLoading] = useState(false);

  const getCategoryIcon = (cat: string) => {
    switch (cat.toLowerCase()) {
      case 'oziq-ovqat': return ShoppingBag;
      case 'transport': return Car;
      case 'restoran va kafe': return Utensils;
      case 'aloqa va internet': return Smartphone;
      case 'kommunal': return Home;
      case 'maosh':
      case 'frilans': return Briefcase;
      default: return HelpCircle;
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;
    setLoading(true);
    try {
      await api.createTransaction(
        {
          amount: parseFloat(amount),
          type,
          category,
          note: note || undefined,
          date: new Date().toISOString(),
          source: 'Plastik karta',
        },
        type === 'expense' && applyRoundUp
      );
      setShowAddModal(false);
      setAmount('');
      setNote('');
      if (onTransactionUpdated) onTransactionUpdated();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deleteTransaction(id);
      if (onTransactionUpdated) onTransactionUpdated();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <h3 className="text-lg font-bold text-slate-900">Oxirgi Tranzaksiyalar</h3>
          <p className="text-xs text-slate-500">Kiritilgan daromad va xarajatlar roʻyxati</p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-1.5 rounded-xl bg-emerald-600 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-emerald-700 transition active:scale-95"
        >
          <Plus className="h-4 w-4" />
          <span>Tranzaksiya qoʻshish</span>
        </button>
      </div>

      <div className="mt-4 divide-y divide-slate-100">
        {transactions.map((tx) => {
          const Icon = getCategoryIcon(tx.category);
          const isIncome = tx.type === 'income';
          return (
            <div key={tx.id} className="flex items-center justify-between py-3.5 transition hover:bg-slate-50/60 px-2 rounded-xl">
              <div className="flex items-center gap-3">
                <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${
                  isIncome ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-700'
                }`}>
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <div className="text-sm font-bold text-slate-900">{tx.category}</div>
                  <div className="text-xs text-slate-400">
                    {tx.note || (isIncome ? 'Daromad' : 'Xarajat')} • {new Date(tx.date).toLocaleDateString('uz-UZ')}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <span className={`text-sm font-extrabold ${isIncome ? 'text-emerald-600' : 'text-slate-900'}`}>
                  {isIncome ? '+' : '-'}{formatUZS(tx.amount)}
                </span>
                <button
                  onClick={() => handleDelete(tx.id)}
                  title="O'chirish"
                  className="text-slate-300 hover:text-rose-500 transition p-1"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Transaction Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-200">
            <h3 className="text-lg font-bold text-slate-900">Yangi Tranzaksiya</h3>
            <form onSubmit={handleCreate} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Turi</label>
                <div className="mt-1 grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setType('expense')}
                    className={`rounded-xl py-2 text-xs font-bold transition ${
                      type === 'expense' ? 'bg-rose-600 text-white shadow' : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    Xarajat
                  </button>
                  <button
                    type="button"
                    onClick={() => setType('income')}
                    className={`rounded-xl py-2 text-xs font-bold transition ${
                      type === 'income' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    Daromad
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Summa (UZS)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="Masalan: 43 200"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Kategoriya</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                >
                  <option value="Oziq-ovqat">Oziq-ovqat</option>
                  <option value="Restoran va Kafe">Restoran va Kafe</option>
                  <option value="Transport">Transport</option>
                  <option value="Kiyim-kechak">Kiyim-kechak</option>
                  <option value="Ko'ngilochar">Ko'ngilochar</option>
                  <option value="Kommunal">Kommunal</option>
                  <option value="Maosh">Maosh</option>
                  <option value="Frilans">Frilans</option>
                  <option value="Boshqa">Boshqa</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase">Izoh</label>
                <input
                  type="text"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="Xarid tafsiloti"
                  className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none"
                />
              </div>

              {type === 'expense' && (
                <label className="flex items-center gap-2 cursor-pointer pt-1">
                  <input
                    type="checkbox"
                    checked={applyRoundUp}
                    onChange={(e) => setApplyRoundUp(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                  />
                  <span className="text-xs font-semibold text-slate-700 flex items-center gap-1">
                    <Sparkles className="h-3.5 w-3.5 text-teal-600" />
                    Round-up yaxlitlashni qoʻllash (Invisible Savings)
                  </span>
                </label>
              )}

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
                  disabled={loading}
                  className="rounded-xl bg-emerald-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-emerald-700"
                >
                  {loading ? 'Saqlanmoqda...' : 'Saqlash'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
