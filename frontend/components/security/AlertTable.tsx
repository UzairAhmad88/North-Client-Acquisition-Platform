'use client';

import React from 'react';
import { SecurityAlertItem } from '@/lib/api/securityOps';
import { AlertTriangle, CheckCircle, Clock, ShieldCheck } from 'lucide-react';

interface AlertTableProps {
  alerts: SecurityAlertItem[];
  loading: boolean;
  onUpdateStatus: (alertId: string, status: string) => void;
  onSelectAlertForRemediation: (alert: SecurityAlertItem) => void;
}

export default function AlertTable({
  alerts,
  loading,
  onUpdateStatus,
  onSelectAlertForRemediation,
}: AlertTableProps) {
  const getSeverityBadge = (severity: string) => {
    const s = severity.toLowerCase();
    if (s === 'critical') return 'bg-rose-100 text-rose-800 border-rose-300';
    if (s === 'high') return 'bg-orange-100 text-orange-800 border-orange-300';
    if (s === 'medium') return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-slate-100 text-slate-700 border-slate-300';
  };

  const getStatusBadge = (status: string) => {
    const st = status.toUpperCase();
    if (st === 'DETECTED') return 'bg-rose-50 text-rose-700 border-rose-200';
    if (st === 'TRIAGED' || st === 'INVESTIGATING') return 'bg-amber-50 text-amber-700 border-amber-200';
    if (st === 'REMEDIATION' || st === 'CONTAINMENT') return 'bg-indigo-50 text-indigo-700 border-indigo-200';
    if (st === 'RESOLVED' || st === 'CLOSED') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    return 'bg-slate-50 text-slate-700 border-slate-200';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            Security Alert Management Lifecycle
          </h3>
          <p className="text-xs text-slate-500">
            Triage, investigate, and approve containment runbooks (Section 17)
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-full">
          {alerts.length} Alerts Active
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700">
          <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2.5 px-3">Alert Title</th>
              <th className="py-2.5 px-3">Anomaly Type</th>
              <th className="py-2.5 px-3">Affected Actor</th>
              <th className="py-2.5 px-3">Risk</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Loading alerts...
                </td>
              </tr>
            ) : alerts.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Zero active alerts. All security vectors healthy.
                </td>
              </tr>
            ) : (
              alerts.map((alt) => (
                <tr key={alt.alert_id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-3">
                    <div className="font-semibold text-slate-900">{alt.title}</div>
                    <div className="text-[11px] text-slate-500 line-clamp-1">{alt.description}</div>
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px] text-slate-600">
                    {alt.anomaly_type}
                  </td>
                  <td className="py-3 px-3 text-slate-800 font-medium">
                    {alt.affected_actor_id || 'System'}
                  </td>
                  <td className="py-3 px-3 font-bold text-slate-900">
                    {alt.risk_score}
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getSeverityBadge(alt.severity)}`}>
                      {alt.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getStatusBadge(alt.status)}`}>
                      {alt.status}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right space-x-1.5 whitespace-nowrap">
                    {alt.status === 'DETECTED' && (
                      <button
                        onClick={() => onUpdateStatus(alt.alert_id, 'TRIAGED')}
                        className="px-2.5 py-1 text-[11px] font-medium rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
                      >
                        Triage
                      </button>
                    )}
                    {alt.status !== 'CLOSED' && (
                      <button
                        onClick={() => onSelectAlertForRemediation(alt)}
                        className="px-2.5 py-1 text-[11px] font-medium rounded-md bg-indigo-600 text-white hover:bg-indigo-700 transition-colors shadow-xs"
                      >
                        Remediate
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
