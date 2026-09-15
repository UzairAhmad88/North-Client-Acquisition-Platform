'use client';

import React from 'react';
import { Award, Compass, TrendingUp, ShieldAlert, Sparkles, CheckCircle, ArrowRight } from 'lucide-react';
import { ParetoFrontier } from '../../lib/api/strategy';

interface ParetoChartProps {
  paretoFrontier: ParetoFrontier | null;
  onSelectPlan?: (planId: string) => void;
}

export const ParetoChart: React.FC<ParetoChartProps> = ({ paretoFrontier, onSelectPlan }) => {
  if (!paretoFrontier || !paretoFrontier.frontier_packages || paretoFrontier.frontier_packages.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 p-8 text-center">
        <Compass className="mx-auto h-10 w-10 text-slate-500 mb-3" />
        <h3 className="text-base font-semibold text-slate-300">No Pareto Analysis Available</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Execute a multi-objective optimization run to generate non-dominated trade-off packages across Growth, Profitability, and Risk reduction.
        </p>
      </div>
    );
  }

  const packages = paretoFrontier.frontier_packages;

  const getPackageBadgeColor = (type: string) => {
    switch (type) {
      case 'GROWTH_MAXIMIZATION':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'PROFIT_MAXIMIZATION':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'DEFENSIVE_RESILIENCE':
        return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
      default:
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-indigo-500/20 bg-gradient-to-r from-indigo-950/40 via-slate-900/60 to-purple-950/30">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white tracking-tight">Pareto Efficient Strategic Packages</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Non-dominated strategic configurations where no single objective (Growth, Profit, Risk) can be improved without sacrificing another.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-slate-400">Analysis ID</div>
            <div className="text-xs font-mono text-indigo-300">{paretoFrontier.frontier_id.slice(0, 12)}...</div>
          </div>
          <div className="px-3 py-1.5 rounded-lg bg-indigo-500/20 border border-indigo-500/40 text-xs font-semibold text-indigo-300">
            {packages.length} Trade-off Options
          </div>
        </div>
      </div>

      {/* Package Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {packages.map((pkg, idx) => (
          <div
            key={pkg.package_id || idx}
            className="flex flex-col justify-between rounded-xl border border-slate-700/60 bg-slate-900/60 p-5 backdrop-blur-sm transition-all hover:border-indigo-500/50 hover:bg-slate-900/90 hover:shadow-lg hover:shadow-indigo-500/5"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <span className={`px-2.5 py-1 rounded-md text-[11px] font-medium border ${getPackageBadgeColor(pkg.package_type)}`}>
                  {pkg.package_type.replace('_', ' ')}
                </span>
                <span className="text-xs font-bold text-slate-400">Option #{idx + 1}</span>
              </div>

              <h3 className="text-base font-semibold text-white mb-2">{pkg.name}</h3>
              <p className="text-xs text-slate-400 mb-4 leading-relaxed">{pkg.description}</p>

              {/* Metrics Grid */}
              <div className="grid grid-cols-3 gap-2 p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 mb-4 text-center">
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500 flex items-center justify-center gap-1">
                    <TrendingUp className="h-3 w-3 text-emerald-400" />
                    Growth
                  </div>
                  <div className="text-sm font-bold text-emerald-400 mt-1">
                    {Math.round(pkg.growth_score * 100)}%
                  </div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500 flex items-center justify-center gap-1">
                    <Award className="h-3 w-3 text-blue-400" />
                    Profit
                  </div>
                  <div className="text-sm font-bold text-blue-400 mt-1">
                    {Math.round(pkg.profit_score * 100)}%
                  </div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500 flex items-center justify-center gap-1">
                    <ShieldAlert className="h-3 w-3 text-amber-400" />
                    Risk
                  </div>
                  <div className="text-sm font-bold text-amber-400 mt-1">
                    {Math.round(pkg.risk_score * 100)}%
                  </div>
                </div>
              </div>

              {/* Budget & FTE Breakdown */}
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Allocated Budget:</span>
                  <span className="font-medium text-white">${pkg.allocated_budget?.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Required FTE:</span>
                  <span className="font-medium text-white">{pkg.required_fte} staff</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Initiatives Included:</span>
                  <span className="font-medium text-indigo-300">{pkg.selected_initiatives?.length || 0} items</span>
                </div>
              </div>

              {/* Trade-off Insights */}
              <div className="p-3 rounded-lg bg-indigo-950/20 border border-indigo-500/20 text-xs text-indigo-300/90 mb-4">
                <div className="font-semibold mb-1 text-indigo-200">Key Trade-off:</div>
                {pkg.trade_off_summary || 'Provides balanced trade-off across growth and profitability while preserving risk thresholds.'}
              </div>
            </div>

            {onSelectPlan && (
              <button
                onClick={() => onSelectPlan(pkg.package_id)}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 transition-all cursor-pointer"
              >
                Select Package for Review
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
