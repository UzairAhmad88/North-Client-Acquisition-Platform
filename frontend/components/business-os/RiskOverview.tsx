'use client';

import React from 'react';
import { OrganizationalRisk } from '@/lib/api/business_os';

interface RiskOverviewProps {
  risks: OrganizationalRisk[];
}

export const RiskOverview: React.FC<RiskOverviewProps> = ({ risks }) => {
  const getSeverityStyle = (sev: string) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'HIGH':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/30';
      case 'MEDIUM':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>🛡️</span> Enterprise Organizational Risk Matrix
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Probability × Impact scoring with evidence signals, mitigations, and owner accountability.
          </p>
        </div>
        <span className="px-3 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded-full text-xs font-semibold">
          {risks.filter(r => r.severity === 'HIGH' || r.severity === 'CRITICAL').length} High/Critical Risks
        </span>
      </div>

      <div className="space-y-4">
        {risks.map((risk) => (
          <div key={risk.risk_id} className="bg-slate-950/60 border border-slate-800 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${getSeverityStyle(risk.severity)}`}>
                  {risk.severity} ({risk.risk_score}/25)
                </span>
                <span className="font-semibold text-slate-100 text-sm">{risk.title}</span>
              </div>
              <span className="text-xs text-slate-400">Owner: <strong className="text-slate-200">{risk.owner}</strong></span>
            </div>

            <p className="text-xs text-slate-400 mb-3">{risk.description}</p>

            {/* Evidence & Mitigation */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-900/60 border border-slate-800/80 rounded-md p-3">
              <div>
                <span className="font-bold text-slate-300">Evidence Signals:</span>
                <ul className="list-disc list-inside text-slate-400 mt-1 space-y-0.5">
                  {risk.evidence_signals.map((sig, i) => (
                    <li key={i}>{sig}</li>
                  ))}
                </ul>
              </div>
              <div>
                <span className="font-bold text-emerald-400">Mitigation Strategy:</span>
                <p className="text-slate-300 mt-1">{risk.mitigation_strategy || 'Mitigation plan under evaluation.'}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
