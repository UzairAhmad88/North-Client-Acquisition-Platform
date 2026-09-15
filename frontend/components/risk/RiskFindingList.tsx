import React from 'react';
import { RiskFinding } from '@/lib/api/risk';

interface RiskFindingListProps {
  findings: RiskFinding[];
}

export function RiskFindingList({ findings }: RiskFindingListProps) {
  if (!findings || findings.length === 0) {
    return (
      <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
        ✓ No risk findings or policy violations detected. Content is clean.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <h4 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Evaluation Findings ({findings.length})</h4>
      {findings.map((f) => {
        let border = 'border-amber-500/30 bg-amber-500/5 text-amber-300';
        if (f.severity === 'CRITICAL' || f.severity === 'HIGH') {
          border = 'border-rose-500/30 bg-rose-500/5 text-rose-300';
        } else if (f.severity === 'LOW' || f.severity === 'INFO') {
          border = 'border-blue-500/30 bg-blue-500/5 text-blue-300';
        }

        return (
          <div key={f.id || f.rule_id} className={`p-3 rounded-lg border text-xs space-y-1 ${border}`}>
            <div className="flex justify-between items-center font-bold">
              <span>[{f.category}] {f.rule_id}</span>
              <span className="uppercase text-[10px] px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-700">{f.severity}</span>
            </div>
            <p className="text-zinc-200">{f.message}</p>
            {f.evidence_reference && (
              <p className="text-[11px] text-zinc-400 italic">Ref: {f.evidence_reference}</p>
            )}
            {f.remediation && (
              <div className="mt-1 p-1.5 rounded bg-zinc-900/80 border border-zinc-800 text-[11px] text-zinc-300">
                <span className="font-semibold text-indigo-400">Remediation:</span> {f.remediation}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
