'use client';

import React from 'react';
import { Activity, ShieldCheck, TrendingDown, TrendingUp, Sparkles } from 'lucide-react';
import { ExperienceHealthItem } from '../../lib/api/customerExperience';

interface ExperienceHealthCardProps {
  health: ExperienceHealthItem;
}

export const ExperienceHealthCard: React.FC<ExperienceHealthCardProps> = ({ health }) => {
  const factors = health.factor_breakdown || {
    engagement: 90,
    product_adoption: 88,
    support_health: 95,
    customer_effort: 85,
    satisfaction_sentiment: 90,
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Activity className="h-4 w-4 text-purple-400" />
          Experience Health & Predictive Churn
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
          {health.health_state}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="text-xs text-slate-400 mb-1">Composite Health Score</div>
          <div className="text-2xl font-bold font-mono text-purple-400">
            {health.overall_health_score.toFixed(1)} <span className="text-xs text-slate-500 font-normal">/ 100</span>
          </div>
        </div>

        <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="text-xs text-slate-400 mb-1 flex items-center gap-1">
            <TrendingDown className="h-3.5 w-3.5 text-emerald-400" />
            Churn Probability
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400">
            {(health.churn_probability * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      <div className="space-y-2 pt-1">
        <div className="text-xs font-semibold text-slate-300">Factor Breakdown</div>
        {Object.entries(factors).map(([k, val]) => (
          <div key={k} className="space-y-1">
            <div className="flex justify-between text-[11px] text-slate-400">
              <span className="capitalize">{k.replace('_', ' ')}</span>
              <span className="font-mono text-slate-200">{val}%</span>
            </div>
            <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
                style={{ width: `${val}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
