'use client';

import React from 'react';
import { GovernanceExecutiveSummary, GovernancePostureData } from '@/lib/api/governance';
import { ShieldCheck, AlertOctagon, FileCheck, Scale, Cpu, Activity, Clock } from 'lucide-react';

interface GovernanceOverviewProps {
  summary: GovernanceExecutiveSummary | null;
  posture: GovernancePostureData | null;
  loading: boolean;
  onRefresh: () => void;
}

export default function GovernanceOverview({ summary, posture, loading, onRefresh }: GovernanceOverviewProps) {
  if (loading || !summary || !posture) {
    return (
      <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-2xl border border-slate-200">
        Loading Unified GRC & Regulatory Compliance Posture...
      </div>
    );
  }

  const healthBadgeColor =
    summary.governance_health === 'HEALTHY'
      ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
      : summary.governance_health === 'DEGRADED'
      ? 'bg-amber-100 text-amber-800 border-amber-300'
      : 'bg-rose-100 text-rose-800 border-rose-300';

  return (
    <div className="space-y-6">
      {/* Executive Hero Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-sm border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">
              Phase 47 Unified GRC Control Plane
            </span>
            <span className="text-xs text-slate-400">
              Synced {new Date(summary.generated_at).toLocaleTimeString()}
            </span>
          </div>
          <h2 className="text-2xl font-bold mt-2 text-white">Governance, Risk, Compliance & Privacy Platform</h2>
          <p className="text-sm text-slate-300 mt-1 max-w-2xl">
            Traceable governance: Requirement &rarr; Policy &rarr; Control &rarr; Implementation &rarr; Evidence &rarr; Test &rarr; Finding &rarr; Remediation.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Compliance Score</div>
            <div className="text-3xl font-extrabold text-white mt-1">
              {summary.composite_compliance_score}%
            </div>
          </div>
          <div className="text-center px-4 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/15">
            <div className="text-xs text-slate-300 uppercase tracking-wider font-medium">Posture Health</div>
            <div className={`text-sm font-bold px-3 py-1 rounded-lg mt-1 border ${healthBadgeColor}`}>
              {summary.governance_health}
            </div>
          </div>
        </div>
      </div>

      {/* Critical Failures Warning (Rule 18: Never let high scores hide critical blockers) */}
      {summary.critical_blockers > 0 && (
        <div className="bg-rose-50 border-l-4 border-rose-600 p-4 rounded-xl flex items-start gap-3">
          <AlertOctagon className="w-5 h-5 text-rose-600 mt-0.5 shrink-0" />
          <div>
            <div className="text-sm font-bold text-rose-900">
              Non-Negotiable Rule 18 Alert: {summary.critical_blockers} Critical Control / Finding Failure(s) Active
            </div>
            <p className="text-xs text-rose-700 mt-0.5">
              An aggregate score of {summary.composite_compliance_score}% does NOT imply zero material risk. Immediate executive review required.
            </p>
          </div>
        </div>
      )}

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Controls Health</span>
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900">{posture.healthy_controls}</span>
            <span className="text-xs text-slate-500">/ {posture.total_controls} controls</span>
          </div>
          <div className="mt-2 text-xs text-slate-500 flex items-center justify-between">
            <span>Failing: {posture.failing_controls}</span>
            <span className="text-emerald-600 font-medium">
              {Math.round((posture.healthy_controls / Math.max(posture.total_controls, 1)) * 100)}% Pass
            </span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Requirements</span>
            <FileCheck className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900">{posture.implemented_requirements}</span>
            <span className="text-xs text-slate-500">/ {posture.total_requirements} active</span>
          </div>
          <div className="mt-2 text-xs text-slate-500 flex items-center justify-between">
            <span>Traceable mappings</span>
            <span className="text-indigo-600 font-medium">
              {Math.round((posture.implemented_requirements / Math.max(posture.total_requirements, 1)) * 100)}% Implemented
            </span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Governance Debt</span>
            <Scale className="w-5 h-5 text-amber-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900">{posture.technical_debt_score}</span>
            <span className="text-xs text-slate-500">points</span>
          </div>
          <div className="mt-2 text-xs text-slate-500 flex items-center justify-between">
            <span>Stale Evidence: {posture.stale_evidence_count}</span>
            <span className="text-amber-700 font-medium">Exceptions: {posture.active_exceptions_count}</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Open Findings</span>
            <Activity className="w-5 h-5 text-rose-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900">{posture.open_findings_count}</span>
            <span className="text-xs text-slate-500">deficiencies</span>
          </div>
          <div className="mt-2 text-xs text-slate-500 flex items-center justify-between">
            <span className="text-rose-600 font-bold">Critical: {posture.critical_findings_count}</span>
            <span className="text-slate-500">Rule 20 Verification Required</span>
          </div>
        </div>
      </div>
    </div>
  );
}
