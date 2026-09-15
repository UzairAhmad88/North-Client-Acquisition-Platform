'use client';

import React from 'react';
import { GovernanceExceptionItem } from '@/lib/api/governance';
import { Clock, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';

interface ExceptionTableProps {
  exceptions: GovernanceExceptionItem[];
  onApproveException: (exceptionCode: string) => void;
}

export default function ExceptionTable({ exceptions, onApproveException }: ExceptionTableProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'APPROVED':
        return <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-bold">APPROVED</span>;
      case 'REQUESTED':
        return <span className="px-2 py-0.5 rounded bg-amber-50 text-amber-700 font-bold">REQUESTED</span>;
      case 'EXPIRED':
        return <span className="px-2 py-0.5 rounded bg-rose-50 text-rose-700 font-bold">EXPIRED</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-bold">{status}</span>;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-600" />
            <span>Time-Bound Exceptions Registry</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Mandatory expiration dates & compensating controls. No permanent silent exceptions.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {exceptions.length} Exceptions Logged
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Code</th>
              <th className="p-3.5">Title & Control</th>
              <th className="p-3.5">Compensating Controls</th>
              <th className="p-3.5">Requester / Approver</th>
              <th className="p-3.5">Expiration Date</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {exceptions.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-6 text-center text-slate-400">
                  No active exceptions recorded.
                </td>
              </tr>
            ) : (
              exceptions.map((exc) => {
                const isRequested = exc.status === 'REQUESTED';

                return (
                  <tr key={exc.exception_code} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-3.5 font-mono font-bold text-slate-900">{exc.exception_code}</td>
                    <td className="p-3.5 max-w-xs">
                      <div className="font-semibold text-slate-900">{exc.title}</div>
                      <div className="text-[11px] font-mono text-indigo-600">{exc.control_code}</div>
                      <div className="text-[11px] text-slate-500 mt-0.5">{exc.reason}</div>
                    </td>
                    <td className="p-3.5 max-w-xs">
                      <div className="flex flex-wrap gap-1">
                        {exc.compensating_controls.map((comp, idx) => (
                          <span
                            key={idx}
                            className="px-1.5 py-0.5 bg-amber-50 text-amber-800 font-medium text-[10px] rounded border border-amber-200"
                          >
                            {comp}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="p-3.5">
                      <div className="text-slate-800 font-medium">Req: {exc.requester_id}</div>
                      <div className="text-[11px] text-slate-500">App: {exc.approver_id || 'Pending'}</div>
                    </td>
                    <td className="p-3.5 font-mono font-semibold text-slate-700">
                      {new Date(exc.expiration_date).toLocaleDateString()}
                    </td>
                    <td className="p-3.5">{getStatusBadge(exc.status)}</td>
                    <td className="p-3.5">
                      {isRequested && (
                        <button
                          onClick={() => onApproveException(exc.exception_code)}
                          className="px-2.5 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold rounded-lg transition-all"
                        >
                          Approve
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
