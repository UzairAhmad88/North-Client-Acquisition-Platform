'use client';

import React, { useState } from 'react';
import { DecisionSupportRecord, predictiveApi } from '@/lib/api/predictive';

interface DecisionCenterProps {
  records: DecisionSupportRecord[];
  onRefresh: () => void;
}

export const DecisionCenter: React.FC<DecisionCenterProps> = ({ records, onRefresh }) => {
  const [selectedRecord, setSelectedRecord] = useState<DecisionSupportRecord | null>(null);
  const [overrideReason, setOverrideReason] = useState('');
  const [chosenAction, setChosenAction] = useState('');
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleAction = async (recordId: string, action: 'ACCEPT' | 'REJECT' | 'OVERRIDE') => {
    setSubmitting(true);
    try {
      await predictiveApi.reviewDecisionSupport(recordId, {
        action,
        reviewer: 'user',
        notes: notes || undefined,
        override_reason: action === 'OVERRIDE' ? overrideReason : undefined,
        chosen_action: action === 'OVERRIDE' ? chosenAction : undefined,
      });
      setSelectedRecord(null);
      setOverrideReason('');
      setChosenAction('');
      setNotes('');
      onRefresh();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-zinc-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
              Human Decision Queue (AI Recommends → You Decide)
            </h3>
            <p className="text-xs text-zinc-400 mt-1">
              Probabilistic recommendations require explicit human decision. Machine learning never acts autonomously.
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 bg-zinc-800 text-zinc-300 font-semibold rounded border border-zinc-700">
            Pending: {records.filter((r) => r.state === 'PENDING_REVIEW').length}
          </span>
        </div>

        {records.length === 0 ? (
          <p className="text-sm text-zinc-500 italic p-6 text-center bg-zinc-950/40 rounded-lg border border-zinc-800/80">
            No decision support records pending human review.
          </p>
        ) : (
          <div className="space-y-4">
            {records.map((rec) => (
              <div
                key={rec.id}
                className="p-6 bg-zinc-950/70 border border-zinc-800 rounded-xl space-y-4 hover:border-zinc-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 text-xs font-bold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                        Urgency: {rec.urgency}
                      </span>
                      <span
                        className={`px-2 py-0.5 text-xs font-bold rounded ${
                          rec.state === 'ACCEPTED'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : rec.state === 'OVERRIDDEN'
                            ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                            : rec.state === 'REJECTED'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}
                      >
                        {rec.state}
                      </span>
                      <span className="text-xs text-zinc-500">
                        Created: {new Date(rec.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    <h4 className="text-base font-bold text-zinc-100 mt-2">{rec.title}</h4>
                    <p className="text-sm text-zinc-200 mt-1 font-medium">
                      Recommended Action: <span className="text-indigo-300">{rec.recommended_action}</span>
                    </p>
                    <p className="text-xs text-zinc-400 mt-1">Tradeoff Analysis: {rec.tradeoff_analysis}</p>
                  </div>

                  {rec.state === 'PENDING_REVIEW' && (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleAction(rec.id, 'ACCEPT')}
                        disabled={submitting}
                        className="px-3.5 py-1.5 text-xs bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded transition-colors disabled:opacity-50"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => setSelectedRecord(rec)}
                        disabled={submitting}
                        className="px-3.5 py-1.5 text-xs bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded transition-colors disabled:opacity-50"
                      >
                        Override
                      </button>
                      <button
                        onClick={() => handleAction(rec.id, 'REJECT')}
                        disabled={submitting}
                        className="px-3.5 py-1.5 text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-semibold rounded transition-colors disabled:opacity-50"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>

                {/* Overrides Audit Trail */}
                {rec.overrides && rec.overrides.length > 0 && (
                  <div className="p-3 bg-purple-950/20 border border-purple-500/20 rounded-lg text-xs space-y-1 text-purple-300">
                    <p className="font-semibold text-purple-200">Human Override Recorded:</p>
                    {rec.overrides.map((ov) => (
                      <p key={ov.id}>
                        • Operator {ov.operator} chose '{ov.chosen_action}': {ov.override_reason}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Override Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 max-w-lg w-full space-y-4">
            <h4 className="text-lg font-bold text-zinc-100">Record Human Override</h4>
            <p className="text-xs text-zinc-400">
              Provide the operator reason and chosen alternative action for model learning audit trail.
            </p>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-zinc-400 mb-1 font-medium">Chosen Action</label>
                <input
                  type="text"
                  value={chosenAction}
                  onChange={(e) => setChosenAction(e.target.value)}
                  placeholder="e.g. 'Proceed with standard sprint without reallocation'"
                  className="w-full bg-zinc-950 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-200 focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="block text-zinc-400 mb-1 font-medium">Override Reason</label>
                <textarea
                  rows={3}
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  placeholder="e.g. 'Client confirmed dependency resolution verbally in sync call.'"
                  className="w-full bg-zinc-950 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-200 focus:outline-none focus:border-purple-500"
                ></textarea>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-zinc-800">
              <button
                onClick={() => setSelectedRecord(null)}
                className="px-4 py-2 text-xs bg-zinc-800 text-zinc-300 rounded font-semibold hover:bg-zinc-700"
              >
                Cancel
              </button>
              <button
                onClick={() => handleAction(selectedRecord.id, 'OVERRIDE')}
                disabled={submitting || !overrideReason.trim()}
                className="px-4 py-2 text-xs bg-purple-600 text-white rounded font-semibold hover:bg-purple-500 disabled:opacity-50"
              >
                {submitting ? 'Submitting...' : 'Save Override'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
