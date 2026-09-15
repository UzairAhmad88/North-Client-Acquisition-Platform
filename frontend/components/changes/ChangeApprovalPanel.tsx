'use client';

import React, { useState } from 'react';
import { approveInternalChange, approveClientChange, updateBaselineVersion, implementChangeTasks, ChangeRequest } from '@/lib/api/changes';
import { FileCheck, ShieldAlert, CheckCircle2, ArrowRight, GitCommit } from 'lucide-react';

interface ChangeApprovalPanelProps {
  change: ChangeRequest;
  onRefresh?: () => void;
}

export const ChangeApprovalPanel: React.FC<ChangeApprovalPanelProps> = ({ change, onRefresh }) => {
  const [approvalStatement, setApprovalStatement] = useState('I explicitly confirm and approve this change request proposal.');
  const [submittingInternal, setSubmittingInternal] = useState(false);
  const [submittingClient, setSubmittingClient] = useState(false);
  const [updatingBaseline, setUpdatingBaseline] = useState(false);
  const [implementing, setImplementing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const activeVersion = change.versions?.[0];

  const handleInternalApprove = async () => {
    setSubmittingInternal(true);
    setError(null);
    try {
      await approveInternalChange(change.id);
      if (onRefresh) onRefresh();
    } catch (err: any) {
      setError(err?.message || 'Failed to submit internal approval.');
    } finally {
      setSubmittingInternal(false);
    }
  };

  const handleClientApprove = async () => {
    setSubmittingClient(true);
    setError(null);
    try {
      await approveClientChange(change.id, { approval_statement: approvalStatement });
      if (onRefresh) onRefresh();
    } catch (err: any) {
      setError(err?.message || 'Failed to submit client approval.');
    } finally {
      setSubmittingClient(false);
    }
  };

  const handleBaselineUpdate = async () => {
    setUpdatingBaseline(true);
    setError(null);
    try {
      await updateBaselineVersion(change.id);
      if (onRefresh) onRefresh();
    } catch (err: any) {
      setError(err?.message || 'Failed to revise contract baseline.');
    } finally {
      setUpdatingBaseline(false);
    }
  };

  const handleImplement = async () => {
    setImplementing(true);
    setError(null);
    try {
      await implementChangeTasks(change.id);
      if (onRefresh) onRefresh();
    } catch (err: any) {
      setError(err?.message || 'Failed to trigger task implementation.');
    } finally {
      setImplementing(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <FileCheck className="w-5 h-5 text-emerald-400" />
            <span>Dual Approval & Baseline Commitment Protocol</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Requires Internal Operator Approval + Client Explicit Sign-Off before baseline revision.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/40 border border-red-800/50 rounded-lg text-xs text-red-300">
          {error}
        </div>
      )}

      {/* Approval Status Pipeline */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
        <div className={`p-4 rounded-xl border space-y-1 ${change.approval_status === 'INTERNAL_APPROVED' ? 'bg-emerald-950/30 border-emerald-800/50' : 'bg-slate-950 border-slate-800'}`}>
          <span className="text-slate-400 block text-[11px]">1. Internal Review</span>
          <span className="font-bold text-slate-200">{change.approval_status}</span>
        </div>

        <div className={`p-4 rounded-xl border space-y-1 ${change.client_approval_status === 'CLIENT_APPROVED' ? 'bg-emerald-950/30 border-emerald-800/50' : 'bg-slate-950 border-slate-800'}`}>
          <span className="text-slate-400 block text-[11px]">2. Client Sign-Off</span>
          <span className="font-bold text-slate-200">{change.client_approval_status}</span>
        </div>

        <div className={`p-4 rounded-xl border space-y-1 ${change.status === 'BASELINE_UPDATE' ? 'bg-emerald-950/30 border-emerald-800/50' : 'bg-slate-950 border-slate-800'}`}>
          <span className="text-slate-400 block text-[11px]">3. Baseline Lock</span>
          <span className="font-bold text-slate-200">{change.status}</span>
        </div>

        <div className={`p-4 rounded-xl border space-y-1 ${change.implementation_status === 'IN_PROGRESS' ? 'bg-purple-950/30 border-purple-800/50' : 'bg-slate-950 border-slate-800'}`}>
          <span className="text-slate-400 block text-[11px]">4. Implementation</span>
          <span className="font-bold text-slate-200">{change.implementation_status}</span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="space-y-3 pt-2">
        {change.approval_status !== 'INTERNAL_APPROVED' && (
          <button
            onClick={handleInternalApprove}
            disabled={submittingInternal}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg flex items-center justify-center space-x-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Grant Internal Engineering & Commercial Approval</span>
          </button>
        )}

        {change.approval_status === 'INTERNAL_APPROVED' && change.client_approval_status !== 'CLIENT_APPROVED' && (
          <div className="space-y-3 bg-slate-950 p-4 rounded-xl border border-slate-800">
            <label className="text-xs font-medium text-slate-300">Client Explicit Approval Statement</label>
            <textarea
              value={approvalStatement}
              onChange={(e) => setApprovalStatement(e.target.value)}
              rows={2}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
            />
            <button
              onClick={handleClientApprove}
              disabled={submittingClient || !approvalStatement.trim()}
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg flex items-center justify-center space-x-2"
            >
              <FileCheck className="w-4 h-4" />
              <span>Record Client Cryptographic Sign-Off</span>
            </button>
          </div>
        )}

        {change.client_approval_status === 'CLIENT_APPROVED' && change.status !== 'BASELINE_UPDATE' && change.status !== 'IMPLEMENTATION' && (
          <button
            onClick={handleBaselineUpdate}
            disabled={updatingBaseline}
            className="w-full py-3 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg flex items-center justify-center space-x-2"
          >
            <GitCommit className="w-4 h-4" />
            <span>Revise Contract Baseline (Lock Baseline v2)</span>
          </button>
        )}

        {change.status === 'BASELINE_UPDATE' && (
          <button
            onClick={handleImplement}
            disabled={implementing}
            className="w-full py-3 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg flex items-center justify-center space-x-2"
          >
            <ArrowRight className="w-4 h-4" />
            <span>Generate Execution Tasks & Implement Change</span>
          </button>
        )}
      </div>
    </div>
  );
};
