'use client';

import React from 'react';
import { DeepHealthResult } from '@/lib/api/reliability';

interface Props {
  health: DeepHealthResult | null;
  onRefresh: () => void;
  isLoading: boolean;
}

export function HealthOverview({ health, onRefresh, isLoading }: Props) {
  if (!health) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 text-center text-slate-400">
        Loading health telemetry...
      </div>
    );
  }

  const isHealthy = health.status === 'HEALTHY';
  const isDegraded = health.status === 'DEGRADED';

  const statusColor = isHealthy
    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    : isDegraded
    ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    : 'bg-rose-500/10 text-rose-400 border-rose-500/30';

  const componentsList = Object.values(health.components || {});
  const healthyCount = componentsList.filter((c) => c.status === 'HEALTHY').length;
  const degradedCount = componentsList.filter((c) => c.status !== 'HEALTHY').length;

  return (
    <div className="space-y-4">
      {/* Top Banner Status */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div className="flex items-center gap-4">
          <div className={`px-4 py-2 rounded-xl text-lg font-bold border flex items-center gap-2 ${statusColor}`}>
            <span className={`w-3 h-3 rounded-full ${isHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400 animate-ping'}`} />
            {health.status}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">System Reliability Posture</h3>
            <p className="text-xs text-slate-400">
              Deep health probing {componentsList.length} primary infrastructure components
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition flex items-center gap-2"
          >
            <span>🔄</span> {isLoading ? 'Probing...' : 'Re-probe All Subsystems'}
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Healthy Components</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">
            {healthyCount} <span className="text-xs text-slate-500">/ {componentsList.length}</span>
          </div>
          <div className="text-[10px] text-emerald-500/80 mt-1">Operational & nominal latency</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Circuit Breakers</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{health.active_circuit_breakers}</div>
          <div className="text-[10px] text-slate-500 mt-1">Isolating faulty upstream providers</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Open Incidents</div>
          <div className={`text-2xl font-bold mt-1 ${health.open_incidents > 0 ? 'text-amber-400' : 'text-slate-300'}`}>
            {health.open_incidents}
          </div>
          <div className="text-[10px] text-slate-500 mt-1">Under active mitigation</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Degraded / Unhealthy</div>
          <div className={`text-2xl font-bold mt-1 ${degradedCount > 0 ? 'text-rose-400' : 'text-slate-400'}`}>
            {degradedCount}
          </div>
          <div className="text-[10px] text-slate-500 mt-1">Degraded dependencies</div>
        </div>
      </div>
    </div>
  );
}
