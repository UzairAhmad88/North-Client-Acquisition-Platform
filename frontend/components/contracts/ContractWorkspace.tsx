'use client';

import React, { useState } from 'react';
import { ContractDetail } from '@/lib/api/contracts';

interface ContractWorkspaceProps {
  contractDetail: ContractDetail;
  onGenerate?: () => void;
  onApprove?: () => void;
  onAccept?: (email: string, statement: string) => void;
  onSign?: () => void;
  onLockBaseline?: () => void;
  isGenerating?: boolean;
}

export function ContractWorkspace({
  contractDetail,
  onGenerate,
  onApprove,
  onAccept,
  onSign,
  onLockBaseline,
  isGenerating,
}: ContractWorkspaceProps) {
  const [showAcceptModal, setShowAcceptModal] = useState(false);
  const [clientEmail, setClientEmail] = useState('');
  const [acceptanceStatement, setAcceptanceStatement] = useState(
    'I have reviewed this contract draft and explicitly approve all contained terms and deliverables.'
  );

  const isApproved = contractDetail.status === 'READY_FOR_CLIENT' || contractDetail.status === 'CLIENT_APPROVED' || contractDetail.status === 'SIGNED' || contractDetail.status === 'ACTIVE';
  const isClientAccepted = contractDetail.status === 'CLIENT_APPROVED' || contractDetail.status === 'SIGNED' || contractDetail.status === 'ACTIVE';
  const isSigned = contractDetail.status === 'SIGNED' || contractDetail.status === 'ACTIVE';
  const isLocked = contractDetail.status === 'ACTIVE';

  const handleAcceptSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!clientEmail || !acceptanceStatement) return;
    if (onAccept) {
      onAccept(clientEmail, acceptanceStatement);
    }
    setShowAcceptModal(false);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100">{contractDetail.title}</h2>
            <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-300 border border-indigo-500/30">
              v{contractDetail.version}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                isLocked
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {contractDetail.status}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Contract #: {contractDetail.contract_number} | ID: {contractDetail.id}
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          {onGenerate && (
            <button
              onClick={onGenerate}
              disabled={isGenerating}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 disabled:opacity-50 transition-all"
            >
              {isGenerating ? 'Generating Contract...' : 'Generate Contract Sections'}
            </button>
          )}

          {!isApproved && onApprove && (
            <button
              onClick={onApprove}
              className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-emerald-500 transition-all"
            >
              Internal Operator Approval
            </button>
          )}

          {isApproved && !isClientAccepted && onAccept && (
            <button
              onClick={() => setShowAcceptModal(true)}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 transition-all"
            >
              Record Client Explicit Acceptance
            </button>
          )}

          {isClientAccepted && !isSigned && onSign && (
            <button
              onClick={onSign}
              className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-purple-500 transition-all"
            >
              Execute Signature (Mock)
            </button>
          )}

          {isSigned && !isLocked && onLockBaseline && (
            <button
              onClick={onLockBaseline}
              className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-emerald-500 transition-all"
            >
              Lock Committed Project Baseline
            </button>
          )}
        </div>
      </div>

      {/* Discrepancy Warnings Panel if any */}
      {contractDetail.discrepancies?.length > 0 && (
        <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-xs text-rose-300">
          <h4 className="font-bold uppercase tracking-wider mb-2">Detected Discrepancies ({contractDetail.discrepancies.length})</h4>
          <ul className="space-y-1 list-disc list-inside">
            {contractDetail.discrepancies.map((d) => (
              <li key={d.id}>
                <strong>[{d.discrepancy_type}]</strong>: {d.description}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Contract Sections View */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
          Contract Clauses & Terms ({contractDetail.sections?.length || 0})
        </h3>
        <div className="space-y-4">
          {contractDetail.sections?.map((sec) => (
            <div key={sec.id} className="rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <h4 className="text-sm font-semibold text-slate-100">{sec.title}</h4>
              <p className="mt-2 text-xs text-slate-300 whitespace-pre-wrap leading-relaxed">
                {sec.content}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Client Explicit Acceptance Modal */}
      {showAcceptModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-xl border border-slate-800 bg-slate-900 p-6 space-y-4">
            <h3 className="text-lg font-bold text-slate-100">Record Explicit Client Acceptance</h3>
            <p className="text-xs text-slate-400">
              Client acceptance requires explicit verification statement. Viewing or opening does not constitute acceptance.
            </p>

            <form onSubmit={handleAcceptSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-300">Client Email Address</label>
                <input
                  type="email"
                  required
                  value={clientEmail}
                  onChange={(e) => setClientEmail(e.target.value)}
                  placeholder="client@business.com"
                  className="mt-1 w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300">Explicit Acceptance Statement</label>
                <textarea
                  required
                  rows={3}
                  value={acceptanceStatement}
                  onChange={(e) => setAcceptanceStatement(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAcceptModal(false)}
                  className="rounded-lg bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500"
                >
                  Confirm Explicit Acceptance
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
