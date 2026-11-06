import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: LucideIcon;
  variant?: 'emerald' | 'blue' | 'rose' | 'amber' | 'slate';
  trend?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  variant = 'emerald',
  trend,
}) => {
  const variantStyles = {
    emerald: {
      bg: 'bg-emerald-500/10',
      text: 'text-emerald-700',
      border: 'border-emerald-200/50',
      iconBg: 'bg-emerald-500 text-white',
    },
    blue: {
      bg: 'bg-blue-500/10',
      text: 'text-blue-700',
      border: 'border-blue-200/50',
      iconBg: 'bg-blue-600 text-white',
    },
    rose: {
      bg: 'bg-rose-500/10',
      text: 'text-rose-700',
      border: 'border-rose-200/50',
      iconBg: 'bg-rose-500 text-white',
    },
    amber: {
      bg: 'bg-amber-500/10',
      text: 'text-amber-700',
      border: 'border-amber-200/50',
      iconBg: 'bg-amber-500 text-white',
    },
    slate: {
      bg: 'bg-slate-500/10',
      text: 'text-slate-700',
      border: 'border-slate-200',
      iconBg: 'bg-slate-700 text-white',
    },
  };

  const style = variantStyles[variant];

  return (
    <div className={`relative overflow-hidden rounded-2xl border ${style.border} bg-white p-5 shadow-sm transition hover:shadow-md`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</span>
        <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${style.iconBg} shadow-sm`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className="mt-3">
        <div className="text-2xl font-bold tracking-tight text-slate-900">{value}</div>
        {(subtitle || trend) && (
          <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
            {trend && <span className={`font-semibold ${style.text}`}>{trend}</span>}
            {subtitle && <span>{subtitle}</span>}
          </div>
        )}
      </div>
    </div>
  );
};
