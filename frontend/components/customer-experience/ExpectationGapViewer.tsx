'use client';

import React from 'react';
import { Split, ShieldAlert, CheckCircle2, ArrowRight } from 'lucide-react';
import { ExpectationGapItem } from '../../lib/api/customerExperience';

interface ExpectationGapViewerProps {
  gaps: ExpectationGapItem[];
}

export const ExpectationGapViewer: React.FC<ExpectationGapViewerProps> = ({ gaps }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Split className="h-4 w-4 text-amber-400" />
          Expectation Gap Analysis (Promised vs Delivered)
        </h3>
        <span className="text-xs text-slate-400 font-mono">Gaps: {gaps.length}</span>
      </div>

      <div className="space-y-3">
        {gaps.map((gap) => (
          <div key={gap.id} className="p-3.5 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-200">{gap.area}</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase font-semibold">
                {gap.gap_severity}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded bg-slate-900/60 border border-slate-800/80">
                <div className="text-[10px] uppercase font-mono text-indigo-400 font-semibold mb-1">Contractually Promised</div>
                <p className="text-slate-300">{gap.promised_capability}</p>
              </div>
              <div className="p-2.5 rounded bg-slate-900/60 border border-slate-800/80">
                <div className="text-[10px] uppercase font-mono text-emerald-400 font-semibold mb-1">Delivered Reality</div>
                <p className="text-slate-300">{gap.delivered_reality}</p>
              </div>
            </div>

            {gap.remediation_action && (
              <div className="text-[11px] text-slate-400 flex items-center gap-1.5 pt-1 border-t border-slate-800/60">
                <ArrowRight className="h-3.5 w-3.5 text-indigo-400 flex-shrink-0" />
                <span>Remediation: {gap.remediation_action}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
