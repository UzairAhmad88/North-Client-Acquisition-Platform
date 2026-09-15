'use client';

import React from 'react';
import { ExecutiveOverview } from '@/lib/api/analytics';

interface ExecutiveDashboardProps {
  overview: ExecutiveOverview | null;
  loading: boolean;
  onRefresh: () => void;
  onRunLearningCycle: () => void;
}

export const ExecutiveDashboard: React.FC<ExecutiveDashboardProps> = ({
  overview,
  loading,
  onRefresh,
  onRunLearningCycle,
}) => {
  if (loading && !overview) {
    return (
      <div className="p-8 text-center text-zinc-400">
        <div className="inline-block animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mb-3"></div>
        <p>Loading Executive Portfolio Analytics...</p>
      </div>
    );
  }

  if (!overview) return null;

  return (
    <div className="space-y-6">
      {/* Top Controls & Health Banner */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-zinc-100">Executive Health & Learning Overview</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Live Real-Time
            </span>
          </div>
          <p className="text-sm text-zinc-400 mt-1">
            Empirical multi-lifecycle synthesis: Discover → Sell → Build → Deliver → Support → Learn.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={onRefresh}
            className="px-3.5 py-2 text-sm bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg transition-colors border border-zinc-700/60 font-medium"
          >
            Refresh
          </button>
          <button
            onClick={onRunLearningCycle}
            className="px-4 py-2 text-sm bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-lg transition-all font-semibold shadow-md shadow-indigo-500/20"
          >
            Run Learning Cycle
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Sales Win Rate</p>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-zinc-100">{overview.pipeline_win_rate_pct}%</span>
            <span className="text-xs text-emerald-400 font-medium">Funnel Conversion</span>
          </div>
          <p className="text-xs text-zinc-500 mt-2">Closed-won ratio from verified leads</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">PERT Effort Variance</p>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-amber-400">+{overview.estimation_variance_pct}%</span>
            <span className="text-xs text-amber-300 font-medium">Actual vs Plan</span>
          </div>
          <p className="text-xs text-zinc-500 mt-2">Mean deviation on completed projects</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Support SLA Compliance</p>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-emerald-400">{overview.sla_compliance_pct}%</span>
            <span className="text-xs text-emerald-300 font-medium">Resolution Target</span>
          </div>
          <p className="text-xs text-zinc-500 mt-2">Active SLA ticket resolution rate</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Authoritative Revenue</p>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-zinc-100">${overview.realized_revenue_usd.toLocaleString()}</span>
            <span className="text-xs text-zinc-400 font-medium">Actuals</span>
          </div>
          <p className="text-xs text-zinc-500 mt-2">AI Cost: ${overview.ai_cost_usd.toFixed(2)} USD</p>
        </div>
      </div>

      {/* Top Insights Highlight */}
      <div className="bg-zinc-900/70 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-zinc-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse"></span>
            Discovered Organizational Insights ({overview.top_insights_count})
          </h3>
          <span className="text-xs text-zinc-400 font-medium">Evidence Grounded • Review Required</span>
        </div>

        {overview.top_insights.length === 0 ? (
          <p className="text-sm text-zinc-500 italic">No pending insights discovered. Click "Run Learning Cycle" to analyze data.</p>
        ) : (
          <div className="space-y-3">
            {overview.top_insights.map((ins) => (
              <div
                key={ins.id}
                className="flex items-center justify-between p-4 bg-zinc-950/60 border border-zinc-800/80 rounded-lg hover:border-zinc-700 transition-colors"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded">
                      {ins.category}
                    </span>
                    <span className="text-xs text-zinc-400">Confidence: {ins.confidence}</span>
                  </div>
                  <p className="text-sm font-semibold text-zinc-200 mt-1">{ins.title}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
