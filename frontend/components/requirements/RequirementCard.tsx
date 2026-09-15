'use client';

import React from 'react';
import { ClientRequirement } from '@/lib/api/requirements';

interface RequirementCardProps {
  requirement: ClientRequirement;
  onConfirm?: (id: string) => void;
}

export function RequirementCard({ requirement, onConfirm }: RequirementCardProps) {
  const isConfirmed = requirement.status === 'CONFIRMED';
  const isExplicit = requirement.explicit;

  return (
    <div
      className={`rounded-lg border p-4 transition-all ${
        isConfirmed
          ? 'border-emerald-500/40 bg-emerald-950/10'
          : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-slate-300">
              {requirement.category.replace(/_/g, ' ')}
            </span>
            <span
              className={`rounded px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                isExplicit ? 'bg-indigo-500/20 text-indigo-300' : 'bg-purple-500/20 text-purple-300'
              }`}
            >
              {isExplicit ? 'CLIENT EXPLICIT' : 'AI INFERRED'}
            </span>
            <span
              className={`rounded px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                isConfirmed
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {requirement.status}
            </span>
          </div>
          <h4 className="mt-2 text-base font-semibold text-slate-100">{requirement.title}</h4>
          <p className="mt-1 text-xs text-slate-300 leading-relaxed">{requirement.description}</p>
        </div>

        {!isConfirmed && onConfirm && (
          <button
            onClick={() => onConfirm(requirement.id)}
            className="shrink-0 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white shadow-sm hover:bg-emerald-500 transition-colors"
          >
            Confirm
          </button>
        )}
      </div>

      <div className="mt-3 flex items-center justify-between border-t border-slate-800/60 pt-2 text-[11px] text-slate-400">
        <div>
          Source: <span className="text-slate-300">{requirement.source_type}</span>
        </div>
        <div>
          Confidence: <span className="font-semibold text-slate-200">{requirement.confidence}</span>
        </div>
        <div>
          Priority: <span className="font-semibold text-slate-200">{requirement.priority}</span>
        </div>
      </div>
    </div>
  );
}
