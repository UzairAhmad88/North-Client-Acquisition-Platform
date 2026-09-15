'use client';

import React, { useState } from 'react';
import { SecurityAlertItem, securityOpsApi } from '@/lib/api/securityOps';
import { ShieldCheck, Lock, AlertTriangle, CheckCircle, X } from 'lucide-react';

interface RemediationPanelProps {
  alert: SecurityAlertItem | null;
  onClose: () => void;
  onSuccess: () => void;
}

export default function RemediationPanel({ alert, onClose, onSuccess }: RemediationPanelProps) {
  const [actionName, setActionName] = useState('revoke_session');
  const [requestedBy, setRequestedBy] = useState('operator_analyst');
  const [approvedBy, setApprovedBy] = useState('lead_ciso');
  const [submitting, setSubmitting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!alert) return null;

  const playbooks = [
    { value: 'revoke_session', label: 'Revoke User / Principal Sessions' },
    { value: 'require_mfa', label: 'Force Immediate Step-Up MFA Challenge' },
    { value: 'disable_api_key', label: 'Disable Compromised API Key' },
    { value: 'quarantine_agent', label: 'Quarantine Autonomous AI Agent' },
    { value: 'disable_workflow', label: 'Suspend Active Workflow' },
    { value: 'block_integration', label: 'Block Third-Party Integration Provider' },
    { value: 'enable_maintenance_mode', label: 'Engage Tenant Maintenance Mode' },
  ];

  const handleExecute = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg(null);
    setExecutionResult(null);

    try {
      const res = await securityOpsApi.executeRemediation({
        alert_id: alert.alert_id,
        action_name: actionName,
        requested_by: requestedBy,
        approved_by: approvedBy,
        parameters: { actor_id: alert.affected_actor_id, target_id: alert.affected_target_id },
      });

      if (res.details?.error) {
        setErrorMsg(res.details.error);
      } else {
        setExecutionResult(res);
        onSuccess();
      }
    } catch (err: any) {
      setErrorMsg(err?.message || 'Remediation action failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg w-full p-6 space-y-5">
        <div className="flex justify-between items-start border-b border-slate-100 pb-3">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200">
              {alert.severity} Alert
            </span>
            <h3 className="text-base font-bold text-slate-900 mt-1.5">{alert.title}</h3>
            <p className="text-xs text-slate-500">{alert.description}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 p-1">
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMsg && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {executionResult ? (
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 space-y-2">
            <div className="flex items-center gap-2 font-bold text-xs">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              Remediation Action Successfully Executed
            </div>
            <pre className="text-[11px] font-mono bg-white/70 p-2.5 rounded-lg border border-emerald-100 overflow-x-auto">
              {JSON.stringify(executionResult.details || executionResult, null, 2)}
            </pre>
            <div className="text-right pt-2">
              <button
                onClick={onClose}
                className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700"
              >
                Done
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleExecute} className="space-y-4 text-xs">
            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Select Remediation Playbook</label>
              <select
                value={actionName}
                onChange={(e) => setActionName(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {playbooks.map((pb) => (
                  <option key={pb.value} value={pb.value}>
                    {pb.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Separation of Duties (Section 46) */}
            <div className="grid grid-cols-2 gap-3 pt-1">
              <div className="space-y-1">
                <label className="font-semibold text-slate-700">Requester ID</label>
                <input
                  type="text"
                  value={requestedBy}
                  onChange={(e) => setRequestedBy(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg border border-slate-200 font-mono text-[11px]"
                />
              </div>
              <div className="space-y-1">
                <label className="font-semibold text-slate-700">Approver ID (Dual Gate)</label>
                <input
                  type="text"
                  value={approvedBy}
                  onChange={(e) => setApprovedBy(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg border border-slate-200 font-mono text-[11px]"
                />
              </div>
            </div>

            <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-900 text-[11px] flex items-start gap-2">
              <Lock className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                Separation of Duties enforced (Section 46): Requester and Approver must be distinct identities. High-impact operations verify idempotency before state mutation.
              </span>
            </div>

            <div className="flex justify-end gap-2.5 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 shadow-xs disabled:opacity-50"
              >
                {submitting ? 'Verifying & Executing...' : 'Approve & Execute Playbook'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
