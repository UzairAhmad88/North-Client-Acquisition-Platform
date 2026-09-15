'use client';

import React from 'react';
import { DeliveryIntelligence } from '@/lib/api/analytics';

interface DeliveryIntelligencePanelProps {
  data: DeliveryIntelligence | null;
  loading: boolean;
}

export const DeliveryIntelligencePanel: React.FC<DeliveryIntelligencePanelProps> = ({ data, loading }) => {
  if (loading && !data) {
    return (
      <div className="p-8 text-center text-zinc-400">
        <div className="inline-block animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mb-3"></div>
        <p>Loading Delivery Intelligence & Variance Analysis...</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Estimation Variance Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase text-zinc-400">Total Planned Hours</p>
          <p className="text-2xl font-bold text-zinc-100 mt-2">{data.total_estimated_hours}h</p>
          <p className="text-xs text-zinc-500 mt-1">Across {data.total_completed_projects} projects</p>
        </div>
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase text-zinc-400">Total Actual Hours</p>
          <p className="text-2xl font-bold text-amber-400 mt-2">{data.total_actual_hours}h</p>
          <p className="text-xs text-zinc-500 mt-1">+{data.average_variance_pct}% Net Variance</p>
        </div>
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase text-zinc-400">Underestimated Projects</p>
          <p className="text-2xl font-bold text-rose-400 mt-2">{data.underestimated_projects_count}</p>
          <p className="text-xs text-zinc-500 mt-1">Effort exceeded by &gt;10%</p>
        </div>
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase text-zinc-400">Escaped Defects Rate</p>
          <p className="text-2xl font-bold text-indigo-400 mt-2">{data.quality_summary.leakage_rate_pct}%</p>
          <p className="text-xs text-zinc-500 mt-1">{data.quality_summary.escaped_to_uat_or_support} escaped post-QA</p>
        </div>
      </div>

      {/* Service-Specific Variance Breakdown */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <h3 className="text-lg font-bold text-zinc-100 mb-4">PERT Estimation Variance by Service Category</h3>
        <div className="space-y-4">
          {data.service_variances.map((sv) => (
            <div key={sv.service} className="p-4 bg-zinc-950/60 border border-zinc-800/80 rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <span className="font-semibold text-zinc-200">{sv.service}</span>
                <span className={`font-bold ${sv.avg_variance_pct > 15 ? 'text-rose-400' : 'text-amber-400'}`}>
                  +{sv.avg_variance_pct}% Avg Variance
                </span>
              </div>
              <p className="text-xs text-zinc-500 mt-1">Sample: {sv.project_count} Completed Projects</p>
            </div>
          ))}
        </div>
      </div>

      {/* Scope Change Root Cause Analysis */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <h3 className="text-lg font-bold text-zinc-100 mb-2">Scope Change Impact & Root Causes</h3>
        <p className="text-xs text-zinc-400 mb-4">
          Total Change Requests: {data.scope_changes_summary.total_change_requests} (Avg {data.scope_changes_summary.avg_changes_per_project}/project)
        </p>
        <div className="p-4 bg-indigo-950/20 border border-indigo-500/20 rounded-lg text-sm text-indigo-300">
          <span className="font-semibold text-indigo-200">Dominant Cause: </span>
          {data.scope_changes_summary.primary_root_cause}
        </div>
      </div>
    </div>
  );
};
