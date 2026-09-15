'use client';

import React, { useState } from 'react';
import { ProviderConfiguration } from '@/lib/api/administration';

interface IntegrationsViewProps {
  providers: ProviderConfiguration[];
  onRefresh: () => void;
}

export function IntegrationsView({ providers, onRefresh }: IntegrationsViewProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const categories = ['ALL', ...Array.from(new Set(providers.map((p) => p.category)))];

  const filteredProviders =
    selectedCategory === 'ALL'
      ? providers
      : providers.filter((p) => p.category.toLowerCase() === selectedCategory.toLowerCase());

  return (
    <div className="space-y-6">
      {/* Filters and Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur">
        <div>
          <h3 className="text-lg font-semibold text-white">External Integration & Provider Gateway</h3>
          <p className="text-xs text-slate-400">
            Real-time latency telemetry, secret references, and health monitoring for third-party upstream providers
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Grid of Providers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredProviders.map((prov) => {
          const isHealthy = prov.health_status === 'HEALTHY';
          return (
            <div
              key={prov.provider_id}
              className="bg-slate-900/40 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition space-y-3"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-sm font-bold text-white">{prov.name}</h4>
                  <code className="text-xs font-mono text-cyan-400 block">{prov.provider_id}</code>
                </div>
                <span
                  className={`text-[10px] font-bold uppercase px-2.5 py-1 rounded border ${
                    isHealthy
                      ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                      : 'bg-rose-950 text-rose-300 border-rose-800'
                  }`}
                >
                  {prov.health_status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs pt-1">
                <div className="bg-slate-950/60 p-2 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-500 uppercase block">Category</span>
                  <span className="font-semibold text-slate-300">{prov.category}</span>
                </div>
                <div className="bg-slate-950/60 p-2 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-500 uppercase block">Latency</span>
                  <span className="font-semibold text-emerald-400 font-mono">{prov.latency_ms}ms</span>
                </div>
                <div className="bg-slate-950/60 p-2 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-500 uppercase block">Rate Limit</span>
                  <span className="font-semibold text-slate-300 font-mono">{prov.rate_limit_rpm} RPM</span>
                </div>
                <div className="bg-slate-950/60 p-2 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-500 uppercase block">Timeout</span>
                  <span className="font-semibold text-slate-300 font-mono">{prov.timeout_seconds}s</span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800/80 flex justify-between items-center text-[11px] text-slate-400">
                <div className="flex items-center gap-1.5">
                  <span>Secret Ref:</span>
                  <code className="font-mono text-indigo-400 bg-indigo-950/40 px-1.5 py-0.5 rounded">
                    {prov.secret_reference}
                  </code>
                </div>
                <span>Error: {prov.error_rate_percentage}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
