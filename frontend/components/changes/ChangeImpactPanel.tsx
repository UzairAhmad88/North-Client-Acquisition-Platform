'use client';

import React from 'react';
import { ChangeVersion } from '@/lib/api/changes';
import { Layers, Clock, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

interface ChangeImpactPanelProps {
  version?: ChangeVersion;
}

export const ChangeImpactPanel: React.FC<ChangeImpactPanelProps> = ({ version }) => {
  if (!version) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 text-xs text-slate-500 text-center py-8">
        Run AI Impact Analysis to evaluate scope, schedule, and technical impacts.
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Layers className="w-5 h-5 text-purple-400" />
            <span>Multi-Dimensional Impact Analysis</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Scope version v{version.version_number} — SHA-256: <code className="text-slate-300 font-mono text-[11px]">{version.content_hash.slice(0, 12)}...</code>
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-1">
          <div className="text-[11px] text-slate-400">Scope Delta Summary</div>
          <p className="text-xs font-semibold text-slate-200">{version.scope_summary || 'Evaluated'}</p>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-1">
          <div className="text-[11px] text-slate-400">Estimated Schedule Shift</div>
          <p className="text-xs font-semibold text-amber-400 flex items-center space-x-1">
            <Clock className="w-3.5 h-3.5" />
            <span>{version.schedule_summary || '0 Days'}</span>
          </p>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-1">
          <div className="text-[11px] text-slate-400">Commercial Impact</div>
          <p className="text-xs font-semibold text-emerald-400">{version.commercial_summary || 'No Delta'}</p>
        </div>
      </div>

      {/* Impact Items Breakdown */}
      <div className="space-y-3">
        <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Affected System Components</h4>
        {version.impacts?.length === 0 ? (
          <p className="text-xs text-slate-500">No specific component impacts logged.</p>
        ) : (
          <div className="divide-y divide-slate-800 border border-slate-800 rounded-xl bg-slate-950 overflow-hidden">
            {version.impacts?.map((imp) => (
              <div key={imp.id} className="p-3.5 flex items-start justify-between text-xs hover:bg-slate-900/50">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                      {imp.impact_type}
                    </span>
                    <span className="font-semibold text-white">{imp.impact_action}</span>
                  </div>
                  <p className="text-slate-400 text-[11px]">{imp.impact_description}</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  {imp.confidence} Confidence
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
