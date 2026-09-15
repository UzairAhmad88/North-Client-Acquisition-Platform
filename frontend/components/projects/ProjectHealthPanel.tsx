'use client';

import React from 'react';

interface ProjectHealthPanelProps {
  health: string;
  reasons: string[];
  effortVariance: number;
  overdueCount: number;
  blockedCount: number;
}

export const ProjectHealthPanel: React.FC<ProjectHealthPanelProps> = ({
  health,
  reasons,
  effortVariance,
  overdueCount,
  blockedCount,
}) => {
  const getBadgeStyle = (status: string) => {
    switch (status) {
      case 'HEALTHY':
        return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300 border-emerald-300';
      case 'AT_RISK':
        return 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border-amber-300';
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300 border-red-300';
      case 'BLOCKED':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300 border-purple-300';
      default:
        return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 border-slate-300';
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Deterministic Project Health</h3>
        <span className={`text-xs font-bold px-3 py-1 rounded-full border ${getBadgeStyle(health)}`}>
          {health}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-100 dark:border-slate-700">
          <span className="text-[11px] text-slate-400 font-medium">Overdue Tasks</span>
          <p className={`text-lg font-bold ${overdueCount > 0 ? 'text-amber-600' : 'text-slate-700 dark:text-slate-200'}`}>
            {overdueCount}
          </p>
        </div>
        <div className="bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-100 dark:border-slate-700">
          <span className="text-[11px] text-slate-400 font-medium">Blocked Tasks</span>
          <p className={`text-lg font-bold ${blockedCount > 0 ? 'text-red-600' : 'text-slate-700 dark:text-slate-200'}`}>
            {blockedCount}
          </p>
        </div>
        <div className="bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-100 dark:border-slate-700">
          <span className="text-[11px] text-slate-400 font-medium">Effort Variance</span>
          <p className={`text-lg font-bold ${effortVariance > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
            {effortVariance > 0 ? `+${effortVariance}h` : `${effortVariance}h`}
          </p>
        </div>
      </div>

      <div className="space-y-1.5">
        <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">Health Reasons:</span>
        <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-400 space-y-1">
          {reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
