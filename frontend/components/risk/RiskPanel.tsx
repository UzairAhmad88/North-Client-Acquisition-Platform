'use client';

import React, { useState } from 'react';
import { checkRisk, overrideRiskAssessment, RiskAssessment } from '@/lib/api/risk';
import { RiskBadge } from './RiskBadge';
import { QualityScoreGauge } from './QualityScoreGauge';
import { EvidenceCoverageBar } from './EvidenceCoverageBar';
import { RiskFindingList } from './RiskFindingList';

interface RiskPanelProps {
  draftId: string;
  assessment: RiskAssessment | null;
  onRefresh?: () => void;
}

export function RiskPanel({ draftId, assessment, onRefresh }: RiskPanelProps) {
  const [loading, setLoading] = useState(false);
  const [overrideReason, setOverrideReason] = useState('');
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  const handleRecheck = async () => {
    setLoading(true);
    try {
      await checkRisk(draftId, 'OUTREACH');
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Failed to recheck risk assessment:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOverride = async (decision: 'ACCEPTED' | 'REJECTED') => {
    if (!assessment || !overrideReason.trim()) return;
    setActionLoading(true);
    try {
      await overrideRiskAssessment(assessment.id, decision, overrideReason);
      setShowOverrideModal(false);
      setOverrideReason('');
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Failed to override risk assessment:', err);
    } finally {
      setActionLoading(false);
    }
  };

  if (!assessment) {
    return (
      <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 text-center space-y-3">
        <p className="text-xs text-zinc-400">No risk assessment evaluated yet for this draft.</p>
        <button
          onClick={handleRecheck}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-medium hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Evaluating Risk...' : 'Run Risk & Quality Assessment'}
        </button>
      </div>
    );
  }

  return (
    <div className="p-5 rounded-xl bg-zinc-900 border border-zinc-800 space-y-4">
      <div className="flex justify-between items-center pb-3 border-b border-zinc-800">
        <div>
          <h3 className="text-sm font-bold text-zinc-100 flex items-center gap-2">
            Risk & Quality Engine
            <RiskBadge decision={assessment.decision} riskLevel={assessment.risk_level} />
          </h3>
          <p className="text-xs text-zinc-400 mt-0.5">
            Engine v{assessment.engine_version} | Policy {assessment.policy_version}
            {assessment.is_stale && <span className="ml-2 text-amber-400 font-semibold">(STALE - Recheck Required)</span>}
          </p>
        </div>
        <button
          onClick={handleRecheck}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-zinc-800 text-zinc-200 hover:bg-zinc-700 text-xs font-medium border border-zinc-700"
        >
          {loading ? 'Rechecking...' : 'Recheck Risk'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <QualityScoreGauge score={assessment.quality_score} />
        <EvidenceCoverageBar coverage={assessment.evidence_coverage} />
      </div>

      {assessment.human_override_decision && (
        <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-xs text-indigo-300 space-y-1">
          <div className="font-bold flex justify-between">
            <span>Human Review Override: {assessment.human_override_decision}</span>
            <span className="text-[10px] text-zinc-400">{new Date(assessment.human_override_at!).toLocaleString()}</span>
          </div>
          <p className="italic">"{assessment.human_override_reason}"</p>
        </div>
      )}

      <RiskFindingList findings={assessment.findings} />

      {assessment.decision === 'REVIEW' && !assessment.human_override_decision && (
        <div className="pt-2 flex justify-end">
          <button
            onClick={() => setShowOverrideModal(true)}
            className="px-3 py-1.5 rounded-lg bg-amber-600 text-white hover:bg-amber-500 text-xs font-medium"
          >
            Record Human Override Review
          </button>
        </div>
      )}

      {showOverrideModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-xl max-w-md w-full space-y-4">
            <h4 className="text-sm font-bold text-zinc-100">Human Risk Override Review</h4>
            <p className="text-xs text-zinc-400">
              Provide justification for overriding the risk assessment recommendation ({assessment.decision}).
            </p>
            <textarea
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value)}
              placeholder="State reason for override (e.g. Claim verified manually via partner document)..."
              rows={3}
              className="w-full p-2 rounded bg-zinc-950 border border-zinc-800 text-xs text-zinc-200 focus:outline-none focus:border-indigo-500"
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowOverrideModal(false)}
                className="px-3 py-1.5 rounded bg-zinc-800 text-zinc-300 text-xs hover:bg-zinc-700"
              >
                Cancel
              </button>
              <button
                onClick={() => handleOverride('REJECTED')}
                disabled={actionLoading || !overrideReason.trim()}
                className="px-3 py-1.5 rounded bg-rose-600 text-white text-xs hover:bg-rose-500 disabled:opacity-50"
              >
                Reject Finding
              </button>
              <button
                onClick={() => handleOverride('ACCEPTED')}
                disabled={actionLoading || !overrideReason.trim()}
                className="px-3 py-1.5 rounded bg-emerald-600 text-white text-xs hover:bg-emerald-500 disabled:opacity-50"
              >
                Accept Risk Finding
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
