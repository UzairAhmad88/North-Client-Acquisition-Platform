'use client';

import React, { useState } from 'react';
import { DecisionRecord, businessOSApi } from '@/lib/api/business_os';

interface DecisionQueueProps {
  decisions: DecisionRecord[];
  onDecisionUpdated?: () => void;
}

export const DecisionQueue: React.FC<DecisionQueueProps> = ({ decisions, onDecisionUpdated }) => {
  const [selectedDecision, setSelectedDecision] = useState<DecisionRecord | null>(decisions[0] || null);
  const [chosenOptionId, setChosenOptionId] = useState<string>('');
  const [rationale, setRationale] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleAuthorize = async () => {
    if (!selectedDecision || !chosenOptionId || !rationale) return;
    try {
      setIsSubmitting(true);
      await businessOSApi.recordDecision(
        selectedDecision.decision_id,
        chosenOptionId,
        rationale,
        'Executive Officer'
      );
      if (onDecisionUpdated) onDecisionUpdated();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>⚖️</span> Executive Decision Queue & Governance
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Human authority decision gate with AI trade-off analysis & strategic learning loop.
          </p>
        </div>
        <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 rounded-full text-xs font-semibold">
          {decisions.filter(d => d.status === 'DECISION_REQUIRED').length} Pending Human Decisions
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Decision List */}
        <div className="space-y-3 lg:col-span-1">
          {decisions.map((dec) => (
            <div
              key={dec.decision_id}
              onClick={() => {
                setSelectedDecision(dec);
                setChosenOptionId('');
              }}
              className={`p-4 rounded-lg border cursor-pointer transition-all ${
                selectedDecision?.decision_id === dec.decision_id
                  ? 'bg-slate-800/90 border-indigo-500/60 shadow-md'
                  : 'bg-slate-950/40 border-slate-800 hover:bg-slate-800/40'
              }`}
            >
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-semibold border border-rose-500/30">
                  {dec.priority}
                </span>
                <span className="text-slate-400">{dec.status}</span>
              </div>
              <h3 className="font-semibold text-slate-100 text-sm">{dec.title}</h3>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{dec.business_question}</p>
            </div>
          ))}
        </div>

        {/* Selected Decision Detail & Authorization */}
        {selectedDecision && (
          <div className="lg:col-span-2 bg-slate-950/60 border border-slate-800 rounded-lg p-5">
            <h3 className="text-lg font-bold text-slate-100">{selectedDecision.title}</h3>
            <p className="text-sm text-indigo-400 font-medium mt-1 mb-4">{selectedDecision.business_question}</p>

            {/* AI Recommendation Box */}
            {selectedDecision.ai_recommendation && (
              <div className="bg-indigo-950/40 border border-indigo-800/60 rounded-lg p-3 mb-4 text-xs">
                <span className="font-bold text-indigo-300">💡 AI Decision Support Draft: </span>
                <span className="text-indigo-200">{selectedDecision.ai_recommendation}</span>
                <p className="text-slate-400 mt-1 italic">{selectedDecision.ai_recommendation_rationale}</p>
              </div>
            )}

            {/* Candidate Options */}
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Candidate Options & Trade-Offs</h4>
            <div className="space-y-3 mb-5">
              {selectedDecision.candidate_options.map((opt) => (
                <div
                  key={opt.option_id}
                  onClick={() => setChosenOptionId(opt.option_id)}
                  className={`p-3 rounded-lg border cursor-pointer text-xs ${
                    chosenOptionId === opt.option_id
                      ? 'bg-emerald-950/30 border-emerald-500/60 text-slate-100'
                      : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between font-bold mb-1">
                    <span>{opt.title}</span>
                    <span className="text-emerald-400 font-normal">Confidence: {opt.confidence}</span>
                  </div>
                  <p className="text-slate-400 mb-2">{opt.description}</p>
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div>
                      <span className="text-emerald-400 font-semibold">Benefits: </span>
                      {opt.expected_benefits.join(', ')}
                    </div>
                    <div>
                      <span className="text-rose-400 font-semibold">Costs/Risks: </span>
                      {opt.expected_costs.concat(opt.risks).join(', ')}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Authorization Action Form */}
            {selectedDecision.status === 'DECISION_REQUIRED' ? (
              <div className="border-t border-slate-800 pt-4">
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Executive Decision Rationale (Required for Audit & Learning Loop):
                </label>
                <textarea
                  value={rationale}
                  onChange={(e) => setRationale(e.target.value)}
                  placeholder="State the strategic rationale for this decision..."
                  rows={2}
                  className="w-full bg-slate-900 border border-slate-800 rounded-md p-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={handleAuthorize}
                  disabled={!chosenOptionId || !rationale || isSubmitting}
                  className="mt-3 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-md text-xs font-semibold transition-all"
                >
                  {isSubmitting ? 'Recording Decision...' : 'Authorize & Record Decision'}
                </button>
              </div>
            ) : (
              <div className="border-t border-slate-800 pt-4 text-xs text-slate-400">
                <span className="text-emerald-400 font-semibold">✓ Decision Decided: </span>
                {selectedDecision.chosen_option_title} by {selectedDecision.decided_by}
                <p className="mt-1 italic">Rationale: {selectedDecision.decision_rationale}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
