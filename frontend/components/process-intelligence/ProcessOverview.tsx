'use client';

import React from 'react';
import { ProcessOverview } from '@/lib/api/processIntelligence';
import { Activity, AlertTriangle, Cpu, GitPullRequest, Layers, Clock, Zap } from 'lucide-react';

interface Props {
  overview: ProcessOverview | null;
}

export default function ProcessOverviewComponent({ overview }: Props) {
  if (!overview) return null;

  return (
    <div className="space-y-6">
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Monitored Processes</span>
            <Layers className="w-5 h-5 text-indigo-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{overview.total_monitored_processes}</p>
          <p className="text-xs text-slate-500 mt-1">Operational across all domains</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Active Cases</span>
            <Activity className="w-5 h-5 text-emerald-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{overview.total_active_cases}</p>
          <p className="text-xs text-slate-500 mt-1">Live executions linked</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Active Bottlenecks</span>
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{overview.total_active_bottlenecks}</p>
          <p className="text-xs text-slate-500 mt-1">Queue & wait latency flags</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Automation Candidates</span>
            <Zap className="w-5 h-5 text-purple-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{overview.automation_opportunities_count}</p>
          <p className="text-xs text-slate-500 mt-1">8-Factor suitability assessed</p>
        </div>
      </div>

      {/* Top Bottlenecks and Recent Violations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Clock className="w-5 h-5 text-amber-400" /> Top Latency Bottlenecks
            </h3>
            <span className="text-xs text-slate-400">{overview.top_bottlenecks.length} Identified</span>
          </div>
          <div className="space-y-3">
            {overview.top_bottlenecks.length === 0 ? (
              <p className="text-sm text-slate-500 italic">No significant bottlenecks detected.</p>
            ) : (
              overview.top_bottlenecks.map((btn) => (
                <div key={btn.bottleneck_code} className="bg-slate-950 border border-slate-800 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <span className="font-medium text-white">{btn.activity_name}</span>
                    <span className="px-2 py-0.5 text-xs rounded bg-amber-500/20 text-amber-300 font-mono">
                      {btn.average_wait_seconds}s wait
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{btn.root_cause_summary}</p>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-400" /> Conformance Deviations
            </h3>
            <span className="text-xs text-slate-400">{overview.recent_violations.length} Detected</span>
          </div>
          <div className="space-y-3">
            {overview.recent_violations.length === 0 ? (
              <p className="text-sm text-slate-500 italic">Zero conformance violations. Workflows aligned.</p>
            ) : (
              overview.recent_violations.map((viol) => (
                <div key={viol.violation_code} className="bg-slate-950 border border-slate-800 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <span className="font-medium text-white">{viol.activity_involved}</span>
                    <span className="px-2 py-0.5 text-xs rounded bg-red-500/20 text-red-300 font-mono">
                      {viol.violation_type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{viol.description}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
