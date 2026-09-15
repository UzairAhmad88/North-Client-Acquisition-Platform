'use client';

import React from 'react';
import { GovernanceRequirementItem } from '@/lib/api/governance';
import { FileText, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface RequirementTableProps {
  frameworkCode: string;
  requirements: GovernanceRequirementItem[];
  loading: boolean;
}

export default function RequirementTable({ frameworkCode, requirements, loading }: RequirementTableProps) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-600" />
            <span>Requirements: {frameworkCode}</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Traceable regulatory requirements mapped to technical controls.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-lg">
          {requirements.length} Requirements Mapped
        </span>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-xs">Loading requirements...</div>
      ) : requirements.length === 0 ? (
        <div className="p-8 text-center text-slate-400 text-xs">No requirements found for framework.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
                <th className="p-3.5">Code</th>
                <th className="p-3.5">Title & Description</th>
                <th className="p-3.5">Category</th>
                <th className="p-3.5">Priority</th>
                <th className="p-3.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {requirements.map((req) => {
                const isImpl = req.status === 'IMPLEMENTED';
                const isHigh = req.priority === 'HIGH';

                return (
                  <tr key={req.requirement_code} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-3.5 font-mono font-bold text-indigo-700">{req.requirement_code}</td>
                    <td className="p-3.5 max-w-md">
                      <div className="font-semibold text-slate-900">{req.title}</div>
                      <div className="text-[11px] text-slate-500 mt-0.5">{req.description}</div>
                    </td>
                    <td className="p-3.5 font-medium">{req.category}</td>
                    <td className="p-3.5">
                      <span
                        className={`px-2 py-0.5 rounded font-semibold text-[10px] ${
                          isHigh ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-600'
                        }`}
                      >
                        {req.priority}
                      </span>
                    </td>
                    <td className="p-3.5">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-semibold ${
                          isImpl
                            ? 'bg-emerald-50 text-emerald-700'
                            : 'bg-amber-50 text-amber-700'
                        }`}
                      >
                        {isImpl ? <CheckCircle className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                        {req.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
