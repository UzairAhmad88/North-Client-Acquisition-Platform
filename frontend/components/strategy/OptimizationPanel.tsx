'use client';

import React, { useState } from 'react';
import { strategyApi, OptimizationResult } from '@/lib/api/strategy';

export const OptimizationPanel: React.FC = () => {
  const [budgetLimit, setBudgetLimit] = useState(100000);
  const [capacityLimit, setCapacityLimit] = useState(8.0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<OptimizationResult | null>(null);

  const handleRunOptimization = async () => {
    setLoading(true);
    try {
      const res = await strategyApi.runOptimization({
        budget_limit_usd: budgetLimit,
        capacity_limit_fte: capacityLimit,
      });
      setResult(res.data);
    } catch (err) {
      console.error('Failed to run optimization', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-bold text-white">Constrained Portfolio Optimization Engine</h3>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Simplex / Knapsack Solver
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          Calculates the mathematically optimal initiative portfolio under hard budget and FTE capacity ceilings.
        </p>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Available Budget Ceiling</span>
            <span className="font-bold text-emerald-400">${budgetLimit.toLocaleString()}</span>
          </div>
          <input
            type="range"
            min="20000"
            max="500000"
            step="10000"
            value={budgetLimit}
            onChange={(e) => setBudgetLimit(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>

        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Available Engineering Capacity</span>
            <span className="font-bold text-amber-400">{capacityLimit.toFixed(1)} FTE</span>
          </div>
          <input
            type="range"
            min="2.0"
            max="30.0"
            step="0.5"
            value={capacityLimit}
            onChange={(e) => setCapacityLimit(parseFloat(e.target.value))}
            className="w-full accent-amber-500 cursor-pointer"
          />
        </div>
      </div>

      <div className="flex justify-end pt-2">
        <button
          onClick={handleRunOptimization}
          disabled={loading}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition shadow-lg shadow-indigo-600/25 flex items-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Optimizing Portfolio...
            </>
          ) : (
            'Solve Optimal Strategy'
          )}
        </button>
      </div>

      {result && (
        <div className="p-5 bg-slate-950/70 rounded-xl border border-slate-800 space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div>
              <span className="text-xs text-slate-400">Run Code:</span>{' '}
              <span className="font-mono text-indigo-400 font-bold">{result.run_code}</span>
            </div>
            <div className="text-xs text-slate-400">
              Runtime: <strong className="text-white">{result.runtime_seconds}s</strong>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-center">
            <div className="p-3 bg-slate-900 rounded-lg">
              <div className="text-xs text-slate-500">Allocated Budget</div>
              <div className="text-base font-bold text-white mt-0.5">
                ${result.allocated_budget_usd.toLocaleString()} ({result.budget_utilization_percentage.toFixed(0)}%)
              </div>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg">
              <div className="text-xs text-slate-500">Allocated Capacity</div>
              <div className="text-base font-bold text-amber-400 mt-0.5">
                {result.allocated_capacity_fte.toFixed(1)} FTE ({result.capacity_utilization_percentage.toFixed(0)}%)
              </div>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg">
              <div className="text-xs text-slate-500">Total Expected Value</div>
              <div className="text-base font-bold text-emerald-400 mt-0.5">
                ${result.total_expected_value_usd.toLocaleString()}
              </div>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg">
              <div className="text-xs text-slate-500">Net Modeled Benefit</div>
              <div className="text-base font-bold text-indigo-400 mt-0.5">
                ${result.net_expected_benefit_usd.toLocaleString()}
              </div>
            </div>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">{result.explanation}</p>
        </div>
      )}
    </div>
  );
};
