'use client';

import React from 'react';
import { GovernanceFindingItem } from '@/lib/api/governance';
import { AlertOctagon, Wrench, CheckCircle2, Clock } from 'lucide-react';

interface FindingTableProps {
  findings: GovernanceFindingItem[];
  onOpenRemediation: (findingCode: string) => void;
}

export default function FindingTable({ findings, onOpenRemediation }: FindingTableProps) {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-bold">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 rounded bg-orange-100 text-orange-800 font-bold">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold">MEDIUM</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-bold">LOW</span>;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'VERIFIED':
      case 'CLOSED':
        return (
          <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full font-bold">
            <CheckCircle2 className="w-3 h-3" /> {status}
          </span>
        );
      case 'READY_FOR_VERIFICATION':
        return (
          <span className="inline-flex items-center gap-1 text-indigo-700 bg-indigo-50 px-2.5 py-0.5 rounded-full font-bold">
            <Clock className="w-3 h-3" /> Needs Verification
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded-full font-bold">
            <AlertOctagon className="w-3 h-3" /> {status}
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <AlertOctagon className="w-5 h-5 text-indigo-600" />
            <span>Deficiencies & Audit Findings</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Deficiencies must be remediated and verified through retest before closure (Rule 20).
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {findings.length} Findings Total
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Code</th>
              <th className="p-3.5">Title & Root Cause</th>
              <th className="p-3.5">Control Code</th>
              <th className="p-3.5">Severity</th>
              <th className="p-3.5">Due Date</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {findings.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-6 text-center text-slate-400">
                  Zero open findings recorded. All controls verified effective.
                </td>
              </tr>
            ) : (
              findings.map((f) => {
                const isClosed = f.status === 'CLOSED' || f.status === 'VERIFIED';

                return (
                  <tr key={f.finding_code} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-3.5 font-mono font-bold text-slate-900">{f.finding_code}</td>
                    <td className="p-3.5 max-w-sm">
                      <div className="font-semibold text-slate-900">{f.title}</div>
                      <div className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{f.description}</div>
                      {f.root_cause && (
                        <div className="text-[10px] text-slate-400 mt-0.5">Root cause: {f.root_cause}</div>
                      )}
                    </td>
                    <td className="p-3.5 font-mono text-indigo-700 font-medium">{f.control_code}</td>
                    <td className="p-3.5">{getSeverityBadge(f.severity)}</td>
                    <td className="p-3.5 font-mono text-slate-600">{new Date(f.due_date).toLocaleDateString()}</td>
                    <td className="p-3.5">{getStatusBadge(f.status)}</td>
                    <td className="p-3.5">
                      {!isClosed && (
                        <button
                          onClick={() => onOpenRemediation(f.finding_code)}
                          className="inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold rounded-lg transition-all"
                        >
                          <Wrench className="w-3 h-3" />
                          <span>Remediate</span>
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
