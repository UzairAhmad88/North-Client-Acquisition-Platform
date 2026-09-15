'use client';

import React from 'react';
import { SLOMetricSnapshot } from '@/lib/api/reliability';

interface Props {
  slos: SLOMetricSnapshot[];
}

export function SLOErrorBudgetCard({ slos }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div>
          <h3 className="text-lg font-semibold text-white">Service Level Objectives & Error Budget Depletion</h3>
          <p className="text-xs text-slate-400">
            30-day rolling evaluation window with automated burn rate alerting
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {slos.map((slo) => {
          const budgetPct = Math.max(0, slo.error_budget_remaining_pct);
          const isHealthy = slo.budget_status === 'HEALTHY';
          const isWarning = slo.budget_status === 'WARNING';

          const budgetColor = isHealthy ? 'bg-emerald-500' : isWarning ? 'bg-amber-500' : 'bg-rose-500';
          const badgeClass = isHealthy
            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
            : isWarning
            ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            : 'bg-rose-500/10 text-rose-400 border-rose-500/20';

          return (
            <div key={slo.name} className="bg-slate-950/60 border border-slate-800/80 p-5 rounded-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-white">{slo.name}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${badgeClass}`}>
                    {slo.budget_status}
                  </span>
                </div>

                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-2xl font-bold font-mono text-white">{slo.current_sli.toFixed(2)}%</span>
                  <span className="text-xs text-slate-400">/ target {slo.target_slo.toFixed(2)}%</span>
                </div>

                {/* Progress bar for remaining error budget */}
                <div className="mt-3">
                  <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                    <span>Error Budget Remaining</span>
                    <span className="font-mono font-medium text-slate-200">{budgetPct.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div className={`h-full ${budgetColor} transition-all duration-500`} style={{ width: `${Math.min(100, budgetPct)}%` }} />
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/50 grid grid-cols-2 gap-2 text-[10px] text-slate-400">
                <div>
                  <span>Burn Rate 1h: </span>
                  <span className={`font-mono font-semibold ${slo.burn_rate_1h > 2 ? 'text-rose-400' : 'text-slate-300'}`}>
                    {slo.burn_rate_1h.toFixed(2)}x
                  </span>
                </div>
                <div>
                  <span>Burn Rate 24h: </span>
                  <span className={`font-mono font-semibold ${slo.burn_rate_24h > 2 ? 'text-amber-400' : 'text-slate-300'}`}>
                    {slo.burn_rate_24h.toFixed(2)}x
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
