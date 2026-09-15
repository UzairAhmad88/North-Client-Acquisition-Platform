'use client';

import React from 'react';
import { InnovationPortfolio, HorizonLevel } from '../../lib/api/innovation';

interface PortfolioHorizonChartProps {
  portfolio?: InnovationPortfolio;
  onOptimizeAllocation?: (targetHorizons?: Record<HorizonLevel, number>) => Promise<void>;
}

export const PortfolioHorizonChart: React.FC<PortfolioHorizonChartProps> = ({
  portfolio,
  onOptimizeAllocation
}) => {
  const h1 = portfolio?.horizon_1_core_pct ?? 70;
  const h2 = portfolio?.horizon_2_adjacent_pct ?? 20;
  const h3 = portfolio?.horizon_3_transformational_pct ?? 10;
  const totalInvested = portfolio?.total_invested_usd ?? 350000;
  const expectedRoi = portfolio?.expected_portfolio_roi ?? 3.8;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 backdrop-blur-md shadow-2xl">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            Innovation Horizons & 70/20/10 Allocation
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Balanced capital & resource distribution across Core, Adjacent, and Transformational initiatives.
          </p>
        </div>

        {onOptimizeAllocation && (
          <button
            onClick={() => onOptimizeAllocation()}
            className="px-3 py-1.5 rounded-lg border border-cyan-500/30 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 text-xs font-semibold transition-all"
          >
            Run Portfolio Optimizer (Phase 51)
          </button>
        )}
      </div>

      {/* Horizon Progress Bar */}
      <div className="mb-6">
        <div className="h-4 w-full bg-slate-950 rounded-full overflow-hidden flex border border-slate-800/80">
          <div
            style={{ width: `${h1}%` }}
            className="bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500 relative group"
            title={`Horizon 1 (Core): ${h1}%`}
          />
          <div
            style={{ width: `${h2}%` }}
            className="bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-500 relative group"
            title={`Horizon 2 (Adjacent): ${h2}%`}
          />
          <div
            style={{ width: `${h3}%` }}
            className="bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500 relative group"
            title={`Horizon 3 (Transformational): ${h3}%`}
          />
        </div>
      </div>

      {/* Horizon Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Horizon 1 */}
        <div className="p-4 rounded-xl border border-emerald-500/20 bg-emerald-950/20">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">Horizon 1 — Core</span>
            <span className="text-lg font-bold text-emerald-300">{h1}%</span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Optimize, scale, and protect current product lines and existing customer segments.
          </p>
          <div className="text-[11px] text-slate-500">
            Est. Budget: <strong className="text-slate-300">${((totalInvested * h1) / 100).toLocaleString()}</strong>
          </div>
        </div>

        {/* Horizon 2 */}
        <div className="p-4 rounded-xl border border-blue-500/20 bg-blue-950/20">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-400">Horizon 2 — Adjacent</span>
            <span className="text-lg font-bold text-blue-300">{h2}%</span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Expand into new customer segments, channels, or complementary service capabilities.
          </p>
          <div className="text-[11px] text-slate-500">
            Est. Budget: <strong className="text-slate-300">${((totalInvested * h2) / 100).toLocaleString()}</strong>
          </div>
        </div>

        {/* Horizon 3 */}
        <div className="p-4 rounded-xl border border-purple-500/20 bg-purple-950/20">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-purple-400">Horizon 3 — Transformational</span>
            <span className="text-lg font-bold text-purple-300">{h3}%</span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Radical breakthroughs, new business models, next-gen AI systems, and non-linear bets.
          </p>
          <div className="text-[11px] text-slate-500">
            Est. Budget: <strong className="text-slate-300">${((totalInvested * h3) / 100).toLocaleString()}</strong>
          </div>
        </div>
      </div>

      {/* Portfolio Economics Summary */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-lg bg-slate-950/60 border border-slate-800">
        <div>
          <div className="text-[10px] text-slate-500 uppercase font-semibold">Total R&D Investment</div>
          <div className="text-sm font-bold text-slate-200 mt-0.5">${totalInvested.toLocaleString()}</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500 uppercase font-semibold">Blended Expected ROI</div>
          <div className="text-sm font-bold text-emerald-400 mt-0.5">{expectedRoi}x</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500 uppercase font-semibold">Active Experiments</div>
          <div className="text-sm font-bold text-slate-200 mt-0.5">8 Running</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500 uppercase font-semibold">Governance Status</div>
          <div className="text-sm font-bold text-indigo-400 mt-0.5">Fully Compliant</div>
        </div>
      </div>
    </div>
  );
};
