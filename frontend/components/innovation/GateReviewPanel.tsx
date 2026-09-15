'use client';

import React, { useState } from 'react';
import { InnovationGateReview, GateStage, GateDecision, PivotAction } from '../../lib/api/innovation';

interface GateReviewPanelProps {
  reviews: InnovationGateReview[];
  onEvaluateGate?: (gateStage: GateStage, checklist: Record<string, boolean>) => Promise<void>;
  onExecutePivot?: (action: PivotAction, rationale: string, changes: string[]) => Promise<void>;
}

const GATE_TITLES: Record<GateStage, string> = {
  [GateStage.GATE_0_IDEA]: 'Gate 0: Idea Shortlisting',
  [GateStage.GATE_1_PROBLEM_VALIDATION]: 'Gate 1: Problem Validation',
  [GateStage.GATE_2_OPPORTUNITY_VALIDATION]: 'Gate 2: Opportunity Sizing & Fit',
  [GateStage.GATE_3_SOLUTION_VALIDATION]: 'Gate 3: Solution Feasibility & Prototype',
  [GateStage.GATE_4_BUSINESS_VALIDATION]: 'Gate 4: Business Case & Economics',
  [GateStage.GATE_5_MVP_APPROVAL]: 'Gate 5: MVP Build Authorization',
  [GateStage.GATE_6_LAUNCH_APPROVAL]: 'Gate 6: Go-to-Market & Launch',
  [GateStage.GATE_7_SCALE_PIVOT_STOP]: 'Gate 7: Scale, Pivot, or Sunset'
};

const DECISION_BADGES: Record<string, { bg: string; text?: string; label: string }> = {
  [GateDecision.PROCEED]: { bg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30', label: 'Proceed to Next Gate' },
  [GateDecision.PIVOT]: { bg: 'bg-amber-500/20 text-amber-300 border-amber-500/30', label: 'Pivot Required' },
  [GateDecision.PAUSE]: { bg: 'bg-blue-500/20 text-blue-300 border-blue-500/30', label: 'Paused / Backlog' },
  [GateDecision.STOP]: { bg: 'bg-rose-500/20 text-rose-300 border-rose-500/30', label: 'Stop & Sunset' },
  [GateDecision.REVISE_EVIDENCE]: { bg: 'bg-purple-500/20 text-purple-300 border-purple-500/30', label: 'Revise & Collect Evidence' }
};

export const GateReviewPanel: React.FC<GateReviewPanelProps> = ({
  reviews,
  onEvaluateGate,
  onExecutePivot
}) => {
  const [selectedGate, setSelectedGate] = useState<GateStage>(GateStage.GATE_1_PROBLEM_VALIDATION);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [checklist, setChecklist] = useState<Record<string, boolean>>({
    evidence_verified: true,
    assumptions_tested: true,
    risk_acceptable: true,
    financials_viable: false
  });

  const handleToggleCheck = (key: string) => {
    setChecklist(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleRunEvaluation = async () => {
    if (!onEvaluateGate) return;
    setIsEvaluating(true);
    try {
      await onEvaluateGate(selectedGate, checklist);
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 backdrop-blur-md shadow-2xl">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Stage-Gate Governance & Pivot Engine
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Strict evidence thresholds required at each gate before transitioning ideas to high-budget development.
          </p>
        </div>
      </div>

      {/* Stage Gates Timeline */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2 mb-8">
        {Object.entries(GATE_TITLES).map(([stageKey, label], idx) => {
          const isCurrent = selectedGate === stageKey;
          const matchingReview = reviews.find(r => r.gate_stage === stageKey);
          const decision = matchingReview?.decision;

          return (
            <button
              key={stageKey}
              onClick={() => setSelectedGate(stageKey as GateStage)}
              className={`p-3 rounded-lg border text-left transition-all relative overflow-hidden ${
                isCurrent
                  ? 'border-indigo-500 bg-indigo-950/40 text-white ring-1 ring-indigo-500'
                  : 'border-slate-800 bg-slate-950/40 text-slate-400 hover:border-slate-700 hover:text-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Gate {idx}</div>
              <div className="text-xs font-medium truncate mt-0.5">{label.replace(/Gate \d: /, '')}</div>
              {decision && (
                <div className="mt-2">
                  <span className={`text-[9px] px-1.5 py-0.5 rounded border font-semibold ${(DECISION_BADGES as any)[decision]?.bg || 'bg-slate-800 text-slate-300'}`}>
                    {decision}
                  </span>
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Gate Evaluation Details & Checklist */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-950/60 border border-slate-800/80 rounded-lg p-5">
          <h4 className="text-sm font-semibold text-slate-200 mb-3 flex items-center justify-between">
            <span>{GATE_TITLES[selectedGate]} Evaluation</span>
            <span className="text-xs font-normal text-slate-400">Formal Gatekeeper Review</span>
          </h4>

          <div className="space-y-3 mb-6">
            <div className="text-xs text-slate-300 font-medium mb-2">Gate Criteria Checklist:</div>
            {Object.entries(checklist).map(([criterion, checked]) => (
              <label
                key={criterion}
                className="flex items-center gap-3 p-2.5 rounded-lg border border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/80 cursor-pointer transition-colors"
              >
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleToggleCheck(criterion)}
                  className="rounded border-slate-700 bg-slate-800 text-indigo-500 focus:ring-indigo-500"
                />
                <span className="text-xs text-slate-300 capitalize">
                  {criterion.replace(/_/g, ' ')}
                </span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <div className="text-xs text-slate-400">
              Required Approval: <strong className="text-slate-200">Human Sponsor + Risk Review</strong>
            </div>
            <button
              onClick={handleRunEvaluation}
              disabled={isEvaluating}
              className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
            >
              {isEvaluating ? 'Evaluating Gate...' : 'Submit Gate Evaluation'}
            </button>
          </div>
        </div>

        {/* Pivot Engine Recommendation */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-5 flex flex-col justify-between">
          <div>
            <h4 className="text-sm font-semibold text-slate-200 mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
              Pivot & Decision Assistant
            </h4>
            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              If customer feedback or empirical experiments reject critical hypotheses, activate the Pivot Engine to preserve organizational learning.
            </p>

            <div className="space-y-2 mb-4">
              <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800 text-xs text-slate-300">
                <span className="text-amber-400 font-semibold block mb-0.5">Problem-Solution Mismatch?</span>
                Shift to <strong className="text-white">Customer Segment Pivot</strong> or <strong className="text-white">Value Proposition Pivot</strong>.
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800 text-xs text-slate-300">
                <span className="text-blue-400 font-semibold block mb-0.5">Unit Economics Infeasible?</span>
                Evaluate <strong className="text-white">Business Model / Monetization Pivot</strong> before sunset.
              </div>
            </div>
          </div>

          {onExecutePivot && (
            <button
              onClick={() => onExecutePivot(PivotAction.CUSTOMER_SEGMENT_PIVOT, 'Empirical interviews revealed higher willingness to pay in mid-market vs SMB', ['Adjust target segment to 50-500 employees', 'Refine core value messaging'])}
              className="w-full py-2 px-3 rounded-lg border border-amber-500/40 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 text-xs font-semibold transition-all text-center"
            >
              Trigger Structured Pivot Flow
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
