'use client';

import React from 'react';
import { SimulationResult } from '@/lib/api/digitalTwin';

interface Props {
  result: SimulationResult | null;
}

export const UncertaintyPanel: React.FC<Props> = ({ result }) => {
  if (!result) {
    return (
      <div className="p-8 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800">
        Run a simulation above to view probabilistic distributions and P10/P50/P90 envelopes.
      </div>
    );
  }

  const metrics = result.metrics_summary || {};
  const dist = result.uncertainty_distribution || {};
  const revDist = dist['cumulative_revenue_usd'];
  const profitDist = dist['cumulative_net_profit_usd'];
  const utilDist = dist['capacity_utilization_percentage'];

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <h3 className="text-lg font-bold text-white">Simulation Results & Uncertainty Envelopes</h3>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              {result.method} ({result.iterations} runs)
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Code: <span className="font-mono text-slate-300">{result.simulation_code}</span> | Runtime:{' '}
            <span className="font-mono text-emerald-400">{result.runtime_seconds}s</span>
          </p>
        </div>

        {result.constraint_violations?.length > 0 && (
          <span className="px-3 py-1 rounded-lg text-xs font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            {result.constraint_violations.length} Constraint Violations
          </span>
        )}
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-950/70 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Expected 12m Revenue</div>
          <div className="text-xl font-bold text-white mt-1">
            ${(metrics.cumulative_revenue_usd || 0).toLocaleString()}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Margin: {(metrics.average_gross_margin_percentage || 0).toFixed(1)}%
          </div>
        </div>

        <div className="p-4 bg-slate-950/70 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Expected Net Profit</div>
          <div className="text-xl font-bold text-emerald-400 mt-1">
            ${(metrics.cumulative_net_profit_usd || 0).toLocaleString()}
          </div>
          <div className="text-xs text-slate-500 mt-1">OpEx & AI costs deducted</div>
        </div>

        <div className="p-4 bg-slate-950/70 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Ending Active Clients</div>
          <div className="text-xl font-bold text-indigo-400 mt-1">
            {(metrics.ending_active_clients || 0).toFixed(1)}
          </div>
          <div className="text-xs text-slate-500 mt-1">Retained + Converted</div>
        </div>

        <div className="p-4 bg-slate-950/70 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-medium">Final Team Utilization</div>
          <div className="text-xl font-bold text-amber-400 mt-1">
            {(metrics.final_capacity_utilization_percentage || 0).toFixed(1)}%
          </div>
          <div className="text-xs text-slate-500 mt-1">
            {(metrics.final_capacity_utilization_percentage || 0) > 90 ? 'High Risk' : 'Optimal'}
          </div>
        </div>
      </div>

      {/* Percentile Distribution Envelopes */}
      {revDist && (
        <div className="p-5 bg-slate-950/60 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-slate-300 uppercase tracking-wider">Revenue Probability Envelope</span>
            <span className="text-slate-400">Monte Carlo Confidence Bands</span>
          </div>

          <div className="grid grid-cols-5 gap-2 text-center text-xs">
            <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800/80">
              <div className="text-slate-500 font-medium">P10 (Pessimistic)</div>
              <div className="text-sm font-bold text-slate-300 mt-1">${revDist.p10.toLocaleString()}</div>
            </div>
            <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800/80">
              <div className="text-slate-500 font-medium">P25</div>
              <div className="text-sm font-bold text-slate-300 mt-1">${revDist.p25.toLocaleString()}</div>
            </div>
            <div className="p-2.5 bg-indigo-950/40 rounded-lg border border-indigo-800/40">
              <div className="text-indigo-400 font-bold">P50 (Median)</div>
              <div className="text-sm font-bold text-indigo-300 mt-1">${revDist.p50.toLocaleString()}</div>
            </div>
            <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800/80">
              <div className="text-slate-500 font-medium">P75</div>
              <div className="text-sm font-bold text-slate-300 mt-1">${revDist.p75.toLocaleString()}</div>
            </div>
            <div className="p-2.5 bg-emerald-950/40 rounded-lg border border-emerald-800/40">
              <div className="text-emerald-400 font-bold">P90 (Optimistic)</div>
              <div className="text-sm font-bold text-emerald-300 mt-1">${revDist.p90.toLocaleString()}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
