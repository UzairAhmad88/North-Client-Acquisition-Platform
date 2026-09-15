'use client';

import React, { useState } from 'react';
import { EnvironmentDefinition, administrationApi } from '@/lib/api/administration';

interface EnvironmentsViewProps {
  environments: EnvironmentDefinition[];
  onRefresh: () => void;
}

export function EnvironmentsView({ environments, onRefresh }: EnvironmentsViewProps) {
  const [sourceEnv, setSourceEnv] = useState<string>('STAGING');
  const [targetEnv, setTargetEnv] = useState<string>('PRODUCTION');
  const [keysToPromote, setKeysToPromote] = useState<string>('system.rate_limit_per_minute, ai.guardrails.enabled');
  const [isPromoting, setIsPromoting] = useState(false);

  const handlePromote = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsPromoting(true);
    try {
      const keys = keysToPromote.split(',').map((k) => k.trim()).filter(Boolean);
      await administrationApi.promoteEnvironmentConfig({
        source_env: sourceEnv,
        target_env: targetEnv,
        keys,
      });
      alert('Promotion request created and applied successfully.');
      onRefresh();
    } catch (err: any) {
      alert(`Promotion failed: ${err.message || err}`);
    } finally {
      setIsPromoting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Environments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {environments.map((env) => (
          <div
            key={env.env_id}
            className={`border rounded-2xl p-5 backdrop-blur transition ${
              env.is_production
                ? 'bg-indigo-950/20 border-indigo-700/80 shadow-lg shadow-indigo-950/20'
                : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <h4 className="text-sm font-bold text-white">{env.name}</h4>
                <code className="text-xs font-mono text-slate-400">{env.env_type}</code>
              </div>
              <span
                className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                  env.status === 'ACTIVE'
                    ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                    : 'bg-slate-800 text-slate-400 border-slate-700'
                }`}
              >
                {env.status}
              </span>
            </div>

            <div className="mt-4 space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Active Version:</span>
                <span className="font-mono font-semibold text-slate-200">{env.active_version}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Approval Required:</span>
                <span className={env.requires_approval_for_changes ? 'text-amber-400 font-semibold' : 'text-slate-500'}>
                  {env.requires_approval_for_changes ? 'YES (Strict)' : 'NO'}
                </span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Mock Providers:</span>
                <span className={env.allow_mock_providers ? 'text-emerald-400' : 'text-rose-400'}>
                  {env.allow_mock_providers ? 'Allowed' : 'Prohibited'}
                </span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Chaos Testing:</span>
                <span className={env.allow_chaos_testing ? 'text-amber-400' : 'text-slate-500'}>
                  {env.allow_chaos_testing ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Real Financial Execution:</span>
                <span className={env.allow_real_financial_execution ? 'text-emerald-400 font-semibold' : 'text-slate-500'}>
                  {env.allow_real_financial_execution ? 'Live Gateway' : 'Sandboxed'}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Promotion Workflow Form */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur shadow-xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>🚀</span>
          <span>Environment Configuration Promotion Pipeline</span>
        </h3>
        <p className="text-xs text-slate-400">
          Promote verified configuration keys from lower environments into production with automatic audit tracking.
        </p>

        <form onSubmit={handlePromote} className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Source Environment</label>
            <select
              value={sourceEnv}
              onChange={(e) => setSourceEnv(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200"
            >
              <option value="DEVELOPMENT">DEVELOPMENT</option>
              <option value="STAGING">STAGING</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Target Environment</label>
            <select
              value={targetEnv}
              onChange={(e) => setTargetEnv(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200"
            >
              <option value="STAGING">STAGING</option>
              <option value="PRODUCTION">PRODUCTION</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={isPromoting}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 px-4 rounded-lg text-xs transition"
            >
              {isPromoting ? 'Promoting...' : 'Promote Configurations'}
            </button>
          </div>

          <div className="md:col-span-3">
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Configuration Keys (Comma-separated)
            </label>
            <input
              type="text"
              value={keysToPromote}
              onChange={(e) => setKeysToPromote(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200 font-mono"
              required
            />
          </div>
        </form>
      </div>
    </div>
  );
}
