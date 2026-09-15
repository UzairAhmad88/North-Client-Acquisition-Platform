'use client';

import React from 'react';
import { GitCommit, AlertTriangle, CheckCircle2, ShieldCheck, Link2 } from 'lucide-react';
import { TraceabilityMatrix, ProductRequirement } from '../../lib/api/productManagement';

interface RequirementsTraceabilityMatrixProps {
  matrix: TraceabilityMatrix;
  onCreateRequirement?: () => void;
}

export const RequirementsTraceabilityMatrix: React.FC<RequirementsTraceabilityMatrixProps> = ({
  matrix,
  onCreateRequirement,
}) => {
  const orphanCount = matrix.orphaned_requirements?.length || 0;
  const scorePercent = Math.round((matrix.traceability_score || 1.0) * 100);

  return (
    <div className="space-y-4">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-4 rounded-xl border border-slate-800 bg-slate-900/60">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Link2 className="h-4 w-4 text-cyan-400" />
            Requirement-to-Release Traceability Matrix
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Total PRD Requirements: {matrix.requirements?.length || 0}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-[10px] text-slate-400 uppercase font-mono">Traceability Score</div>
            <div className={`text-base font-black ${scorePercent === 100 ? 'text-emerald-400' : 'text-amber-400'}`}>
              {scorePercent}%
            </div>
          </div>

          {orphanCount > 0 ? (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-semibold">
              <AlertTriangle className="h-3.5 w-3.5" />
              {orphanCount} Orphaned
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              <CheckCircle2 className="h-3.5 w-3.5" />
              0 Orphaned
            </div>
          )}
        </div>
      </div>

      {/* Requirements List */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden">
        <div className="px-4 py-3 border-b border-slate-800 bg-slate-950/40 text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center justify-between">
          <span>PRD Requirement Specifications</span>
          <span className="text-[10px] font-mono text-slate-500">Live Status</span>
        </div>

        <div className="divide-y divide-slate-800/60">
          {(matrix.requirements || []).map((req) => (
            <div key={req.id} className="p-4 hover:bg-slate-800/30 transition-colors">
              <div className="flex items-start justify-between gap-3 mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold uppercase">
                      {req.category}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold uppercase">
                      {req.priority}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-white">{req.title}</h4>
                  <p className="text-xs text-slate-400 mt-1">{req.description}</p>
                </div>

                <div className="shrink-0 text-right">
                  {req.is_traceable ? (
                    <span className="inline-flex items-center gap-1 text-[10px] font-mono font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                      <CheckCircle2 className="h-3 w-3" /> Linked
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[10px] font-mono font-semibold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                      <AlertTriangle className="h-3 w-3" /> Orphan
                    </span>
                  )}
                </div>
              </div>

              {/* Acceptance Criteria */}
              {req.acceptance_criteria && req.acceptance_criteria.length > 0 && (
                <div className="mt-3 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800 text-[11px] text-slate-300">
                  <div className="text-[10px] font-mono text-slate-400 uppercase mb-1">Acceptance Criteria:</div>
                  <ul className="space-y-1">
                    {req.acceptance_criteria.map((crit, idx) => (
                      <li key={idx} className="flex items-center gap-1.5">
                        <CheckCircle2 className="h-3 w-3 text-cyan-400 shrink-0" />
                        <span>{crit}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
