'use client';

import React, { useState } from 'react';
import { FeatureFlagItem, administrationApi } from '@/lib/api/administration';

interface FeatureFlagsViewProps {
  flags: FeatureFlagItem[];
  onRefresh: () => void;
}

export function FeatureFlagsView({ flags, onRefresh }: FeatureFlagsViewProps) {
  const [selectedEnv, setSelectedEnv] = useState<string>('ALL');
  const [updatingKey, setUpdatingKey] = useState<string | null>(null);

  const environments = ['ALL', 'PRODUCTION', 'STAGING', 'DEVELOPMENT'];

  const filteredFlags =
    selectedEnv === 'ALL' ? flags : flags.filter((f) => f.environment.toUpperCase() === selectedEnv.toUpperCase());

  const handleToggleStatus = async (flag: FeatureFlagItem) => {
    setUpdatingKey(flag.key);
    try {
      const nextStatus = flag.status === 'ENABLED' ? 'DISABLED' : 'ENABLED';
      await administrationApi.updateFlagStatus(flag.key, nextStatus);
      onRefresh();
    } catch (err: any) {
      alert(`Failed to update flag status: ${err.message || err}`);
    } finally {
      setUpdatingKey(null);
    }
  };

  const handlePercentageChange = async (flag: FeatureFlagItem, newPct: number) => {
    try {
      await administrationApi.updateFlagRollout(flag.key, {
        rollout_type: flag.rollout_type,
        rollout_percentage: newPct,
        allowed_tiers: flag.allowed_tiers,
      });
      onRefresh();
    } catch (err: any) {
      alert(`Failed to update rollout percentage: ${err.message || err}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Env Filter */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur">
        <div>
          <h3 className="text-lg font-semibold text-white">Feature Flag & Canary Rollout Matrix</h3>
          <p className="text-xs text-slate-400">
            Dynamically gate capabilities by tenant tier, percentage rollouts, or environment targets
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Environment:</label>
          <select
            value={selectedEnv}
            onChange={(e) => setSelectedEnv(e.target.value)}
            className="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {environments.map((env) => (
              <option key={env} value={env}>
                {env}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Flag List */}
      <div className="grid grid-cols-1 gap-4">
        {filteredFlags.map((flag) => {
          const isEnabled = flag.status === 'ENABLED' || flag.status === 'CANARY';
          return (
            <div
              key={flag.key}
              className="bg-slate-900/40 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition"
            >
              <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2.5">
                    <span className="text-sm font-bold text-white">{flag.name}</span>
                    <code className="text-xs font-mono text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40">
                      {flag.key}
                    </code>
                    <span
                      className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                        flag.status === 'ENABLED'
                          ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                          : flag.status === 'CANARY'
                          ? 'bg-indigo-950 text-indigo-300 border-indigo-800'
                          : flag.status === 'SUNSET'
                          ? 'bg-amber-950 text-amber-300 border-amber-800'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      {flag.status}
                    </span>
                    <span className="text-[10px] text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                      {flag.environment}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{flag.description}</p>
                  <div className="flex items-center gap-3 text-[11px] text-slate-500 pt-1">
                    <span>Strategy: <strong className="text-slate-300">{flag.rollout_type}</strong></span>
                    <span>•</span>
                    <span>Tiers: <strong className="text-slate-300">{flag.allowed_tiers?.join(', ') || 'All'}</strong></span>
                  </div>
                </div>

                {/* Status Toggle & Percentage Control */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                  {flag.rollout_type === 'PERCENTAGE' && (
                    <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-lg border border-slate-800">
                      <span className="text-[11px] text-slate-400 font-mono">{flag.rollout_percentage}%</span>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        step="5"
                        value={flag.rollout_percentage}
                        onChange={(e) => handlePercentageChange(flag, parseInt(e.target.value, 10))}
                        className="w-24 accent-indigo-500 cursor-pointer"
                      />
                    </div>
                  )}

                  <button
                    onClick={() => handleToggleStatus(flag)}
                    disabled={updatingKey === flag.key}
                    className={`text-xs px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 ${
                      isEnabled
                        ? 'bg-emerald-600 hover:bg-emerald-500 text-white'
                        : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
                    }`}
                  >
                    <span>{isEnabled ? '🟢 ACTIVE' : '⚪ DISABLED'}</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
