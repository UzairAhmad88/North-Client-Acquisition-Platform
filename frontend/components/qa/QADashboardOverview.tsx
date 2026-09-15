'use client';

import React from 'react';
import { CheckCircle2, AlertTriangle, ShieldCheck, ShieldAlert, Sparkles, Activity } from 'lucide-react';

interface QADashboardOverviewProps {
  testRunCount: number;
  passRate: number;
  openDefectsCount: number;
  criticalDefectsCount: number;
  readinessScore: number;
  isReadyForRelease: boolean;
  uatApproved: boolean;
  onEvaluateGate?: () => void;
}

export const QADashboardOverview: React.FC<QADashboardOverviewProps> = ({
  testRunCount,
  passRate,
  openDefectsCount,
  criticalDefectsCount,
  readinessScore,
  isReadyForRelease,
  uatApproved,
  onEvaluateGate,
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Test Pass Rate */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Test Pass Rate</p>
          <p className="text-2xl font-black text-white mt-1">{passRate.toFixed(1)}%</p>
          <p className="text-[10px] text-slate-500 mt-0.5">{testRunCount} active test runs</p>
        </div>
        <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
          <CheckCircle2 className="w-6 h-6" />
        </div>
      </div>

      {/* Open Defects */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Open Defects</p>
          <p className="text-2xl font-black text-white mt-1">{openDefectsCount}</p>
          <p className="text-[10px] text-red-400 mt-0.5">{criticalDefectsCount} critical blocking</p>
        </div>
        <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
          <AlertTriangle className="w-6 h-6" />
        </div>
      </div>

      {/* Client UAT Status */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Client UAT Sign-off</p>
          <p className="text-lg font-bold text-white mt-1">
            {uatApproved ? (
              <span className="text-emerald-400">APPROVED</span>
            ) : (
              <span className="text-amber-400">PENDING</span>
            )}
          </p>
          <p className="text-[10px] text-slate-500 mt-0.5">SHA-256 signature verification</p>
        </div>
        <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
          <ShieldCheck className="w-6 h-6" />
        </div>
      </div>

      {/* Release Readiness Gate */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400 font-medium">Release Readiness</p>
          <p className="text-2xl font-black text-white mt-1">{readinessScore}/100</p>
          <p className="text-[10px] text-slate-400 mt-0.5">
            Gate Status:{' '}
            {isReadyForRelease ? (
              <span className="text-emerald-400 font-bold">READY</span>
            ) : (
              <span className="text-red-400 font-bold">BLOCKED</span>
            )}
          </p>
        </div>
        <button
          onClick={onEvaluateGate}
          className="p-3 bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/20 rounded-xl text-purple-400 transition"
          title="Run Gate Evaluation"
        >
          <Sparkles className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
};
