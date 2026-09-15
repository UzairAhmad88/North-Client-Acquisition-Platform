'use client';

import React from 'react';
import { Clock, TrendingDown, Zap, BarChart2 } from 'lucide-react';

interface Props {
  cycleMetrics?: {
    total_cases: number;
    average_cycle_time_seconds: number;
    average_processing_time_seconds: number;
    average_waiting_time_seconds: number;
    flow_efficiency_percentage: number;
  };
}

export default function CycleTimeChart({ cycleMetrics }: Props) {
  const metrics = cycleMetrics || {
    total_cases: 24,
    average_cycle_time_seconds: 34200,
    average_processing_time_seconds: 7200,
    average_waiting_time_seconds: 27000,
    flow_efficiency_percentage: 21.05,
  };

  const processingPct = Math.round((metrics.average_processing_time_seconds / (metrics.average_cycle_time_seconds || 1)) * 100);
  const waitingPct = 100 - processingPct;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Clock className="w-5 h-5 text-indigo-400" /> Cycle-Time & Flow Efficiency Analysis
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Separation of Value-Adding processing duration from waiting and queue latency
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
          <span className="text-xs text-slate-400">Total Avg Cycle Time</span>
          <p className="text-2xl font-bold text-white mt-1">{Math.round(metrics.average_cycle_time_seconds / 3600 * 10) / 10} hrs</p>
          <span className="text-xs text-slate-500">{metrics.average_cycle_time_seconds}s total</span>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
          <span className="text-xs text-slate-400">Value-Adding Processing</span>
          <p className="text-2xl font-bold text-emerald-400 mt-1">{Math.round(metrics.average_processing_time_seconds / 3600 * 10) / 10} hrs</p>
          <span className="text-xs text-emerald-500/80 font-mono">{processingPct}% of cycle</span>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
          <span className="text-xs text-slate-400">Waiting & Queue Latency</span>
          <p className="text-2xl font-bold text-amber-400 mt-1">{Math.round(metrics.average_waiting_time_seconds / 3600 * 10) / 10} hrs</p>
          <span className="text-xs text-amber-500/80 font-mono">{waitingPct}% wasted time</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-slate-400 font-medium">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Value Add Processing ({processingPct}%)</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Queue & Waiting ({waitingPct}%)</span>
        </div>
        <div className="w-full h-4 bg-slate-950 rounded-full overflow-hidden flex border border-slate-800">
          <div style={{ width: `${processingPct}%` }} className="bg-emerald-500 h-full"></div>
          <div style={{ width: `${waitingPct}%` }} className="bg-amber-500 h-full"></div>
        </div>
      </div>
    </div>
  );
}
