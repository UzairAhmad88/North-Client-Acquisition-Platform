'use client';

import React from 'react';
import { ConformanceViolation } from '@/lib/api/processIntelligence';
import { AlertOctagon, CheckCircle2, ShieldAlert } from 'lucide-react';

interface Props {
  violations: ConformanceViolation[];
}

export default function ConformancePanel({ violations }: Props) {
  if (violations.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">Full Process Conformance</p>
        <p className="text-sm text-slate-500 mt-1">Observed executions strictly match designed policy rules and approval gates.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400" /> Conformance Violations & Deviations
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {violations.length} governance violations detected in active case executions
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
            <tr>
              <th className="px-4 py-3">Violation Code</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Activity</th>
              <th className="px-4 py-3">Severity</th>
              <th className="px-4 py-3">Description</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {violations.map((v) => (
              <tr key={v.violation_code} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-mono font-medium text-red-400">{v.violation_code}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 text-xs rounded bg-red-500/20 text-red-300 font-mono">
                    {v.violation_type}
                  </span>
                </td>
                <td className="px-4 py-3 font-medium text-white">{v.activity_involved}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 text-xs rounded font-semibold ${
                    v.severity === 'CRITICAL' ? 'bg-red-500/30 text-red-200' : 'bg-amber-500/20 text-amber-300'
                  }`}>
                    {v.severity}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate-300">{v.description}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 text-xs rounded bg-slate-800 text-slate-300">
                    {v.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
