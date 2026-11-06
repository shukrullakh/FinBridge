import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  Timer, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  HelpCircle, 
  ArrowRight,
  TrendingDown,
  Sparkles
} from 'lucide-react';
import { api, formatUZS } from '../services/api';
import { SmartPauseEvaluateResponse } from '../types';

interface SmartPauseModalProps {
  onSuccess?: () => void;
}

export const SmartPauseModal: React.FC<SmartPauseModalProps> = ({ onSuccess }) => {
  const [amount, setAmount] = useState<string>('850000');
  const [category, setCategory] = useState<string>('Ko\'ngilochar');
  const [description, setDescription] = useState<string>('PlayStation 5 o\'yini xaridi');
  const [evaluating, setEvaluating] = useState<boolean>(false);
  const [evaluation, setEvaluation] = useState<SmartPauseEvaluateResponse | null>(null);
  
  // 15-minute countdown timer state
  const [secondsLeft, setSecondsLeft] = useState<number>(15 * 60);
  const [isTimerRunning, setIsTimerRunning] = useState<boolean>(false);
  const [recordedStatus, setRecordedStatus] = useState<string | null>(null);

  useEffect(() => {
    let interval: any = null;
    if (isTimerRunning && secondsLeft > 0) {
      interval = setInterval(() => {
        setSecondsLeft((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, secondsLeft]);

  const formatTimer = (totalSeconds: number) => {
    const m = Math.floor(totalSeconds / 60);
    const s = totalSeconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const handleEvaluate = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;

    setEvaluating(true);
    setRecordedStatus(null);
    try {
      const res = await api.evaluateSmartPause({
        amount: parseFloat(amount),
        category,
        description,
      });
      setEvaluation(res);
      setSecondsLeft(15 * 60);
      setIsTimerRunning(true);
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  const handleDecision = async (decision: 'cancelled' | 'postponed' | 'proceeded') => {
    if (!evaluation) return;
    try {
      await api.recordDecision({
        amount: evaluation.amount,
        category: evaluation.category,
        description,
        risk_level: evaluation.risk_level,
        decision,
        cooling_off_taken: true,
        notes: `Foydalanuvchi 15 daqiqalik sovutish vaqtida '${decision}' qarorini tanladi.`,
      });

      if (decision === 'proceeded') {
        // If proceeded, also register as real transaction
        await api.createTransaction({
          amount: evaluation.amount,
          type: 'expense',
          category: evaluation.category,
          note: description || 'Smart Pause orqali tasdiqlangan xarid',
          date: new Date().toISOString(),
          source: 'Plastik karta',
        });
      }

      setRecordedStatus(decision);
      setIsTimerRunning(false);
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  const setPreset = (pAmount: string, pCat: string, pDesc: string) => {
    setAmount(pAmount);
    setCategory(pCat);
    setDescription(pDesc);
    setEvaluation(null);
    setRecordedStatus(null);
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-50 text-rose-600">
              <ShieldAlert className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Smart Pause — Emotsional Xaridlarni Toʻxtatish</h2>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            Rejalashtirilgan xaridni kiritib, uning oylik byudjetingiz va maqsadingizga xavfini 15 daqiqalik sovutish taymeri bilan baholang.
          </p>
        </div>

        {/* Demo Quick Presets */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-medium">Tezkor namunalar:</span>
          <button
            onClick={() => setPreset('850000', 'Ko\'ngilochar', 'PlayStation 5 yangi o\'yini')}
            className="rounded-lg bg-rose-50 px-2.5 py-1 text-xs font-semibold text-rose-700 hover:bg-rose-100 border border-rose-200"
          >
            🎮 Katta xarid
          </button>
          <button
            onClick={() => setPreset('45000', 'Transport', 'Taksi safari')}
            className="rounded-lg bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-100 border border-emerald-200"
          >
            🚕 Xavfsiz xarid
          </button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Purchase Input Form */}
        <div className="lg:col-span-5 space-y-4">
          <form onSubmit={handleEvaluate} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase">
                Xarid summasi (UZS)
              </label>
              <div className="relative mt-1">
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="Masalan: 850 000"
                  className="w-full rounded-xl border border-slate-300 px-4 py-2.5 text-base font-bold text-slate-900 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  required
                />
                <span className="absolute right-3.5 top-3 text-xs font-semibold text-slate-400">UZS</span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase">
                Toifa (Kategoriya)
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm font-semibold text-slate-900 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
              >
                <option value="Ko'ngilochar">Ko'ngilochar va Gadjetlar</option>
                <option value="Restoran va Kafe">Restoran va Kafe</option>
                <option value="Kiyim-kechak">Kiyim-kechak</option>
                <option value="Oziq-ovqat">Oziq-ovqat</option>
                <option value="Transport">Transport</option>
                <option value="Boshqa">Boshqa xarajat</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase">
                Xarid maqsadi / Izoh
              </label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Nima sotib olmoqchisiz?"
                className="mt-1 w-full rounded-xl border border-slate-300 px-4 py-2.5 text-sm text-slate-900 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
              />
            </div>

            <button
              type="submit"
              disabled={evaluating}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-600/20 transition hover:from-emerald-700 hover:to-teal-700 active:scale-98 disabled:opacity-50"
            >
              <Sparkles className="h-4 w-4" />
              <span>{evaluating ? 'Tahlil qilinmoqda...' : 'Xaridni Smart Pause orqali Baholash'}</span>
            </button>
          </form>

          <div className="rounded-2xl bg-amber-50/70 p-4 border border-amber-200/60 text-xs text-amber-900 leading-relaxed">
            <span className="font-bold">Eslatma:</span> FinBridge real bank toʻlovlarini bloklamaydi. 
            Smart Pause sizni hissiy shoshqaloqlikdan himoya qiluvchi xulq-atvor psixologiyasi qurolidir.
          </div>
        </div>

        {/* Evaluation & Cooling Off Screen */}
        <div className="lg:col-span-7">
          {evaluation ? (
            <div className={`rounded-2xl border p-6 transition-all ${
              evaluation.risk_level === 'high' 
                ? 'border-rose-300 bg-rose-50/40' 
                : evaluation.risk_level === 'moderate'
                ? 'border-amber-300 bg-amber-50/40'
                : 'border-emerald-300 bg-emerald-50/40'
            }`}>
              {/* Risk Badge and 15 min Timer */}
              <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200/60 pb-4">
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-extrabold uppercase tracking-wider ${
                    evaluation.risk_level === 'high'
                      ? 'bg-rose-100 text-rose-800 border border-rose-300'
                      : evaluation.risk_level === 'moderate'
                      ? 'bg-amber-100 text-amber-800 border border-amber-300'
                      : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  }`}>
                    {evaluation.risk_level === 'high' ? '⚠️ Yuqori Moliyaviy Xavf' : evaluation.risk_level === 'moderate' ? '⚡ Diqqat Talab Xarid' : '✅ Xavfsiz Xarid'}
                  </span>
                </div>

                {/* 15-Minute Cooling-off Display */}
                <div className="flex items-center gap-2 rounded-xl bg-white px-3 py-1.5 shadow-sm border border-slate-200">
                  <Timer className={`h-4 w-4 ${isTimerRunning ? 'animate-pulse text-rose-600' : 'text-slate-400'}`} />
                  <span className="text-xs font-semibold text-slate-500">Sovutish taymeri:</span>
                  <span className="font-mono text-base font-extrabold text-slate-900">
                    {formatTimer(secondsLeft)}
                  </span>
                </div>
              </div>

              {/* Reasons */}
              <div className="mt-4 space-y-2">
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Tahlil natijasi:</h4>
                <ul className="space-y-1.5">
                  {evaluation.reasons.map((reason, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-slate-800">
                      <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-slate-500" />
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Budget Impact comparison */}
              <div className="mt-5 grid grid-cols-2 gap-3 rounded-xl bg-white p-4 border border-slate-200/80">
                <div>
                  <div className="text-[11px] font-semibold text-slate-500">Xariddan keyingi balans:</div>
                  <div className={`text-base font-bold ${evaluation.projected_balance < 0 ? 'text-rose-600' : 'text-slate-900'}`}>
                    {formatUZS(evaluation.projected_balance)}
                  </div>
                </div>
                <div>
                  <div className="text-[11px] font-semibold text-slate-500">Toifa boʻyicha sarf:</div>
                  <div className="text-base font-bold text-slate-900">
                    {formatUZS(evaluation.projected_category_spent)}
                    {evaluation.category_limit && (
                      <span className="text-xs font-normal text-slate-500"> / {formatUZS(evaluation.category_limit)}</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Reflection Prompts */}
              <div className="mt-5 rounded-xl bg-white/80 p-4 border border-slate-200/60">
                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 uppercase tracking-wide">
                  <HelpCircle className="h-4 w-4 text-emerald-600" />
                  <span>Oʻylab koʻrish uchun savollar:</span>
                </div>
                <div className="mt-2 space-y-1 text-xs text-slate-600 italic">
                  {evaluation.reflection_prompts.map((prompt, i) => (
                    <p key={i}>"{prompt}"</p>
                  ))}
                </div>
              </div>

              {/* Decision Buttons */}
              <div className="mt-6">
                {recordedStatus ? (
                  <div className="flex items-center gap-2 rounded-xl bg-slate-900 p-3.5 text-white">
                    <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                    <span className="text-sm font-semibold">
                      Qaror saqlandi: 
                      {recordedStatus === 'cancelled' && ' Xarid bekor qilindi (Ortiqcha xarajatning oldi olindi!)'}
                      {recordedStatus === 'postponed' && ' 24 soatga keyinga qoldirildi.'}
                      {recordedStatus === 'proceeded' && ' Baribir amalga oshirildi.'}
                    </span>
                  </div>
                ) : (
                  <div>
                    <div className="text-xs font-bold text-slate-600 mb-2">Qaroringizni tanlang:</div>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                      <button
                        onClick={() => handleDecision('cancelled')}
                        className="flex items-center justify-center gap-1.5 rounded-xl bg-emerald-600 px-4 py-2.5 text-xs font-bold text-white shadow-md hover:bg-emerald-700 transition"
                      >
                        <XCircle className="h-4 w-4" />
                        <span>Bekor qilish (Tejash)</span>
                      </button>
                      <button
                        onClick={() => handleDecision('postponed')}
                        className="flex items-center justify-center gap-1.5 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 transition"
                      >
                        <Clock className="h-4 w-4" />
                        <span>Keyinga qoldirish</span>
                      </button>
                      <button
                        onClick={() => handleDecision('proceeded')}
                        className="flex items-center justify-center gap-1.5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-2.5 text-xs font-bold text-rose-700 hover:bg-rose-100 transition"
                      >
                        <ArrowRight className="h-4 w-4" />
                        <span>Baribir xarid qilish</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex h-full min-h-[300px] flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50/50 p-8 text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white shadow-sm border border-slate-200 text-slate-400">
                <ShieldAlert className="h-6 w-6" />
              </div>
              <h3 className="mt-3 text-sm font-bold text-slate-800">Tahlil qilish kutilmoqda</h3>
              <p className="mt-1 max-w-sm text-xs text-slate-500">
                Chap tomondagi maydonga xarid maʼlumotlarini kiriting yoki yuqoridagi tezkor namunalardan birini tanlang.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
