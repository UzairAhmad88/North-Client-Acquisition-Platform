'use client';

import React, { useState } from 'react';
import { ReleaseVersion, evaluateReleaseGate } from '@/lib/api/qa';
import { ShieldCheck, ShieldAlert, Sparkles, Server, CheckCircle2, AlertOctagon } from 'lucide-react';

interface ReleaseReadinessChecklistProps {
  releases: ReleaseVersion[];
  projectId: string;
  onRefresh: () => void;
}

export const ReleaseReadinessChecklist: React.FC<ReleaseReadinessChecklistProps> = ({ releases, projectId, onRefresh }) => {
  const [evaluating, setEvaluating] = useState(false);
  const [gateResult, setGateResult] = useState<any>(null);

  const activeRelease = releases[0];

  const handleEvaluate = async () => {
    if (!activeRelease) return;
    setEvaluating(true);
    try {
      const res = await evaluateReleaseGate(activeRelease.id);
      setGateResult(res);
      onRefresh();
    } catch (err: any) {
      alert(err?.message || 'Failed to evaluate release gate.');
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-lg text-purple-400">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Release Readiness & Gate Enforcement</h2>
            <p className="text-xs text-slate-400">Evaluate quality criteria before production deployment and handover</p>
          </div>
        </div>

        <button
          onClick={handleEvaluate}
          disabled={evaluating || !activeRelease}
          className="px-3.5 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center space-x-1.5 disabled:opacity-50"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>{evaluating ? 'Evaluating...' : 'Evaluate Release Gate'}</span>
        </button>
      </div>

      {activeRelease ? (
        <div className="space-y-4">
          {/* Release Version Overview Card */}
          <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs font-bold text-purple-400 bg-purple-500/10 px-2.5 py-0.5 rounded border border-purple-500/20">
                  {activeRelease.version_tag}
                </span>
                <span className="text-xs text-slate-400 font-medium">Target: {activeRelease.target_environment}</span>
              </div>
              <p className="text-xs text-slate-300 mt-1">{activeRelease.release_notes || 'Initial production release candidate.'}</p>
            </div>

            <div className="flex items-center space-x-3">
              <div className="text-right">
                <div className="text-xs text-slate-400 font-medium">QA Gate Status</div>
                <div
                  className={`text-xs font-bold ${
                    activeRelease.qa_approval_status === 'APPROVED' ? 'text-emerald-400' : 'text-amber-400'
                  }`}
                >
                  {activeRelease.qa_approval_status}
                </div>
              </div>
            </div>
          </div>

          {/* Gate Evaluation Results Card */}
          {gateResult && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  <span>Gate Evaluation Metrics</span>
                </h3>
                <span className="text-lg font-black text-white">
                  Readiness Score: <span className="text-purple-400">{gateResult.readiness_score}/100</span>
                </span>
              </div>

              {/* Blocking Conditions */}
              {gateResult.blocking_conditions && gateResult.blocking_conditions.length > 0 ? (
                <div className="bg-red-950/30 border border-red-800/40 rounded-lg p-4 space-y-2">
                  <div className="text-xs font-bold text-red-400 flex items-center space-x-1.5">
                    <AlertOctagon className="w-4 h-4" />
                    <span>Deployment Blockers Identified ({gateResult.blocking_conditions.length})</span>
                  </div>
                  <ul className="list-disc list-inside text-xs text-red-300 space-y-1">
                    {gateResult.blocking_conditions.map((cond: string, idx: number) => (
                      <li key={idx}>{cond}</li>
                    ))}
                  </ul>
                </div>
              ) : (
                <div className="bg-emerald-950/30 border border-emerald-800/40 rounded-lg p-4 text-xs text-emerald-300 font-semibold flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Zero deployment blockers detected. Release gate passed!</span>
                </div>
              )}

              {/* Recommendations */}
              {gateResult.recommendations && (
                <div className="space-y-1 text-xs">
                  <span className="text-slate-400 font-medium">System Recommendations:</span>
                  <ul className="list-disc list-inside text-slate-300 space-y-1 pl-1">
                    {gateResult.recommendations.map((rec: string, idx: number) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="py-8 text-center text-xs text-slate-500">
          No release versions draft configured for this project.
        </div>
      )}
    </div>
  );
};
