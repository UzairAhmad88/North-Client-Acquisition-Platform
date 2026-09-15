'use client';

import React, { useState } from 'react';
import { GovernanceRiskItem } from '@/lib/api/governance';
import { AlertTriangle, ShieldCheck, CheckSquare, UserCheck } from 'lucide-react';

interface RiskRegisterProps {
  risks: GovernanceRiskItem[];
  onAcceptRisk: (riskCode: string, approverId: string, justification: string) => void;
}

export default function RiskRegister({ risks, onAcceptRisk }: RiskRegisterProps) {
  const [acceptingRisk, setAcceptingRisk] = useState<string | null>(null);
  const [approverId, setApproverId] = useState<string>('ciso-admin');
  const [justification, setJustification] = useState<string>('');

  const handleConfirmAccept = (riskCode: string) => {
    if (!justification.trim()) return;
    onAcceptRisk(riskCode, approverId, justification);
    setAcceptingRisk(null);
    setJustification('');
  };

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-bold">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 rounded bg-orange-100 text-orange-800 font-bold">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold">MEDIUM</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-bold">LOW</span>;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-indigo-600" />
            <span>Enterprise Risk Register</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Inherent vs residual risk scoring with human-governed treatment authorization.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {risks.length} Risks Logged
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Risk Code</th>
              <th className="p-3.5">Title & Category</th>
              <th className="p-3.5">Inherent</th>
              <th className="p-3.5">Residual</th>
              <th className="p-3.5">Level</th>
              <th className="p-3.5">Treatment</th>
              <th className="p-3.5">Mitigating Controls</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {risks.map((risk) => {
              const isAccepted = risk.treatment === 'ACCEPT' || risk.status === 'ACCEPTED';

              return (
                <tr key={risk.risk_code} className="hover:bg-slate-50/70 transition-colors">
                  <td className="p-3.5 font-mono font-bold text-slate-900">{risk.risk_code}</td>
                  <td className="p-3.5 max-w-xs">
                    <div className="font-semibold text-slate-900">{risk.title}</div>
                    <div className="text-[11px] text-slate-500">{risk.category}</div>
                  </td>
                  <td className="p-3.5 font-mono font-bold text-slate-700">{risk.inherent_risk_score}</td>
                  <td className="p-3.5 font-mono font-bold text-indigo-700">{risk.residual_risk_score}</td>
                  <td className="p-3.5">{getRiskBadge(risk.risk_level)}</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 font-semibold">
                      {risk.treatment}
                    </span>
                  </td>
                  <td className="p-3.5 max-w-xs">
                    <div className="flex flex-wrap gap-1">
                      {risk.mitigating_controls.map((c, i) => (
                        <span key={i} className="px-1.5 py-0.5 bg-slate-100 text-slate-700 font-mono text-[10px] rounded">
                          {c}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="p-3.5 font-semibold">{risk.status}</td>
                  <td className="p-3.5">
                    {!isAccepted && (
                      <button
                        onClick={() => setAcceptingRisk(risk.risk_code)}
                        className="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 font-semibold rounded-lg transition-all"
                      >
                        Accept Risk
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Human Risk Acceptance Modal */}
      {acceptingRisk && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-xl border border-slate-200 space-y-4">
            <div className="flex items-center gap-2 text-rose-700 font-bold">
              <UserCheck className="w-5 h-5" />
              <span>Human Risk Acceptance Authorization</span>
            </div>
            <p className="text-xs text-slate-600">
              Non-negotiable governance rule: AI cannot accept risk. A designated human officer must provide explicit justification and authorization.
            </p>

            <div>
              <label className="text-xs font-semibold text-slate-700">Approver ID / Officer</label>
              <input
                type="text"
                value={approverId}
                onChange={(e) => setApproverId(e.target.value)}
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Business Justification & Compensating Measures</label>
              <textarea
                value={justification}
                onChange={(e) => setJustification(e.target.value)}
                placeholder="State the business rationale and risk monitoring strategy..."
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg h-20"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setAcceptingRisk(null)}
                className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={() => handleConfirmAccept(acceptingRisk)}
                disabled={!justification.trim()}
                className="px-3 py-1.5 text-xs font-bold bg-amber-600 hover:bg-amber-700 text-white rounded-lg disabled:opacity-50"
              >
                Authorize Acceptance
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
