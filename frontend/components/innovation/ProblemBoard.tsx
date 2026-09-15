'use client';

import React from 'react';
import { AlertCircle, DollarSign, Clock, CheckCircle2, Flame } from 'lucide-react';
import { InnovationProblem } from '../../lib/api/innovation';

interface ProblemBoardProps {
  problems: InnovationProblem[];
}

export const ProblemBoard: React.FC<ProblemBoardProps> = ({ problems }) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL':
        return { label: 'Critical Severity', color: 'bg-rose-500/10 text-rose-400 border-rose-500/30' };
      case 'HIGH':
        return { label: 'High Severity', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
      default:
        return { label: 'Medium Severity', color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Flame className="h-4 w-4 text-rose-400" />
            Validated Customer Problem Repository
          </h3>
          <p className="text-xs text-slate-400">
            Real customer pain points with empirical willingness-to-pay signals and evidence sources.
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
          {problems.length} Problems Cataloged
        </span>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
        {problems.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            No customer problems registered in this workspace yet.
          </div>
        ) : (
          problems.map((prob) => {
            const sev = getSeverityBadge(prob.severity);
            return (
              <div
                key={prob.id}
                className="p-4 rounded-lg border border-slate-800/80 bg-slate-950/40 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <p className="text-xs font-medium text-slate-200 leading-relaxed">
                    "{prob.statement}"
                  </p>
                  <span className={`text-[10px] px-2 py-0.5 rounded border font-semibold shrink-0 ${sev.color}`}>
                    {sev.label}
                  </span>
                </div>

                <div className="flex flex-wrap items-center justify-between gap-2 text-[10px] text-slate-400 pt-2 border-t border-slate-900">
                  <div className="flex items-center gap-3">
                    {prob.affected_users && (
                      <span className="text-indigo-400 font-medium">
                        Users: {prob.affected_users}
                      </span>
                    )}
                    <span className="text-slate-500">
                      Frequency: <span className="text-slate-300 font-mono">{prob.frequency}</span>
                    </span>
                  </div>

                  {prob.willingness_to_pay_signal && (
                    <div className="flex items-center gap-1 text-emerald-400 font-mono font-bold">
                      <DollarSign className="h-3 w-3" />
                      <span>Est WTP: ${prob.willingness_to_pay_signal}/mo</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
