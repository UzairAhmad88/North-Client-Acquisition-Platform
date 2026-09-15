'use client';

import React, { useState } from 'react';
import { DriftItem, administrationApi } from '@/lib/api/administration';

interface DriftDetectorViewProps {
  drifts: DriftItem[];
  onRefresh: () => void;
}

export function DriftDetectorView({ drifts, onRefresh }: DriftDetectorViewProps) {
  const [resolvingId, setResolvingId] = useState<string | null>(null);

  const handleResolveDrift = async (driftId: string) => {
    setResolvingId(driftId);
    try {
      await administrationApi.resolveDrift(driftId);
      onRefresh();
    } catch (err: any) {
      alert(`Failed to resolve configuration drift: ${err.message || err}`);
    } finally {
      setResolvingId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur">
        <div>
          <h3 className="text-lg font-semibold text-white">Runtime Configuration Drift Detector</h3>
          <p className="text-xs text-slate-400">
            Detects discrepancies between declared database configuration schema and live in-memory runtime parameters
          </p>
        </div>
        <span
          className={`text-xs font-bold uppercase px-3 py-1 rounded-full border ${
            drifts.length === 0
              ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
              : 'bg-rose-950 text-rose-300 border-rose-800 animate-pulse'
          }`}
        >
          {drifts.length === 0 ? '0 DRIFTS DETECTED' : `${drifts.length} DRIFTS OUT OF SYNC`}
        </span>
      </div>

      {/* Drifts List */}
      {drifts.length === 0 ? (
        <div className="bg-slate-900/30 border border-slate-800 rounded-2xl p-12 text-center space-y-3">
          <span className="text-4xl">✨</span>
          <h4 className="text-base font-bold text-white">All Subsystems Fully Synchronized</h4>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Zero configuration drift detected. In-memory runtime instances across all workers and API nodes match database declarations.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {drifts.map((d) => (
            <div
              key={d.drift_id}
              className="bg-slate-900/40 border border-rose-850/60 rounded-xl p-5 hover:border-rose-700/80 transition space-y-3"
            >
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                <div className="flex items-center gap-2.5">
                  <span className="text-sm font-bold text-white font-mono">{d.key}</span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                    {d.severity}
                  </span>
                  <span className="text-[10px] text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                    {d.environment}
                  </span>
                </div>
                <button
                  onClick={() => handleResolveDrift(d.drift_id)}
                  disabled={resolvingId === d.drift_id}
                  className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-1.5 px-3 rounded-lg text-xs transition"
                >
                  {resolvingId === d.drift_id ? 'Reconciling...' : 'Reconcile & Sync'}
                </button>
              </div>

              {/* Side-by-side comparison */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-1 font-mono">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="text-[10px] text-emerald-400 uppercase font-bold block">
                    Expected Declared Value
                  </span>
                  <span className="text-emerald-300 block">{JSON.stringify(d.expected_value)}</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-lg border border-rose-900/50 space-y-1">
                  <span className="text-[10px] text-rose-400 uppercase font-bold block">
                    Actual Live Runtime Value
                  </span>
                  <span className="text-rose-300 block">{JSON.stringify(d.actual_value)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
