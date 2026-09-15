'use client';

import React from 'react';

interface ForecastVisualizerProps {
  forecastData: any;
}

export const ForecastVisualizer: React.FC<ForecastVisualizerProps> = ({ forecastData }) => {
  if (!forecastData || !forecastData.forecast) {
    return (
      <div className="p-8 text-center text-zinc-500 bg-zinc-900/40 border border-zinc-800 rounded-xl">
        No forecast data generated.
      </div>
    );
  }

  const f = forecastData.forecast;
  const ci = forecastData.confidence_intervals || {};

  return (
    <div className="space-y-6">
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-bold text-zinc-100">Multi-Horizon Workload & AI Cost Forecast</h3>
            <p className="text-xs text-zinc-400 mt-1">
              Probabilistic projection across the next {forecastData.time_horizon || '30d'} with confidence interval bounds.
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 bg-zinc-800 text-zinc-300 font-semibold rounded border border-zinc-700">
            Horizon: {forecastData.time_horizon || '30d'}
          </span>
        </div>

        {/* Forecast KPI Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="p-4 bg-zinc-950/70 border border-zinc-800 rounded-lg">
            <p className="text-xs font-semibold uppercase text-zinc-400">Leads to Research</p>
            <p className="text-2xl font-bold text-zinc-100 mt-1">{f.expected_leads_requiring_research}</p>
            <p className="text-xs text-zinc-500 mt-1">
              Interval: {ci.leads_range?.lower || 35} – {ci.leads_range?.upper || 55}
            </p>
          </div>

          <div className="p-4 bg-zinc-950/70 border border-zinc-800 rounded-lg">
            <p className="text-xs font-semibold uppercase text-zinc-400">Project Starts</p>
            <p className="text-2xl font-bold text-indigo-400 mt-1">{f.expected_project_starts}</p>
            <p className="text-xs text-zinc-500 mt-1">Estimated sprint load</p>
          </div>

          <div className="p-4 bg-zinc-950/70 border border-zinc-800 rounded-lg">
            <p className="text-xs font-semibold uppercase text-zinc-400">Support Requests</p>
            <p className="text-2xl font-bold text-amber-400 mt-1">{f.expected_support_requests}</p>
            <p className="text-xs text-zinc-500 mt-1">
              Interval: {ci.support_range?.lower || 22} – {ci.support_range?.upper || 36}
            </p>
          </div>

          <div className="p-4 bg-zinc-950/70 border border-zinc-800 rounded-lg">
            <p className="text-xs font-semibold uppercase text-zinc-400">Projected AI Cost</p>
            <p className="text-2xl font-bold text-emerald-400 mt-1">${f.expected_ai_cost_usd?.toFixed(2)} USD</p>
            <p className="text-xs text-zinc-500 mt-1">
              Interval: ${ci.ai_cost_range_usd?.lower || 30.0} – ${ci.ai_cost_range_usd?.upper || 48.0}
            </p>
          </div>
        </div>

        {/* Weekly Timeline Progression */}
        {f.weekly_timeline && (
          <div>
            <h4 className="text-sm font-bold text-zinc-200 mb-3">Weekly Workload Distribution</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {f.weekly_timeline.map((wt: any) => (
                <div key={wt.week} className="p-4 bg-zinc-950/60 border border-zinc-800/80 rounded-lg text-xs space-y-1">
                  <p className="font-bold text-indigo-400">{wt.week}</p>
                  <p className="text-zinc-300">Expected Leads: {wt.leads}</p>
                  <p className="text-zinc-300">Support Load: {wt.support}</p>
                  <p className="text-emerald-400">AI Tokens Cost: ${wt.ai_cost_usd?.toFixed(2)}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
