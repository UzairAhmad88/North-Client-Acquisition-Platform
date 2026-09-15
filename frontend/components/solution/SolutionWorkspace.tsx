'use client';

import React from 'react';
import { SolutionDesignDetail } from '@/lib/api/solutions';

interface SolutionWorkspaceProps {
  solutionDetail: SolutionDesignDetail;
  onAnalyze?: () => void;
  onApprove?: () => void;
  isAnalyzing?: boolean;
}

export function SolutionWorkspace({
  solutionDetail,
  onAnalyze,
  onApprove,
  isAnalyzing,
}: SolutionWorkspaceProps) {
  const isApproved = solutionDetail.status === 'APPROVED';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100">Solution Design Workspace</h2>
            <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-300 border border-indigo-500/30">
              v{solutionDetail.version}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                isApproved
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {solutionDetail.status}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Solution ID: {solutionDetail.id} | Discovery Session ID: {solutionDetail.discovery_session_id}
          </p>
        </div>

        <div className="flex gap-3">
          {onAnalyze && (
            <button
              onClick={onAnalyze}
              disabled={isAnalyzing}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 disabled:opacity-50 transition-all"
            >
              {isAnalyzing ? 'Analyzing Solution...' : 'Analyze Solution Specs'}
            </button>
          )}

          {!isApproved && onApprove && (
            <button
              onClick={onApprove}
              className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-emerald-500 transition-all"
            >
              Approve Solution Design
            </button>
          )}
        </div>
      </div>

      {/* Overview & Architecture */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Solution Overview</h3>
          <p className="mt-2 text-sm text-slate-200 leading-relaxed">{solutionDetail.overview}</p>
          <div className="mt-4 flex items-center gap-4 text-xs text-slate-400">
            <span>
              Complexity Tier: <strong className="text-amber-400">{solutionDetail.complexity_tier}</strong>
            </span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Technical Architecture</h3>
          <div className="mt-2 rounded-lg border border-slate-800 bg-slate-950/60 p-3 font-mono text-xs text-emerald-400">
            {solutionDetail.architecture_summary}
          </div>
        </div>
      </div>

      {/* Recommended Features */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Recommended Features ({solutionDetail.features?.length || 0})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {solutionDetail.features?.map((f) => (
            <div key={f.id} className="rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <div className="flex items-center justify-between gap-2">
                <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-300">
                  {f.category}
                </span>
                <span className="rounded bg-indigo-500/20 px-2 py-0.5 text-[10px] font-semibold text-indigo-300">
                  {f.status}
                </span>
              </div>
              <h4 className="mt-2 text-sm font-semibold text-slate-100">{f.title}</h4>
              <p className="mt-1 text-xs text-slate-400">{f.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Concrete Deliverables */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Project Deliverables ({solutionDetail.deliverables?.length || 0})
        </h3>
        <div className="space-y-3">
          {solutionDetail.deliverables?.map((d) => (
            <div key={d.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <div>
                <h4 className="text-sm font-semibold text-slate-100">{d.name}</h4>
                <p className="text-xs text-slate-400">{d.description}</p>
              </div>
              <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-300">
                {d.priority}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
