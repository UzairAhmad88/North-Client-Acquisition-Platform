'use client';

import React from 'react';
import { AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';
import { DealRiskItem } from '../../lib/api/revenueGrowth';

interface DealRiskRadarProps {
  risks: DealRiskItem[];
}

export const DealRiskRadar: React.FC<DealRiskRadarProps> = ({ risks }) => {
  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'critical':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase font-semibold">Critical</span>;
      case 'high':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase font-semibold">High</span>;
      default:
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase font-semibold">Medium</span>;
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-amber-400" />
          Deal Risk & Commercial Vulnerabilities
        </h3>
        <span className="text-xs text-slate-400 font-mono">Open Risks: {risks.length}</span>
      </div>

      <div className="space-y-2.5">
        {risks.map((r) => (
          <div key={r.id} className="p-3 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-200 capitalize">{r.risk_category.replace('_', ' ')}</span>
              {getSeverityBadge(r.severity)}
            </div>
            <p className="text-xs text-slate-300">{r.description}</p>
            {r.mitigation_strategy && (
              <div className="flex items-center gap-1.5 pt-1 border-t border-slate-800/60 text-[11px] text-slate-400">
                <ArrowRight className="h-3.5 w-3.5 text-indigo-400 flex-shrink-0" />
                <span>Mitigation: {r.mitigation_strategy}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
