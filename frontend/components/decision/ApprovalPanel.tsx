"use client";

import React, { useState } from "react";
import { DecisionApproval } from "@/lib/api/decision_rooms";
import { ShieldCheck, CheckCircle2, Clock, XCircle, UserCheck } from "lucide-react";

interface Props {
  approvals: DecisionApproval[];
  onApprove?: (stepId: string, status: string, notes?: string) => Promise<void>;
}

export const ApprovalPanel: React.FC<Props> = ({ approvals, onApprove }) => {
  const [actingStepId, setActingStepId] = useState<string | null>(null);

  const handleAction = async (stepId: string, status: string) => {
    if (!onApprove) return;
    setActingStepId(stepId);
    try {
      await onApprove(stepId, status);
    } finally {
      setActingStepId(null);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Separation of Duties & Approval Governance
          </h3>
          <p className="text-xs text-slate-400">
            Authoritative multi-role sign-off. High-impact decisions require independent risk, security, and executive approval.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {approvals.map((appr) => (
          <div key={appr.id} className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-white">{appr.step_name.replace(/_/g, " ")}</span>
                <span className="text-xs px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono">
                  Role: {appr.required_role}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {appr.status === "APPROVED" ? (
                  <span className="text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Approved by {appr.approver_id || "Executive"}
                  </span>
                ) : (
                  <span className="text-amber-400 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" /> Pending human review
                  </span>
                )}
              </p>
            </div>

            <div className="flex items-center gap-2">
              {appr.status === "PENDING" && onApprove && (
                <>
                  <button
                    disabled={actingStepId === appr.id}
                    onClick={() => handleAction(appr.id, "APPROVED")}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold flex items-center gap-1 transition disabled:opacity-50"
                  >
                    <UserCheck className="w-3.5 h-3.5" /> Approve Step
                  </button>
                  <button
                    disabled={actingStepId === appr.id}
                    onClick={() => handleAction(appr.id, "REJECTED")}
                    className="px-3 py-1.5 bg-rose-900/60 hover:bg-rose-800 text-rose-200 rounded text-xs font-semibold flex items-center gap-1 transition disabled:opacity-50"
                  >
                    <XCircle className="w-3.5 h-3.5" /> Reject
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
