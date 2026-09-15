'use client';

import React from 'react';
import { StrategyOverview as IStrategyOverview } from '@/lib/api/strategy';

interface Props {
  overview?: IStrategyOverview | null;
  loading?: boolean;
  onRefresh?: () => void;
}

export const StrategyOverview: React.FC<Props> = ({ overview, loading = false, onRefresh = () => {} }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3"></div>
        Loading Strategic Operating Overview...
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900/50 rounded-xl border border-slate-800">
        Strategic overview currently unavailable.
      </div>
    );
  }

  const sc = overview.scorecard || { dimensions: {} };
  const healthPct = Math.round(overview.composite_health_percentage || 100);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-white tracking-tight">Autonomous Strategy & Goal Intelligence</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              PHASE 51 GOVERNED
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Active Objectives: <strong className="text-white">{overview.total_active_objectives}</strong> | Initiatives:{' '}
            <strong className="text-white">{overview.total_active_initiatives}</strong>
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs text-slate-400 font-medium">Strategic Health Index</div>
            <div className="text-2xl font-black text-emerald-400">{healthPct}%</div>
          </div>
          <button
            onClick={onRefresh}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition shadow-lg shadow-indigo-600/20"
          >
            Refresh Strategy
          </button>
        </div>
      </div>

      {/* 4 Multi-Dimensional Strategy Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/70 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs text-slate-400 mb-1">
            <span>Growth Momentum</span>
            <span className="font-bold text-indigo-400">{sc.dimensions?.growth || 88}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${sc.dimensions?.growth || 88}%` }}></div>
          </div>
        </div>

        <div className="p-4 bg-slate-900/70 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs text-slate-400 mb-1">
            <span>Capital & Profitability</span>
            <span className="font-bold text-emerald-400">{sc.dimensions?.profitability || 82}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${sc.dimensions?.profitability || 82}%` }}></div>
          </div>
        </div>

        <div className="p-4 bg-slate-900/70 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs text-slate-400 mb-1">
            <span>Delivery & Capacity</span>
            <span className="font-bold text-purple-400">{sc.dimensions?.delivery || 90}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-purple-500 h-full rounded-full" style={{ width: `${sc.dimensions?.delivery || 90}%` }}></div>
          </div>
        </div>

        <div className="p-4 bg-slate-900/70 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs text-slate-400 mb-1">
            <span>AI & Automation</span>
            <span className="font-bold text-amber-400">{sc.dimensions?.ai || 94}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-amber-500 h-full rounded-full" style={{ width: `${sc.dimensions?.ai || 94}%` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};
