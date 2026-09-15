'use client';

import React, { useState } from 'react';
import { digitalTwinApi } from '@/lib/api/digitalTwin';

export const DecisionMatrix: React.FC = () => {
  const [question, setQuestion] = useState('Should we expand active engineering capacity to 8 FTE?');
  const [rationale, setRationale] = useState(
    'Monte Carlo simulation reveals +$45k net profit upside with team utilization dropping to a safe 72%.'
  );
  const [owner, setOwner] = useState('Executive Chief Operating Officer');
  const [recordedDecision, setRecordedDecision] = useState<any | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSignoffDecision = async () => {
    setSubmitting(true);
    try {
      const res = await digitalTwinApi.recordDecision({
        question,
        rationale,
        decision_owner: owner,
        selected_option_id: 'OPT-HIRE-2-DEV',
      });
      setRecordedDecision((res as any)?.data || res);
    } catch (err) {
      console.error('Failed to record human decision', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-bold text-white">Strategic Decision Governance & Human Sign-off</h3>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            Phase 50 Governance
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          AI systems simulate and present options. Mandatory rule: Only authorized human executives decide and sign off.
        </p>
      </div>

      {/* Decision Input Fields */}
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Strategic Question</label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Decision Rationale & Evidence</label>
          <textarea
            rows={3}
            value={rationale}
            onChange={(e) => setRationale(e.target.value)}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Authorized Human Decision Owner</label>
          <input
            type="text"
            value={owner}
            onChange={(e) => setOwner(e.target.value)}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>

      <div className="flex items-center justify-between pt-2">
        <span className="text-xs text-slate-500">
          Decision will be immutable and recorded in the audit ledger.
        </span>
        <button
          onClick={handleSignoffDecision}
          disabled={submitting || !question || !owner}
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition shadow-lg shadow-emerald-600/25"
        >
          {submitting ? 'Recording Sign-off...' : 'Sign & Record Executive Decision'}
        </button>
      </div>

      {recordedDecision && (
        <div className="p-4 bg-emerald-950/40 rounded-xl border border-emerald-800/40 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-emerald-400">DECISION RECORDED & LOCKED</span>
            <span className="font-mono text-emerald-300">{recordedDecision.decision_code}</span>
          </div>
          <p className="text-xs text-slate-300">
            Owner: <strong className="text-white">{recordedDecision.decision_owner}</strong> | Approved At:{' '}
            {new Date(recordedDecision.approved_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
};
