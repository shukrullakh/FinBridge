import React from 'react';
import { Award, Info, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';
import { BehaviorScoreResponse } from '../types';

interface BehaviorScoreGaugeProps {
  scoreData: BehaviorScoreResponse | null;
}

export const BehaviorScoreGauge: React.FC<BehaviorScoreGaugeProps> = ({ scoreData }) => {
  if (!scoreData || !scoreData.has_sufficient_data) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <Award className="mx-auto h-12 w-12 text-slate-300" />
        <h3 className="mt-3 text-base font-bold text-slate-800">Maʼlumotlar yetarli emas</h3>
        <p className="mt-1 text-xs text-slate-500">
          Moliyaviy xatti-harakat balingizni hisoblash uchun dastlab bir nechta daromad va xarajatlarni kiriting.
        </p>
      </div>
    );
  }

  const { total_score, grade, grade_label, dimensions, summary_insights, disclaimer } = scoreData;

  const getGradeColor = (g: string) => {
    switch (g) {
      case 'A': return 'text-emerald-600 bg-emerald-50 border-emerald-200';
      case 'B': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'C': return 'text-amber-600 bg-amber-50 border-amber-200';
      default: return 'text-rose-600 bg-rose-50 border-rose-200';
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600">
              <Award className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Moliyaviy Xulq-atvor Bali (Score)</h2>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            Moliyaviy intizomingizni 4 ta shaffof mezon orqali oʻlchovchi yoʻnaltiruvchi koʻrsatkich.
          </p>
        </div>

        {/* Total Score Badge */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Umumiy Ball:</div>
            <div className="text-2xl font-black text-slate-900">{total_score}<span className="text-sm font-semibold text-slate-400">/100</span></div>
          </div>
          <div className={`flex h-14 w-14 items-center justify-center rounded-2xl border text-2xl font-black shadow-sm ${getGradeColor(grade)}`}>
            {grade}
          </div>
        </div>
      </div>

      {/* Grade status banner */}
      <div className="mt-6 rounded-2xl bg-slate-50 p-4 border border-slate-200 flex items-center justify-between">
        <div>
          <div className="text-xs font-bold text-slate-900">{grade_label}</div>
          <p className="text-xs text-slate-500 mt-0.5">Xarajatlaringiz va jamgʻarmangiz muvozanati tahlil qilingan.</p>
        </div>
        <div className="flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-100/60 px-3 py-1.5 rounded-xl">
          <TrendingUp className="h-4 w-4" />
          <span>Barqaror holat</span>
        </div>
      </div>

      {/* 4 Dimensions breakdown */}
      <div className="mt-6 space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">4 Asosiy Oʻlcham Tahlili:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dimensions.map((dim) => (
            <div key={dim.key} className="rounded-2xl border border-slate-200 bg-slate-50/50 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-900">{dim.name}</h4>
                  <span className="text-[11px] text-slate-400 font-medium">Ogʻirligi: {dim.weight_percentage}%</span>
                </div>
                <div className="text-right">
                  <span className="text-base font-extrabold text-slate-900">{dim.score}</span>
                  <span className="text-xs text-slate-400">/100</span>
                </div>
              </div>

              {/* Dimension Bar */}
              <div className="mt-3 h-2 w-full rounded-full bg-slate-200 overflow-hidden">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500"
                  style={{ width: `${dim.score}%` }}
                />
              </div>

              <p className="mt-3 text-xs text-slate-600 leading-relaxed">{dim.explanation}</p>
              <div className="mt-2 rounded-lg bg-white px-3 py-1.5 text-[11px] text-emerald-800 font-semibold border border-slate-200/80">
                💡 {dim.recommendation}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="mt-6 flex items-start gap-2.5 rounded-2xl bg-amber-50/60 p-4 border border-amber-200 text-xs text-amber-900">
        <Info className="h-4 w-4 text-amber-700 flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed">{disclaimer}</p>
      </div>
    </div>
  );
};
