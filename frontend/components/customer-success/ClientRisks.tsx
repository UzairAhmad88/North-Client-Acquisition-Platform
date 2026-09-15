'use client';

import React from 'react';
import { ClientRisk } from '@/lib/api/customer_success';

interface ClientRisksProps {
  risks: ClientRisk[];
}

export function ClientRisks({ risks }: ClientRisksProps) {
  if (!risks || risks.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center text-slate-500">
        No active risks currently detected for this client.
      </div>
    );
  }

  const getSeverityBadge = (s: string) => {
    switch (s.toUpperCase()) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded text-xs font-semibold">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 bg-orange-500/10 text-orange-400 border border-orange-500/30 rounded text-xs font-semibold">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded text-xs font-semibold">MEDIUM</span>;
      default:
        return <span className="px-2 py-0.5 bg-slate-500/10 text-slate-400 border border-slate-500/30 rounded text-xs font-semibold">LOW</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Active Risks & Churn Indicators</h3>
          <p className="text-xs text-slate-400 mt-0.5">Early warning detection grounded in communication telemetry and payment latencies.</p>
        </div>
        <span className="text-xs px-2.5 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-full font-semibold">
          {risks.length} Detected
        </span>
      </div>

      <div className="space-y-3">
        {risks.map((risk, i) => (
          <div key={risk.id || i} className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl space-y-2 hover:border-slate-700 transition">
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-white">{risk.title}</span>
                  {getSeverityBadge(risk.severity)}
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider font-mono">[{risk.category || risk.risk_category}]</span>
                </div>
                {risk.description ? <p className="text-xs text-slate-400 leading-relaxed">{risk.description}</p> : null}
              </div>
              <span className="text-[11px] text-slate-500 shrink-0 font-medium">Status: {risk.status}</span>
            </div>

            {risk.mitigation_plan ? (
              <div className="mt-2 p-2.5 bg-slate-900/80 border border-slate-800 rounded-lg text-xs text-slate-300">
                <span className="font-semibold text-amber-400">Recommended Mitigation: </span>
                {risk.mitigation_plan}
              </div>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}
