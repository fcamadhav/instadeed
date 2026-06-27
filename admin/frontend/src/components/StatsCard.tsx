'use client';

import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';

interface StatsCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  trend?: number;
  trendLabel?: string;
  accentColor?: string;
}

export default function StatsCard({
  icon: Icon,
  label,
  value,
  trend,
  trendLabel,
  accentColor = 'bg-admin-500',
}: StatsCardProps) {
  const isUp = trend !== undefined && trend >= 0;
  const isDown = trend !== undefined && trend < 0;

  return (
    <div className="card card-hover overflow-hidden">
      <div className={`h-1 ${accentColor}`} />
      <div className="p-5">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-medium text-slate-500 dark:text-slate-400">{label}</span>
          <div className="w-9 h-9 rounded-lg bg-admin-50 dark:bg-admin-900/30 flex items-center justify-center">
            <Icon className="w-4 h-4 text-admin-600 dark:text-admin-400" />
          </div>
        </div>
        <div className="flex items-end justify-between">
          <span className="text-2xl font-bold text-slate-900 dark:text-white">{value}</span>
          {trend !== undefined && (
            <div className={`flex items-center gap-1 text-xs font-medium ${isUp ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
              {isUp ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
              <span>{Math.abs(trend)}%</span>
              {trendLabel && <span className="text-slate-400 dark:text-slate-500">vs {trendLabel}</span>}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
