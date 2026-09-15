'use client';

import React from 'react';

interface ReadinessIndicatorProps {
  readinessStage: string;
  readinessScore: number;
  completenessScore: number;
  scopeComplexity: string;
}

export function ReadinessIndicator({
  readinessStage,
  readinessScore,
  completenessScore,
  scopeComplexity,
}: ReadinessIndicatorProps) {
  const getStageBadgeColor = (stage: string) => {
    switch (stage) {
      case 'READY_FOR_NEXT_STAGE':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
      case 'READY_FOR_REVIEW':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
      case 'PARTIALLY_READY':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      default:
        return 'bg-slate-500/20 text-slate-300 border-slate-500/30';
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Discovery Readiness</h3>
          <div className="mt-1 flex items-center gap-3">
            <span
              className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${getStageBadgeColor(
                readinessStage
              )}`}
            >
              {readinessStage.replace(/_/g, ' ')}
            </span>
            <span className="text-xs text-slate-400">
              Complexity: <strong className="text-slate-200">{scopeComplexity}</strong>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-emerald-400">{readinessScore}%</div>
            <div className="text-[10px] uppercase text-slate-400">Readiness Score</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">{completenessScore}%</div>
            <div className="text-[10px] uppercase text-slate-400">Completeness</div>
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div>
          <div className="mb-1 flex justify-between text-xs text-slate-400">
            <span>Readiness Threshold</span>
            <span>{readinessScore}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full bg-gradient-to-r from-amber-500 to-emerald-500 transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, readinessScore))}%` }}
            />
          </div>
        </div>

        <div>
          <div className="mb-1 flex justify-between text-xs text-slate-400">
            <span>Requirements Completeness</span>
            <span>{completenessScore}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, completenessScore))}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
