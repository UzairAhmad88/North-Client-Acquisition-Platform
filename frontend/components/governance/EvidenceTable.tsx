'use client';

import React from 'react';
import { GovernanceEvidenceItem } from '@/lib/api/governance';
import { Database, CheckCircle, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';

interface EvidenceTableProps {
  evidence: GovernanceEvidenceItem[];
}

export default function EvidenceTable({ evidence }: EvidenceTableProps) {
  const getFreshnessBadge = (freshness: string) => {
    switch (freshness) {
      case 'FRESH':
        return (
          <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full font-bold">
            <CheckCircle className="w-3 h-3" /> Fresh
          </span>
        );
      case 'AGING':
        return (
          <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full font-bold">
            <Clock className="w-3 h-3" /> Aging
          </span>
        );
      case 'STALE':
        return (
          <span className="inline-flex items-center gap-1 text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full font-bold">
            <AlertTriangle className="w-3 h-3" /> Stale
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full font-bold">
            Missing
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-600" />
            <span>Cryptographic Evidence Ledger</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Immutable SHA-256 evidence records linked directly to operational source records.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
            {evidence.length} Evidence Records
          </span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Evidence ID</th>
              <th className="p-3.5">Type & Subsystem</th>
              <th className="p-3.5">Summary</th>
              <th className="p-3.5">SHA-256 Hash</th>
              <th className="p-3.5">Freshness</th>
              <th className="p-3.5">Collected</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {evidence.length === 0 ? (
              <tr>
                <td colSpan={6} className="p-6 text-center text-slate-400">
                  No evidence records collected yet. Run automated collectors or continuous monitoring.
                </td>
              </tr>
            ) : (
              evidence.map((ev) => (
                <tr key={ev.evidence_id} className="hover:bg-slate-50/70 transition-colors">
                  <td className="p-3.5 font-mono font-bold text-slate-900">{ev.evidence_id}</td>
                  <td className="p-3.5">
                    <div className="font-semibold text-slate-900">{ev.evidence_type}</div>
                    <div className="text-[11px] text-slate-500">{ev.source_subsystem}</div>
                  </td>
                  <td className="p-3.5 max-w-sm text-slate-800">{ev.summary}</td>
                  <td className="p-3.5 font-mono text-[11px] text-slate-500 max-w-xs truncate" title={ev.sha256_hash}>
                    {ev.sha256_hash}
                  </td>
                  <td className="p-3.5">{getFreshnessBadge(ev.freshness_status)}</td>
                  <td className="p-3.5 text-slate-500">{new Date(ev.collected_at).toLocaleDateString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
