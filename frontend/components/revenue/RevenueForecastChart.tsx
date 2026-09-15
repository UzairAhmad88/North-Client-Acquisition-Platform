'use client';

import React from 'react';
import { TrendingUp, BarChart3, ShieldCheck, HelpCircle } from 'lucide-react';
import { SalesForecastItem } from '../../lib/api/revenueGrowth';

interface RevenueForecastChartProps {
  forecasts: SalesForecastItem[];
}

export const RevenueForecastChart: React.FC<RevenueForecastChartProps> = ({ forecasts }) => {
  const baseForecast = forecasts.find((f) => f.scenario === 'base') || forecasts[0] || {
    forecast_period: 'Q4-2026',
    p10_usd: 994000,
    p25_usd: 1207000,
    p50_usd: 1420000,
    p75_usd: 1633000,
    p90_usd: 1846000,
    pipeline_total_usd: 3850000,
  };

  const percentiles = [
    { label: 'P10 (Floor)', value: baseForecast.p10_usd, color: 'from-slate-600 to-slate-500', desc: '90% probability to exceed' },
    { label: 'P25 (Conservative)', value: baseForecast.p25_usd, color: 'from-blue-600 to-blue-500', desc: '75% probability to exceed' },
    { label: 'P50 (Expected Base)', value: baseForecast.p50_usd, color: 'from-indigo-600 to-indigo-500', desc: 'Most likely median outcome' },
    { label: 'P75 (Strong Upside)', value: baseForecast.p75_usd, color: 'from-purple-600 to-purple-500', desc: 'Accelerated conversion velocity' },
    { label: 'P90 (Stretch Target)', value: baseForecast.p90_usd, color: 'from-emerald-600 to-emerald-500', desc: 'High-leverage scenario' },
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-emerald-400" />
            Probabilistic Revenue Forecast Distribution
          </h3>
          <p className="text-xs text-slate-400 font-mono">Period: {baseForecast.forecast_period} | Model: Probabilistic Ensemble v3</p>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
          Calibrated P50: ${(baseForecast.p50_usd / 1000).toFixed(0)}k
        </span>
      </div>

      <div className="space-y-3 pt-2">
        {percentiles.map((p) => {
          const pctWidth = Math.min(100, Math.max(15, (p.value / (baseForecast.p90_usd * 1.1)) * 100));

          return (
            <div key={p.label} className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">{p.label}</span>
                <span className="font-mono text-white font-bold">${p.value.toLocaleString()}</span>
              </div>
              <div className="h-3 w-full bg-slate-800 rounded-full overflow-hidden flex items-center">
                <div
                  className={`h-full bg-gradient-to-r ${p.color} rounded-full transition-all duration-500`}
                  style={{ width: `${pctWidth}%` }}
                />
              </div>
              <div className="text-[10px] text-slate-500 text-right">{p.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
