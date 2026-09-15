'use client';

import React from 'react';
import { DollarSign, TrendingUp, Layers, Target, Users, Zap, Scale } from 'lucide-react';
import { RevenueOverviewMetrics as MetricsType } from '../../lib/api/revenueGrowth';

interface RevenueOverviewMetricsProps {
  metrics: MetricsType;
}

export const RevenueOverviewMetrics: React.FC<RevenueOverviewMetricsProps> = ({ metrics }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
          <span>Current Annual Run Rate</span>
          <DollarSign className="h-4 w-4 text-emerald-400" />
        </div>
        <div className="text-2xl font-bold text-white font-mono">
          ${(metrics.current_annual_run_rate_usd / 1000000).toFixed(2)}M
        </div>
        <div className="text-[11px] text-emerald-400 mt-1 font-mono">
          NRR: {metrics.net_revenue_retention_pct}%
        </div>
      </div>

      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
          <span>Active Pipeline (Total)</span>
          <Layers className="h-4 w-4 text-indigo-400" />
        </div>
        <div className="text-2xl font-bold text-white font-mono">
          ${(metrics.active_pipeline_total_usd / 1000000).toFixed(2)}M
        </div>
        <div className="text-[11px] text-indigo-400 mt-1 font-mono">
          Weighted: ${(metrics.weighted_pipeline_usd / 1000000).toFixed(2)}M
        </div>
      </div>

      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
          <span>Win Rate & Deals</span>
          <Target className="h-4 w-4 text-purple-400" />
        </div>
        <div className="text-2xl font-bold text-white font-mono">
          {metrics.win_rate_percentage}%
        </div>
        <div className="text-[11px] text-slate-400 mt-1 font-mono">
          {metrics.active_opportunities_count} active opportunities
        </div>
      </div>

      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
          <span>Unit Economics (LTV:CAC)</span>
          <Scale className="h-4 w-4 text-cyan-400" />
        </div>
        <div className="text-2xl font-bold text-white font-mono">
          {metrics.ltv_to_cac_ratio}x
        </div>
        <div className="text-[11px] text-cyan-400 mt-1 font-mono">
          CAC: ${metrics.blended_cac_usd.toLocaleString()}
        </div>
      </div>
    </div>
  );
};
