'use client';

import React from 'react';
import { SecurityExecutiveOverview } from '@/lib/api/securityOps';
import { ShieldCheck, AlertTriangle, Activity, Lock, Cpu, Database } from 'lucide-react';

interface SecurityOverviewProps {
  overview: SecurityExecutiveOverview | null;
  loading: boolean;
  onRefresh: () => void;
}

export default function SecurityOverview({ overview, loading, onRefresh }: SecurityOverviewProps) {
  if (loading || !overview) {
    return (
      <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
        Loading Enterprise Security Posture & SOC Metrics...
      </div>
    );
  }

  const gradeColors: Record<string, string> = {
    'A+': 'bg-emerald-100 text-emerald-800 border-emerald-300',
    'A': 'bg-emerald-100 text-emerald-800 border-emerald-300',
    'B': 'bg-blue-100 text-blue-800 border-blue-300',
    'C': 'bg-amber-100 text-amber-800 border-amber-300',
    'D': 'bg-orange-100 text-orange-800 border-orange-300',
    'F': 'bg-rose-100 text-rose-800 border-rose-300',
  };

  const gradeColor = gradeColors[overview.posture_grade] || 'bg-slate-100 text-slate-800';

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white p-6 rounded-2xl shadow-sm border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">
              Phase 46 SOC Control Plane
            </span>
            <span className="text-xs text-slate-400">
              Generated {new Date(overview.generated_at).toLocaleTimeString()}
            </span>
          </div>
          <h2 className="text-2xl font-bold mt-2 text-white">Unified Security Operations & Threat Intelligence</h2>
          <p className="text-sm text-slate-300 mt-1 max-w-2xl">
            Continuous telemetry normalization, automated detection rules, multi-stage attack chain correlation, and conservative automated containment.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Posture Grade</div>
            <div className={`text-3xl font-extrabold px-3 py-0.5 rounded-lg mt-1 border ${gradeColor}`}>
              {overview.posture_grade}
            </div>
          </div>
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Risk Score</div>
            <div className="text-3xl font-extrabold text-white mt-1">
              {overview.composite_risk_score} <span className="text-xs font-normal text-slate-400">/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Open Incidents</span>
            <AlertTriangle className={`w-5 h-5 ${overview.open_critical_incidents > 0 ? 'text-rose-500' : 'text-slate-400'}`} />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.soc_metrics.open_incidents}</div>
          <p className="text-xs text-slate-500 mt-1">
            {overview.open_critical_incidents} critical priority requiring triage
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Active Alerts</span>
            <Activity className="w-5 h-5 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.soc_metrics.total_alerts}</div>
          <p className="text-xs text-slate-500 mt-1">
            {overview.soc_metrics.critical_high_alerts} high or critical severity
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Mean Time to Detect (MTTD)</span>
            <ShieldCheck className="w-5 h-5 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.soc_metrics.mttd_minutes} <span className="text-sm font-normal text-slate-500">mins</span></div>
          <p className="text-xs text-emerald-600 mt-1 font-medium">
            {overview.soc_metrics.detection_coverage_pct}% detection coverage
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Mean Time to Contain (MTTC)</span>
            <Lock className="w-5 h-5 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">{overview.soc_metrics.mttc_minutes} <span className="text-sm font-normal text-slate-500">mins</span></div>
          <p className="text-xs text-slate-500 mt-1">
            {overview.soc_metrics.containment_success_rate * 100}% containment success
          </p>
        </div>
      </div>

      {/* Recommendations Banner */}
      <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-5">
        <h3 className="text-sm font-bold text-indigo-900 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-indigo-600" />
          Executive Security Guidance & Strategic Directives
        </h3>
        <ul className="mt-2 space-y-1.5">
          {overview.executive_recommendations.map((rec, idx) => (
            <li key={idx} className="text-xs text-indigo-800 flex items-start gap-2">
              <span className="text-indigo-500 font-bold">•</span>
              <span>{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
