'use client';

import React, { useState } from 'react';
import { approveDeliverable, DeliverableApproval } from '@/lib/api/client_portal';
import { FileCheck, ShieldAlert, CheckCircle2, AlertTriangle, History, ArrowRight } from 'lucide-react';

interface DeliverableVersion {
  version_number: number;
  title: string;
  description: string;
  content_payload: string;
  created_at: string;
  status: 'PENDING_REVIEW' | 'APPROVED' | 'REJECTED';
}

interface DeliverableReviewPanelProps {
  deliverableId: string;
  deliverableTitle: string;
  currentVersion: DeliverableVersion;
  versionHistory?: DeliverableVersion[];
  onApprovalComplete?: (approval: DeliverableApproval) => void;
}

export const DeliverableReviewPanel: React.FC<DeliverableReviewPanelProps> = ({
  deliverableId,
  deliverableTitle,
  currentVersion,
  versionHistory = [],
  onApprovalComplete,
}) => {
  const [approvalStatement, setApprovalStatement] = useState(
    'I explicitly confirm and approve this deliverable version for baseline sign-off.'
  );
  const [submitting, setSubmitting] = useState(false);
  const [approvalResult, setApprovalResult] = useState<DeliverableApproval | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const handleApprove = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const res = await approveDeliverable(deliverableId, {
        version_number: currentVersion.version_number,
        approval_statement: approvalStatement,
        content_payload: currentVersion.content_payload,
      });
      setApprovalResult(res);
      setShowConfirmModal(false);
      if (onApprovalComplete) {
        onApprovalComplete(res);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to submit deliverable approval.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-xl font-bold text-white">{deliverableTitle}</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
              v{currentVersion.version_number}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">{currentVersion.description}</p>
        </div>
        <div>
          {approvalResult || currentVersion.status === 'APPROVED' ? (
            <span className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-4 h-4" />
              <span>Approved & Sealed</span>
            </span>
          ) : (
            <span className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <AlertTriangle className="w-4 h-4" />
              <span>Pending Sign-Off</span>
            </span>
          )}
        </div>
      </div>

      {/* Non-Approval Notice (Legal Safeguard) */}
      <div className="bg-amber-950/30 border border-amber-800/40 rounded-lg p-4 flex items-start space-x-3 text-amber-200 text-xs">
        <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div>
          <strong className="font-semibold text-amber-300">Important Policy Notice:</strong> Viewing or opening a deliverable does <em>NOT</em> constitute approval or baseline commitment. Formal client approval requires explicit submission below with cryptographic SHA-256 integrity verification.
        </div>
      </div>

      {/* Deliverable Content View */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-slate-300">Deliverable Payload / Specifications</h3>
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs text-slate-300 max-h-60 overflow-y-auto whitespace-pre-wrap">
          {currentVersion.content_payload}
        </div>
      </div>

      {/* Version History */}
      {versionHistory.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-slate-300 flex items-center space-x-2">
            <History className="w-4 h-4 text-slate-400" />
            <span>Version History</span>
          </h3>
          <div className="divide-y divide-slate-800 border border-slate-800 rounded-lg bg-slate-950/50">
            {versionHistory.map((ver) => (
              <div key={ver.version_number} className="p-3 flex items-center justify-between text-xs">
                <div>
                  <span className="font-semibold text-white">Version {ver.version_number}</span>
                  <span className="text-slate-400 ml-2">— {ver.description}</span>
                </div>
                <span className="text-slate-500">{new Date(ver.created_at).toLocaleDateString()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Approval Form / Status */}
      {approvalResult ? (
        <div className="bg-emerald-950/30 border border-emerald-800/50 rounded-xl p-5 space-y-3">
          <div className="flex items-center space-x-2 text-emerald-400 font-semibold text-sm">
            <CheckCircle2 className="w-5 h-5" />
            <span>Cryptographic Deliverable Sign-Off Recorded</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-300">
            <div>
              <span className="text-slate-400">Approval ID:</span> <code className="text-emerald-300">{approvalResult.id}</code>
            </div>
            <div>
              <span className="text-slate-400">Approved Version:</span> v{approvalResult.version_number}
            </div>
            <div className="md:col-span-2">
              <span className="text-slate-400">SHA-256 Hash:</span> <code className="text-xs break-all text-slate-300 bg-slate-900 px-2 py-1 rounded border border-slate-800">{approvalResult.content_hash}</code>
            </div>
            <div>
              <span className="text-slate-400">Signer:</span> {approvalResult.signer_name} ({approvalResult.signer_email})
            </div>
            <div>
              <span className="text-slate-400">Timestamp:</span> {new Date(approvalResult.approved_at).toLocaleString()}
            </div>
          </div>
        </div>
      ) : (
        <div className="pt-2">
          <button
            onClick={() => setShowConfirmModal(true)}
            className="w-full py-3 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm shadow-lg hover:shadow-emerald-600/20 transition duration-200 flex items-center justify-center space-x-2"
          >
            <FileCheck className="w-4 h-4" />
            <span>Formally Approve Deliverable v{currentVersion.version_number}</span>
          </button>
        </div>
      )}

      {/* Modal for Explicit Approval */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 space-y-5 shadow-2xl">
            <div className="flex items-center space-x-3 text-slate-100">
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
                <FileCheck className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-white">Confirm Deliverable Sign-Off</h3>
                <p className="text-xs text-slate-400">Version {currentVersion.version_number} — {deliverableTitle}</p>
              </div>
            </div>

            {error && (
              <div className="p-3 bg-red-950/40 border border-red-800/50 rounded-lg text-xs text-red-300">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <label className="text-xs font-medium text-slate-300">Approval Statement & Commitment</label>
              <textarea
                value={approvalStatement}
                onChange={(e) => setApprovalStatement(e.target.value)}
                rows={3}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-[11px] text-slate-400 space-y-1">
              <p className="font-semibold text-slate-300">Client Sign-off Verification:</p>
              <p>• A SHA-256 fingerprint will be generated for version {currentVersion.version_number}.</p>
              <p>• This action creates an auditable record in the baseline database.</p>
            </div>

            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowConfirmModal(false)}
                disabled={submitting}
                className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300"
              >
                Cancel
              </button>
              <button
                onClick={handleApprove}
                disabled={submitting || !approvalStatement.trim()}
                className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-xs font-semibold text-white flex items-center space-x-1.5"
              >
                {submitting ? (
                  <span>Hashing & Recording...</span>
                ) : (
                  <>
                    <span>Submit Binding Approval</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
