"use client";

import React from "react";
import { MarketingForecast } from "@/lib/api/marketing";

interface Props {
  forecasts: MarketingForecast[];
}

export const MarketingForecastChart: React.FC<Props> = ({ forecasts }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Probabilistic Demand Forecasting (P10 – P90)</h3>
          <p className="text-xs text-slate-400 mt-0.5">Monte Carlo simulated distributions across demand scenarios</p>
        </div>
        <span className="text-xs bg-indigo-950 text-indigo-400 border border-indigo-800 px-2.5 py-0.5 rounded-full font-mono">
          v1.0-monte-carlo
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {forecasts.map((fc) => (
          <div key={fc.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-100">{fc.scenario} SCENARIO</span>
              <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono">
                {fc.period}
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400">P10 (Conservative Floor):</span>
                <span className="font-mono text-slate-200">{fc.p10_leads} Leads</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">P25 (Lower Quartile):</span>
                <span className="font-mono text-slate-200">{fc.p25_leads} Leads</span>
              </div>
              <div className="flex items-center justify-between py-1 bg-slate-900/60 px-2 rounded border border-indigo-500/20">
                <span className="text-cyan-400 font-medium">P50 (Expected Median):</span>
                <span className="font-mono font-bold text-cyan-400">{fc.p50_leads} Leads</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">P75 (Upper Quartile):</span>
                <span className="font-mono text-slate-200">{fc.p75_leads} Leads</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">P90 (Optimistic Ceiling):</span>
                <span className="font-mono text-slate-200">{fc.p90_leads} Leads</span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-700/40 text-xs flex justify-between">
              <span className="text-slate-400">Est. Pipeline:</span>
              <span className="text-emerald-400 font-semibold">${fc.p50_pipeline_usd.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
