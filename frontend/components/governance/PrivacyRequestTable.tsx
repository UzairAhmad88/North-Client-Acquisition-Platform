'use client';

import React from 'react';
import { PrivacyRequestItem } from '@/lib/api/governance';
import { UserCheck, ShieldAlert, CheckCircle, Clock, AlertTriangle } from 'lucide-react';

interface PrivacyRequestTableProps {
  requests: PrivacyRequestItem[];
}

export default function PrivacyRequestTable({ requests }: PrivacyRequestTableProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
      case 'FULFILLED':
        return (
          <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full font-bold">
            <CheckCircle className="w-3 h-3" /> {status}
          </span>
        );
      case 'REJECTED_LEGAL_HOLD':
        return (
          <span className="inline-flex items-center gap-1 text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full font-bold">
            <ShieldAlert className="w-3 h-3" /> Legal Hold
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full font-bold">
            <Clock className="w-3 h-3" /> {status}
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-indigo-600" />
            <span>Data Subject Access & Privacy Requests (DSAR)</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            GDPR / CCPA request state machine with legal-hold boundary protections.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {requests.length} Privacy Requests
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Request Code</th>
              <th className="p-3.5">Subject ID</th>
              <th className="p-3.5">Request Type</th>
              <th className="p-3.5">Requested At</th>
              <th className="p-3.5">Due Date</th>
              <th className="p-3.5">Assigned To</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {requests.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-6 text-center text-slate-400">
                  No active data subject requests pending.
                </td>
              </tr>
            ) : (
              requests.map((r) => (
                <tr key={r.request_code} className="hover:bg-slate-50/70 transition-colors">
                  <td className="p-3.5 font-mono font-bold text-slate-900">{r.request_code}</td>
                  <td className="p-3.5 font-medium text-slate-800">{r.subject_id}</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 font-semibold">
                      {r.request_type}
                    </span>
                  </td>
                  <td className="p-3.5 text-slate-500">{new Date(r.requested_at).toLocaleDateString()}</td>
                  <td className="p-3.5 font-mono text-slate-700">{new Date(r.due_date).toLocaleDateString()}</td>
                  <td className="p-3.5 text-slate-600">{r.assigned_to}</td>
                  <td className="p-3.5">{getStatusBadge(r.status)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
