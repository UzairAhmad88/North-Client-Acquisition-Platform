'use client';

import React, { useState, useEffect } from 'react';
import { digitalTwinApi, SensitivityRanking } from '@/lib/api/digitalTwin';

export const SensitivityChart: React.FC = () => {
  const [rankings, setRankings] = useState<SensitivityRanking[]>([]);
  const [loading, setLoading] = useState(false);
  const [targetMetric, setTargetMetric] = useState('cumulative_revenue_usd');

  const fetchSensitivity = async () => {
    setLoading(true);
    try {
      const res = await digitalTwinApi.getSensitivity({ target_metric: targetMetric });
      setRankings(Array.isArray(res) ? res : ((res as any)?.data || []));
    } catch (err) {
      console.error('Failed to load sensitivity analysis', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSensitivity();
  }, [targetMetric]);

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Parameter Elasticity & Tornado Rankings</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Evaluates which business variables exert the greatest leverage on key outcomes.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Target Metric:</label>
          <select
            value={targetMetric}
            onChange={(e) => setTargetMetric(e.target.value)}
            className="px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="cumulative_revenue_usd">Cumulative Revenue ($)</option>
            <option value="cumulative_net_profit_usd">Cumulative Net Profit ($)</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center p-8 text-slate-400">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500 mr-3"></div>
          Computing parameter elasticity sweeps...
        </div>
      ) : rankings.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No sensitivity data available.</div>
      ) : (
        <div className="space-y-3">
          {rankings.map((r, idx) => {
            const pct = Math.min(100, Math.round(r.sensitivity_score * 100));
            const badgeColor =
              r.impact_level === 'CRITICAL'
                ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                : r.impact_level === 'HIGH'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                : 'bg-slate-800 text-slate-300 border-slate-700';

            return (
              <div
                key={idx}
                className="p-3.5 bg-slate-950/60 rounded-xl border border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-3"
              >
                <div className="min-w-[200px]">
                  <div className="text-sm font-semibold text-white">{r.parameter_name}</div>
                  <div className="text-xs text-slate-500 font-mono">{r.parameter_code}</div>
                </div>

                {/* Tornado Bar Visual */}
                <div className="flex-1 max-w-md">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>-${r.low_impact_value.toLocaleString()}</span>
                    <span className="font-semibold text-white">Score: {r.sensitivity_score.toFixed(3)}</span>
                    <span>+${r.high_impact_value.toLocaleString()}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        r.impact_level === 'CRITICAL' ? 'bg-rose-500' : r.impact_level === 'HIGH' ? 'bg-amber-500' : 'bg-indigo-500'
                      }`}
                      style={{ width: `${Math.max(10, pct)}%` }}
                    ></div>
                  </div>
                </div>

                <div className="min-w-[100px] text-right">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeColor}`}>
                    {r.impact_level}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
