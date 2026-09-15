'use client';

import React from 'react';
import { FeatureFlag } from '@/lib/api/reliability';

interface Props {
  flags: FeatureFlag[];
  onToggleFlag: (flag: FeatureFlag) => void;
  onUpdateRollout: (flag: FeatureFlag, newPct: number) => void;
}

export function FeatureFlagController({ flags, onToggleFlag, onUpdateRollout }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Feature Flags, Canary Rollouts & Kill-Switches</h3>
          <p className="text-xs text-slate-400">
            Tenant-aware capability gating, percentage rollouts, and instant fault isolation kill-switches
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {flags.map((f) => (
          <div key={f.name} className="bg-slate-950/60 border border-slate-800/80 p-5 rounded-xl space-y-4">
            <div className="flex items-start justify-between gap-2">
              <div>
                <div className="text-xs font-bold text-white uppercase font-mono">{f.name}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">{f.description || 'No description'}</div>
              </div>

              <button
                onClick={() => onToggleFlag({ ...f, enabled: !f.enabled })}
                className={`px-3 py-1 text-xs font-semibold rounded-lg border transition ${
                  f.enabled
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30'
                    : 'bg-rose-500/20 text-rose-300 border-rose-500/40 hover:bg-rose-500/30'
                }`}
              >
                {f.enabled ? 'ACTIVE' : 'DISABLED'}
              </button>
            </div>

            {/* Percentage Rollout Slider */}
            <div>
              <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                <span>Canary Traffic Allocation</span>
                <span className="font-mono text-cyan-400 font-bold">{f.percentage_rollout}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="5"
                value={f.percentage_rollout}
                onChange={(e) => onUpdateRollout(f, parseInt(e.target.value, 10))}
                className="w-full accent-cyan-400 bg-slate-800 h-1.5 rounded-lg cursor-pointer"
              />
            </div>

            {/* Allowed Tiers */}
            <div className="pt-2 border-t border-slate-800/50 flex items-center justify-between text-[10px] text-slate-400">
              <span>Allowed Tiers:</span>
              <div className="flex gap-1">
                {(f.allowed_tiers || ['ALL']).map((t) => (
                  <span key={t} className="px-1.5 py-0.5 bg-slate-800 text-slate-300 rounded font-mono">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
