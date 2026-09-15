'use client';

import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle, GitCommit, Split } from 'lucide-react';
import { ResearchClaim, ResearchConflict } from '../../lib/api/research_intelligence';

interface VerificationPanelProps {
  claims: ResearchClaim[];
  conflicts: ResearchConflict[];
}

export const VerificationPanel: React.FC<VerificationPanelProps> = ({ claims, conflicts }) => {
  const getClaimStatusBadge = (status: string) => {
    switch (status.toUpperCase()) {
      case 'SUPPORTED':
        return {
          icon: <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />,
          label: 'Supported',
          color: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30',
        };
      case 'PARTIALLY_SUPPORTED':
        return {
          icon: <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />,
          label: 'Partially Supported',
          color: 'bg-amber-500/10 text-amber-300 border-amber-500/30',
        };
      case 'CONFLICTED':
        return {
          icon: <Split className="h-3.5 w-3.5 text-rose-400" />,
          label: 'Conflicted Sources',
          color: 'bg-rose-500/10 text-rose-300 border-rose-500/30',
        };
      case 'UNSUPPORTED':
        return {
          icon: <XCircle className="h-3.5 w-3.5 text-red-400" />,
          label: 'Unsupported',
          color: 'bg-red-500/10 text-red-400 border-red-500/30',
        };
      default:
        return {
          icon: <HelpCircle className="h-3.5 w-3.5 text-slate-400" />,
          label: 'Pending Verification',
          color: 'bg-slate-500/10 text-slate-300 border-slate-500/30',
        };
    }
  };

  return (
    <div className="space-y-6">
      {/* Claims Verification Section */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-indigo-400" />
              Claim Verification & Corroboration Engine
            </h3>
            <p className="text-xs text-slate-400">
              Corroborated across independent sources. Syndicated duplicates filtered out.
            </p>
          </div>
          <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
            {claims.length} Claims Assessed
          </span>
        </div>

        <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
          {claims.length === 0 ? (
            <div className="text-center py-6 text-xs text-slate-500">
              No claims submitted for verification yet.
            </div>
          ) : (
            claims.map((claim) => {
              const badge = getClaimStatusBadge(claim.verification_status || 'PENDING');
              return (
                <div
                  key={claim.id}
                  className="p-3.5 rounded-lg border border-slate-800 bg-slate-950/40 hover:border-slate-700/80 transition-colors"
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <p className="text-xs font-medium text-slate-200 leading-relaxed">
                      "{claim.claim_text}"
                    </p>
                    <span className={`flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded border shrink-0 ${badge.color}`}>
                      {badge.icon}
                      {badge.label}
                    </span>
                  </div>

                  {claim.explanation && (
                    <p className="text-[11px] text-slate-400 bg-slate-900/80 p-2 rounded border border-slate-800/80 mb-2">
                      <span className="text-slate-300 font-medium">Analyst Assessment:</span> {claim.explanation}
                    </p>
                  )}

                  <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
                    <div className="flex items-center gap-2">
                      <span>Supporting Sources: <span className="text-emerald-400 font-mono font-medium">{claim.supporting_source_ids?.length || 0}</span></span>
                      <span>Contradicting: <span className="text-rose-400 font-mono font-medium">{claim.contradicting_source_ids?.length || 0}</span></span>
                    </div>
                    <span className="font-mono text-indigo-400">
                      Confidence: {Math.round((claim.confidence_score || 0.8) * 100)}%
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Surface Conflicts Section */}
      {conflicts.length > 0 && (
        <div className="rounded-xl border border-rose-900/40 bg-rose-950/10 p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-rose-300 flex items-center gap-2">
                <Split className="h-4 w-4 text-rose-400" />
                Detected Contradictions & Disagreements ({conflicts.length})
              </h3>
              <p className="text-xs text-rose-400/80">
                Differences in methodology, measurement dates, or baseline definitions surfaced transparently.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {conflicts.map((conflict) => (
              <div
                key={conflict.id}
                className="p-3 rounded-lg border border-rose-800/40 bg-slate-950/60"
              >
                <h4 className="text-xs font-semibold text-rose-200 mb-2">
                  Conflict on: "{conflict.claim_text}"
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] mb-2">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 font-medium block mb-0.5">Source A Value:</span>
                    <span className="text-amber-300 font-mono">{conflict.value_a || 'Value X'}</span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 font-medium block mb-0.5">Source B Value:</span>
                    <span className="text-rose-300 font-mono">{conflict.value_b || 'Value Y'}</span>
                  </div>
                </div>
                {conflict.possible_explanation && (
                  <p className="text-[10px] text-slate-400 italic">
                    Likely Root Cause: {conflict.possible_explanation}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
