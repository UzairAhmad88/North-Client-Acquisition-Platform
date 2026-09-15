'use client';

import React from 'react';
import { RiskHeatmapItem } from '@/lib/api/securityOps';
import { ShieldCheck, TrendingUp, AlertTriangle } from 'lucide-react';

interface RiskScoreProps {
  heatmap: RiskHeatmapItem[];
  loading: boolean;
}

export default function RiskScore({ heatmap, loading }: RiskScoreProps) {
  const getSeverityBadge = (severity: string) => {
    const s = severity.toLowerCase();
    if (s === 'critical') return 'bg-rose-100 text-rose-800 border-rose-300';
    if (s === 'high') return 'bg-orange-100 text-orange-800 border-orange-300';
    if (s === 'medium') return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-emerald-100 text-emerald-800 border-emerald-300';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-indigo-600" />
            Security Risk Heatmap & Multi-Vector Evaluation
          </h3>
          <p className="text-xs text-slate-500">
            Probability × Potential Impact × Evidence Strength × Blast Radius (Sections 16 & 35)
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700">
          <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2.5 px-3">Domain</th>
              <th className="py-2.5 px-3">Threat Category</th>
              <th className="py-2.5 px-3">Risk Score</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Probability</th>
              <th className="py-2.5 px-3">Exposure</th>
              <th className="py-2.5 px-3">Control Strength</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Computing risk matrix...
                </td>
              </tr>
            ) : heatmap.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  No risk data available.
                </td>
              </tr>
            ) : (
              heatmap.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-3 font-semibold text-slate-900">
                    {row.domain}
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {row.category}
                  </td>
                  <td className="py-3 px-3 font-bold text-slate-900">
                    {row.risk_score} <span className="text-[10px] font-normal text-slate-400">/100</span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getSeverityBadge(row.severity)}`}>
                      {row.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-600 font-medium">
                    {row.probability}
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-semibold ${row.exposure === 'Critical' || row.exposure === 'High' ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-700'}`}>
                      {row.exposure}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-medium text-slate-700">
                    {row.control_strength}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
