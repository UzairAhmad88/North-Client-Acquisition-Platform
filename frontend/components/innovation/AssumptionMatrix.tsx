'use client';

import React from 'react';
import { Target, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';
import { InnovationAssumption } from '../../lib/api/innovation';

interface AssumptionMatrixProps {
  assumptions: InnovationAssumption[];
}

export const AssumptionMatrix: React.FC<AssumptionMatrixProps> = ({ assumptions }) => {
  const getPriorityBadge = (priority: string) => {
    switch (priority?.toUpperCase()) {
      case 'CRITICAL':
        return { label: 'High Impact / High Uncertainty (Critical)', color: 'bg-rose-500/10 text-rose-300 border-rose-500/30' };
      case 'HIGH':
        return { label: 'High Impact / Low Uncertainty', color: 'bg-amber-500/10 text-amber-300 border-amber-500/30' };
      case 'MEDIUM':
        return { label: 'Low Impact / High Uncertainty', color: 'bg-blue-500/10 text-blue-300 border-blue-500/30' };
      default:
        return { label: 'Low Impact / Low Uncertainty', color: 'bg-slate-500/10 text-slate-300 border-slate-500/30' };
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Target className="h-4 w-4 text-indigo-400" />
            2x2 Impact vs Uncertainty Assumption Mapping
          </h3>
          <p className="text-xs text-slate-400">
            Assumptions ranked for experiment validation priority. High-impact/high-uncertainty tested first.
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
          {assumptions.length} Assumptions
        </span>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {assumptions.length === 0 ? (
          <div className="text-center py-6 text-xs text-slate-500">
            No mapped assumptions for this hypothesis yet.
          </div>
        ) : (
          assumptions.map((asm) => {
            const badge = getPriorityBadge(asm.validation_priority);
            return (
              <div
                key={asm.id}
                className="p-3.5 rounded-lg border border-slate-800 bg-slate-950/40 flex items-start justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-400 border border-slate-700 font-semibold">
                      {asm.category}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded border font-semibold ${badge.color}`}>
                      {badge.label}
                    </span>
                  </div>
                  <p className="text-xs text-slate-200 leading-relaxed">
                    "{asm.assumption_text}"
                  </p>
                </div>

                <div className="shrink-0 pt-1">
                  {asm.is_validated ? (
                    <span className="flex items-center gap-1 text-[10px] text-emerald-400 font-semibold">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Validated
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[10px] text-amber-400 font-semibold">
                      <AlertTriangle className="h-3.5 w-3.5" /> Needs Test
                    </span>
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
