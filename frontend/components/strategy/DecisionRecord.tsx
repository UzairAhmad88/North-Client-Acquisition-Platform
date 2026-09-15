'use client';

import React, { useState } from 'react';
import { UserCheck, Shield, CheckCircle2, XCircle, Clock, FileText, AlertOctagon, Sparkles } from 'lucide-react';
import { StrategicDecisionRecord } from '../../lib/api/strategy';

interface DecisionRecordProps {
  decisions: StrategicDecisionRecord[];
  pendingOptions?: Array<{
    option_id: string;
    question: string;
    description: string;
    trade_off_summary: string;
    required_approval_role: string;
    plan_id: string;
  }>;
  onApproveDecision?: (optionId: string, rationale: string) => Promise<void>;
  onRejectDecision?: (optionId: string, reason: string) => Promise<void>;
}

export const DecisionRecord: React.FC<DecisionRecordProps> = ({
  decisions,
  pendingOptions = [],
  onApproveDecision,
  onRejectDecision,
}) => {
  const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null);
  const [rationale, setRationale] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleApprove = async (optionId: string) => {
    if (!onApproveDecision) return;
    try {
      setIsSubmitting(true);
      await onApproveDecision(optionId, rationale);
      setSelectedOptionId(null);
      setRationale('');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReject = async (optionId: string) => {
    if (!onRejectDecision) return;
    try {
      setIsSubmitting(true);
      await onRejectDecision(optionId, rationale);
      setSelectedOptionId(null);
      setRationale('');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-indigo-500/20 bg-gradient-to-r from-slate-900/80 via-slate-900/60 to-indigo-950/40">
        <div>
          <div className="flex items-center gap-2">
            <UserCheck className="h-5 w-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white tracking-tight">Strategic Decision Ledger & Human Governance</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Strict human-in-the-loop audit trail. Strategic recommendations produced by AI models require explicit executive ratification before plan activation or resource commitments.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold flex items-center gap-1.5">
            <Shield className="h-3.5 w-3.5" />
            Human-in-the-Loop Active
          </span>
        </div>
      </div>

      {/* Pending Strategic Actions / Review Queue */}
      {pendingOptions && pendingOptions.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm font-semibold text-amber-300">
            <AlertOctagon className="h-4 w-4" />
            <span>Pending Strategic Decisions Awaiting Ratification ({pendingOptions.length})</span>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {pendingOptions.map((opt) => (
              <div
                key={opt.option_id}
                className="rounded-xl border border-amber-500/30 bg-amber-950/10 p-5 space-y-4"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
                      Required Role: {opt.required_approval_role}
                    </span>
                    <h3 className="text-base font-bold text-white mt-1.5">{opt.question}</h3>
                  </div>
                  <div className="text-xs text-slate-400">Plan Ref: {opt.plan_id.slice(0, 8)}</div>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">{opt.description}</p>

                <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300">
                  <span className="font-semibold text-indigo-300">Trade-off & Consequence: </span>
                  {opt.trade_off_summary}
                </div>

                {/* Ratification Box */}
                <div className="pt-2 border-t border-slate-800/80 space-y-3">
                  <textarea
                    value={selectedOptionId === opt.option_id ? rationale : ''}
                    onChange={(e) => {
                      setSelectedOptionId(opt.option_id);
                      setRationale(e.target.value);
                    }}
                    placeholder="Enter strategic rationale / approval conditions for audit memory..."
                    className="w-full h-16 rounded-lg bg-slate-950/80 border border-slate-700/80 p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />

                  <div className="flex items-center justify-end gap-3">
                    <button
                      disabled={isSubmitting}
                      onClick={() => handleReject(opt.option_id)}
                      className="px-4 py-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                    >
                      <XCircle className="h-3.5 w-3.5" />
                      Reject Recommendation
                    </button>
                    <button
                      disabled={isSubmitting}
                      onClick={() => handleApprove(opt.option_id)}
                      className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-emerald-600/20 cursor-pointer disabled:opacity-50"
                    >
                      <CheckCircle2 className="h-3.5 w-3.5" />
                      Ratify & Activate Plan
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Historical Decision Ledger */}
      <div className="rounded-xl border border-slate-700/60 bg-slate-900/60 p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4 text-slate-400" />
            <h3 className="text-sm font-bold text-white">Immutable Decision History (Phase 48 Linked)</h3>
          </div>
          <span className="text-xs text-slate-400">{decisions.length} Decisions Logged</span>
        </div>

        {decisions.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            No historical strategic decisions recorded yet.
          </div>
        ) : (
          <div className="space-y-3">
            {decisions.map((dec, idx) => (
              <div
                key={dec.id || dec.decision_id || idx}
                className="p-4 rounded-lg bg-slate-950/60 border border-slate-800/80 space-y-2"
              >
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        dec.status === 'APPROVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                      }`}
                    >
                      {dec.status || 'RECORDED'}
                    </span>
                    <span className="font-semibold text-white">{dec.question || dec.title}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-400">
                    <Clock className="h-3 w-3" />
                    <span>{dec.created_at ? new Date(dec.created_at).toLocaleDateString() : (dec.date || 'Recent')}</span>
                  </div>
                </div>

                <div className="text-xs text-slate-300">
                  <span className="text-slate-500">Selected Option: </span>
                  <span className="font-medium text-indigo-300">
                    {typeof dec.selected_option === 'string' ? dec.selected_option : (dec.decision || JSON.stringify(dec.selected_option || ''))}
                  </span>
                </div>

                <div className="text-xs text-slate-400 italic bg-slate-900/40 p-2 rounded border border-slate-800/40">
                  &ldquo;{dec.rationale}&rdquo;
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                  <span>Sign-off: {dec.decided_by || dec.author}</span>
                  <span>Impact: {dec.impact_rating || 'HIGH'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
