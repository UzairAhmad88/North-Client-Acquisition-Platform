'use client';

import React, { useState } from 'react';
import { Wrench, CheckCircle2, ShieldAlert, ArrowRight } from 'lucide-react';

interface RemediationTrackerProps {
  findingCode: string | null;
  onClose: () => void;
  onCreatePlan: (findingCode: string, planTitle: string, actions: any[], ownerId: string) => void;
  onVerify: (findingCode: string, verifierId: string, evidenceId: string, retestPassed: boolean) => void;
}

export default function RemediationTracker({
  findingCode,
  onClose,
  onCreatePlan,
  onVerify,
}: RemediationTrackerProps) {
  const [step, setStep] = useState<'plan' | 'verify'>('plan');
  const [planTitle, setPlanTitle] = useState('');
  const [actionTitle, setActionTitle] = useState('');
  const [ownerId, setOwnerId] = useState('eng-lead');
  const [verifierId, setVerifierId] = useState('qa-auditor');
  const [evidenceId, setEvidenceId] = useState('EVD-VERIFY-001');
  const [retestPassed, setRetestPassed] = useState(true);

  if (!findingCode) return null;

  const handleCreatePlan = (e: React.FormEvent) => {
    e.preventDefault();
    if (!planTitle.trim()) return;
    const actions = [
      {
        action_title: actionTitle || 'Implement required configuration changes',
        assigned_to: ownerId,
        due_date: new Date(Date.now() + 7 * 86400000).toISOString(),
      },
    ];
    onCreatePlan(findingCode, planTitle, actions, ownerId);
    setStep('verify');
  };

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    onVerify(findingCode, verifierId, evidenceId, retestPassed);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-6 max-w-lg w-full shadow-xl border border-slate-200 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <Wrench className="w-5 h-5 text-indigo-600" />
            <h3 className="text-base font-bold text-slate-900">Remediation Engine &mdash; {findingCode}</h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-sm font-bold">
            &times;
          </button>
        </div>

        {/* Tab Selection */}
        <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-xl">
          <button
            type="button"
            onClick={() => setStep('plan')}
            className={`flex-1 py-1 text-xs font-bold rounded-lg transition-all ${
              step === 'plan' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-600'
            }`}
          >
            1. Formulate Remediation Plan
          </button>
          <button
            type="button"
            onClick={() => setStep('verify')}
            className={`flex-1 py-1 text-xs font-bold rounded-lg transition-all ${
              step === 'verify' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-600'
            }`}
          >
            2. Verify & Retest (Rule 20)
          </button>
        </div>

        {step === 'plan' ? (
          <form onSubmit={handleCreatePlan} className="space-y-3">
            <div>
              <label className="text-xs font-semibold text-slate-700">Plan Title</label>
              <input
                type="text"
                required
                value={planTitle}
                onChange={(e) => setPlanTitle(e.target.value)}
                placeholder="e.g. Patch Tenant Isolation Filter & Retest RBAC"
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Action Item Summary</label>
              <input
                type="text"
                value={actionTitle}
                onChange={(e) => setActionTitle(e.target.value)}
                placeholder="e.g. Enforce tenant_id query filter in repository and add unit tests"
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs font-semibold text-slate-700">Owner ID</label>
                <input
                  type="text"
                  value={ownerId}
                  onChange={(e) => setOwnerId(e.target.value)}
                  className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
                />
              </div>
              <div className="flex items-end">
                <button
                  type="submit"
                  className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-lg transition-all"
                >
                  Save Plan &rarr;
                </button>
              </div>
            </div>
          </form>
        ) : (
          <form onSubmit={handleVerify} className="space-y-3">
            <div className="p-3 bg-indigo-50/70 border border-indigo-200 rounded-xl text-xs text-indigo-900 space-y-1">
              <div className="font-bold flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-indigo-600" />
                Non-Negotiable Rule 20 Enforcement
              </div>
              <p className="text-[11px] text-indigo-800">
                Remediation is NOT complete until verification retesting succeeds. Closure cannot occur without cryptographic evidence and independent verification.
              </p>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Independent Verifier ID</label>
              <input
                type="text"
                required
                value={verifierId}
                onChange={(e) => setVerifierId(e.target.value)}
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Verification Evidence ID</label>
              <input
                type="text"
                required
                value={evidenceId}
                onChange={(e) => setEvidenceId(e.target.value)}
                className="mt-1 w-full text-xs p-2 border border-slate-300 rounded-lg"
              />
            </div>

            <div className="flex items-center gap-2 pt-1">
              <input
                type="checkbox"
                id="retestPassed"
                checked={retestPassed}
                onChange={(e) => setRetestPassed(e.target.checked)}
                className="rounded text-indigo-600 border-slate-300"
              />
              <label htmlFor="retestPassed" className="text-xs font-bold text-slate-800">
                Retest verification passed successfully (Satisfies Rule 20)
              </label>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg transition-all"
              >
                Verify & Close Finding
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
