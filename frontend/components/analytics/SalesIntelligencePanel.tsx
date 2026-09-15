'use client';

import React from 'react';
import { SalesIntelligence } from '@/lib/api/analytics';

interface SalesIntelligencePanelProps {
  data: SalesIntelligence | null;
  loading: boolean;
}

export const SalesIntelligencePanel: React.FC<SalesIntelligencePanelProps> = ({ data, loading }) => {
  if (loading && !data) {
    return (
      <div className="p-8 text-center text-zinc-400">
        <div className="inline-block animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mb-3"></div>
        <p>Loading Sales Intelligence Funnel...</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Funnel Stage Breakdown */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-bold text-zinc-100">End-to-End Sales Pipeline Funnel</h3>
            <p className="text-xs text-zinc-400 mt-1">Multi-stage conversion rates from discovery to won contracts</p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 bg-zinc-800 text-zinc-300 rounded border border-zinc-700">
            Sample: {data.sample_size} Leads
          </span>
        </div>

        <div className="space-y-3">
          {data.funnel.map((step, idx) => {
            const maxCount = data.funnel[0]?.count || 1;
            const widthPct = Math.max(8, Math.round((step.count / maxCount) * 100));

            return (
              <div key={step.stage} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-zinc-300">
                    {idx + 1}. {step.stage}
                  </span>
                  <div className="flex items-center gap-3">
                    <span className="text-zinc-400">{step.count} leads</span>
                    <span className="text-indigo-400 font-semibold">{step.conversion_to_next_pct}% to next</span>
                  </div>
                </div>
                <div className="w-full bg-zinc-950 rounded-full h-3 overflow-hidden border border-zinc-800/80">
                  <div
                    className="bg-gradient-to-r from-indigo-500 to-purple-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${widthPct}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Lead Score Calibration Analysis */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-zinc-100">Lead Score Precision & Calibration</h3>
            <p className="text-xs text-zinc-400 mt-1">Evaluation of AI scoring bands vs empirical conversion outcomes</p>
          </div>
          <span className="text-xs px-2.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Audit Only • No Auto-Weight Changes
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          {Object.entries(data.score_calibration).map(([band, stats]) => (
            <div key={band} className="bg-zinc-950/60 border border-zinc-800 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-zinc-300">Score Band: {band}</span>
                <span className="text-xs font-extrabold text-emerald-400">{stats.conversion_pct}% won</span>
              </div>
              <div className="mt-3 text-xs text-zinc-400 space-y-1">
                <div className="flex justify-between">
                  <span>Total Leads:</span>
                  <span className="font-semibold text-zinc-200">{stats.count}</span>
                </div>
                <div className="flex justify-between">
                  <span>Converted:</span>
                  <span className="font-semibold text-emerald-400">{stats.won}</span>
                </div>
                <div className="flex justify-between">
                  <span>Lost:</span>
                  <span className="font-semibold text-rose-400">{stats.count - stats.won}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
