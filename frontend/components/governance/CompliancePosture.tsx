'use client';

import React from 'react';
import { GovernancePostureData } from '@/lib/api/governance';
import { Layers, CheckCircle2, AlertTriangle, XCircle, ShieldAlert } from 'lucide-react';

interface CompliancePostureProps {
  posture: GovernancePostureData | null;
}

export default function CompliancePosture({ posture }: CompliancePostureProps) {
  if (!posture) return null;

  const domainLabels: Record<string, string> = {
    SECURITY: 'Security & Access Controls',
    PRIVACY: 'Privacy & Data Protection (ROPA)',
    AI: 'AI Governance & Model Safety',
    DATA: 'Data Governance & Classification',
    IDENTITY: 'Identity & Authentication (MFA/RBAC)',
    FINANCE: 'Financial & Ledger Controls',
    RELIABILITY: 'Reliability, DR & Backup Controls',
    OPERATIONS: 'Operational Policy Governance',
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-2xs space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-600" />
            <span>Multi-Domain Compliance Posture</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time compliance calculation across all active organizational domains.
          </p>
        </div>
        <span className="text-xs font-semibold px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full border border-indigo-200">
          Composite: {posture.composite_compliance_score}%
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(posture.domain_scores || {}).map(([domain, score]) => {
          const label = domainLabels[domain] || domain;
          const isHigh = score >= 90;
          const isMid = score >= 75 && score < 90;
          const progressColor = isHigh
            ? 'bg-emerald-500'
            : isMid
            ? 'bg-amber-500'
            : 'bg-rose-500';

          return (
            <div key={domain} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 space-y-2">
              <div className="flex justify-between items-center text-xs font-semibold">
                <span className="text-slate-800">{label}</span>
                <span className={`font-mono font-bold ${isHigh ? 'text-emerald-700' : isMid ? 'text-amber-700' : 'text-rose-700'}`}>
                  {score}%
                </span>
              </div>
              <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className={`h-full ${progressColor} transition-all duration-500 rounded-full`}
                  style={{ width: `${Math.min(score, 100)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between text-xs text-slate-600">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-slate-500" />
          <span>Technical Debt Score: <strong className="text-slate-800">{posture.technical_debt_score} pts</strong></span>
        </div>
        <div className="flex items-center gap-4">
          <span>Stale Evidence: <strong className="text-amber-600">{posture.stale_evidence_count}</strong></span>
          <span>Exceptions: <strong className="text-indigo-600">{posture.active_exceptions_count}</strong></span>
          <span>Critical Findings: <strong className="text-rose-600">{posture.critical_findings_count}</strong></span>
        </div>
      </div>
    </div>
  );
}
