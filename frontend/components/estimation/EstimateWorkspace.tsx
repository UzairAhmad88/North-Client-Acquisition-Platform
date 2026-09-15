'use client';

import React from 'react';
import { ProjectEstimateDetail } from '@/lib/api/estimates';

interface EstimateWorkspaceProps {
  estimateDetail: ProjectEstimateDetail;
  onCalculate?: () => void;
  onApprove?: () => void;
  isCalculating?: boolean;
}

export function EstimateWorkspace({
  estimateDetail,
  onCalculate,
  onApprove,
  isCalculating,
}: EstimateWorkspaceProps) {
  const isApproved = estimateDetail.status === 'APPROVED';

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100">Commercial & Effort Estimate</h2>
            <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-300 border border-indigo-500/30">
              v{estimateDetail.version}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                isApproved
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {estimateDetail.status}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Estimate ID: {estimateDetail.id} | Solution ID: {estimateDetail.solution_id}
          </p>
        </div>

        <div className="flex gap-3">
          {onCalculate && (
            <button
              onClick={onCalculate}
              disabled={isCalculating}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 disabled:opacity-50 transition-all"
            >
              {isCalculating ? 'Calculating Effort & Costs...' : 'Calculate Effort & Costs'}
            </button>
          )}

          {!isApproved && onApprove && (
            <button
              onClick={onApprove}
              className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-emerald-500 transition-all"
            >
              Approve Commercial Estimate
            </button>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <span className="text-xs text-slate-400 uppercase font-semibold">Total PERT Effort</span>
          <div className="mt-1 text-2xl font-bold text-slate-100">
            {estimateDetail.estimated_hours} <span className="text-sm font-normal text-slate-400">hrs</span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Range: {estimateDetail.minimum_hours}h – {estimateDetail.maximum_hours}h
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <span className="text-xs text-slate-400 uppercase font-semibold">Internal Labor Cost</span>
          <div className="mt-1 text-2xl font-bold text-amber-400">
            ${estimateDetail.internal_cost || 0}
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Rate: Standard Authoritative Labor
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <span className="text-xs text-slate-400 uppercase font-semibold">External Operating Costs</span>
          <div className="mt-1 text-2xl font-bold text-indigo-400">
            ${estimateDetail.external_cost || 0}
          </div>
          <p className="mt-1 text-xs text-slate-400">
            APIs, Hosting & Infrastructure
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <span className="text-xs text-slate-400 uppercase font-semibold">Recommended Commercial Range</span>
          <div className="mt-1 text-lg font-bold text-emerald-400">
            ${estimateDetail.recommended_min || 0} – ${estimateDetail.recommended_max || 0}
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Risk Buffer: {estimateDetail.risk_buffer_percent}%
          </p>
        </div>
      </div>

      {/* Work Breakdown Structure (WBS) */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Work Breakdown Structure (WBS) ({estimateDetail.work_items?.length || 0})
        </h3>
        <div className="space-y-3">
          {estimateDetail.work_items?.map((item) => (
            <div key={item.id} className="flex flex-wrap items-center justify-between rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-300">
                    {item.category}
                  </span>
                  <h4 className="text-sm font-semibold text-slate-100">{item.name}</h4>
                </div>
                <p className="text-xs text-slate-400">{item.description}</p>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono text-slate-300">
                <span>Optimistic: <strong>{item.optimistic_hours}h</strong></span>
                <span>Likely: <strong>{item.most_likely_hours}h</strong></span>
                <span>Pessimistic: <strong>{item.pessimistic_hours}h</strong></span>
                <span className="rounded bg-indigo-500/20 px-2 py-1 text-indigo-300 font-bold border border-indigo-500/30">
                  PERT: {item.expected_hours}h
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Scenarios Comparison */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Scope & Commercial Scenarios ({estimateDetail.scenarios?.length || 0})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {estimateDetail.scenarios?.map((scen) => (
            <div key={scen.id} className="rounded-lg border border-slate-800 bg-slate-950/40 p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm text-slate-100">{scen.name}</span>
                <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-300">
                  {scen.risk_level} Risk
                </span>
              </div>
              <p className="text-xs text-slate-400">{scen.description}</p>
              <div className="border-t border-slate-800 pt-2 space-y-1 text-xs">
                <div className="flex justify-between text-slate-300">
                  <span>Hours:</span>
                  <strong>{scen.estimated_hours}h</strong>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Labor Cost:</span>
                  <strong>${scen.internal_cost || 0}</strong>
                </div>
                <div className="flex justify-between text-emerald-400 font-semibold">
                  <span>Recommended Range:</span>
                  <span>${scen.recommended_min || 0} – ${scen.recommended_max || 0}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
